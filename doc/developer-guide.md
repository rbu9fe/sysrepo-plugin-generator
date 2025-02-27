# Developer Guide

Once source code has been generated for a set of Yang models, individual Yang nodes must be enabled in case they were generated with the `disabled` flag set in the configuration file. This can be achieved by these changes:
- `CMakeLists.txt`: Enable compilation of the generated source code file.
- In parent container or list activate the child's outcommented code:
  - Header file: `#include` the child's header file and instantiate the child's object.
  - Source file: Activate all occurrences of the child's object.

Then the Yang node is compiled and being used, however, by default it doesn't carry any data, hence, it doesn't contribute anything to the plugin. In order to make it productive some manual implementation is needed. Therefore, the source code is generated with comments like `// TODO: [generator] Load system and fill cache using SetValue.` to indicate where manual implementation may be required and what exactly should be done there.

Note that these comments only indicate potential required changes, however, in practice typically only a subset of them are required depending on the system correspondance of the Yang node and its desired feature set (e.g. dynamic creation and deletion vs. only changing an existing resource).

Possibly required manual implementations are:
- If needed, extend the context that's provided by the parent before passing it to children.
- _List_ node: Implement the parent's constructor to load the system in order to populate the list entries.
- _List_/_leaf-list_ node:
  - Implement `Load()` to initialize the internal cache.
  - _State_ node:
    - `push` or `pull` mode: Configure whether the state data shall be pushed into the operational datastore or whether it shall be pulled from the system each time it's being requested by adjusting a parameter in the base class instantiation.
  - _Configuration_ node:
    - Implement `Validate()` to check whether an incoming configuration shall be accepted (in case there are any constraints other than the Yang model already defines).
    - Implement `Store()` to apply the internal cache to the system.
- Implement destructor to remove system setting if that shall be supported.
  
  **_Note_**: A regular plugin teardown does _not_ remove system settings. Instead, when a sysrepo element is deleted, the generated code handles that as follows depending on the Yang node's type:
  - _Container_: The object will _not_ be destructed but the request will be forwarded to all children by clearing their internal cache.
  - _List_ entry: The list entry object will be tagged with a flag that the system setting is to be removed upon destruction. The parent container will finally remove the entry from the list in it's `Store()` implementation.
  - _Leaf_/_leaf-list_: The object will _not_ be destructed but the cached data will be cleared. Its `Store()` implementation must then remove the setting from the system.
