# coding:utf-8
import re

import ctypes

import subprocess

import lxuniverse.core as unr_core

import lxbasic.core as bsc_core
# arnold
from .wrap import *

from . import configure as and_cor_configure

if bsc_core.SysBaseMtd.get_is_windows():
    # noinspection PyUnresolvedReferences
    NO_WINDOW = subprocess.STARTUPINFO()
    NO_WINDOW.dwFlags |= subprocess.STARTF_USESHOWWINDOW
else:
    NO_WINDOW = None


class AndUtil(object):
    FLOAT_ROUND = 8

    @staticmethod
    def begin_and_universe():
        if not ai.AiUniverseIsActive():
            ai.AiBegin()
            ai.AiMsgSetConsoleFlags(ai.AI_LOG_NONE)
            return True
        return False

    @staticmethod
    def end_and_universe():
        if ai.AiUniverseIsActive():
            if ai.AiRendering():
                ai.AiRenderInterrupt()
            if ai.AiRendering():
                ai.AiRenderAbort()
            ai.AiEnd()


class AndImage(object):
    @staticmethod
    @bsc_core.MdfBaseMtd.run_as_ignore
    def get_resolution(file_path):
        return ai.AiTextureGetResolution(file_path)

    @staticmethod
    @bsc_core.MdfBaseMtd.run_as_ignore
    def get_bit(file_path):
        return ai.AiTextureGetBitDepth(file_path)

    @staticmethod
    @bsc_core.MdfBaseMtd.run_as_ignore
    def get_type(file_path):
        return ai.AiTextureGetFormat(file_path)

    @staticmethod
    @bsc_core.MdfBaseMtd.run_as_ignore
    def get_channel_count(file_path):
        return ai.AiTextureGetNumChannels(file_path)


class AndTypeOpt(object):
    def __init__(self, type_):
        self._and_instance = type_

    @property
    def and_instance(self):
        return self._and_instance

    @property
    def name(self):
        return ai.AiParamGetTypeName(self.and_instance)

    def get_is_array(self):
        return self.and_instance == ai.AI_TYPE_ARRAY

    def get_dcc_type_args(self, is_array):
        dcc_type_name = and_cor_configure.AndTypes.get_name(self.and_instance)
        dcc_category_name = unr_core.UnrType.get_category_name(dcc_type_name, is_array)
        return dcc_category_name, dcc_type_name

    def get_dcc_channel_names(self):
        dcc_type_name = and_cor_configure.AndTypes.get_name(self.and_instance)
        return unr_core.UnrType.get_channel_names(dcc_type_name)


class AndArrayOpt(object):
    def __init__(self, array):
        self._and_instance = array

    @property
    def and_instance(self):
        return self._and_instance

    def get_element_count(self):
        return ai.AiArrayGetNumElements(self.and_instance)


