# coding:utf-8
import lxuniverse.core as unr_core
# arnold
from .wrap import *


class AndBase(object):
    if ARNOLD_FLAG is True:
        TYPE_NAME_QUERY = {
            # <category-constant>
            ai.AI_TYPE_STRING: unr_core.UnrType.STRING,
            ai.AI_TYPE_ENUM: unr_core.UnrType.STRING,
            #
            ai.AI_TYPE_BYTE: unr_core.UnrType.INTEGER,
            ai.AI_TYPE_INT: unr_core.UnrType.INTEGER,
            ai.AI_TYPE_UINT: unr_core.UnrType.INTEGER,
            #
            ai.AI_TYPE_FLOAT: unr_core.UnrType.FLOAT,
            ai.AI_TYPE_BOOLEAN: unr_core.UnrType.BOOLEAN,
            #
            ai.AI_TYPE_RGB: unr_core.UnrType.COLOR3,
            ai.AI_TYPE_RGBA: unr_core.UnrType.COLOR4,
            #
            ai.AI_TYPE_VECTOR2: unr_core.UnrType.VECTOR2,
            ai.AI_TYPE_VECTOR: unr_core.UnrType.VECTOR3,
            ai.AI_TYPE_MATRIX: unr_core.UnrType.MATRIX44,
            ai.AI_TYPE_NODE: unr_core.UnrType.NODE,
            #
            ai.AI_TYPE_CLOSURE: unr_core.UnrType.CLOSURE,
            #
            ai.AI_TYPE_UNDEFINED: unr_core.UnrType.UNDEFINED,
            ai.AI_TYPE_NONE: unr_core.UnrType.NONE,
        }

        OUTPUT_PORT_NAME_QUERY = {
            # <category-constant>
            ai.AI_TYPE_STRING: unr_core.UnrOutputPort.STRING,
            ai.AI_TYPE_ENUM: unr_core.UnrOutputPort.STRING,
            ai.AI_TYPE_INT: unr_core.UnrOutputPort.INTEGER,
            ai.AI_TYPE_UINT: unr_core.UnrOutputPort.INTEGER,
            ai.AI_TYPE_BYTE: unr_core.UnrOutputPort.INTEGER,
            ai.AI_TYPE_FLOAT: unr_core.UnrOutputPort.FLOAT,
            ai.AI_TYPE_BOOLEAN: unr_core.UnrOutputPort.BOOLEAN,
            # <category-vector>
            ai.AI_TYPE_VECTOR2: unr_core.UnrOutputPort.VECTOR2,
            ai.AI_TYPE_VECTOR: unr_core.UnrOutputPort.VECTOR3,
            #
            ai.AI_TYPE_RGB: unr_core.UnrOutputPort.COLOR3,
            ai.AI_TYPE_RGBA: unr_core.UnrOutputPort.COLOR4,
            #
            ai.AI_TYPE_MATRIX: unr_core.UnrOutputPort.MATRIX44,
            #
            ai.AI_TYPE_NODE: unr_core.UnrOutputPort.NODE,
            #
            ai.AI_TYPE_UNDEFINED: unr_core.UnrOutputPort.NONE,
            ai.AI_TYPE_NONE: unr_core.UnrOutputPort.NONE,
            #
            ai.ai_params.AI_TYPE_POINTER: unr_core.UnrOutputPort.POINTER,
            ai.AI_TYPE_CLOSURE: unr_core.UnrOutputPort.CLOSURE,
        }

        AR_CHANNELS_DICT = {
            ai.AI_TYPE_VECTOR: 'xyz',
            ai.AI_TYPE_VECTOR2: 'xy',
            ai.AI_TYPE_RGB: 'rgb',
            ai.AI_TYPE_RGBA: 'rgba'
        }
        AR_DEFAULT_VALUE_FNC_DICT = {
            ai.AI_TYPE_STRING: lambda ar_port_entry: unicode(ai.AiParamGetDefault(ar_port_entry).contents.STR),
            ai.AI_TYPE_INT: lambda ar_port_entry: ai.AiParamGetDefault(ar_port_entry).contents.INT,
            ai.AI_TYPE_UINT: lambda ar_port_entry: ai.AiParamGetDefault(ar_port_entry).contents.UINT,
            ai.AI_TYPE_BYTE: lambda ar_port_entry: ai.AiParamGetDefault(ar_port_entry).contents.BYTE,
            ai.AI_TYPE_FLOAT: lambda ar_port_entry: ai.AiParamGetDefault(ar_port_entry).contents.FLT,
            ai.AI_TYPE_BOOLEAN: lambda ar_port_entry: ai.AiParamGetDefault(ar_port_entry).contents.BOOL,
            ai.AI_TYPE_RGB: lambda ar_port_entry: ai.AiParamGetDefault(ar_port_entry).contents.RGB,
            ai.AI_TYPE_RGBA: lambda ar_port_entry: ai.AiParamGetDefault(ar_port_entry).contents.RGBA,
            ai.AI_TYPE_VECTOR: lambda ar_port_entry: ai.AiParamGetDefault(ar_port_entry).contents.VEC,
            ai.AI_TYPE_VECTOR2: lambda ar_port_entry: ai.AiParamGetDefault(ar_port_entry).contents.VEC2,
            ai.AI_TYPE_MATRIX: lambda ar_port_entry: ai.AiParamGetDefault(ar_port_entry).contents.pMTX,
            ai.AI_TYPE_NODE: lambda ar_port_entry: None,
            #
            ai.AI_TYPE_ENUM: lambda ar_port_entry: ai.AiParamGetDefault(ar_port_entry).contents.INT,
        }
        AR_VALUE_FNC_DICT = {
            ai.AI_TYPE_STRING: lambda and_obj, and_port: unicode(ai.AiNodeGetStr(and_obj, and_port)),
            ai.AI_TYPE_INT: lambda and_obj, and_port: ai.AiNodeGetInt(and_obj, and_port),
            ai.AI_TYPE_UINT: lambda and_obj, and_port: ai.AiNodeGetUInt(and_obj, and_port),
            ai.AI_TYPE_BYTE: lambda and_obj, and_port: ai.AiNodeGetByte(and_obj, and_port),
            ai.AI_TYPE_FLOAT: lambda and_obj, and_port: ai.AiNodeGetFlt(and_obj, and_port),
            ai.AI_TYPE_BOOLEAN: lambda and_obj, and_port: ai.AiNodeGetBool(and_obj, and_port),
            ai.AI_TYPE_RGB: lambda and_obj, and_port: ai.AiNodeGetRGB(and_obj, and_port),
            ai.AI_TYPE_RGBA: lambda and_obj, and_port: ai.AiNodeGetRGBA(and_obj, and_port),
            ai.AI_TYPE_VECTOR: lambda and_obj, and_port: ai.AiNodeGetVec(and_obj, and_port),
            ai.AI_TYPE_VECTOR2: lambda and_obj, and_port: ai.AiNodeGetVec2(and_obj, and_port),
            ai.AI_TYPE_MATRIX: lambda and_obj, and_port: ai.AiNodeGetMatrix(and_obj, and_port),
            ai.AI_TYPE_NODE: lambda and_obj, and_port: ai.AiNodeGetPtr(and_obj, and_port),
            #
            ai.AI_TYPE_ENUM: lambda and_obj, and_port: ai.AiNodeGetInt(and_obj, and_port),
        }
        AR_ARRAY_VALUE_FNC_DICT = {
            ai.AI_TYPE_STRING: ai.AiArrayGetStr,
            ai.AI_TYPE_INT: ai.AiArrayGetInt,
            ai.AI_TYPE_UINT: ai.AiArrayGetUInt,
            ai.AI_TYPE_BYTE: ai.AiArrayGetByte,
            ai.AI_TYPE_FLOAT: ai.AiArrayGetFlt,
            ai.AI_TYPE_BOOLEAN: ai.AiArrayGetBool,
            ai.AI_TYPE_RGB: ai.AiArrayGetRGB,
            ai.AI_TYPE_RGBA: ai.AiArrayGetRGBA,
            ai.AI_TYPE_VECTOR: ai.AiArrayGetVec,
            ai.AI_TYPE_VECTOR2: ai.AiArrayGetVec2,
            ai.AI_TYPE_MATRIX: ai.AiArrayGetMtx,
            ai.AI_TYPE_NODE: ai.AiArrayGetPtr,
        }

        AOV_TYPES = [
            ("int", ai.ai_params.AI_TYPE_INT),
            ("uint", ai.ai_params.AI_TYPE_UINT),
            ("bool", ai.ai_params.AI_TYPE_BOOLEAN),
            ("float", ai.ai_params.AI_TYPE_FLOAT),
            ("rgb", ai.ai_params.AI_TYPE_RGB),
            ("rgba", ai.ai_params.AI_TYPE_RGBA),
            ("vector", ai.ai_params.AI_TYPE_VECTOR),
            ("vector2", ai.ai_params.AI_TYPE_VECTOR2),
            ("pointer", ai.ai_params.AI_TYPE_POINTER)
        ]


