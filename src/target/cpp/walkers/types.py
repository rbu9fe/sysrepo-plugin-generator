from typing import List, Dict
from libyang.schema import Node as LyNode

from core.utils import to_c_variable
from core.walker import Walker

from libyang.schema import SNode


class Typedef:
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.typedef = "{}_t".format(name)

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def get_typedef(self):
        return self.typedef


class Def:
    def __init__(self, name, path):
        self.name: str = name
        self.path: str = path

    def get_name(self):
        return self.name

    def get_path(self):
        return self.path


class VarDef(Def):
    def __init__(self, type, name, path, kind):
        super().__init__(name, path)
        self.type = type
        self.kind = kind

    def get_type(self):
        return self.type

    def get_kind(self):
        return self.kind


class StructDef(Def):
    vars: List[VarDef]

    def __init__(self, name, path):
        super().__init__(name, path)
        self.vars = []

    def add_var(self, vd: VarDef):
        self.vars.append(vd)

    def get_vars(self):
        return self.vars

    def __str__(self):
        return "StructDef: {}".format(self.name)

    def __repr__(self):
        return str(self)

    def reverse_vars(self):
        self.vars.reverse()


class EnumValue():
    def __init__(self, name, value):
        self.name: str = name
        self.value: int = value

    def __str__(self):
        return "{} = {}".format(self.name, self.value)

class EnumDef(Def):
    def __init__(self, name, path, values):
        super().__init__(name, path)
        self.values: List[EnumValue] = values

    def __str__(self):
        return "EnumDef: {}".format(self.name)

    def __repr__(self):
        return str(self)

    def get_values(self):
        return self.values

    def reverse_values(self):
        self.values.reverse()


class BitValue():
    def __init__(self, name, value):
        self.name: str = name
        self.value: int = value

    def __str__(self):
        return "{} = {}".format(self.name, self.value)

class BitDef(Def):
    def __init__(self, name, path, values):
        super().__init__(name, path)
        self.values: List[BitValue] = values

    def __str__(self):
        return "BitDef: {}".format(self.name)

    def __repr__(self):
        return str(self)

    def get_values(self):
        return self.values

    def reverse_values(self):
        self.values.reverse()


class UnionType():
    def __init__(self, name, type):
        self.name: str = name
        self.type: str = type

    def __str__(self):
        return "{} = {}".format(self.name, self.type)

class UnionDef(Def):
    def __init__(self, name, path, types):
        super().__init__(name, path)
        self.types: List[UnionType] = types

    def __str__(self):
        return "UnionDef: {}".format(self.name)

    def __repr__(self):
        return str(self)

    def get_types(self):
        return self.types

    def reverse_values(self):
        self.types.reverse()


class TypesContext:
    """
    Context for types walker.

    Attributes
    ----------
    prefix : str
        Plugin prefix.
    parent_stack : Dict[int, str]
        Parent stack for the current tree.
    structs : List[StructDef]
        List of structure definitions.
    enums : List[EnumDef]
        List of enum definitions.
    typedefs: List[Typedef]
        List of typedefs.
    types_map: Dict[str, Def]
        Map of type names to their definitions.
    """
    prefix: str
    parent_stack: Dict[int, str]
    structs: List[StructDef]
    unions: List[UnionDef]
    enums: List[EnumDef]
    bits: List[BitDef]
    typedefs: List[Typedef]
    types_map: Dict[str, Def]

    def __init__(self, prefix: str):
        self.prefix = prefix
        self.parent_stack = {}
        self.structs: List[StructDef] = []
        self.unions: List[UnionDef] = []
        self.enums: List[EnumDef] = []
        self.bits: List[BitDef] = []
        self.typedefs: List[Typedef] = []
        self.types_map = {}

    def get_prefix(self):
        return self.prefix

    def add_struct(self, sd: StructDef):
        self.structs.append(sd)

    def add_union(self, ud: UnionDef):
        self.unions.append(ud)

    def add_enum(self, ed: EnumDef):
        if not any(enum.name == ed.name for enum in self.enums):
            self.enums.append(ed)

    def add_bits(self, ed: BitDef):
        if not any(bit.name == ed.name for bit in self.bits):
            self.bits.append(ed)

    def add_typedef(self, d: Def, td: Typedef):
        self.typedefs.append(td)
        self.types_map[d.get_name()] = d

    def parent_exists(self, parent: str) -> bool:
        return parent in self.types_map

    def add_var(self, parent: str, vd: VarDef):
        if self.parent_exists(parent) and type(self.types_map[parent]) == StructDef:
            self.types_map[parent].add_var(vd)
        else:
            raise KeyError("Parent {} not found".format(parent))

    def push_parent(self, depth: int, node_name: str):
        self.parent_stack[depth] = node_name

    def get_parent(self, depth: int) -> str:
        return self.parent_stack[depth-1]

    def reverse_structs(self):
        self.structs.reverse()

        for s in self.structs:
            s.reverse_vars()

    def reverse_typedefs(self):
        self.typedefs.reverse()

    def reverse_enums(self):
        self.enums.reverse()

        for e in self.enums:
            e.reverse_values()

    def reverse_bits(self):
        self.bits.reverse()

        for e in self.bits:
            e.reverse_values()

    def reverse_unions(self):
        self.unions.reverse()

        for e in self.unions:
            e.reverse_values()