class AndPortOpt(object):
    def __init__(self, obj, port):
        self._obj = obj
        self._and_instance = port

    @property
    def obj(self):
        return self._obj

    @property
    def category(self):
        if self.get_type_is_array():
            return ai.AI_TYPE_ARRAY
        return ai.type

    @property
    def type(self):
        return ai.AiParamGetType(self.and_instance)

    @property
    def type_name(self):
        return ai.AiParamGetTypeName(self.type)

    @property
    def exact_type(self):
        if self.get_type_is_array():
            return ai.AiArrayGetType(ai.AiParamGetDefault(self.and_instance).contents.ARRAY.contents)
        return self.type

    @property
    def exact_type_name(self):
        return ai.AiParamGetTypeName(self.exact_type)

    @property
    def port(self):
        return self.and_instance

    @property
    def and_instance(self):
        return self._and_instance

    @property
    def port_name(self):
        return ai.AiParamGetName(self.and_instance)

    def get_array(self):
        return ai.AiNodeGetArray(self.obj, self.port_name)

    def get_array_element_count(self):
        return ai.AiArrayGetNumElements(self.get_array())

    def get_type_is_array(self):
        return self.type == ai.AI_TYPE_ARRAY

    def get_is_enumerate_type(self):
        return self.type == ai.AI_TYPE_ENUM

    def get_enumerate_strings(self):
        and_port = self.and_instance
        strings = []
        and_port = ai.AiParamGetEnum(and_port)
        i = 0
        t = True
        while t:
            try:
                t = ai.AiEnumGetString(and_port, i)
                if t:
                    strings.append(t)
            except UnicodeDecodeError as e:
                raise e
            i += 1
        return strings

    def get(self):
        return self._get_raw_()

    def _get_raw_(self):
        if self.get_type_is_array() is True:
            return self._get_array_raw_()
        return self._get_constant_raw_()

    def _get_constant_raw_(self):
        and_obj = self.obj
        and_type = self.type
        and_port = self.and_instance
        and_port_name = self.port_name
        if and_type in and_cor_configure.AndBase.AR_VALUE_FNC_DICT:
            fnc = and_cor_configure.AndBase.AR_VALUE_FNC_DICT[and_type]
            if fnc is not None:
                raw = fnc(and_obj, and_port_name)
                return self._set_raw_convert_to_dcc_style_(and_type, and_port, raw)

    def _get_array_raw_(self):
        and_port = self.and_instance
        #
        and_exact_type = self.exact_type
        if and_exact_type in and_cor_configure.AndBase.AR_ARRAY_VALUE_FNC_DICT:
            lis = []
            fnc = and_cor_configure.AndBase.AR_ARRAY_VALUE_FNC_DICT[and_exact_type]
            and_array = self.get_array()
            and_array_element_count = AndArrayOpt(and_array).get_element_count()
            for and_array_element_index in range(and_array_element_count):
                raw = fnc(and_array, and_array_element_index)
                lis.append(
                    self._set_raw_convert_to_dcc_style_(and_exact_type, and_port, raw)
                )
            return lis

    def get_default(self):
        return self._get_default_raw_()

    def _get_default_raw_(self):
        if self.get_type_is_array() is True:
            return self._get_default_array_raw_()
        return self._get_default_constant_raw_()

    def _get_default_constant_raw_(self):
        and_type = self.type
        and_port = self.and_instance
        if and_type in and_cor_configure.AndBase.AR_DEFAULT_VALUE_FNC_DICT:
            fnc = and_cor_configure.AndBase.AR_DEFAULT_VALUE_FNC_DICT[and_type]
            raw = fnc(and_port)
            return self._set_raw_convert_to_dcc_style_(and_type, and_port, raw)

    def _get_default_array_raw_(self):
        and_port = self.and_instance
        and_exact_type = self.exact_type
        if and_exact_type in and_cor_configure.AndBase.AR_ARRAY_VALUE_FNC_DICT:
            lis = []
            fnc = and_cor_configure.AndBase.AR_ARRAY_VALUE_FNC_DICT[and_exact_type]
            ar_array_default = ai.AiParamGetDefault(and_port).contents.ARRAY.contents
            and_array_element_count = ai.AiArrayGetNumElements(ar_array_default)
            for and_array_element_index in range(and_array_element_count):
                raw = fnc(ar_array_default, and_array_element_index)
                lis.append(
                    self._set_raw_convert_to_dcc_style_(and_exact_type, and_port, raw)
                )
            return lis

    @classmethod
    def _set_raw_convert_to_dcc_style_(cls, and_type, and_port, raw):
        # enumerate
        round_count = AndUtil.FLOAT_ROUND
        if and_type is ai.AI_TYPE_ENUM:
            idx = raw
            return ai.AiEnumGetString(
                ai.AiParamGetEnum(and_port),
                idx
            )
        # color
        elif and_type is ai.AI_TYPE_RGB:
            rgb = raw
            _r, _g, _b = rgb.r, rgb.g, rgb.b
            _raw = round(_r, round_count), round(_g, round_count), round(_b, round_count)
        elif and_type is ai.AI_TYPE_RGBA:
            rgba = raw
            _r, _g, _b, _a = rgba.r, rgba.g, rgba.b, rgba.a
            _raw = round(_r, round_count), round(_g, round_count), round(_b, round_count), round(_a, round_count)
        # tuple/vector2
        elif and_type is ai.AI_TYPE_VECTOR2:
            vec = raw
            _x, _y = vec.x, vec.y
            _raw = round(_x, round_count), round(_y, round_count)
        # tuple/vector3
        elif and_type is ai.AI_TYPE_VECTOR:
            vec = raw
            _x, _y, _z = vec.x, vec.y, vec.z
            _raw = round(_x, round_count), round(_y, round_count), round(_z, round_count)
        # matrix44 (
        #      (float, float, float, float),
        #      (float, float, float, float),
        #      (float, float, float, float),
        #      (float, float, float, float)
        # )
        elif and_type is ai.AI_TYPE_MATRIX:
            mtx = raw
            if isinstance(mtx, ai.ai_matrix.AtMatrix) is False:
                mtx = raw[0]
            _raw = tuple([tuple([mtx[i][j] for j in xrange(4)]) for i in xrange(4)])
        # node
        elif and_type is ai.AI_TYPE_NODE:
            node = raw
            _raw = ai.AiNodeGetName(node)
        # float:
        elif and_type is ai.AI_TYPE_FLOAT:
            _raw = round(raw, round_count)
        else:
            _raw = raw
        return _raw


