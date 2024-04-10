# coding:utf-8


class UnrCategory(object):
    PATHSEP = '/'
    #
    CONSTANT = 'constant'
    COLOR = 'color'
    VECTOR = 'vector'
    MATRIX = 'matrix'
    ARRAY = 'array'


class UnrType(object):
    PATHSEP = UnrCategory.PATHSEP
    # basic
    NONE = 'none'
    #
    CLOSURE = 'closure'
    UNDEFINED = 'undefined'
    #
    RAW = 'raw'
    CONSTANT_RAW = UnrCategory.CONSTANT, RAW
    ARRAY_RAW = UnrCategory.ARRAY, RAW
    #
    STRING = 'string'
    CONSTANT_STRING = UnrCategory.CONSTANT, STRING
    ARRAY_STRING = UnrCategory.ARRAY, STRING
    #
    BYTE = 'byte'
    #
    UINT = 'uint'
    CONSTANT_UINT = UnrCategory.CONSTANT, UINT
    ARRAY_UINT = UnrCategory.ARRAY, UINT
    #
    INTEGER = 'integer'
    CONSTANT_INTEGER = UnrCategory.CONSTANT, INTEGER
    ARRAY_INTEGER = UnrCategory.ARRAY, INTEGER
    #
    FLOAT = 'float'
    CONSTANT_FLOAT = UnrCategory.CONSTANT, FLOAT
    ARRAY_FLOAT = UnrCategory.ARRAY, FLOAT
    #
    BOOLEAN = 'boolean'
    CONSTANT_BOOLEAN = UnrCategory.CONSTANT, BOOLEAN
    ARRAY_BOOLEAN = UnrCategory.ARRAY, BOOLEAN
    #
    CONSTANT_NONE = UnrCategory.CONSTANT, NONE
    ARRAY_NONE = UnrCategory.ARRAY, NONE
    # color
    COLOR2 = 'color2'
    COLOR_COLOR2 = UnrCategory.COLOR, COLOR2
    ARRAY_COLOR2 = UnrCategory.ARRAY, COLOR2
    COLOR3 = 'color3'
    COLOR_COLOR3 = UnrCategory.COLOR, COLOR3
    ARRAY_COLOR3 = UnrCategory.ARRAY, COLOR3
    COLOR4 = 'color4'
    COLOR_COLOR4 = UnrCategory.COLOR, COLOR4
    ARRAY_COLOR4 = UnrCategory.ARRAY, COLOR4
    # vector
    VECTOR2 = 'vector2'
    VECTOR_VECTOR2 = UnrCategory.VECTOR, VECTOR2
    VECTOR3 = 'vector3'
    VECTOR_VECTOR3 = UnrCategory.VECTOR, VECTOR3
    VECTOR4 = 'vector4'
    VECTOR_VECTOR4 = UnrCategory.VECTOR, VECTOR4
    # matrix
    MATRIX33 = 'matrix33'
    MATRIX_MATRIX33 = UnrCategory.MATRIX, MATRIX33
    MATRIX44 = 'matrix44'
    MATRIX_MATRIX44 = UnrCategory.MATRIX, MATRIX44
    #
    NODE = 'node'
    CONSTANT_NODE = UnrCategory.CONSTANT, NODE
    ARRAY_NODE = UnrCategory.ARRAY, NODE
    #
    POINTER = 'pointer'
    CONSTANT_POINTER = UnrCategory.CONSTANT, POINTER
    ARRAY_POINTER = UnrCategory.ARRAY, POINTER
    #
    COLORS = [
        COLOR2,
        COLOR3,
        COLOR4,
    ]
    COLOR_COLORS = [
        COLOR_COLOR2,
        COLOR_COLOR3,
        COLOR_COLOR4,
    ]
    # vectors
    VECTORS = [
        VECTOR2,
        VECTOR3,
        VECTOR4
    ]
    VECTOR_VECTORS = [
        VECTOR_VECTOR2,
        VECTOR_VECTOR3,
        VECTOR_VECTOR4,
    ]
    # matrices
    MATRICES = [
        MATRIX33,
        MATRIX44
    ]
    MATRIX_MATRICES = [
        MATRIX_MATRIX33,
        MATRIX_MATRIX44,
    ]
    #
    ALL = [
              CONSTANT_RAW, ARRAY_RAW,
              CONSTANT_STRING, ARRAY_STRING,
              CONSTANT_UINT, ARRAY_UINT,
              CONSTANT_INTEGER, ARRAY_INTEGER,
              CONSTANT_FLOAT, ARRAY_FLOAT,
              CONSTANT_BOOLEAN, ARRAY_BOOLEAN,
              CONSTANT_NONE, ARRAY_NONE,
              CONSTANT_NODE, ARRAY_NODE,
              CONSTANT_POINTER, ARRAY_POINTER,
          ]+COLOR_COLORS+VECTOR_VECTORS+MATRIX_MATRICES
    #
    CONSTANT_NONE_ = PATHSEP.join(CONSTANT_NONE)
    CONSTANT_RAW_ = PATHSEP.join(CONSTANT_RAW)
    #
    CHANNEL_NAMES_DICT = {
        # color
        COLOR2: ('r', 'a'),
        COLOR3: ('r', 'g', 'b'),
        COLOR4: ('r', 'g', 'b', 'a'),
        # vector
        VECTOR2: ('x', 'y'),
        VECTOR3: ('x', 'y', 'z'),
        VECTOR4: ('x', 'y', 'z', 'w'),
    }

    # constant
    @classmethod
    def get_is_boolean(cls, type_name):
        return type_name == cls.BOOLEAN

    #
    @classmethod
    def get_is_color(cls, type_name):
        return type_name in cls.COLORS

    @classmethod
    def get_is_vector(cls, type_name):
        return type_name in cls.VECTORS

    @classmethod
    def get_is_tuple(cls, type_name):
        return (
                cls.get_is_color(type_name) or
                cls.get_is_vector(type_name) or
                cls.get_is_matrix(type_name)
        )

    #
    @classmethod
    def get_is_matrix(cls, type_name):
        return type_name in cls.MATRICES

    @classmethod
    def get_channel_names(cls, type_name):
        if type_name in cls.CHANNEL_NAMES_DICT:
            return cls.CHANNEL_NAMES_DICT[type_name]
        return []

    @classmethod
    def get_channel_type_name(cls, category_name):
        if category_name == UnrCategory.COLOR or category_name == UnrCategory.VECTOR:
            return cls.FLOAT
        elif category_name == UnrCategory.MATRIX:
            return cls.VECTOR3

    @classmethod
    def get_category_name(cls, type_name, is_array):
        if is_array is True:
            return UnrCategory.ARRAY
        #
        if cls.get_is_color(type_name):
            return UnrCategory.COLOR
        elif cls.get_is_vector(type_name):
            return UnrCategory.VECTOR
        elif cls.get_is_matrix(type_name):
            return UnrCategory.MATRIX
        return UnrCategory.CONSTANT

    @classmethod
    def get_tuple_size(cls, type_name):
        if cls.get_is_tuple(type_name):
            return int(type_name[-1])
        return 1