class TypesWalker(Walker):
    def __init__(self, prefix, root_nodes):
        super().__init__(root_nodes)
        self.ctx = TypesContext(prefix)

    def get_parent_name(self, depth: int) -> str:
        return to_c_variable("{}_{}".format(
            self.ctx.get_prefix(), self.ctx.get_parent(depth)))
    
    def get_type_name(self, node):
        # As name use the node name if it's a native type, otherwise, use node type name (after the optional ':') to make sure that types are only defined once
        name = node.name() if node.type().name() == node.type().basename() else node.type().name()
        if ":" in name:
            name = name.split(":")[1] 
        return name

    def walk_node(self, node: SNode, depth: int):
        if node.nodetype() == LyNode.CONTAINER:
            self.ctx.push_parent(depth, node.name())

            struct_name = to_c_variable(
                "{}_{}".format(self.ctx.get_prefix(), node.name()))
            var_name = to_c_variable(node.name())

            td = Typedef("struct", struct_name)
            sd = StructDef(struct_name, node.data_path())

            self.ctx.add_struct(sd)
            self.ctx.add_typedef(sd, td)

            if depth > 0:
                parent = self.get_parent_name(depth)

                assert (self.ctx.parent_exists(parent))

                # add var def to the parent
                self.ctx.add_var(parent, VarDef(
                    td.get_typedef(), var_name, node.data_path(), "struct"))
        elif node.nodetype() == LyNode.LEAF:
            # print("{} {}".format(node.type().basename(), node.name()))

            if node.type().basename() == "union":
                # add union type
                union_name = self.get_type_name(node)

                union_ed = UnionDef(union_name, node.data_path(),
                    [UnionType(str(t), t.basename()) for t in node.type().union_types(True)])
                union_td = Typedef("union", union_name)

                self.ctx.add_union(union_ed)
                self.ctx.add_typedef(union_ed, union_td)

                assert (depth > 0)

                parent = self.get_parent_name(depth)

                assert (self.ctx.parent_exists(parent))

                self.ctx.add_var(parent, VarDef(
                    union_td.typedef, to_c_variable(node.name()), node.data_path(), "union"))

            elif node.type().basename() == "enumeration":
                # add enum type
                enum_name = self.get_type_name(node)

                enum_ed = EnumDef(enum_name, node.data_path(),
                    [EnumValue(str(e), e.position()) for e in node.type().enums()])
                enum_td = Typedef("enum", enum_name)

                self.ctx.add_enum(enum_ed)
                self.ctx.add_typedef(enum_ed, enum_td)

                assert (depth > 0)

                parent = self.get_parent_name(depth)

                assert (self.ctx.parent_exists(parent))

                self.ctx.add_var(parent, VarDef(
                    enum_td.typedef, to_c_variable(node.name()), node.data_path(), "enum"))
            
            elif node.type().basename() == "bits":
                # add bits type as an enum
                bits_name = self.get_type_name(node)

                bits_ed = BitDef(bits_name, node.data_path(),
                    [BitValue(str(e), e.position()) for e in node.type().bits()])
                bits_td = Typedef("enum", bits_name)

                self.ctx.add_bits(bits_ed)
                self.ctx.add_typedef(bits_ed, bits_td)

                assert (depth > 0)

                parent = self.get_parent_name(depth)

                assert (self.ctx.parent_exists(parent))

                self.ctx.add_var(parent, VarDef(
                    bits_td.typedef, to_c_variable(node.name()), node.data_path(), "enum"))
                
            else:
                # previous value has to be a struct of some kind

                assert (depth > 0)

                parent = self.get_parent_name(depth)

                assert (self.ctx.parent_exists(parent))

                self.ctx.add_var(parent, VarDef(
                    node.type().basename(), to_c_variable(node.name()), node.data_path(), "var"))

        elif node.nodetype() == LyNode.LEAFLIST:
            struct_name = to_c_variable(
                "{}_{}".format(self.ctx.get_prefix(), node.name()))
            var_name = to_c_variable(node.name())

            # element struct
            element_name = to_c_variable("{}_element".format(struct_name))
            element_var_name = to_c_variable(node.name())

            # element
            element_td = Typedef("struct", element_name)
            element_sd = StructDef(element_name, node.data_path())

            # data
            data_td = Typedef("struct", struct_name)
            data_sd = StructDef(struct_name, node.data_path())

            # add struct variables - data element + pointer to the next node
            element_sd.add_var(
                VarDef(data_td.typedef, element_var_name, node.data_path(), "var"))
            element_sd.add_var(VarDef(element_td.typedef + "*", "next", node.data_path(), "var"))

            self.ctx.add_struct(element_sd)
            self.ctx.add_typedef(element_sd, element_td)

            self.ctx.add_struct(data_sd)
            self.ctx.add_typedef(data_sd, data_td)

            self.ctx.typedefs.append(element_td)
            self.ctx.structs.append(element_sd)

            # add data variable to the data struct
            if node.type().basename() == "union":
                # add union type
                union_name = self.get_type_name(node)

                union_ed = UnionDef(union_name, node.data_path(),
                    [UnionType(str(t), t.basename()) for t in node.type().union_types(True)])
                union_td = Typedef("union", union_name)

                self.ctx.add_union(union_ed)
                self.ctx.add_typedef(union_ed, union_td)

                assert (depth > 0)

                parent = self.get_parent_name(depth)

                assert (self.ctx.parent_exists(parent))

                self.ctx.add_var(parent, VarDef(
                    union_td.typedef, to_c_variable(node.name()), node.data_path(), "union"))

            elif node.type().basename() == "enumeration":
                # add enum type
                enum_name = self.get_type_name(node)

                enum_ed = EnumDef(enum_name, node.data_path(),
                    [EnumValue(str(e), e.position()) for e in node.type().enums()])
                enum_td = Typedef("enum", enum_name)

                self.ctx.add_enum(enum_ed)
                self.ctx.add_typedef(enum_ed, enum_td)

                assert (depth > 0)

                parent = self.get_parent_name(depth)

                assert (self.ctx.parent_exists(parent))

                self.ctx.add_var(parent, VarDef(
                    enum_td.typedef, to_c_variable(node.name()), node.data_path(), "enum"))
                
            elif node.type().basename() == "bits":
                # add bits type as an enum
                bits_name = self.get_type_name(node)

                bits_ed = BitDef(bits_name, node.data_path(),
                    [BitValue(str(e), e.position()) for e in node.type().bits()])
                bits_td = Typedef("enum", bits_name)

                self.ctx.add_bits(bits_ed)
                self.ctx.add_typedef(bits_ed, bits_td)

                assert (depth > 0)

                parent = self.get_parent_name(depth)

                assert (self.ctx.parent_exists(parent))

                self.ctx.add_var(parent, VarDef(
                    bits_td.typedef, to_c_variable(node.name()), node.data_path(), "enum"))
                
            else:
                # previous value has to be a struct of some kind

                assert (depth > 0)

                parent = self.get_parent_name(depth)

                assert (self.ctx.parent_exists(parent))

                self.ctx.add_var(parent, VarDef(
                    node.type().basename(), to_c_variable(node.name()), node.data_path(), "var"))

            # add to parent struct
            assert (depth > 0)

            parent = self.get_parent_name(depth)

            assert (self.ctx.parent_exists(parent))

            # add var def to the parent
            self.ctx.add_var(parent, VarDef(
                element_td.get_typedef() + "*", var_name, node.data_path(), "var"))

        elif node.nodetype() == LyNode.LIST:
            self.ctx.push_parent(depth, node.name())

            struct_name = to_c_variable(
                "{}_{}".format(self.ctx.get_prefix(), node.name()))
            var_name = to_c_variable(node.name())

            # element struct
            element_name = to_c_variable("{}_element".format(struct_name))
            element_var_name = to_c_variable(node.name())

            # element
            element_td = Typedef("struct", element_name)
            element_sd = StructDef(element_name, node.data_path())

            # data
            data_td = Typedef("struct", struct_name)
            data_sd = StructDef(struct_name, node.data_path())

            # add struct variables - data element + pointer to the next node
            element_sd.add_var(
                VarDef(data_td.typedef, element_var_name, node.data_path(), "var"))
            element_sd.add_var(VarDef(element_td.typedef + "*", "next", node.data_path(), "var"))

            self.ctx.add_struct(element_sd)
            self.ctx.add_typedef(element_sd, element_td)

            self.ctx.add_struct(data_sd)
            self.ctx.add_typedef(data_sd, data_td)

            self.ctx.typedefs.append(element_td)
            self.ctx.structs.append(element_sd)

            if depth > 0:
                parent = self.get_parent_name(depth)

                assert (self.ctx.parent_exists(parent))

                # add var def to the parent
                self.ctx.add_var(parent, VarDef(
                    element_td.get_typedef() + "*", var_name, node.data_path(), "var"))

        return False

    def add_node(self, node):
        return not node.nodetype() in [LyNode.RPC, LyNode.ACTION, LyNode.NOTIF]

    def get_enums(self) -> List[EnumDef]:
        return self.ctx.enums
    
    def get_bits(self):
        return self.ctx.bits
    
    def get_unions(self):
        return self.ctx.unions

    def get_enum(self, name):
        enums = list(filter(lambda enum: enum.name == name, self.ctx.enums))
        return enums[0] if len(enums) > 0 else None
    
    def get_bit(self, name):
        bits = list(filter(lambda bit: bit.name == name, self.ctx.bits))
        return bits[0] if len(bits) > 0 else None
    
    def get_union(self, name):
        unions = list(filter(lambda union: union.name == name, self.ctx.unions))
        return unions[0] if len(unions) > 0 else None

    def on_finish(self):
        self.ctx.reverse_structs()
        # self.ctx.reverse_enums()
        self.ctx.reverse_typedefs()
