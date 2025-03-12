import logging
import os
import shutil
import subprocess
import pathlib

import jinja2

import libyang

from pprint import pformat

from typing import List, Dict, Any, Optional

from core.config import GeneratorConfiguration
from core.generator import Generator

from core.log.filters import DebugLevelFilter, InfoLevelFilter

from .walkers.api.cppclass import ClassAPIWalker
from .walkers.types import TypesWalker

from core.utils import to_camel_case, to_c_variable, format_descr

from libyang.schema import Node as LyNode


class ModuleGenerator:
    def __init__(self, ly_mod, name, prefix, disable, skip_prefix_mode):
        self.ly_mod: libyang.Module = ly_mod
        self.name: str = name
        self.prefix: str = prefix
        self.disable: bool = disable
        self.skip_prefix_mode: bool = skip_prefix_mode

    def get_ly_module(self) -> libyang.Module:
        return self.ly_mod
    
    def get_name(self) -> str:
        return self.name
    
    def get_prefix(self) -> str:
        return self.prefix
    
    def get_disable(self) -> bool:
        return self.disable
    
    def get_skip_prefix_mode(self) -> bool:
        return self.skip_prefix_mode

class YangNodeType:
    def __init__(self, nodetype):
        self.type: int = nodetype

    def __str__(self):
        return "Container" if self.type == LyNode.CONTAINER else \
            "List" if self.type == LyNode.LIST else \
            "Leaf" if self.type == LyNode.LEAF else \
            "Leaflist" if self.type == LyNode.LEAFLIST else \
            "RPC" if self.type == LyNode.RPC else \
            "<unknown>"


class GeneratedFile:
    def __init__(self, file, disabled=False):
        self.file: str = file
        self.disabled: bool = disabled

    def __str__(self):
        return ("[Disabled] " if self.disabled else "[Enabled]  ") + self.file

    def get_file(self):
        return self.file

    def get_disabled(self):
        return self.disabled


