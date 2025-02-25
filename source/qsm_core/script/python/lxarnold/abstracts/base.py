# coding:utf-8
import copy

import lxbasic.resource as bsc_resource

import lxbasic.content as bsc_content

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgeneral.dcc.core as gnl_dcc_core

import lxuniverse.core as unr_core

import lxuniverse.abstracts as unr_abstracts
# arnold
from ..core.wrap import *

from .. import core as and_core


class AbsDotAssDef(object):
    def _set_dot_ass_def_init_(self):
        pass


# noinspection PyUnusedLocal
class AbsDotMtlxDef(object):
    @property
    def universe(self):
        raise NotImplementedError()

    def restore_all(self):
        raise NotImplementedError()

    def _set_dot_mtlx_def_init_(self):
        pass

    def _set_geometry_objs_build_(self, geometries_properties, root):
        and_obj_type = ai.AiNodeEntryLookUp(and_core.AndNodeTypes.AND_MESH_NAME)
        for geometry_properties in geometries_properties:
            obj_category = self.universe.generate_obj_category(and_core.AndNodeCategories.LYNXI)
            obj_type_name = geometry_properties.get('type')
            obj_type = obj_category.create_type(obj_type_name)
            obj_path = geometry_properties.get('path')
            if root is not None:
                obj_path = '{}{}'.format(root, obj_path)
            obj = obj_type.create_obj(obj_path)

    def _set_load_by_dot_mtlx_(self, file_obj, root=None, path_lstrip=None):
        self.restore_all()
        file_path = file_obj.path
        universe_created = False
        if not ai.AiUniverseIsActive():
            universe_created = True
            ai.AiBegin()
        #
        self._and_universe = ai.AiUniverse()
        self._root = root
        self._path_lstrip = path_lstrip
        #
        dot_mtlx_file_reader = gnl_dcc_core.DotMtlxOptOld(file_path)
        geometries_properties = dot_mtlx_file_reader.get_geometries_properties()
        self._set_geometry_objs_build_(geometries_properties, root=self._root)

        ai.AiUniverseDestroy(self._and_universe)
        if universe_created is True:
            ai.AiEnd()


