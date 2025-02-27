#!/usr/bin/env python3

import argparse
from core.config import GeneratorConfiguration
from target.cpp.generator import CPPGenerator

import toml

# setup args
arg_parser = argparse.ArgumentParser(description="Sysrepo plugin generator.")
arg_parser.add_argument("-c", "--config", type=str, dest="config", required=True,
                        help="Configuration file to use for generation, perhaps one from the 'config' subfolder.")
arg_parser.add_argument("-o", "--outdir", type=str, dest="out_dir", required=True,
                        help="Output source directory to use.")
arg_parser.add_argument("-d", "--dir", type=str, dest="yang_dir", default="yang",
                        help="Directory containing all the yang modules. Default: yang")
args = arg_parser.parse_args()

data = toml.load(args.config)

config = GeneratorConfiguration(data)

# currently only C++ generator is supported
generator = CPPGenerator(args.yang_dir, args.out_dir, config)

# generate project directory structure
generator.generate_directories()

# copy files which do not need generation
# generator.copy_files()

# generate all project files
generator.generate_files()

# apply formatting to the generated files
generator.apply_formatting()