class CPPGenerator(Generator):
    def __init__(self, yang_dir: str, out_dir: str, config: GeneratorConfiguration):
        super().__init__(yang_dir, out_dir, config)

        # setup logger for the generator
        self.logger: logging.Logger = logging.getLogger("CPPGenerator")
        self.logger.setLevel(logging.DEBUG)

        # Debug level handler
        debug_handler = logging.StreamHandler()
        debug_handler.setLevel(logging.DEBUG)
        debug_formatter = logging.Formatter(
            '[%(levelname)s][%(name)s][%(pathname)s:%(lineno)s]: %(message)s')
        debug_handler.setFormatter(debug_formatter)
        debug_handler.addFilter(DebugLevelFilter())
        self.logger.addHandler(debug_handler)

        # Info level handler
        info_handler = logging.StreamHandler()
        info_handler.setLevel(logging.INFO)
        info_formatter = logging.Formatter(
            '[%(levelname)s][%(name)s]: %(message)s')
        info_handler.setFormatter(info_formatter)
        info_handler.addFilter(InfoLevelFilter())
        self.logger.addHandler(info_handler)

        self.logger.info("Starting C++ generator")

        # initialize libyang and jinja2
        self.modules: List[ModuleGenerator] = []
        self.__setup_libyang_ctx(yang_dir)
        self.__setup_jinja2_env()

        # list of generated files
        self.generated_files: List[GeneratedFile] = []

        # setup and run walkers
        self.source_dir = out_dir

        for module in self.modules:
            module.class_api_walker = ClassAPIWalker(
                module.get_prefix(), module.get_skip_prefix_mode(), module.get_ly_module().children(), self.source_dir)
            module.types_walker = TypesWalker(
                module.get_prefix(), module.get_ly_module().children())

            # run walkers
            walkers = [
                module.class_api_walker,
                module.types_walker
            ]

            for walker in walkers:
                walker.walk()


    def __setup_libyang_ctx(self, yang_dir: str):
        self.ctx = libyang.Context(yang_dir)

        # access configurations
        yang_cfg = self.config.get_yang_configuration()
        mod_cfg = yang_cfg.get_modules_configuration()

        # load features (optional, if None then all are enabled)
        features = mod_cfg.get_features()

        # load main modules
        for module in mod_cfg.get_main_modules():
            m = module.get_name()
            mod = self.ctx.load_module(m, None, "*" if not m in features else features[m])
            enabled_features = [feature.name() for feature in mod.features() if feature.state()]
            self.logger.info("Loaded module {} with features: {}".format(mod.name(), ", ".join(enabled_features) if len(enabled_features) > 0 else "<none>"))

        # load all needed modules
        for m in yang_cfg.get_modules_configuration().get_other_modules():
            mod = self.ctx.load_module(m, None, "*" if not m in features else features[m])
            enabled_features = [feature.name() for feature in mod.features() if feature.state()]
            self.logger.info("Loaded module {} with features: {}".format(mod.name(), ", ".join(enabled_features) if len(enabled_features) > 0 else "<none>"))

        # use main modules for plugin generation
        for module in mod_cfg.get_main_modules():
            ly_mod = self.ctx.get_module(module.get_name())
            self.modules.append(ModuleGenerator(ly_mod, module.get_name(), module.get_prefix(), module.get_disable(), module.get_skip_prefix_mode()))

            self.logger.info("Loaded module {}".format((ly_mod.name())))

    def __setup_jinja2_env(self):
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(["templates/cpp/", "templates/cpp/utils/"]),
            extensions=['jinja2.ext.loopcontrols'],
            autoescape=jinja2.select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def generate_directories(self):
        plugin_dir = os.path.join(self.source_dir, "core")
        dirs = [
            self.source_dir,
            plugin_dir,
            os.path.join(plugin_dir, "api"),
        ]

        for dir in dirs:
            if not os.path.exists(dir):
                os.mkdir(dir)

        for module in self.modules:
            self.__generate_walker_dirs(module.class_api_walker)

    def __generate_walker_dirs(self, walker):
        dirs = walker.get_directories()
        for dir in dirs:
            if not os.path.exists(dir):
                os.mkdir(dir)

    def copy_files(self):
        # copy CMake Find scripts
        modules_input_dir = "templates/common/CMakeModules"
        modules_output_dir = os.path.join(self.out_dir, "CMakeModules")

        for module in os.listdir(modules_input_dir):
            src_path = os.path.join(modules_input_dir, module)
            dst_path = os.path.join(modules_output_dir, module)

            shutil.copyfile(src_path, dst_path)

    def __generate_file(self, file, disabled = False, outfile = "", **kwargs):
        template = self.jinja_env.get_template("{}.jinja2".format(file))

        path = os.path.join(self.out_dir, file if outfile == "" else outfile)
        self.generated_files.append(GeneratedFile(file if outfile == "" else outfile, disabled))
        self.logger.info("Generating {}".format(path))

        with open(path, "w") as file:
            file.write(template.render(kwargs))

        num_lines = 0
        with open(path, "rbU") as file:
            num_lines = sum(1 for _ in file)

        return num_lines

    def __generate_core_files(self):
        self.__generate_file(
            "core/context.hpp", 
            plugin_name=self.config.get_name())

    def __generate_module_files(self):
        self.__generate_file(
            "core/module.hpp")
        self.__generate_file(
            "core/module.cpp",
            modules=self.modules,
            to_c_variable=to_c_variable,
            to_camel_case=to_camel_case)

    def __generate_plugin_files(self):
        self.__generate_file(
            "plugin.hpp")
        self.__generate_file(
            "plugin.cpp", 
            modules=self.modules,
            to_c_variable=to_c_variable,
            to_camel_case=to_camel_case)
        
    def __generate_api_files(self):
        self.logger.info("Generating API files:")

        self.__generate_file(
            "core/api/api-defs.hpp")

        self.__generate_file(
            "core/api/base.hpp")

        self.__generate_file(
            "core/api/logging.hpp")

        counters = {}
        total_class_count = 0
        total_loc_count = 0
        for module in self.modules:
            self.logger.info("Generating API files for module {}:".format(module.get_name()))

            user_types = self.config.get_yang_configuration().get_types_configuration().get_types_map()
            static_types = module.class_api_walker.get_types()

            self.__generate_file(
                "core/api/types.hpp", False, "core/api/" + module.name + "/types.hpp",
                namespace=to_camel_case(to_c_variable(module.get_prefix()), True) + "Types",
                enums=module.types_walker.get_enums(),
                bits=module.types_walker.get_bits(),
                unions=module.types_walker.get_unions(),
                str=str,
                user_types=user_types, 
                static_types=static_types, 
                to_c_variable=to_c_variable, 
                to_camel_case=to_camel_case)

            for idx,file in enumerate(module.class_api_walker.get_api_filenames()):
                ctx = module.class_api_walker.get_file_ctx(file)
                node=ctx.node
                node_type_name = None
                node_types = []
                if node.nodetype() in [LyNode.LEAF, LyNode.LEAFLIST]:
                    node_type_name = module.types_walker.get_type_name(node)
                    enum = module.types_walker.get_enum(node_type_name)
                    node_types += [enum.name] if enum is not None else []
                    bit = module.types_walker.get_bit(node_type_name)
                    node_types += [bit.name] if bit is not None else []
                    union = module.types_walker.get_union(node_type_name)
                    node_types += [union.name] if union is not None else []
                
                # In case the node itself or any of its children is a list then get the types of their keys since they're required e.g. for the constructor.
                known_keys = []
                check_nodes = [node] + (list(node.children()) if not node.nodetype() in [LyNode.LEAF, LyNode.LEAFLIST] else [])
                for entry in check_nodes:
                    if entry.nodetype() == LyNode.LIST:
                        for key in entry.keys():
                            # Since that's a list both enum and union are still None
                            key_name = module.types_walker.get_type_name(key)
                            enum_key = module.types_walker.get_enum(key_name)
                            if enum_key:
                                known_keys.append(enum_key)
                            bit_key = module.types_walker.get_bit(key_name)
                            if bit_key:
                                known_keys.append(bit_key)
                            union_key = module.types_walker.get_union(key_name)
                            if union_key:
                                known_keys.append(union_key)

                # disable cmake build if module.get_disable() except for the Yang root nodes
                disable = module.get_disable() if idx != 0 else False

                ext = os.path.splitext(file)[1]
                loc_count = self.__generate_file(
                    "core/api/class{}".format(ext if not file.endswith("-ctx.hpp") else "-ctx.hpp"), disable, file[len(self.out_dir):][1:],
                    module=module,
                    prefix=ctx.prefix, 
                    parent_prefix=ctx.parent_prefix,
                    node=node, 
                    LyNode=LyNode,
                    user_types=user_types, 
                    static_types=static_types, 
                    node_types=node_types, 
                    comment="// " if module.get_disable() else "",
                    node_types_namespace=to_camel_case(to_c_variable(module.get_prefix()), True) + "Types",
                    known_keys=known_keys,
                    node_type_name=node_type_name,
                    children_skip_prefix=module.get_skip_prefix_mode() == "all" or (module.get_skip_prefix_mode() == "root" and not ctx.parent_prefix),
                    to_c_variable=to_c_variable, 
                    to_camel_case=to_camel_case,
                    format_descr=format_descr)
            
                if ext == ".cpp":
                    node_type = str(YangNodeType(node.nodetype()))
                    if not node_type in counters:
                        item = {"state": 0, "config": 0}
                        counters[node_type] = item

                    state_type = "state" if node.config_false() else "config"
                    counters[node_type][state_type] = counters[node_type][state_type] + 1
                    total_class_count += 1
                    total_loc_count += loc_count

        self.logger.info("core/api Generation Summary:")
        self.logger.info("------------------------------")
        self.logger.info('| sum: {:>4} | {:>6} | {:>5} |'.format(total_class_count, "config", "state"))
        self.logger.info("|-----------|--------|-------|")
        for row in counters.items():
            self.logger.info('| {:<9} | {:>6} | {:>5} |'.format(row[0], row[1]["config"], row[1]["state"]))
        self.logger.info("|----------------------------|")
        self.logger.info("| Generated LOC (cpp): {:>5} |".format(total_loc_count))
        self.logger.info("------------------------------")

        # generated_files = ""
        # for key, value in counters.items():
        #     generated_files += "  {}: state={}, config={}".format(key, value["state"], value["config"])
        
        # self.logger.info("API Generation Summary:\n{}".format(generated_files))

            
    def __generate_cmake_files(self):
        # CMakeLists.txt
        # print(self.generated_files)
        self.__generate_file(
            "CMakeLists.txt", 
            module_name=self.config.get_name(),
            files=self.generated_files,
            src_folder="")

    def generate_files(self):
        self.__generate_core_files()
        self.__generate_module_files()
        self.__generate_plugin_files()
        self.__generate_api_files()
        self.__generate_cmake_files()
        
        self.__generate_file(
            "main.cpp", 
            plugin_name=self.config.get_name())

    def apply_formatting(self):
        self.logger.info("Applying .clang-format style")

        if shutil.which("clang-format") is not None:
            self.logger.info("Running clang-format...")
            # copy the used clang-format file into the source directory and apply it to all generated files
            src_path = "templates/common/.clang-format"
            dst_path = os.path.join(self.out_dir, ".clang-format")

            shutil.copyfile(src_path, dst_path)

            for entry in self.generated_files:
                # run clang-format command
                gen = entry.get_file()
                if gen[-3:] == "cpp" or gen[-3:] == "hpp":
                    # self.logger.info("Running clang-format on {}".format(gen))
                    params = ["clang-format", "-style=file",
                              os.path.join(self.out_dir, gen)]
                    output = subprocess.check_output(params)
                    with open(os.path.join(self.out_dir, gen), "wb") as out_file:
                        out_file.write(output)
            
            self.logger.info("Finished!")

            pathlib.Path(dst_path).unlink()