class AndCategories(object):
    ARRAY_NAME = 'array'
    COLOR_NAME = 'tuple'
    CONSTANT_NAME = 'constant'


class AndTypes(object):
    PATHSEP = '/'

    @classmethod
    def get_name(cls, and_type):
        if and_type in AndBase.TYPE_NAME_QUERY:
            return AndBase.TYPE_NAME_QUERY[and_type]
        return unr_core.UnrType.NONE

    @classmethod
    def get_is_ar_array(cls, and_type):
        return and_type == ai.AI_TYPE_ARRAY

    @classmethod
    def get_is_ar_enumerate(cls, and_type):
        return and_type == ai.AI_TYPE_ENUM

    @classmethod
    def get_path(cls, category_name, type_name):
        return cls.PATHSEP.join(
            (category_name, type_name)
        )


class AndNodeCategories(object):
    AND_SHAPE_NAME = 'shape'
    AND_SHADER_NAME = 'shader'
    #
    LYNXI = 'lynxi'


class AndNodeTypes(object):
    PATHSEP = '/'
    #
    AND_MESH_NAME = 'polymesh'
    AND_CURVE_NAME = 'curves'
    AND_XGEN_NAME = 'xgen_procedural'
    # geometry
    QSM_MESH_ARGS = AndNodeCategories.LYNXI, 'mesh'
    QSM_MESH = PATHSEP.join(QSM_MESH_ARGS)
    #
    QSM_CURVE_ARGS = AndNodeCategories.LYNXI, 'curve'
    QSM_CURVE = PATHSEP.join(QSM_CURVE_ARGS)
    #
    QSM_XGEN_DESCRIPTION_ARGS = AndNodeCategories.LYNXI, 'xgen_description'
    QSM_XGEN_DESCRIPTION = PATHSEP.join(QSM_XGEN_DESCRIPTION_ARGS)
    # material
    QSM_MATERIAL_ARGS = AndNodeCategories.LYNXI, 'material'
    QSM_MATERIAL = PATHSEP.join(QSM_MATERIAL_ARGS)


