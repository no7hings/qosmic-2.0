# coding:utf-8
import lxcontent.core as ctt_core
# universe
from .. import core as unr_core

from .. import abstracts as unr_abstracts

from . import stack as unr_obj_stack

from . import raw as unr_obj_raw


class ObjToken(unr_abstracts.AbsObjToken):
    TYPE_PATHSEP = unr_core.UnrType.PATHSEP
    OBJ_PATHSEP = unr_core.UnrObj.PATHSEP
    #
    PORT_PATHSEP = unr_core.UnrPort.PATHSEP
    PORT_ASSIGN_PATHSEP = unr_core.UnrPortAssign.PATHSEP

    def __init__(self):
        super(ObjToken, self).__init__()


class Type(unr_abstracts.AbsType):
    PATHSEP = unr_core.UnrType.PATHSEP

    def __init__(self, category, name):
        super(Type, self).__init__(category, name)

    def _get_value_class_(self, type_name, is_array):
        if is_array:
            return unr_obj_raw.Array
        #
        if unr_core.UnrType.get_is_color(type_name):
            return unr_obj_raw.Color
        elif unr_core.UnrType.get_is_vector(type_name):
            return unr_obj_raw.Vector
        elif unr_core.UnrType.get_is_matrix(type_name):
            return unr_obj_raw.Matrix
        return unr_obj_raw.Constant


class Category(unr_abstracts.AbsCategory):
    PATHSEP = unr_core.UnrCategory.PATHSEP
    #
    TYPE_CLS = Type

    def __init__(self, universe, name):
        super(Category, self).__init__(universe, name)


class PortChannel(unr_abstracts.AbsPortChannel):
    OBJ_TOKEN = ObjToken
    #
    PATHSEP = unr_core.UnrPort.PATHSEP

    def __init__(self, parent, name):
        super(PortChannel, self).__init__(parent, name)


class PortElement(unr_abstracts.AbsPortElement):
    OBJ_TOKEN = ObjToken
    #
    PATHSEP = unr_core.UnrPort.PATHSEP
    #
    PORT_CHANNEL_STACK_CLS = unr_obj_stack.PortChannelStack
    PORT_CHANNEL_CLS = PortChannel

    def __init__(self, parent, index):
        super(PortElement, self).__init__(parent, index)


class Port(unr_abstracts.AbsPort):
    OBJ_TOKEN = ObjToken
    #
    PATHSEP = unr_core.UnrPort.PATHSEP
    #
    PORT_ELEMENT_STACK_CLS = unr_obj_stack.PortElementStack
    PORT_ELEMENT_CLS = PortElement
    #
    PORT_CHANNEL_STACK_CLS = unr_obj_stack.PortChannelStack
    PORT_CHANNEL_CLS = PortChannel

    def __init__(self, node, type_, assign, name):
        super(Port, self).__init__(node, type_, assign, name)


class Properties(unr_abstracts.AbsProperties):
    PATHSEP = unr_core.UnrProperties.PATHSEP

    def __init__(self, obj, raw):
        super(Properties, self).__init__(obj, raw)


class Attributes(unr_abstracts.AbsProperties):
    PATHSEP = unr_core.UnrProperties.PATHSEP

    def __init__(self, obj, raw):
        super(Attributes, self).__init__(obj, raw)


class ObjDagPath(unr_abstracts.AbsObjDagPath):
    def __init__(self, path):
        super(ObjDagPath, self).__init__(path)


class PortDagPath(unr_abstracts.AbsPortDagPath):
    def __init__(self, path):
        super(PortDagPath, self).__init__(path)


class Obj(unr_abstracts.AbsObj):
    OBJ_TOKEN = ObjToken
    #
    PATHSEP = unr_core.UnrObj.PATHSEP
    # port/def
    DCC_PORT_CLS = Port
    PORT_STACK_CLS = unr_obj_stack.PrxPortStack
    #
    PROPERTIES_CLS = ctt_core.Properties
    ATTRIBUTES_CLS = Attributes

    def __init__(self, type_, path):
        super(Obj, self).__init__(type_, path)


class PortQuery(unr_abstracts.AbsPortQuery):
    OBJ_TOKEN = ObjToken
    #
    PATHSEP = unr_core.UnrPort.PATHSEP

    def __init__(self, obj_type, raw_type, port_path, port_assign, raw):
        super(PortQuery, self).__init__(obj_type, raw_type, port_path, port_assign, raw)


class ObjType(unr_abstracts.AbsObjType):
    OBJ_TOKEN = ObjToken
    # type/def
    PATHSEP = unr_core.UnrObjType.PATHSEP
    # obj_type/def
    DCC_NODE_CLS = Obj
    # port_query/def
    PORT_QUERY_CLS = PortQuery
    PORT_QUERY_STACK_CLS = unr_obj_stack.PortQueryStack

    def __init__(self, category, name):
        super(ObjType, self).__init__(category, name)


class ObjCategory(unr_abstracts.AbsObjCategory):
    OBJ_TOKEN = ObjToken
    #
    PATHSEP = unr_core.UnrObjCategory.PATHSEP
    #
    TYPE_CLS = ObjType
    #
    # port_query/def
    PORT_QUERY_CLS = PortQuery
    PORT_QUERY_STACK_CLS = unr_obj_stack.PortQueryStack

    def __init__(self, universe, name):
        super(ObjCategory, self).__init__(universe, name)


class ObjConnection(unr_abstracts.AbsObjConnection):
    OBJ_TOKEN = ObjToken
    OBJ_PATHSEP = unr_core.UnrObj.PATHSEP
    PORT_PATHSEP = unr_core.UnrPort.PATHSEP
    PORT_ASSIGN_PATHSEP = unr_core.UnrPortAssign.PATHSEP

    def __init__(self, universe, source_obj_path, source_port_path, target_obj_path, target_port_path):
        super(ObjConnection, self).__init__(
            universe,
            source_obj_path, source_port_path,
            target_obj_path, target_port_path
        )


class ObjBind(unr_abstracts.AbsObjBind):
    def __init__(self, universe, obj):
        super(ObjBind, self).__init__(universe, obj)


class ObjUniverse(unr_abstracts.AbsObjUniverse):
    ROOT = unr_core.UnrObj.PATHSEP
    #
    CATEGORY_STACK_CLS = unr_obj_stack.CategoryStack
    CATEGORY_CLS = Category
    TYPE_STACK_CLS = unr_obj_stack.TypeStack
    #
    OBJ_CATEGORY_STACK_CLS = unr_obj_stack.ObjCategoryStack
    OBJ_CATEGORY_CLS = ObjCategory
    OBJ_TYPE_STACK_CLS = unr_obj_stack.ObjTypeStack
    #
    OBJ_STACK_CLS = unr_obj_stack.ObjStack
    OBJ_STACK_CLS_TEST = unr_obj_stack.ObjStackTest
    #
    OBJ_CONNECTION_STACK_CLS = unr_obj_stack.ObjConnectionStack
    OBJ_CONNECTION_CLS = ObjConnection
    #
    OBJ_BIND_STACK_CLS = unr_obj_stack.ObjBindStack
    OBJ_BIND_CLS = ObjBind

    def __init__(self):
        super(ObjUniverse, self).__init__()
