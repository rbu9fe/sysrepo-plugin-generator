# Generated Source Code

## Source Code Structure

The generator will create the following source directory structure. Under `core/api` all Yang nodes are created as directories, where each Yang node is represented as a **pre-implemented** C++ class that's declared and defined in a `hpp` and `cpp` file, respectively. Furthermore, there is a context header file that can be adjusted to pass some arbitrary context between different nodes.

Besides classes that represent Yang nodes, the generator creates some additional files (see below).

The following example was generated for the Yang module `ietf-interfaces` without any features or augmentations:

```
src
├── core
│   ├── api
│   │   ├── interfaces
│   │   │   ├── interface
│   │   │   │   ├── description
│   │   │   │   │   ├── description.cpp
│   │   │   │   │   ├── description-ctx.hpp
│   │   │   │   │   └── description.hpp
│   │   │   │   ├── enabled
│   │   │   │   │   ├── enabled.cpp
│   │   │   │   │   ├── enabled-ctx.hpp
│   │   │   │   │   └── enabled.hpp
│   │   │   │   ├── higher-layer-if
│   │   │   │   │   ├── higher-layer-if.cpp
│   │   │   │   │   ├── higher-layer-if-ctx.hpp
│   │   │   │   │   └── higher-layer-if.hpp
│   │   │   │   ├── last-change
│   │   │   │   │   ├── last-change.cpp
│   │   │   │   │   ├── last-change-ctx.hpp
│   │   │   │   │   └── last-change.hpp
│   │   │   │   ├── lower-layer-if
│   │   │   │   │   ├── lower-layer-if.cpp
│   │   │   │   │   ├── lower-layer-if-ctx.hpp
│   │   │   │   │   └── lower-layer-if.hpp
│   │   │   │   ├── name
│   │   │   │   │   ├── name.cpp
│   │   │   │   │   ├── name-ctx.hpp
│   │   │   │   │   └── name.hpp
│   │   │   │   ├── oper-status
│   │   │   │   │   ├── oper-status.cpp
│   │   │   │   │   ├── oper-status-ctx.hpp
│   │   │   │   │   └── oper-status.hpp
│   │   │   │   ├── phys-address
│   │   │   │   │   ├── phys-address.cpp
│   │   │   │   │   ├── phys-address-ctx.hpp
│   │   │   │   │   └── phys-address.hpp
│   │   │   │   ├── speed
│   │   │   │   │   ├── speed.cpp
│   │   │   │   │   ├── speed-ctx.hpp
│   │   │   │   │   └── speed.hpp
│   │   │   │   ├── statistics
│   │   │   │   │   ├── discontinuity-time
│   │   │   │   │   │   ├── discontinuity-time.cpp
│   │   │   │   │   │   ├── discontinuity-time-ctx.hpp
│   │   │   │   │   │   └── discontinuity-time.hpp
│   │   │   │   │   ├── in-broadcast-pkts
│   │   │   │   │   │   ├── in-broadcast-pkts.cpp
│   │   │   │   │   │   ├── in-broadcast-pkts-ctx.hpp
│   │   │   │   │   │   └── in-broadcast-pkts.hpp
│   │   │   │   │   ├── in-discards
│   │   │   │   │   │   ├── in-discards.cpp
│   │   │   │   │   │   ├── in-discards-ctx.hpp
│   │   │   │   │   │   └── in-discards.hpp
│   │   │   │   │   ├── in-errors
│   │   │   │   │   │   ├── in-errors.cpp
│   │   │   │   │   │   ├── in-errors-ctx.hpp
│   │   │   │   │   │   └── in-errors.hpp
│   │   │   │   │   ├── in-multicast-pkts
│   │   │   │   │   │   ├── in-multicast-pkts.cpp
│   │   │   │   │   │   ├── in-multicast-pkts-ctx.hpp
│   │   │   │   │   │   └── in-multicast-pkts.hpp
│   │   │   │   │   ├── in-octets
│   │   │   │   │   │   ├── in-octets.cpp
│   │   │   │   │   │   ├── in-octets-ctx.hpp
│   │   │   │   │   │   └── in-octets.hpp
│   │   │   │   │   ├── in-unicast-pkts
│   │   │   │   │   │   ├── in-unicast-pkts.cpp
│   │   │   │   │   │   ├── in-unicast-pkts-ctx.hpp
│   │   │   │   │   │   └── in-unicast-pkts.hpp
│   │   │   │   │   ├── in-unknown-protos
│   │   │   │   │   │   ├── in-unknown-protos.cpp
│   │   │   │   │   │   ├── in-unknown-protos-ctx.hpp
│   │   │   │   │   │   └── in-unknown-protos.hpp
│   │   │   │   │   ├── out-broadcast-pkts
│   │   │   │   │   │   ├── out-broadcast-pkts.cpp
│   │   │   │   │   │   ├── out-broadcast-pkts-ctx.hpp
│   │   │   │   │   │   └── out-broadcast-pkts.hpp
│   │   │   │   │   ├── out-discards
│   │   │   │   │   │   ├── out-discards.cpp
│   │   │   │   │   │   ├── out-discards-ctx.hpp
│   │   │   │   │   │   └── out-discards.hpp
│   │   │   │   │   ├── out-errors
│   │   │   │   │   │   ├── out-errors.cpp
│   │   │   │   │   │   ├── out-errors-ctx.hpp
│   │   │   │   │   │   └── out-errors.hpp
│   │   │   │   │   ├── out-multicast-pkts
│   │   │   │   │   │   ├── out-multicast-pkts.cpp
│   │   │   │   │   │   ├── out-multicast-pkts-ctx.hpp
│   │   │   │   │   │   └── out-multicast-pkts.hpp
│   │   │   │   │   ├── out-octets
│   │   │   │   │   │   ├── out-octets.cpp
│   │   │   │   │   │   ├── out-octets-ctx.hpp
│   │   │   │   │   │   └── out-octets.hpp
│   │   │   │   │   ├── out-unicast-pkts
│   │   │   │   │   │   ├── out-unicast-pkts.cpp
│   │   │   │   │   │   ├── out-unicast-pkts-ctx.hpp
│   │   │   │   │   │   └── out-unicast-pkts.hpp
│   │   │   │   │   ├── statistics.cpp
│   │   │   │   │   ├── statistics-ctx.hpp
│   │   │   │   │   └── statistics.hpp
│   │   │   │   ├── type
│   │   │   │   │   ├── type.cpp
│   │   │   │   │   ├── type-ctx.hpp
│   │   │   │   │   └── type.hpp
│   │   │   │   ├── interface.cpp
│   │   │   │   ├── interface-ctx.hpp
│   │   │   │   └── interface.hpp
│   │   │   ├── interfaces.cpp
│   │   │   ├── interfaces-ctx.hpp
│   │   │   ├── interfaces.hpp
│   │   │   └── types.hpp
│   │   ├── base.hpp
│   │   └── logging.hpp
│   ├── context.cpp
│   ├── context.hpp
│   ├── module.cpp
│   └── module.hpp
├── CMakeLists.txt
├── main.cpp
├── plugin.cpp
└── plugin.hpp
```