class AndNodes(object):
    PATHSEP = '/'
    MAYA_PATHSEP = '|'
    ARNOLD_PATHSEP = '/'
    HOUDINI_PATHSEP = '/'
    #
    BUILTINS = [
        'root',
        'options',
        'ai_default_reflection_shader',
        'ai_bad_shader',
        '_default_arnold_shader',
        '_default_arnold_shader_color'
    ]

    @classmethod
    def get_output_name(cls, and_type):
        return AndBase.OUTPUT_PORT_NAME_QUERY[and_type]


class AndPorts(object):
    PATHSEP = '.'

    AR_MESH_BLACKLIST = [
        'name',
        'matrix',
        'vidxs',
        'vlist',
        'nsides',
        'uvidxs',
        'shidxs',
        'nlist',
        'nidxs',
        'uvlist',
        'crease_idxs',
        'crease_sharpness',
        'degree_u',
        'degree_v',
        'transform_type',
        'num_points',
        'points',
        'orientations',
        'uvs',
        'cvs',
        'knots_u',
        'knots_v',
        'degree_u',
        'degree_v',
    ]

    AR_WHITELIST = [
        'maya_full_name'
    ]

    PORT_TOKEN_FORMAT = '{assign}{assign_pathsep}{port_path}'
    ELEMENT_PATH_FORMAT = '{port_path}[{element_index}]'
    CHANNEL_PATH_FORMAT = '{port_path}{pathsep}{channel_name}'