class UnrObjCategory(object):
    PATHSEP = '/'
    #
    BUILTIN = 'builtin'
    ALL = [
        BUILTIN
    ]
    LYNXI = 'lynxi'
    #
    MAYA = 'maya'
    KATANA = 'katana'
    HOUDINI = 'houdini'
    USD = 'usd'
    #
    PORT_QUERY_RAW = {
        'icon': {
            'type': 'constant/raw',
            'assign': 'variants',
            'raw': 'group'
        }
    }


class UnrObjType(object):
    PATHSEP = UnrObjCategory.PATHSEP
    #
    ROOT = 'root'
    BUILTIN_ROOT = UnrObjCategory.BUILTIN, ROOT
    #
    NULL = 'null'
    BUILTIN_NULL = UnrObjCategory.BUILTIN, NULL
    Xform = 'transform'
    BUILTIN_TRANSFORM = UnrObjCategory.BUILTIN, Xform
    ALL = [
        BUILTIN_ROOT,
        BUILTIN_NULL
    ]
    PORT_QUERY_RAW = {
        'icon': {
            'type': 'constant/raw',
            'assign': 'variants',
            'raw': 'group'
        }
    }


class UnrObj(object):
    PATHSEP = '/'
    NAMESPACESEP = ':'
    #
    PORTS_GAIN_REGEX = '{port_assign}{port_assign_pathsep}*'
    PORTS_GAIN_REGEX_EXTRA = '{port_assign}{port_assign_pathsep}{regex_extra}'


class UnrPort(object):
    PATHSEP = '.'
    PORT_TOKEN_FORMAT = '{port_assign}{port_assign_pathsep}{port_path}'
    # etc: port[0]
    ELEMENT_PATH_FORMAT = '{port_path}[{element_index}]'
    # etc port.r
    CHANNEL_PATH_FORMAT = '{port_path}{pathsep}{channel_name}'


class UnrProperties(object):
    PATHSEP = '.'


class UnrOutputPort(object):
    INTEGER = 'integer'
    FLOAT = 'float'
    BOOLEAN = 'boolean'
    STRING = 'string'
    #
    COLOR2 = 'ra'
    COLOR3 = 'rgb'
    COLOR4 = 'rgba'
    #
    VECTOR2 = 'coord'
    VECTOR3 = 'vector'
    #
    MATRIX33 = 'matrix'
    MATRIX44 = 'matrix'
    #
    NODE = 'node'
    CLOSURE = 'shader'
    #
    UNDEFINED = 'undefined'
    #
    POINTER = 'pointer'
    #
    NONE = 'none'
    #
    ALL = [
        INTEGER,
        FLOAT,
        BOOLEAN,
        STRING,
        #
        COLOR2,
        COLOR3,
        COLOR4,
        #
        VECTOR2,
        VECTOR3,
        #
        MATRIX33,
        MATRIX44,
        #
        NODE,
        CLOSURE,
        #
        UNDEFINED,
        #
        POINTER,
        #
        NONE,
    ]


class UnrPortAssign(object):
    PATHSEP = ':'
    #
    VARIANTS = 'variants'
    #
    BINDS = 'binds'
    #
    INPUTS = 'inputs'
    OUTPUTS = 'outputs'
    #
    ALL = [
        VARIANTS,
        BINDS,
        INPUTS,
        OUTPUTS,
    ]