class AndPortOptForCustomize(AndPortOpt):
    def __init__(self, obj, port):
        super(AndPortOptForCustomize, self).__init__(obj, port)

    @property
    def type(self):
        return ai.AiUserParamGetType(self.and_instance)

    @property
    def exact_type(self):
        if self.get_type_is_array():
            return ai.AiUserParamGetArrayType(self.and_instance)
        return self.type

    @property
    def port_name(self):
        return ai.AiUserParamGetName(self.and_instance)

    def get(self):
        return self._get_raw_()

    def get_default(self):
        return None


class AndNodeTypeOpt(object):
    def __init__(self, type_):
        self._and_instance = type_

    @property
    def and_instance(self):
        return self._and_instance

    @property
    def name(self):
        return ai.AiNodeEntryGetName(self.and_instance)

    @property
    def output_type(self):
        return ai.AiNodeEntryGetOutputType(self._and_instance)


class AndNodeOpt(object):
    PORT_MTD_CLS = AndPortOpt
    CUSTOM_PORT_MTD_CLS = AndPortOptForCustomize

    def __init__(self, universe, obj):
        self._universe = universe
        self._and_instance = obj
        self._and_obj_type_instance = ai.AiNodeGetNodeEntry(obj)
        self._obj_category = ai.AiNodeEntryGetType(self._and_obj_type_instance)

    @property
    def universe(self):
        return self._universe

    @property
    def obj(self):
        return self.and_instance

    @property
    def and_instance(self):
        return self._and_instance

    @property
    def name(self):
        return ai.AiNodeGetName(self.and_instance)

    @property
    def category(self):
        return self._obj_category

    @property
    def category_name(self):
        return ai.AiNodeEntryGetTypeName(self.type)

    @property
    def type(self):
        return self._and_obj_type_instance

    @property
    def type_name(self):
        return AndNodeTypeOpt(self.type).name

    @property
    def output_type(self):
        return ai.AiNodeEntryGetOutputType(self.type)

    @property
    def output_type_name(self):
        return ai.AiParamGetTypeName(self.output_type)

    def get_orig_name(self):
        return ai.AiNodeGetName(self.and_instance)

    @classmethod
    def set_name_clear(cls, name):
        return re.sub(
            ur'[^\u4e00-\u9fa5a-zA-Z0-9]', '_', name
        )

    def set_name_prettify(self, index, look_pass_name=None, time_tag=None):
        type_name = self.type_name
        tags = [
            type_name, index, look_pass_name, time_tag
        ]
        return '_'.join([str(i) for i in tags if i is not None])

    def get_parent(self):
        return ai.AiNodeGetParent(self.and_instance)

    def get_port(self, port_name):
        return ai.AiNodeEntryLookUpParameter(self.type, port_name)

    def get_port_mtd(self, port_name):
        return self.PORT_MTD_CLS(self.and_instance, self.get_port(port_name))

    def get_customize_port(self, port_name):
        return ai.AiNodeLookUpUserParameter(self.and_instance, port_name)

    def get_array_port(self, port_name):
        return ai.AiNodeGetArray(self.and_instance, port_name)

    def get_port_has_source(self, port_name):
        return ai.AiNodeIsLinked(self.and_instance, port_name)

    # dcc
    def get_dcc_port_source_args(self, port_name):
        and_obj = self.and_instance
        #
        and_output_port_index = ctypes.c_int()
        and_source_obj = ai.AiNodeGetLink(and_obj, port_name, ctypes.byref(and_output_port_index))
        if and_source_obj:
            source_and_obj_mtd = self.__class__(self.universe, and_source_obj)
            source_and_obj_name = source_and_obj_mtd.name
            and_output_port_index_value = and_output_port_index.value
            and_type = source_and_obj_mtd.output_type
            #
            dcc_obj_output_name = and_cor_configure.AndNodes.get_output_name(and_type)
            # port-connection / element-connection
            if and_output_port_index_value == -1:
                dcc_source_port_args = (dcc_obj_output_name,)
            # channel-connection
            else:
                dcc_port_channel_names = AndTypeOpt(and_type).get_dcc_channel_names()
                dcc_source_port_args = dcc_obj_output_name, dcc_port_channel_names[and_output_port_index_value]
            return ('', source_and_obj_name), dcc_source_port_args

    def get_dcc_output_port_name(self):
        output_type = self.output_type
        return and_cor_configure.AndNodes.get_output_name(output_type)

    def get_input_ports(self):
        input_dict = {}

        it = ai.AiNodeEntryGetParamIterator(ai.AiNodeGetNodeEntry(self._and_instance))
        while not ai.AiParamIteratorFinished(it):
            i_and_input_port = ai.AiParamIteratorGetNext(it)
            # OSL parameters start with "param_"
            if str(ai.AiParamGetName(i_and_input_port)).startswith("param_"):
                p = ai.AiParamGetName(i_and_input_port)
                i_and_input_port_opt = AndPortOpt(self._and_instance, i_and_input_port)
                input_dict[p] = {}
                input_dict[p]['paramName'] = i_and_input_port_opt.port_name
                input_dict[p]['paramType'] = i_and_input_port_opt.type_name
                input_dict[p]['paramDefaultValue'] = i_and_input_port_opt.get_default()
        return input_dict