class AndMaterialPorts(object):
    SURFACE = 'surface'
    DISPLACEMENT = 'displacement'
    VOLUME = 'volume'


class AndGeometryPorts(object):
    MATERIAL = 'material'


class AndNodeProperties(object):
    AR_MESH_BLACKLIST = [
        'id',
        'visibility',
        'name',
        'matrix',
        'motion_start',
        'motion_end',
        'shader',
        'disp_map',
        'vidxs',
        'vlist',
        'nsides',
        'uvidxs',
        'shidxs',
        'nlist',
        'nidxs',
        'uvlist',
        'crease_idxs',
        'crease_sharpness',
        'degree_u',
        'degree_v',
        'transform_type',
        'num_points',
        'points',
        'orientations',
        'uvs',
        'cvs',
        'knots_u',
        'knots_v',
        'degree_u',
        'degree_v'
    ]
    AR_XGEN_BLACKLIST = [
        'id',
        'visibility',
        'name',
        'matrix',
        'motion_start',
        'motion_end',
        #
        'shader',
        'disp_map',
    ]
    AR_CURVE_BLACKLIST = [
        'id',
        'visibility',
        'name',
        'matrix',
        'motion_start',
        'motion_end',
        #
        'num_points',
        'points',
        'radius',
        'shidxs',
        'uvs',
        'orientations',
        #
        'shader',
        'disp_map',
    ]


class AndGeometryProperties(object):
    AllKeys = [
        'opaque',
        'matte',
        # visibility
        'self_shadows',
        # export
        'sss_setname',
        'trace_sets',
        # volume
        'step_size',
        'volume_padding',
        'smoothing',
        # mesh-subdiv
        'subdiv_type',
        'subdiv_iterations',
        'subdiv_adaptive_error',
        'subdiv_adaptive_metric',
        'subdiv_adaptive_space',
        'subdiv_uv_smoothing',
        'subdiv_smooth_derivs',
        'subdiv_frustum_ignore',
        # mesh-displacement
        'disp_height',
        'disp_padding',
        'disp_zero_value',
        'disp_autobump',
        # curve
        'mode',
        'min_pixel_width',
    ]
    MayaMapper = {
        'opaque': 'aiOpaque',
        'matte': 'aiMatte',
        'self_shadows': 'aiSelfShadows',
        #
        'sss_setname': 'aiSssSetname',
        'trace_sets': 'aiTraceSets',
        #
        'subdiv_type': 'aiSubdivType',
        'subdiv_iterations': 'aiSubdivIterations',
        'subdiv_adaptive_error': 'aiSubdivPixelError',
        'subdiv_adaptive_metric': 'aiSubdivAdaptiveMetric',
        'subdiv_adaptive_space': 'aiSubdivAdaptiveSpace',
        'subdiv_uv_smoothing': 'aiSubdivUvSmoothing',
        'subdiv_smooth_derivs': 'aiSubdivSmoothDerivs',
        'subdiv_frustum_ignore': 'aiSubdivFrustumIgnore',
        # mesh-displacement
        'disp_height': 'aiDispHeight',
        'disp_padding': 'aiDispPadding',
        'disp_zero_value': 'aiDispZeroValue',
        'disp_autobump': 'aiDispAutobump',
        # volume
        'step_size': 'aiStepSize',
        'volume_padding': 'aiVolumePadding',
    }
    AdaptiveSubdivision = dict(
        subdiv_type='catclark',
        subdiv_iterations=2,
        subdiv_adaptive_metric='auto',
        subdiv_adaptive_error=25,
        subdiv_adaptive_space='raster'
    )