The generator prints a summary about the C++ classes that were generated under `core/api`:
```
[INFO][CPPGenerator]: core/api Generation Summary:
[INFO][CPPGenerator]: ------------------------------
[INFO][CPPGenerator]: | sum:   27 | config | state |
[INFO][CPPGenerator]: |-----------|--------|-------|
[INFO][CPPGenerator]: | Container |      1 |     1 |
[INFO][CPPGenerator]: | List      |      1 |     0 |
[INFO][CPPGenerator]: | Leaf      |      4 |    18 |
[INFO][CPPGenerator]: | Leaflist  |      0 |     2 |
[INFO][CPPGenerator]: |----------------------------|
[INFO][CPPGenerator]: | Generated LOC (cpp):  2554 |
[INFO][CPPGenerator]: ------------------------------
```

### `CMakeLists.txt`

CMake file listing all generated source code files. By default the plugin is built as both a shared library, that can be loaded by `sysrepo-plugind`, and an executable that links against the shared library.

### `main.cpp`

Used to build the plugin as an executable.

### `module.hpp` and `module.cpp`

Wrapper of a single main Yang node, which constructs its generated C++ class. Its tasks are:

- Register initializers for the running and operational datastores.
- Register value applier for the startup datastore, in order to apply the startup datastore into the system.
- Define callback functions that shall be executed on sysrepo operational, running and RPC callbacks.

### `context.hpp`