# noinspection PyUnusedLocal
class AbsObjScene(
    unr_abstracts.AbsObjScene,
    AbsDotAssDef,
    AbsDotMtlxDef
):
    AR_OBJ_CATEGORY_MASK = []
    #
    OPTION = dict(
        shader_rename=False,
        path_lstrip=None,
        #
        look_pass='default',
    )

    def __init__(self, option=None):
        super(AbsObjScene, self).__init__()
        #
        self._option = copy.copy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                self._option[k] = v
        #
        self._shader_rename_enable = self._option['shader_rename']
        self._look_pass_name = self._option['look_pass']
        #
        self._and_universe = None
        self._material_name_dict = {}
        self._shader_name_dict = {}
        self._index_dict = {}
        #
        self._platform = bsc_core.BscPlatform.get_current()

        self._node_configure = bsc_content.Content(
            value=bsc_resource.BscExtendConfigure.get_yaml('arnold/node')
        )
        self._node_configure.do_flatten()

    @property
    def ar_universe(self):
        return self._and_universe

    def load_from_file(self, file_path, path_lstrip=None, path_mapper=None):
        file_obj = self.FILE_CLS(file_path)
        if file_obj.get_is_exists() is True:
            file_ext = file_obj.ext
            if file_ext in ['.ass']:
                self.load_from_dot_ass_fnc(file_obj, path_lstrip)

    def load_from_dot_ass(self, file_path, path_lstrip=None, path_mapper=None, time_tag=None):
        file_obj = self.FILE_CLS(file_path)
        self.load_from_dot_ass_fnc(file_obj, path_lstrip=path_lstrip, path_mapper=path_mapper, time_tag=time_tag)

    def set_load_from_dot_mtlx(self, file_path, root=None, path_lstrip=None):
        file_obj = self.FILE_CLS(file_path)
        self._set_load_by_dot_mtlx_(file_obj, root=root, path_lstrip=path_lstrip)

    # node
    def _set_dcc_obj_build_(self, and_obj_mtd):
        and_universe = and_obj_mtd.universe
        and_obj = and_obj_mtd.obj
        and_obj_type_name = and_obj_mtd.type_name
        and_obj_category_name = and_obj_mtd.category_name
        # shape
        if and_obj_category_name in {and_core.AndNodeCategories.AND_SHAPE_NAME}:
            shape_and_obj_mtd = and_core.AndShapeOpt(and_universe, and_obj)
            # mesh
            if and_obj_type_name in {and_core.AndNodeTypes.AND_MESH_NAME}:
                self._set_dcc_mesh_objs_build_(shape_and_obj_mtd)
            # curve
            elif and_obj_type_name in {and_core.AndNodeTypes.AND_CURVE_NAME}:
                self._set_dcc_curves_build_(shape_and_obj_mtd)
            # xgen
            elif and_obj_type_name in {and_core.AndNodeTypes.AND_XGEN_NAME}:
                self._set_dcc_xgen_objs_build_(shape_and_obj_mtd)
        # shader
        elif and_obj_category_name in {and_core.AndNodeCategories.AND_SHADER_NAME}:
            shader_and_obj_mtd = and_core.AndShaderOpt(and_universe, and_obj)
            self._set_dcc_shader_objs_build(shader_and_obj_mtd)
        # others
        else:
            shader_and_obj_mtd = and_core.AndShaderOpt(and_universe, and_obj)
            self._set_dcc_shader_objs_build(shader_and_obj_mtd)

    # <input-port>
    def _set_dcc_obj_input_ports_build_(self, and_obj_mtd, dcc_obj, include=None, exclude=None):
        and_obj = and_obj_mtd.obj
        and_obj_type = and_obj_mtd.type
        # definition port iterator start
        input_port_iterator = ai.AiNodeEntryGetParamIterator(and_obj_type)
        while not ai.AiParamIteratorFinished(input_port_iterator):
            and_input_port = ai.AiParamIteratorGetNext(input_port_iterator)
            and_input_port_mtd = and_core.AndPortOpt(and_obj, and_input_port)
            and_input_port_name = and_input_port_mtd.port_name
            #
            if isinstance(include, (tuple, list)):
                if and_input_port_name not in include:
                    continue
            #
            if isinstance(exclude, (tuple, list)):
                if and_input_port_name in exclude:
                    continue
            #
            self._set_dcc_obj_input_port_build_(
                and_obj_mtd=and_obj_mtd,
                and_port_mtd=and_input_port_mtd,
                dcc_obj=dcc_obj,
                is_custom=False
            )
        # definition port iterator finish
        ai.AiParamIteratorDestroy(input_port_iterator)
        # custom port iterator start
        custom_input_port_iterator = ai.AiNodeGetUserParamIterator(and_obj)
        while not ai.AiUserParamIteratorFinished(custom_input_port_iterator):
            and_custom_input_port = ai.AiUserParamIteratorGetNext(custom_input_port_iterator)
            and_custom_input_port_mtd = and_core.AndPortOptForCustomize(and_obj, and_custom_input_port)
            and_custom_input_port_name = and_custom_input_port_mtd.port_name
            #
            if isinstance(include, (tuple, list)):
                if and_custom_input_port_name not in include:
                    continue
            #
            if isinstance(exclude, (tuple, list)):
                if and_custom_input_port_name in exclude:
                    continue
            #
            self._set_dcc_obj_input_port_build_(
                and_obj_mtd=and_obj_mtd,
                and_port_mtd=and_custom_input_port_mtd,
                dcc_obj=dcc_obj,
                is_custom=True
            )
        # custom port iterator finish
        ai.AiUserParamIteratorDestroy(custom_input_port_iterator)

    #
    def _set_dcc_obj_input_port_build_(self, and_obj_mtd, and_port_mtd, dcc_obj, is_custom):
        and_port_name = and_port_mtd.port_name
        #
        and_type_is_array = and_port_mtd.get_type_is_array()
        and_is_enumerate_type = and_port_mtd.is_enumerate_type()
        if and_is_enumerate_type is True:
            ar_port_enumerate_strings = and_port_mtd.get_enumerate_strings()
        else:
            ar_port_enumerate_strings = []
        # type
        and_exact_type = and_port_mtd.exact_type
        dcc_category_name, dcc_type_name = and_core.AndTypeOpt(and_exact_type).get_dcc_type_args(and_type_is_array)
        dcc_type = self.universe.create_type(dcc_category_name, dcc_type_name)
        #
        dcc_port_raw_default = and_port_mtd.get_default()
        #
        dcc_port_raw = and_port_mtd.get()
        #
        if and_port_name == 'filename':
            if and_exact_type == ai.AI_TYPE_STRING:
                dcc_port_raw = bsc_storage.StgEnvPathMapper.map_to_path(dcc_port_raw)
        #
        dcc_input_port = dcc_obj.generate_port(dcc_type, and_port_name, unr_core.UnrPortAssign.INPUTS)
        dcc_input_port.set_custom(is_custom)
        #
        dcc_input_port.set(dcc_port_raw)
        dcc_input_port.set_default(dcc_port_raw_default)
        #
        dcc_input_port.set_enumerate(and_is_enumerate_type)
        dcc_input_port.set_enumerate_raw(ar_port_enumerate_strings)
        # input connection
        self._set_dcc_obj_connection_build_(
            and_obj_mtd=and_obj_mtd,
            and_port_name=and_port_name
        )
        # input children
        if and_type_is_array is True:
            # input element
            and_input_port_array = and_port_mtd.get_array()
            and_input_port_array_element_count = and_core.AndArrayOpt(and_input_port_array).get_element_count()
            self._set_dcc_port_elements_build_(
                and_obj_mtd=and_obj_mtd,
                and_type=and_exact_type,
                ar_element_count=and_input_port_array_element_count,
                dcc_port=dcc_input_port
            )
        else:
            # input channel
            self._set_dcc_port_channels_build_(
                and_obj_mtd=and_obj_mtd,
                and_type=and_exact_type,
                dcc_port=dcc_input_port
            )

    # <output-port>
    def _set_dcc_obj_output_ports_build_(self, and_obj_mtd, dcc_obj):
        and_type_is_array = False
        and_output_type = and_obj_mtd.output_type
        dcc_output_port_name = and_obj_mtd.get_dcc_output_port_name()

        dcc_category_name, dcc_type_name = and_core.AndTypeOpt(and_output_type).get_dcc_type_args(and_type_is_array)
        dcc_type = self.universe.create_type(dcc_category_name, dcc_type_name)
        dcc_output = dcc_obj.generate_port(dcc_type, dcc_output_port_name, unr_core.UnrPortAssign.OUTPUTS)
        # output channel
        self._set_dcc_port_channels_build_(
            and_obj_mtd=and_obj_mtd,
            and_type=and_output_type,
            dcc_port=dcc_output
        )

    # <port-element>
    def _set_dcc_port_elements_build_(self, and_obj_mtd, and_type, ar_element_count, dcc_port):
        if ar_element_count > 0:
            for port_element_index in range(ar_element_count):
                port_element_dcc_obj = dcc_port._set_element_create_(port_element_index)
                # <port-path>
                and_element_port_name = port_element_dcc_obj.port_path
                # <obj-connection>
                self._set_dcc_obj_connection_build_(
                    and_obj_mtd=and_obj_mtd,
                    and_port_name=and_element_port_name
                )
                # <port-channel>
                self._set_dcc_port_channels_build_(
                    and_obj_mtd=and_obj_mtd,
                    and_type=and_type,
                    dcc_port=port_element_dcc_obj
                )

    # <port-channel>
    def _set_dcc_port_channels_build_(self, and_obj_mtd, and_type, dcc_port):
        port_channel_dcc_names = and_core.AndTypeOpt(and_type).get_dcc_channel_names()
        for port_channel_dcc_name in port_channel_dcc_names:
            port_channel_dcc_obj = dcc_port._set_channel_create_(port_channel_dcc_name)
            port_channel_dcc_path = port_channel_dcc_obj.port_path
            # channel connection
            self._set_dcc_obj_connection_build_(
                and_obj_mtd=and_obj_mtd,
                and_port_name=port_channel_dcc_path
            )

    # <obj-connection>
    def _set_dcc_obj_connection_build_(self, and_obj_mtd, and_port_name):
        target_and_obj_name = and_obj_mtd.name
        target_and_clear_obj_name = and_obj_mtd.set_name_clear(target_and_obj_name)
        target_index = self._index_dict[target_and_obj_name]
        target_and_prettify_obj_name = and_obj_mtd.set_name_prettify(target_index, self._look_pass_name, self._time_tag)
        if and_obj_mtd.get_port_has_source(and_port_name) is True:
            source_args = and_obj_mtd.get_dcc_port_source_args(and_port_name)
            if source_args is not None:
                dcc_source_obj_args, dcc_source_port_args = source_args
                source_and_obj_name = dcc_source_obj_args[-1]
                and_universe = and_obj_mtd.universe
                source_and_obj = and_core.AndUniverseOpt(and_universe).get_obj(source_and_obj_name)
                source_and_obj_mtd = and_core.AndNodeOpt(and_universe, source_and_obj)
                source_index = self._index_dict[source_and_obj_name]
                source_and_prettify_obj_name = source_and_obj_mtd.set_name_prettify(
                    source_index, self._look_pass_name, self._time_tag
                    )
                dcc_source_obj_args = ('', source_and_prettify_obj_name)
                self.universe.create_connection(
                    dcc_source_obj_args, dcc_source_port_args,
                    ('', target_and_prettify_obj_name), (and_port_name,)
                )

    #
    def _set_dcc_shader_objs_build(self, shader_and_obj_mtd):
        and_orig_obj_name = shader_and_obj_mtd.get_orig_name()
        and_clear_obj_name = shader_and_obj_mtd.set_name_clear(and_orig_obj_name)
        index = self._index_dict[and_orig_obj_name]
        and_prettify_obj_name = shader_and_obj_mtd.set_name_prettify(index, self._look_pass_name, self._time_tag)
        #
        and_obj_type_name = shader_and_obj_mtd.type_name
        and_obj_category_name = shader_and_obj_mtd.category_name
        dcc_obj_type = self.universe.create_obj_type(and_obj_category_name, and_obj_type_name)
        dcc_obj_path_args = ('', and_prettify_obj_name)
        dcc_obj = dcc_obj_type.generate_obj(dcc_obj_path_args)
        # port/input
        self._set_dcc_obj_input_ports_build_(shader_and_obj_mtd, dcc_obj)
        # port/output
        self._set_dcc_obj_output_ports_build_(shader_and_obj_mtd, dcc_obj)

    # mesh
    def _set_dcc_mesh_objs_build_(self, shape_and_obj_mtd):
        and_obj_name = shape_and_obj_mtd.name
        maya_obj_path = shape_and_obj_mtd.get_maya_path()
        if maya_obj_path is not None:
            mesh_dcc_objs = self.create_mesh_for_maya_fnc(maya_obj_path)
        else:
            mesh_dcc_objs = self.create_mesh_fnc(and_obj_name)
        # material
        dcc_material_objs = self._set_dcc_materials_build_(shape_and_obj_mtd)
        for i_dcc_mesh in mesh_dcc_objs:
            # material
            self._set_dcc_obj_material_input_build_(i_dcc_mesh, [i.path for i in dcc_material_objs], [])
            # property
            self._set_dcc_geometry_obj_properties_build_(
                shape_and_obj_mtd, i_dcc_mesh,
                blacklist=and_core.AndNodeProperties.AR_MESH_BLACKLIST
            )
            # visibility
            self._set_dcc_geometry_obj_visibilities_build_(shape_and_obj_mtd, i_dcc_mesh)

    def _set_dcc_geometry_create_(self, obj_type_args, obj_path_args):
        dcc_obj_type = self.universe.create_obj_type(*obj_type_args)
        # clear namespace per component for path args
        obj_path_args = [bsc_core.BscNodePath.get_dag_name_with_namespace_clear(i) for i in obj_path_args]
        # path lstrip
        obj_path = bsc_core.BscNodePath.get_dag_path(obj_path_args)
        obj_path = bsc_core.BscNodePath.get_dag_path_lstrip(obj_path, self._path_lstrip)
        if self._path_mapper_opt is not None:
            obj_path = self._path_mapper_opt.get(obj_path)
        dcc_obj = dcc_obj_type.create_obj(obj_path)
        return dcc_obj

    def create_mesh_for_maya_fnc(self, maya_obj_path):
        dcc_obj = self._set_dcc_geometry_create_(
            # trim <shape-name>
            and_core.AndNodeTypes.QSM_MESH_ARGS, maya_obj_path.split(and_core.AndNodes.MAYA_PATHSEP)
        )
        return [dcc_obj]

    def create_mesh_fnc(self, shape_and_obj_path):
        dcc_obj = self._set_dcc_geometry_create_(
            and_core.AndNodeTypes.QSM_MESH_ARGS, shape_and_obj_path.split(and_core.AndNodes.ARNOLD_PATHSEP)
        )
        return [dcc_obj]

    # geometry-properties
    def _set_dcc_geometry_obj_properties_build_(self, and_obj_mtd, dcc_obj, blacklist):
        dcc_obj_type_name = dcc_obj.type.name
        includes = self._node_configure.get('properties.{}'.format(dcc_obj_type_name))
        self._set_dcc_obj_input_ports_build_(
            and_obj_mtd, dcc_obj,
            include=includes
        )

    def _set_dcc_geometry_obj_visibilities_build_(self, shape_and_obj_mtd, dcc_obj):
        visibility_dict = shape_and_obj_mtd.get_visibility_dict()
        for k, v in visibility_dict.items():
            self._set_dcc_geometry_obj_visibility_build_(dcc_obj, k, v)

    def _set_dcc_geometry_obj_visibility_build_(self, dcc_obj, dcc_port_name, dcc_port_raw):
        and_type_is_array = False
        dcc_category_name, dcc_type_name = and_core.AndTypeOpt(ai.AI_TYPE_BOOLEAN).get_dcc_type_args(and_type_is_array)
        dcc_type = self.universe.create_type(dcc_category_name, dcc_type_name)
        dcc_port = dcc_obj.generate_port(dcc_type, dcc_port_name, unr_core.UnrPortAssign.INPUTS)
        dcc_port.set(dcc_port_raw)
        dcc_port.set_default(True)
        return dcc_port

    def _set_dcc_obj_material_input_build_(self, dcc_obj, dcc_port_raw, dcc_port_raw_default):
        and_type_is_array = True
        dcc_category_name, dcc_type_name = and_core.AndTypeOpt(ai.AI_TYPE_NODE).get_dcc_type_args(and_type_is_array)
        dcc_type = self.universe.create_type(dcc_category_name, dcc_type_name)
        dcc_port_name = and_core.AndGeometryPorts.MATERIAL
        #
        _dcc_material_port = dcc_obj.generate_port(dcc_type, dcc_port_name, unr_core.UnrPortAssign.INPUTS)
        _dcc_material_port.set(dcc_port_raw)
        _dcc_material_port.set_default(dcc_port_raw_default)

    # curve
    def _set_dcc_curves_build_(self, shape_and_obj_mtd):
        and_obj_name = shape_and_obj_mtd.name
        maya_obj_path = shape_and_obj_mtd.get_maya_path()
        if maya_obj_path is not None:
            dcc_curve_objs = self._get_maya_curve_objs_(maya_obj_path)
        else:
            dcc_curve_objs = self._set_curve_objs_create_(and_obj_name)
        # material
        dcc_material_objs = self._set_dcc_materials_build_(shape_and_obj_mtd)
        for dcc_curve_obj in dcc_curve_objs:
            # material
            self._set_dcc_obj_material_input_build_(dcc_curve_obj, [i.name for i in dcc_material_objs], [])
            # property
            self._set_dcc_geometry_obj_properties_build_(
                shape_and_obj_mtd, dcc_curve_obj,
                blacklist=and_core.AndNodeProperties.AR_CURVE_BLACKLIST
            )
            # visibility
            self._set_dcc_geometry_obj_visibilities_build_(shape_and_obj_mtd, dcc_curve_obj)

    def _set_curve_objs_create_(self, shape_and_obj_path):
        dcc_obj = self._set_dcc_geometry_create_(
            and_core.AndNodeTypes.QSM_CURVE_ARGS, shape_and_obj_path.split(and_core.AndNodes.ARNOLD_PATHSEP)
        )
        return [dcc_obj]

    def _get_maya_curve_objs_(self, maya_obj_path):
        dcc_obj = self._set_dcc_geometry_create_(
            # trim <shape-name>
            and_core.AndNodeTypes.QSM_CURVE_ARGS, maya_obj_path.split(and_core.AndNodes.MAYA_PATHSEP)
        )
        return [dcc_obj]

    # xgen
    def _set_dcc_xgen_objs_build_(self, shape_and_obj_mtd):
        and_obj_name = shape_and_obj_mtd.name
        maya_obj_path = shape_and_obj_mtd.get_maya_path()
        if maya_obj_path is not None:
            dcc_xgen_objs = self._get_maya_xgen_objs_(maya_obj_path)
        else:
            dcc_xgen_objs = self._set_xgen_description_objs_create_(and_obj_name)
        #
        dcc_material_objs = self._set_dcc_materials_build_(shape_and_obj_mtd)
        for dcc_xgen_obj in dcc_xgen_objs:
            # material
            self._set_dcc_obj_material_input_build_(dcc_xgen_obj, [i.name for i in dcc_material_objs], [])
            # property
            self._set_dcc_geometry_obj_properties_build_(
                shape_and_obj_mtd, dcc_xgen_obj,
                blacklist=and_core.AndNodeProperties.AR_XGEN_BLACKLIST
            )
            # visibility
            self._set_dcc_geometry_obj_visibilities_build_(shape_and_obj_mtd, dcc_xgen_obj)

    def _get_maya_xgen_objs_(self, maya_obj_path):
        dcc_obj = self._set_dcc_geometry_create_(
            # trim <shape-name>
            and_core.AndNodeTypes.QSM_XGEN_DESCRIPTION_ARGS, maya_obj_path.split(and_core.AndNodes.MAYA_PATHSEP)[:-1]
        )
        return [dcc_obj]

    def _set_xgen_description_objs_create_(self, dcc_obj_path):
        obj_path_args = dcc_obj_path.split(and_core.AndNodes.ARNOLD_PATHSEP)
        if obj_path_args[-1].endswith('Shape'):
            obj_path_args = obj_path_args[:-1]
        dcc_obj = self._set_dcc_geometry_create_(
            # trim <shape-name>
            obj_type_args=and_core.AndNodeTypes.QSM_XGEN_DESCRIPTION_ARGS, obj_path_args=obj_path_args
        )
        return [dcc_obj]

    # material
    def _set_dcc_materials_build_(self, shape_and_obj_mtd):
        # material
        and_universe = shape_and_obj_mtd.universe
        and_surface_shader_objs = shape_and_obj_mtd.get_surface_shader_objs()
        and_surface_shader_obj_name = None
        if and_surface_shader_objs:
            and_surface_shader_obj_mtd = and_core.AndShaderOpt(and_universe, and_surface_shader_objs[0])
            orig_and_surface_shader_obj_name = and_surface_shader_obj_mtd.name
            if orig_and_surface_shader_obj_name is not None:
                if orig_and_surface_shader_obj_name != 'ai_default_reflection_shader':
                    surface_index = self._index_dict[orig_and_surface_shader_obj_name]
                    and_surface_shader_obj_name = and_surface_shader_obj_mtd.set_name_prettify(
                        surface_index, self._look_pass_name, self._time_tag
                        )
        #
        and_displacement_shader_obj_name = None
        and_displacement_shader_objs = shape_and_obj_mtd.get_displacement_shader_objs()
        if and_displacement_shader_objs:
            and_displacement_shader_obj_mtd = and_core.AndShaderOpt(and_universe, and_displacement_shader_objs[0])
            orig_and_displacement_shader_obj_name = and_displacement_shader_obj_mtd.name
            if orig_and_displacement_shader_obj_name is not None:
                if orig_and_displacement_shader_obj_name != 'ai_default_reflection_shader':
                    displacement_index = self._index_dict[orig_and_displacement_shader_obj_name]
                    and_displacement_shader_obj_name = and_displacement_shader_obj_mtd.set_name_prettify(
                        displacement_index, self._look_pass_name, self._time_tag
                        )
        # volume
        and_volume_shader_obj_name = None
        #
        material_key = ';'.join(
            [str(i) for i in
             (and_surface_shader_obj_name, and_displacement_shader_obj_name, and_volume_shader_obj_name)]
        )
        if material_key != ';'.join([str(None)]*3):
            if material_key not in self._material_name_dict:
                if self._time_tag is not None:
                    dcc_material_name = '{}__material__{}__{}'.format(
                        self._look_pass_name, len(self._material_name_dict), self._time_tag
                        )
                else:
                    dcc_material_name = '{}__material__{}'.format(self._look_pass_name, len(self._material_name_dict))
                #
                dcc_obj = self._set_dcc_material_build_(
                    dcc_material_name,
                    (
                        and_surface_shader_obj_name,
                        and_displacement_shader_obj_name,
                        and_volume_shader_obj_name)
                )
                self._material_name_dict[material_key] = dcc_material_name
            else:
                dcc_material_name = self._material_name_dict[material_key]
                dcc_obj = self.universe.get_obj(dcc_material_name)
            #
            dcc_nodes = [dcc_obj]
        else:
            dcc_nodes = []
        return dcc_nodes

    def _set_dcc_material_build_(self, material_dcc_obj_name, shader_dcc_obj_names):
        dcc_obj_type = self.universe.create_obj_type(*and_core.AndNodeTypes.QSM_MATERIAL_ARGS)
        obj_path_args = ('', material_dcc_obj_name)
        dcc_obj = dcc_obj_type.generate_obj(obj_path_args)
        # shader port
        and_surface_shader_obj_name, and_displacement_shader_obj_name, and_volume_shader_obj_name = shader_dcc_obj_names
        shader_build_args = [
            (and_surface_shader_obj_name, and_core.AndMaterialPorts.SURFACE),
            (and_displacement_shader_obj_name, and_core.AndMaterialPorts.DISPLACEMENT),
            (and_volume_shader_obj_name, and_core.AndMaterialPorts.VOLUME)
        ]
        for shader_and_obj_name, material_dcc_port_name in shader_build_args:
            self._set_dcc_material_bind_port_build_(
                dcc_obj=dcc_obj,
                dcc_port_name=material_dcc_port_name,
                dcc_port_raw=shader_and_obj_name
            )
        return dcc_obj

    def _set_dcc_material_bind_port_build_(self, dcc_obj, dcc_port_name, dcc_port_raw):
        and_type_is_array = False
        dcc_category_name, dcc_type_name = and_core.AndTypeOpt(ai.AI_TYPE_CLOSURE).get_dcc_type_args(and_type_is_array)
        dcc_type = self.universe.create_type(dcc_category_name, dcc_type_name)
        dcc_port = dcc_obj.generate_port(dcc_type, dcc_port_name, unr_core.UnrPortAssign.INPUTS)
        if dcc_port_raw is not None:
            shader_obj_path = '/{}'.format(dcc_port_raw)
        else:
            shader_obj_path = None
        dcc_port.set(shader_obj_path)
        dcc_port.set_default(None)
        return dcc_port

    def _set_ar_universe_load_(self):
        pass

    # main method
    def load_from_dot_ass_fnc(self, file_obj, path_lstrip=None, path_mapper=None, time_tag=None):
        self.restore_all()
        #
        if path_mapper is not None:
            self._path_mapper_opt = bsc_core.BscNodePathMapOpt(path_mapper)
        #
        file_path = file_obj.path

        universe_created = False
        if not ai.AiUniverseIsActive():
            universe_created = True
            ai.AiBegin()
        #
        self._and_universe = ai.AiUniverse()
        self._path_lstrip = path_lstrip
        self._time_tag = time_tag
        ai.AiASSLoad(self._and_universe, file_path, ai.AI_NODE_ALL)
        # node iterator start
        and_obj_iterator = ai.AiUniverseGetNodeIterator(self._and_universe, sum(self.AR_OBJ_CATEGORY_MASK))
        self.get_index_dict()
        bsc_log.Log.trace_method_result(
            'ass load',
            u'file="{}"'.format(file_path)
        )
        with bsc_log.LogProcessContext.create(maximum=len(self._index_dict.keys()), label='ass load') as l_p:
            while not ai.AiNodeIteratorFinished(and_obj_iterator):
                l_p.do_update()
                and_obj = ai.AiNodeIteratorGetNext(and_obj_iterator)
                and_obj_mtd = and_core.AndNodeOpt(self._and_universe, and_obj)
                and_obj_name = and_obj_mtd.name
                if and_obj_name not in and_core.AndNodes.BUILTINS:
                    # filter by node-type-category
                    self._set_dcc_obj_build_(and_obj_mtd)
        # node iterator finish
        ai.AiNodeIteratorDestroy(and_obj_iterator)
        #
        ai.AiUniverseDestroy(self._and_universe)
        if universe_created is True:
            ai.AiEnd()

    def get_index_dict(self):
        and_obj_iterator = ai.AiUniverseGetNodeIterator(self._and_universe, sum(self.AR_OBJ_CATEGORY_MASK))
        index = 0
        while not ai.AiNodeIteratorFinished(and_obj_iterator):
            and_obj = ai.AiNodeIteratorGetNext(and_obj_iterator)
            and_obj_mtd = and_core.AndNodeOpt(self._and_universe, and_obj)
            and_obj_name = and_obj_mtd.name
            #
            index += 1
            self._index_dict[and_obj_name] = index

    def restore_all(self):
        self._universe = self.UNIVERSE_CLS()
        self._path_lstrip = None
        self._path_mapper_opt = None
        self._and_universe = None
        self._material_name_dict = {}

    #
    def _test(self):
        pass
