# coding:utf-8
import collections

import copy

import lxbasic.content as bsc_content

import lxbasic.resource as bsc_resource

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# arnold
import lxarnold.core as and_core

import lxarnold.dcc.objects as and_dcc_objects

import lxarnold.dcc.operators as and_dcc_operators
# katana
from .. import core as ktn_core
# katana dcc
from ..dcc import objects as ktn_dcc_objects


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class ScpLookAssImport(object):
    OPTION = dict(
        root='/master',
        geometry_location='/root/world/geo',
        material_location='/root/materials',
        look_pass='default',
        #
        path_mapper=[
            ('/master/mod/hi', '/master/hi'),
            ('/master/mod/lo', '/master/lo'),
        ]
    )
    CACHE = {}

    def __init__(self, file_path, option=None):
        self._file_path = file_path
        self._option = copy.copy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                self._option[k] = v

        self._look_pass_name = self._option.get('look_pass')
        self._root_location = self._option.get('root')
        self._geometry_root_location = self._option.get('geometry_location')
        self._material_root_location = self._option.get('material_location')

        self._time_tag = bsc_core.TimestampOpt(
            bsc_storage.StgFileOpt(self._file_path).get_modify_timestamp()
            ).get_as_tag_36()

        self._convert_configure = bsc_content.Content(
            value=bsc_resource.RscExtendConfigure.get_yaml('arnold/convert')
        )
        self._convert_configure.do_flatten()

        self._shader_includes = []

        self._material_hash_cache = {}
        self._geometry_properties_hash_cache = {}

        self._ramp_dcc_objs = []

        self._create_universe_()

    def _create_universe_(self):
        key = self._time_tag
        if key in ScpLookAssImport.CACHE:
            self._and_universe = ScpLookAssImport.CACHE[key]
        else:
            obj_scene = and_dcc_objects.Scene(
                option=dict(
                    shader_rename=True,
                    path_lstrip=self._geometry_root_location,
                    look_pass=None,
                    time_tag=None,
                )
            )
            #
            obj_scene.load_from_dot_ass(
                self._file_path,
                path_lstrip=self._geometry_root_location,
                path_mapper=collections.OrderedDict(self._option.get('path_mapper')),
                time_tag=self._time_tag
            )
            self._and_universe = obj_scene.universe
            ScpLookAssImport.CACHE[key] = self._and_universe
        # geometry
        mesh_and_type = self._and_universe.get_obj_type(and_core.AndNodeTypes.QSM_MESH)
        mesh_and_objs = mesh_and_type.get_objs() if mesh_and_type is not None else []
        curve_and_type = self._and_universe.get_obj_type(and_core.AndNodeTypes.QSM_CURVE)
        curve_and_objs = curve_and_type.get_objs() if curve_and_type is not None else []
        xgen_and_type = self._and_universe.get_obj_type(and_core.AndNodeTypes.QSM_XGEN_DESCRIPTION)
        xgen_and_objs = xgen_and_type.get_objs() if xgen_and_type is not None else []
        #
        self._and_geometries = mesh_and_objs+curve_and_objs+xgen_and_objs

    @ktn_core.Modifier.undo_run
    def create_materials(self, material_group_opt):
        and_geometries = self._and_geometries
        if and_geometries:
            look_pass_name = self._look_pass_name
            with bsc_log.LogProcessContext.create(maximum=len(and_geometries), label='create material') as g_p:
                for i_and_geometry in and_geometries:
                    g_p.do_update()
                    self._create_network_material_(material_group_opt, i_and_geometry, look_pass_name)

            self._build_ramp_()

    def _get_material_name_(self, and_geometry_opt):
        materials = and_geometry_opt.get_material_assigns()
        hash_key = bsc_core.BscHash.get_hash_value(
            materials, as_unique_id=True
        )
        if hash_key in self._material_hash_cache:
            return self._material_hash_cache[hash_key]
        #
        name = and_geometry_opt.obj.name
        self._material_hash_cache[hash_key] = name
        return name

    def _get_geometry_properties_name_(self, and_geometry_opt):
        properties = and_geometry_opt.get_properties()
        visibilities = and_geometry_opt.get_visibilities()
        properties.update(visibilities)
        hash_key = bsc_core.BscHash.get_hash_value(
            properties, as_unique_id=True
        )
        if hash_key in self._geometry_properties_hash_cache:
            return self._geometry_properties_hash_cache[hash_key]
        #
        name = and_geometry_opt.obj.name
        self._geometry_properties_hash_cache[hash_key] = name
        return name

    def _get_node_path_(self, group_path, name, look_pass_name, tag, time_tag=None):
        dcc_name_format = '{group}/{name}__{look_pass}_{tag}'
        dcc_name = dcc_name_format.format(
            group=group_path,
            look_pass=look_pass_name,
            name=name,
            tag=tag
        )
        return dcc_name

    def _create_network_material_(self, material_group_opt, and_geometry, look_pass_name):
        and_geometry_opt = and_dcc_operators.ShapeLookOpt(and_geometry)
        #
        and_material_paths = and_geometry.get_input_port('material').get()
        if and_material_paths:
            and_material = self._and_universe.get_obj(and_material_paths[0])
            material_name = self._get_material_name_(and_geometry_opt)
            #
            material_group_path = material_group_opt.get_path()
            network_material_path = self._get_node_path_(
                material_group_path, material_name, look_pass_name, tag='MTL_NTW'
            )
            ktn_obj, is_create = ktn_core.NGNodeOpt._generate_group_child_create_args(
                network_material_path, 'Material_Wsp'
            )
            if is_create is True:
                network_material_opt = ktn_core.NGNodeOpt(ktn_obj)
                self._create_material_(
                    network_material_opt, and_material, material_name, look_pass_name
                )

    def _create_material_(self, network_material_opt, and_material, material_name, look_pass_name):
        network_material_path = network_material_opt.get_path()
        material_path = self._get_node_path_(network_material_path, material_name, look_pass_name, tag='MTL')
        sg_material_path = self._get_node_path_(
            self._material_root_location, material_name, look_pass_name, tag='MTL'
        )
        ktn_obj, is_create = ktn_core.NGNodeOpt._generate_material_node_graph_create_args(
            material_path, 'NetworkMaterial'
        )
        if is_create is True:
            material_opt = ktn_core.NGNodeOpt(ktn_obj)
            material_opt.set('rootLocation', sg_material_path)
            dcc_material = ktn_dcc_objects.Material(material_path)
            self._create_material_shaders_(and_material, dcc_material, network_material_path, look_pass_name)
            material_opt.gui_layout_shader_graph(
                size=(320, 320), shader_view_state=1.0
            )

    def _create_material_shaders_(self, and_material, dcc_material, network_material_path, look_pass_name):
        convert_dict = {
            'surface': 'arnoldSurface',
            'displacement': 'arnoldDisplacement',
            'volume': 'arnoldVolume'
        }
        for i_and_bind_name in convert_dict.keys():
            if self._shader_includes:
                if i_and_bind_name not in self._shader_includes:
                    continue
            #
            i_raw = and_material.get_input_port(i_and_bind_name).get()
            if i_raw is not None:
                i_and_shader = self._and_universe.get_obj(i_raw)
                if i_and_shader is not None:
                    i_shader_type_name = i_and_shader.type.name
                    i_shader_path = self._get_node_path_(
                        network_material_path, i_and_shader.name, look_pass_name, tag='SDR'
                        )
                    i_ktn_obj, i_is_create = ktn_core.NGNodeOpt._generate_material_node_graph_create_args(
                        i_shader_path, 'ArnoldShadingNode', i_shader_type_name
                    )
                    #
                    i_ktn_obj.checkDynamicParameters()

                    i_dcc_shader = ktn_dcc_objects.Node(i_shader_path)
                    #
                    self._create_shader_parameters_(i_and_shader, i_dcc_shader)
                    #
                    ktn_core.NGNodeOpt._create_connections_by_data(
                        [
                            '{}.out'.format(i_dcc_shader.get_path()),
                            '{}.{}'.format(dcc_material.get_path(), convert_dict.get(i_and_bind_name)),
                        ]
                    )
                    #
                    self._create_material_shader_node_graph_(i_and_shader, network_material_path, look_pass_name)
                else:
                    bsc_log.Log.trace_method_warning(
                        'shader create',
                        'obj="{}" is non-exists'.format(i_raw)
                    )

    def _create_material_shader_node_graph_(self, and_shader, network_material_path, look_pass_name):
        convert_dict = {}
        #
        and_nodes = and_shader.get_all_source_objs()
        for seq, i_and_source_node in enumerate(and_nodes):
            i_and_node_type_name = i_and_source_node.type.name
            #
            i_dcc_node_type_name = i_and_source_node.type.name
            i_dcc_node_path = self._get_node_path_(
                network_material_path, i_and_source_node.name, look_pass_name, tag='SDR'
                )
            #
            if i_and_node_type_name in ['ramp_float', 'ramp_rgb']:
                i_dcc_node = ktn_dcc_objects.AndRamp(i_dcc_node_path)
                self._ramp_dcc_objs.append(i_dcc_node)
            else:
                i_dcc_node = ktn_dcc_objects.Node(i_dcc_node_path)
            #
            i_ktn_node, _ = i_dcc_node.get_dcc_instance('ArnoldShadingNode')
            i_dcc_node.set_shader_type(i_dcc_node_type_name)
            #
            i_ktn_node.checkDynamicParameters()
            #
            if i_and_node_type_name in ['image']:
                # remove katana event value
                i_dcc_node.get_port(
                    'parameters.filename.value'
                ).ktn_port.setExpressionFlag(False)
                #
                i_dcc_node.set('parameters.ignore_missing_textures.value', 1)
            #
            self._create_shader_parameters_(i_and_source_node, i_dcc_node)
        # connection
        and_connections = and_shader.get_all_source_connections()
        for i_and_connection in and_connections:
            i_and_source_node, i_and_target_node = (
                i_and_connection.source_obj,
                i_and_connection.target_obj
            )
            i_and_source_port, i_and_target_port = (
                i_and_connection.source,
                i_and_connection.target
            )
            nod_source_ar_port_path, nod_target_ar_port_path = (
                i_and_source_port.port_path, i_and_target_port.port_path
            )
            nod_source_ktn_obj_path, nod_target_ktn_obj_path = (
                self._get_node_path_(network_material_path, i_and_source_node.name, look_pass_name, tag='SDR'),
                self._get_node_path_(network_material_path, i_and_target_node.name, look_pass_name, tag='SDR')
            )
            nod_source_dcc_obj, nod_target_dcc_obj = (
                ktn_dcc_objects.Node(nod_source_ktn_obj_path),
                ktn_dcc_objects.Node(nod_target_ktn_obj_path)
            )
            nod_source_ktn_obj, nod_target_ktn_obj = (
                nod_source_dcc_obj.ktn_obj, nod_target_dcc_obj.ktn_obj
            )
            nod_source_ktn_port_path, nod_target_ktn_port_path = (
                '.'.join(['out']+nod_source_ar_port_path.split('.')[1:]),
                convert_dict.get(nod_target_ar_port_path, nod_target_ar_port_path)
            )
            nod_source_ktn_port, nod_target_ktn_port = (
                nod_source_ktn_obj.getOutputPort(nod_source_ktn_port_path),
                nod_target_ktn_obj.getInputPort(nod_target_ktn_port_path)
            )
            if nod_source_ktn_port is None:
                bsc_log.Log.trace_error(
                    'connection: "{}" >> "{}"'.format(i_and_source_port.path, i_and_target_port.path)
                )
                continue
            if nod_target_ktn_port is None:
                bsc_log.Log.trace_error(
                    'connection: "{}" >> "{}"'.format(i_and_source_port.path, i_and_target_port.path)
                )
                continue
            nod_source_ktn_port.connect(nod_target_ktn_port)

    def _build_ramp_(self):
        for i in self._ramp_dcc_objs:
            i._set_ramp_dict_write0_()
            i._set_ramp_dict_read_()

    def _create_shader_parameters_(self, and_obj, dcc_obj):
        and_obj_type_name = and_obj.type.name
        convert_and_obj_type_names = self._convert_configure.get_key_names_at(
            'input-ports.to-katana'
        )
        for i_and_port in and_obj.get_input_ports():
            if i_and_port.get_is_element() is False and i_and_port.get_is_channel() is False:
                i_and_port_name = i_and_port.port_name
                dcc_port_key = i_and_port_name
                if and_obj_type_name in convert_and_obj_type_names:
                    convert_and_port_names = self._convert_configure.get_key_names_at(
                        'input-ports.to-katana.{}'.format(and_obj_type_name)
                    )
                    if i_and_port_name in convert_and_port_names:
                        dcc_port_key = self._convert_configure.get(
                            'input-ports.to-katana.{}.{}'.format(and_obj_type_name, i_and_port_name)
                        )
                #
                i_enable_dcc_port = dcc_obj.get_port('parameters.{}.enable'.format(dcc_port_key))
                i_value_dcc_port = dcc_obj.get_port('parameters.{}.value'.format(dcc_port_key))
                i_raw = i_and_port.get()
                if i_value_dcc_port.get_is_exists() is True:
                    if dcc_port_key in ['ramp_Knots', 'ramp_Interpolation', 'ramp_Floats', 'ramp_Colors']:
                        dcc_obj._set_ramp_value_update_(dcc_port_key, i_raw)
                    else:
                        value = i_raw
                        if i_and_port.get_is_enumerate():
                            ktn_type = i_value_dcc_port.type
                            if ktn_type == 'string':
                                value = str(i_and_port.get_as_index())
                            elif ktn_type == 'number':
                                value = i_and_port.get_as_index()
                        #
                        if value is not None:
                            if i_and_port.get_is_value_changed() is True:
                                i_enable_dcc_port.set(True)
                                i_value_dcc_port.set(value)
                else:
                    if i_and_port_name == 'name':
                        dcc_obj.get_port('arnold_name').set_create('string', i_raw)
                    else:
                        bsc_log.Log.trace_method_warning(
                            'shader-port set',
                            'attribute="{}" is non-exists'.format(i_value_dcc_port.path)
                        )

    @ktn_core.Modifier.undo_run
    def create_material_assigns(self, material_assign_group_opt):
        and_geometries = self._and_geometries
        if and_geometries:
            look_pass_name = self._look_pass_name
            with bsc_log.LogProcessContext.create(maximum=len(and_geometries), label='create material-assign') as g_p:
                for i_and_geometry in and_geometries:
                    g_p.do_update()
                    self._create_material_assign_(material_assign_group_opt, i_and_geometry, look_pass_name)

    # assign
    def _create_material_assign_(self, material_assign_group_opt, and_geometry, look_pass_name):
        and_geometry_opt = and_dcc_operators.ShapeLookOpt(and_geometry)
        #
        and_material_paths = and_geometry.get_input_port('material').get()
        if and_material_paths:
            material_assign_group_path = material_assign_group_opt.get_path()
            material_name = self._get_material_name_(and_geometry_opt)
            #
            material_assign_path = self._get_node_path_(
                material_assign_group_path, material_name, look_pass_name, tag='MTA'
            )

            sg_material_path = self._get_node_path_(
                self._material_root_location, material_name, look_pass_name, tag='MTL'
            )
            #
            ktn_obj, is_create = ktn_core.NGNodeOpt._generate_group_child_create_args(
                material_assign_path, 'MaterialAssign_Wsp'
            )
            obj_opt = ktn_core.NGNodeOpt(ktn_obj)
            #
            geometry_path = and_geometry.get_path()
            geometry_path = '{}{}{}'.format(
                self._geometry_root_location, self._root_location, geometry_path.split(self._root_location)[-1]
            )
            obj_opt.update_cell(
                'CEL', geometry_path
            )
            if is_create is True:
                # value
                obj_opt.set(
                    'args.materialAssign.value', sg_material_path
                )
                # material_assign_dcc_opt.set_material_path(sg_material_path)

    def create_geometry_properties_assigns(self, geometry_properties_assign_group_opt):
        and_geometries = self._and_geometries
        if and_geometries:
            look_pass_name = self._look_pass_name
            with bsc_log.LogProcessContext.create(
                    maximum=len(and_geometries), label='create geometry properties-assign'
            ) as g_p:
                for i_and_geometry in and_geometries:
                    g_p.do_update()
                    self._create_geometry_properties_assign_(
                        geometry_properties_assign_group_opt, i_and_geometry, look_pass_name
                        )

    @ktn_core.Modifier.undo_run
    def _create_geometry_properties_assign_(self, geometry_properties_assign_group_opt, and_geometry, look_pass_name):
        geometry_properties_assign_group_path = geometry_properties_assign_group_opt.get_path()

        and_geometry_opt = and_dcc_operators.ShapeLookOpt(and_geometry)

        hash_name = self._get_geometry_properties_name_(and_geometry_opt)

        geometry_properties_assign_path = self._get_node_path_(
            geometry_properties_assign_group_path, hash_name, look_pass_name, tag='GPA'
        )
        #
        ktn_obj, is_create = ktn_core.NGNodeOpt._generate_group_child_create_args(
            geometry_properties_assign_path, 'GeometryPropertiesAssign_Wsp'
        )
        obj_opt = ktn_core.NGNodeOpt(ktn_obj)
        #
        geometry_path = and_geometry.get_path()
        geometry_path = '{}{}{}'.format(
            self._geometry_root_location, self._root_location, geometry_path.split(self._root_location)[-1]
        )
        obj_opt.update_cell(
            'CEL', geometry_path
        )
        if is_create is True:
            dcc_geometry = ktn_dcc_objects.Node(geometry_properties_assign_path)
            self._set_geometry_property_ports_(and_geometry_opt, dcc_geometry)
            #
            self._set_geometry_visibility_ports_(and_geometry_opt, dcc_geometry)

    @classmethod
    def _set_geometry_property_ports_(cls, and_geometry_opt, dcc_geometry):
        port_name_convert_dict = dict(
            subdiv_iterations='iterations',
            disp_zero_value='zero_value'
        )
        value_type_convert_dict = dict(
            trace_sets=lambda x: ' '.join(x)
        )
        #
        and_geometry = and_geometry_opt.obj
        properties = and_geometry_opt.get_properties()
        for i_and_port_name, v in properties.items():
            i_and_port = and_geometry.get_input_port(i_and_port_name)
            #
            i_dcc_port_name = i_and_port_name
            if i_and_port_name in port_name_convert_dict:
                i_dcc_port_name = port_name_convert_dict[i_and_port_name]
            # do not ignore value changed
            if i_and_port.get_is_value_changed() is False:
                pass
            #
            i_enable_ktn_port_name = 'args.arnoldStatements.{}.enable'.format(i_dcc_port_name)
            i_enable_dcc_port = dcc_geometry.get_port(i_enable_ktn_port_name)
            if i_enable_dcc_port.get_is_exists() is True:
                i_enable_dcc_port.set(True)
            else:
                bsc_log.Log.trace_warning(
                    'port-name="{}" is unknown'.format(i_dcc_port_name)
                )
            #
            i_value_ktn_port_name = 'args.arnoldStatements.{}.value'.format(i_dcc_port_name)
            i_value_dcc_port = dcc_geometry.get_port(i_value_ktn_port_name)
            if i_value_dcc_port.get_is_exists() is True:
                i_raw = i_and_port.get()
                if i_dcc_port_name in value_type_convert_dict:
                    i_raw = value_type_convert_dict[i_dcc_port_name](i_raw)
                else:
                    if i_value_dcc_port.type == 'number':
                        if i_and_port.get_is_enumerate():
                            i_raw = i_and_port.get_as_index()
                #
                if i_raw is not None:
                    i_value_dcc_port.set(i_raw)

    @classmethod
    def _set_geometry_visibility_ports_(cls, and_geometry_opt, dcc_geometry):
        # port_name_convert_dict = dict()
        and_geometry = and_geometry_opt.obj
        visibilities = and_geometry_opt.get_visibilities()
        for i_and_port_name, v in visibilities.items():
            i_and_port = and_geometry.get_input_port(i_and_port_name)
            #
            i_dcc_port_name = 'AI_RAY_{}'.format(i_and_port_name.upper())
            #
            if i_and_port.get_is_value_changed() is False:
                pass
            #
            i_enable_ktn_port_name = 'args.arnoldStatements.visibility.{}.enable'.format(i_dcc_port_name)
            i_enable_dcc_port = dcc_geometry.get_port(i_enable_ktn_port_name)
            if i_enable_dcc_port.get_is_exists() is True:
                i_enable_dcc_port.set(True)
            else:
                bsc_log.Log.trace_warning(
                    'port-name="{}" is unknown'.format(i_dcc_port_name)
                )
            #
            i_value_ktn_port_name = 'args.arnoldStatements.visibility.{}.value'.format(i_dcc_port_name)
            i_value_dcc_port = dcc_geometry.get_port(i_value_ktn_port_name)
            if i_value_dcc_port.get_is_exists() is True:
                i_raw = i_and_port.get()
                if i_value_dcc_port.type == 'number':
                    if i_and_port.get_is_enumerate():
                        i_raw = i_and_port.get_as_index()
                if i_raw is not None:
                    i_value_dcc_port.set(i_raw)


