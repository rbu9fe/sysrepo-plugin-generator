import os
from typing import List
from libyang.schema import Node as LyNode
from libyang.schema import SNode, Module

from core.utils import LibyangTreeFunction, to_c_variable
from core.walker import Walker


class ClassAPIContext:
    def __init__(self, source_dir):
        self.source_dir = source_dir
        self.extensions = ['cpp', 'hpp']

        # Yang tree enriched with some properties
        self.tree = {}

        # mapping files to their context
        self.file_map = {}

        self.types = {
            "unknown": None,
            "binary": None,
            "uint8": "uint8_t",
            "uint16": "uint16_t",
            "uint32": "uint32_t",
            "uint64": "uint64_t",
            "string": "std::string",
            "bits": None,
            "boolean": "bool",
            "decimal64": "double",
            "empty": "bool",
            "enumeration": None,
            "identityref": "std::string",
            "instance-id": None,
            "leafref": None,
            "union": None,
            "int8": "int8_t",
            "int16": "int16_t",
            "int32": "int32_t",
            "int64": "int64_t",
        }

class RootNode():
    def __init__(self, module: Module):
        self.mod: Module = module
        self.node_name: str = module.name()
        self.descr: str = module.description()
        self.child_list: List[SNode] = []

    def add_child(self, child: SNode):
        self.child_list.append(child)

    def get_parent(self):
        return None

    def name(self):
        return self.node_name
    def module(self):
        return self.mod
    def parent(self):
        return None
    def nodetype(self):
        return LyNode.CONTAINER
    def config_false(self):
        return False
    def deprecated(self):
        return False
    def obsolete(self):
        return False
    def data_path(self):
        return "/" + self.node_name
    def schema_path(self):
        return "/" + self.node_name
    def description(self):
        return self.descr
    def children(self):
        return self.child_list
    def if_features(self):
        return []
    
class ClassAPIWalker(Walker):
    def __init__(self, prefix, skip_prefix_mode, root_nodes, source_dir):
        super().__init__(root_nodes)
        self.ctx = ClassAPIContext(source_dir)
        self.prefix = prefix
        self.skip_prefix_mode = skip_prefix_mode

    def walk_node(self, node, depth):

        if node.parent():
            parent = self.ctx.tree[node.parent().data_path()]
        else:
            parent_path = "/" + node.module().name()
            if not parent_path in self.ctx.tree:
                # Add a config container as the root node owning all the top-level nodes
                file_path = os.path.join(self.ctx.source_dir, "core", "api", node.module().name())
                self.ctx.tree[parent_path] = LibyangTreeFunction(self.prefix, None, RootNode(node.module()), file_path)
                self.ctx.file_map[file_path] = parent_path
            
            parent = self.ctx.tree[parent_path]
            # This node is under the top-level node, add it as a child
            parent.node.add_child(node)

        # Add custom function to get the desired parent also for the top-level nodes (for which parent() returns None)
        node.get_parent = lambda: parent.node

        file_path = os.path.join(parent.file_path, node.name())
        if self.skip_prefix_mode == "all":
            prefix = node.name()
        elif self.skip_prefix_mode == "root":
            prefix = node.name() if not parent.parent_prefix else parent.prefix + "_" + node.name()
        else:
            prefix = parent.prefix + "_" + node.name()
        entry = LibyangTreeFunction(prefix, parent.prefix if parent != None else None, node, file_path)

        self.ctx.tree[node.data_path()] = entry
        self.ctx.file_map[file_path] = node.data_path()

        return False

    def add_node(self, node):
        return not node.deprecated() and not node.obsolete() and not node.nodetype() in [LyNode.NOTIF, LyNode.ACTION]

    def get_directories(self):
        dirs = []
        for key,entry in self.ctx.tree.items():
            if not entry.file_path in dirs:
                dirs.append(entry.file_path)

        return dirs

    def get_api_filenames(self):
        files = []
        for key,entry in self.ctx.tree.items():
            for ext in self.ctx.extensions:
                files.append(os.path.join(entry.file_path, entry.node.name() + "." + ext))
            files.append(os.path.join(entry.file_path, entry.node.name() + "-ctx.hpp"))

        return files

    def get_file_ctx(self, file):
        file_path = os.path.split(file)[0]
        xpath = self.ctx.file_map[file_path]
        return self.ctx.tree[xpath]

    def get_types(self):
        return self.ctx.types