Provides a context for the entire plugin in order to provide information (e.g. list of enabled Yang features) or to get, add and remove context objects, that can be shared between arbitrary Yang nodes throughout the entire Yang tree.

### `plugin.hpp` and `plugin.cpp`

Entry point of the Sysrepo plugin. Creates the main Yang module instances and binds everything together. Its tasks are:

- Initialization:
  - Create a plugin context carrying the list of enabled features and a map of context objects, that can be shared between arbitrary Yang nodes.
  - Register a module object for each main Yang module.
  - For each registered module
    - call datastore initializers in order to generate the initial operational and candidate datastores based on the current system state,
    - copy the candidate into the running datastore (atomic commit into running required to satisfy potential Yang _when_ restrictions).
    - register operational, change and RPC subscriptions, and
    - call datastore appliers to apply startup settings to the system.
- Deinitialization:
  - Delete the plugin context, leads to destruction of the registered main modules.

### `core/api/logging.hpp`

Defines logging utilities, in particular for function calls of the _sysrepo-cpp_ API.

### `core/api/base.hpp`

Base class definitions for the following Yang node types, where each (except _RPC_) can be either a _configuration_ or _state_ node:

- Container
- List
- Leaf (data type as class template parameter)
- Leaf-list (data type as class template parameter)
- RPC

Additionally, various helper functions are provided like:
- `GetValueAsString`: Convert a data value of a Yang leaf/leaf-list node to a string.
- `GetValueFromLyNode`: Convert the data value of a libyang data node to the data type the corresponding Yang leaf/af-list node's C++ uses internally.
- `YangBase::GetSchemaPath`: Get the Yang schema path a C++ class was generated for.
- `YangBase::GetNodePath`: Get the Yang node path a C++ class was generated for.
- `YangBase::GetDataType`: Get the data type (configuration or push-/pull state node) a C++ class was generated for.
- `YangBase::GetPluginCtx`: Get the plugin context.
- `YangBase::GetOwnedApiContext`: Get the API context that's owned by the derived C++ class.
- `YangBase::AddOwnedApiContext`: Add an API context that's owned by the derived C++ class.
- `YangBase::RemoveOwnedApiContext`: Remove an API context that's owned by the derived C++ class.
- `YangBase::MergeNodes`: Merge two libyang data nodes.
- `YangBase::DumpSubtree`: Print a libyang data node to `stdout`.
- `YangBase::DumpRoot`: Print the entire tree to `stdout` that a libyang data node is part of.

### `core/api/<main-module-name>/types.hpp`

Yang module specific data type declarations of leaf-/leaf-list data types for C++ (i.e. enumerations, unions, bit-fields).

## Yang Node Representation as C++ Classes

The C++ class of each Yang node is derived from a base class (defined in `core/api/base.hpp`) that's specific to the Yang node type, and it implements functionalitites that are common for the underlying Yang node type (_is-a_ relationship). Classes of Yang containers and lists can own children (_has-a_ relationship), whereas classes of Yang leafs and leaf-lists carry templated data value(s). 

The following table lists the different Yang nodes and the most important functions the corresponding class (or its base) provides. If not empty, the cell entries indicate whether a function is defined in the base class already or in the derived class (because its implementation varies for different node types).

| Node Type | Can Have                                   | `Load`  | `Store`  | `Validate` | `Finalize` | `RevertNode` | `InsertNode` | `GetNode` | `SetNode` | `GetValue` | `SetValue` | `SetConfig` |
| --------- | ------------------------------------------ | ------- | -------- | ---------- | ---------- | ------------ | ------------ | --------- | --------- | ---------- | ---------- | ----------- |
| Container | Containers, Lists, Leafs, Leaf-lists       | derived | derived* | derived*   | derived*   | derived*     | derived      | base      | derived   |            |            | base*       |
| List      | Keys, Containers, Lists, Leafs, Leaf-lists | derived | derived* | derived*   | derived*   | derived*     | derived      | base      | derived   |            |            | base*       |
| Leaf      | Data Item                                  | derived | derived* | derived*   | base*      | base*        | base         | base      | base      | base       | base       |             |
| Leaf-list | Data Item                                  | derived | derived* | derived*   | base*      | base*        | base         | base      | base      | base**     | base**     |             |
| Key       | Data Item                                  |         |          |            |            |              | base         | base      |           | base       |            |             |

*) Only for configuration nodes, not present for state nodes.