class ScpLookMaterialImport(object):
    """
# coding:utf-8
import lxkatana
lxkatana.set_reload()

import lxkatana.process as ktn_core

import lxkatana.scripts as ktn_scripts

ktn_scripts.ScpLookMaterialImport(
    ktn_core.NGNodeOpt(
        'MaterialGroup_Wsp'
    )
).import_from_ass_file(
    '/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/look/scene/v001/all.ass'
)
    """

    def __init__(self, obj_opt, option=None):
        self._obj_opt = obj_opt
        self._option = option

    def import_from_ass_file(self, file_path):
        ScpLookAssImport(file_path, self._option).create_materials(
            self._obj_opt
        )


class ScpLookMaterialAssignImport(object):
    def __init__(self, obj_opt, option=None):
        self._obj_opt = obj_opt
        self._option = option

    def import_from_ass_file(self, file_path):
        ScpLookAssImport(file_path, self._option).create_material_assigns(
            self._obj_opt
        )


class ScpLookGeometryPropertiesAssignImport(object):
    def __init__(self, obj_opt, option=None):
        self._obj_opt = obj_opt
        self._option = option

    def import_from_ass_file(self, file_path):
        ScpLookAssImport(file_path, self._option).create_geometry_properties_assigns(
            self._obj_opt
        )