class AndVisibilities(object):
    VISIBILITY = 'visibility'
    AUTOBUMP_VISIBILITY = 'autobump_visibility'
    #
    CAMERA = 'camera'
    SHADOW = 'shadow'
    DIFFUSE_REFLECT = 'diffuse_reflect'
    SPECULAR_REFLECT = 'specular_reflect'
    DIFFUSE_TRANSMIT = 'diffuse_transmit'
    SPECULAR_TRANSMIT = 'specular_transmit'
    VOLUME = 'volume'
    SUBSURFACE = 'subsurface'
    #
    ALL = [
        CAMERA,
        SHADOW,
        DIFFUSE_REFLECT, SPECULAR_REFLECT,
        DIFFUSE_TRANSMIT, SPECULAR_TRANSMIT,
        VOLUME,
        SUBSURFACE,
    ]
    # need keep order
    if ARNOLD_FLAG is True:
        AR_RAY_ALL = [
            ai.AI_RAY_CAMERA,
            ai.AI_RAY_SHADOW,
            ai.AI_RAY_DIFFUSE_TRANSMIT,
            ai.AI_RAY_SPECULAR_TRANSMIT,
            ai.AI_RAY_VOLUME,
            ai.AI_RAY_DIFFUSE_REFLECT,
            ai.AI_RAY_SPECULAR_REFLECT,
            ai.AI_RAY_SUBSURFACE,
        ]
        NAME_DICT = {
            ai.AI_RAY_CAMERA: CAMERA,
            ai.AI_RAY_SHADOW: SHADOW,
            ai.AI_RAY_DIFFUSE_REFLECT: DIFFUSE_REFLECT,
            ai.AI_RAY_SPECULAR_REFLECT: SPECULAR_REFLECT,
            ai.AI_RAY_DIFFUSE_TRANSMIT: DIFFUSE_TRANSMIT,
            ai.AI_RAY_SPECULAR_TRANSMIT: SPECULAR_TRANSMIT,
            ai.AI_RAY_VOLUME: VOLUME,
            ai.AI_RAY_SUBSURFACE: SUBSURFACE,
        }
    #
    MAYA_VISIBILITY_DICT = {
        CAMERA: 'primaryVisibility',
        SHADOW: 'castsShadows',
        DIFFUSE_REFLECT: 'aiVisibleInDiffuseReflection',
        SPECULAR_REFLECT: 'aiVisibleInSpecularReflection',
        DIFFUSE_TRANSMIT: 'aiVisibleInDiffuseTransmission',
        SPECULAR_TRANSMIT: 'aiVisibleInSpecularTransmission',
        VOLUME: 'aiVisibleInVolume',
    }
    MAYA_AUTOBUMP_VISIBILITY = 'aiAutobumpVisibility'

    @classmethod
    def get_name(cls, ray):
        return cls.NAME_DICT[ray]

    @classmethod
    def get_visibility(cls, **kwargs):
        ray_dict = {v: k for k, v in cls.NAME_DICT.items()}
        value = ai.AI_RAY_ALL
        for k in cls.ALL:
            v = kwargs.get(k, True)
            ray = ray_dict[k]
            if v is False:
                value &= ~ray
        return value

    @classmethod
    def get_visibility_as_dict(cls, value):
        ar_rays = AndVisibilities.AR_RAY_ALL
        dic = {}
        for v in ar_rays:
            n = AndVisibilities.get_name(v)
            dic[n] = True
        #
        _ = ai.AI_RAY_ALL
        if value < _:
            for v in reversed([v for v in ar_rays]):
                _ &= ~v
                if value <= _:
                    n = AndVisibilities.get_name(v)
                    dic[n] = False
                else:
                    _ += v
        return dic


class AndHairProperties(object):
    ALL = [
        'opaque',
        'matte',
        # visibility
        'self_shadows',
        'trace_sets',
        # export
        'sss_setname',
        # curve
        'mode',
        'min_pixel_width',
    ]
    MAYA_XGEN_DESCRIPTION_DICT = {
        'opaque': 'aiOpaque',
        'matte': 'aiMatte',
        'self_shadows': 'aiSelfShadows',
        #
        'sss_setname': 'aiSssSetname',
        'trace_sets': 'aiTraceSets',
        #
        'mode': 'aiMode',
        'min_pixel_width': 'aiMinPixelWidth',
    }


class AndAovs(object):

    @classmethod
    def get_index(cls, type_name):
        return dict(AndBase.AOV_TYPES)[type_name]
