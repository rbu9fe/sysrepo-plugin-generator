# sysrepo-plugin-generator

Sysrepo plugin generator for C++ based on a set of YANG modules used for the specific plugin.

## Dependencies

- libyang-python (>=3.0.4)
- Jinja2
- clang-format (>=11.0)

### How to update clang-format to a newer version

Instructions from: <https://askubuntu.com/questions/1409031/how-to-use-a-more-recent-clang-format-or-clang-tidy-version-on-ubuntu-18-04>

```[shell]
sudo apd update
sudo apd upgrade
# Install add-apt-repository
sudo apt install software-properties-common
# Install gpg-agent
sudo apt install gpg-agent
# Ubuntu 20.04 - for others see the repo list under https://apt.llvm.org/
sudo add-apt-repository 'deb http://apt.llvm.org/focal/ llvm-toolchain-focal main'
# Install their public key
wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key|sudo apt-key add -
sudo apt update
sudo apt install clang-format
```

## Usage

### Run Program

```[shell]
$ python3 sysrepo-plugin-generator.py -h
usage: sysrepo-plugin-generator.py [-h] -c CONFIG -o OUT_DIR [-d YANG_DIR]

Sysrepo plugin generator.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Configuration file to use for generation, perhaps one from the 'config' subfolder.
  -o OUT_DIR, --outdir OUT_DIR
                        Output source directory to use.
  -d YANG_DIR, --dir YANG_DIR
                        Directory containing all the yang modules. Default: yang
```

### Configuration Files

Some exemplary configuration files are stored in the `config` subfolder. The used configuration files control, for which Yang models, augmentations and features code is to be generated and how. Possible settings are:

#### [generator]

- `name`: Sets the plugin name. Used in the CMake file as well as in `PluginContext::getPluginName()`.

#### [yang.modules]

- `main`: A list of main Yang modules, each described by:
  - `name`: The name of this Yang module.
  - `prefix`: The prefix to be used for this Yang module for namespaces, classes and types.
  - `skip_prefix_mode`: Possibility to skip all or some prefixes in the generated object names. One of:
    - `None`: Don't skip prefixes, i.e. the object name of a Yang node object starts with the name of its parent (or, for top-level nodes with the configured Yang module prefix) followed by the name of the node it's generated for. 
    - `"all"`: Skip all prefixes, i.e. the object name of an object is solely determined by the Yang node's name it was generated for.
    - `"root"`: Only skip the prefix for the root node object, typically used when the Yang module top-level nodes already indicate the module name they're defined in.
  - `disable`: A boolean indicating whether generated code shall be compiled and used. If `True` then the source code files in the Makefile as well as children in a container node will be commented out. _Default_: `False`.
- `other`: List of Yang modules that augment the main modules.
- `features`: A dictionary where each entry defines a list of features that shall be enabled for a certain Yang module. If a Yang module is not listed then all its features are enabled, otherwise, a feature is only enabled when it's listed.

#### [yang.types]

The generator tries to map all Yang types to C++ types (enumerations, integers, strings, ...). Here that internal mapping can be overwritten for certain Yang types.

Example:
`identityref = "std::string"`

_Note_: Typically it should _not_ be necessary to overwrite the internal mapping of types, otherwise, this indicates that the generator should probably be extended to add support for the missing type.

## Generated Source Code

For additional documentation of the generated source code please refer to:
- [Generated Source Code](doc/generated-source-code.md)
- [Sequence Diagrams](doc/sequence-diagrams.md)
- [Developer Guide](doc/developer-guide.md)