**) The data storage of leaf-lists is implemented as a `std::list` container. Hence, for leaf-lists, `GetValue` and `SetValue` are named `GetValues` and `SetValues`, and additionally there are  `AddValue` and `DeleteValue` functions.

The purpose of these functions is:
- `Load`: Read both configuration and state data from the system into the internal cache.
- `Store`: Apply configuration data from the internal cache to the system.
- `Validate`: Validate requested configuration change. Even though the incoming configuration request satisfies the Yang schema, there may be additional constraints to be considered. Called by `SetNode`.
- `Finalize`: Called to finalize a trancaction after it has been approved by all sysrepo clients and successfully applied to the system.
- `RevertNode`: Revert any previous configuration change, that was not yet applied to the system in this node and its children. Called by a sysrepo abort callback.
- `InsertNode`: Create and insert the Yang tree of the current configuration and/or state data of this node including its children into an incoming Yang tree. Used to generate the running and operational datastores.
- `GetNode`: Provide a Yang tree of the current configuration and/or state data of this node including its children. Provided as a convenience function for user code.
  
  **Note**: There are two different types of state data:
  - _Push_: Data is pushed into sysrepo's operational datastore, from where sysrepo provides it to applications asking for operational data. Intended for state data that is constant or doesn't change frequently.
  - _Pull_: Data is queried at runtime using the operational callback subscription, overwriting whatever may have been pushed into sysrepo's operational datastore. Intended for data that changes frequently like statistic counters.
  
    Each C++ class that refers to operational data can be selected to provide the data using the _push_ or _pull_ mechanism. **Default**: _Push_ - even though _pull_ is simpler to use, however, due to performance reasons by default it's preferred to _push_ operational data into the datastore. **Furthermore, by default the operational datastore callback to provide additional _pull_ data is disabled as sysrepo may run into a deadlock when mixing both operational _pull_ and _push_ data!**

- `SetNode`: Inject configuration and/or state data changes into a tree by providing a Yang tree. Containers and lists forward the requested change down the tree until the correct node is reached. Leafs and leaf-lists call `Validate` and, unless rejected, update their internal cache without applying configuration data to the system yet. Called by a sysrepo change callback.
- `GetValue`: Get the current configuration or state data by value from the internal cache.
- `SetValue`: Set the current configuration or state data by value. Updates the internal cache but configuration data is not yet applied to the system.
- `SetConfig`: Convenience wrapper around `SetNode` to inject configuration data by value into a container or list (forwarding it to the right place in the tree).

> **_Note_**: Most of these functions typically don't need manual rework or extensions!

**There are some exceptions, though, where the developer may have to extend/modify the generated code:**
- _List_ constructor: Load the system and populate the list with the already existing entries.
- Destructor: If triggered by an explicit sysrepo delete request (i.e. not on regular teardown) a system setting may have to be removed.
- `Load` in _leaf_ and _leaf-list_: Read system to get current value(s).
- `Store` in _list_ entry: Create system resource.
- `Store` in _leaf_ and _leaf-list_: Write system to apply changed value(s).
- `Validate` in _leaf_ and _leaf-list_: Check requested configuration change against custom constraints.

In these source code locations there is a comment like `// TODO: [generator] Load system and fill cache using SetValue.` to indicate that system interactions may have to be added.
Additionally, one may want to explicitly remove a pre-implemented feature like dynamically creating or deleting a system resource, in case it doesn't make sense for the underlying resource.

See also [Developer Guide](developer-guide.md) for more information.

## Exchange Context between Yang Nodes

In practice some resource has to be exchanged between different Yang nodes. For example, a container may want to create a resource that shall be reused by several children. For that purpose a node receives a context object from its parent, derives an own context object from it and passes that to its children. By default the derived object class is identical to the parent's context, but that way each node can easily extend its context while still having access to the parent's context without having to manually adjust constructor signatures all over the Yang tree.

However, by passing a context from parents to children its contents can only be accessed from Yang nodes under the subtree that created the context, whereas non-children can't access it. For that purpose, `plugin.cpp` creates an _API context_ which is accessible in the entire Yang tree. This API context can be used to store arbitrary context objects using a unique name (should perhaps always be the owner's Yang node path to make sure it's unique) in a globally managed map, from where any other Yang node - even from a different Yang model - can fetch it.