class AndShapeOpt(AndNodeOpt):
    def __init__(self, universe, obj):
        super(AndShapeOpt, self).__init__(universe, obj)

    def get_maya_path(self):
        return AndPortOptForCustomize(self.and_instance, self.get_customize_port('maya_full_name')).get()

    def get_surface_shader_objs(self):
        and_obj_type_name = self.type_name
        if and_obj_type_name in [and_cor_configure.AndNodeTypes.AND_MESH_NAME, and_cor_configure.AndNodeTypes.AND_CURVE_NAME]:
            shader_names = self.get_port_mtd('shader').get() or []
            return [AndUniverseOpt(self.universe).get_obj(i) for i in shader_names]
        elif and_obj_type_name in [and_cor_configure.AndNodeTypes.AND_XGEN_NAME]:
            shader_names = AndPortOptForCustomize(self.and_instance, self.get_customize_port('xgen_shader')).get() or []
            if shader_names:
                return [AndUniverseOpt(self.universe).get_obj(i) for i in shader_names]
            #
            shader_names = self.get_port_mtd('shader').get() or []
            return [AndUniverseOpt(self.universe).get_obj(i) for i in shader_names]

    def get_displacement_shader_objs(self):
        and_obj_type_name = self.type_name
        if and_obj_type_name in [and_cor_configure.AndNodeTypes.AND_MESH_NAME, and_cor_configure.AndNodeTypes.AND_CURVE_NAME]:
            shader_names = self.get_port_mtd('disp_map').get() or []
            return [AndUniverseOpt(self.universe).get_obj(i) for i in shader_names]
        elif and_obj_type_name in [and_cor_configure.AndNodeTypes.AND_XGEN_NAME]:
            shader_names = AndPortOptForCustomize(self.and_instance, self.get_customize_port('xgen_disp_map')).get() or []
            if shader_names:
                return [AndUniverseOpt(self.universe).get_obj(i) for i in shader_names]
            #
            shader_names = self.get_port_mtd('disp_map').get() or []
            return [AndUniverseOpt(self.universe).get_obj(i) for i in shader_names]

    def get_visibility_port(self):
        return self.get_port('visibility')

    def get_sidedness_port(self):
        return self.get_port('sidedness')

    def get_visibility_raw(self):
        return self.get_port_mtd('visibility').get()

    def get_visibility_dict(self):
        return self._set_visibility_unpack_(self.get_visibility_raw())

    @classmethod
    def _set_visibility_unpack_(cls, raw):
        ar_rays = and_cor_configure.AndVisibilities.AR_RAY_ALL
        dic = {}
        for v in ar_rays:
            n = and_cor_configure.AndVisibilities.get_name(v)
            dic[n] = True
        comp = ai.AI_RAY_ALL
        if raw < comp:
            for v in reversed([v for v in ar_rays]):
                comp &= ~v
                if raw <= comp:
                    n = and_cor_configure.AndVisibilities.get_name(v)
                    dic[n] = False
                else:
                    comp += v
        return dic

    def get_sidedness_row(self):
        return self.get_port_mtd('sidedness').get()


class AndShaderOpt(AndNodeOpt):
    def __init__(self, universe, obj):
        super(AndShaderOpt, self).__init__(universe, obj)


class AndUniverseOpt(object):
    OBJ_MTD_CLS = AndNodeOpt

    def __init__(self, universe):
        self._and_instance = universe

    @property
    def and_instance(self):
        return self._and_instance

    def get_obj(self, obj_name):
        return ai.AiNodeLookUpByName(self.and_instance, obj_name)


class AndOslShaderMtd(object):
    # noinspection PyUnusedLocal
    @classmethod
    def get_data(cls, code):
        input_dict = {}
        errors = ''
        is_active = ai.AiUniverseIsActive()
        if not is_active:
            ai.AiBegin()

        # create a universe dedicated to OSL node compilation
        # for parameter/output type introspection and error checking
        compilation_universe = ai.AiUniverse()

        and_obj = ai.AiNode(compilation_universe, "osl", "test_node")
        and_obj_opt = AndNodeOpt(compilation_universe, and_obj)

        ai.AiNodeSetStr(and_obj, "code", code)

        if ai.AiNodeLookUpUserParameter(and_obj, "compilation_errors"):
            compilation_errors = ai.AiNodeGetArray(and_obj, "compilation_errors")
        else:
            compilation_errors = None

        if compilation_errors is None or ai.AiArrayGetNumElements(compilation_errors) == 0:
            compile_state = True
            input_dict = and_obj_opt.get_input_ports()
        else:
            compile_state = False
            for i in range(ai.AiArrayGetNumElements(compilation_errors)):
                errors += ai.AiArrayGetStr(compilation_errors, i)+"\n"
        # cleanup the node
        ai.AiUniverseDestroy(compilation_universe)

        if not is_active:
            ai.AiEnd()
        return input_dict
