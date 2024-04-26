# coding:utf-8
import lxbasic.content as bsc_content

import lxbasic.resource as bsc_resource

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxgeneral.fnc.abstracts as gnl_fnc_abstracts

import lxarnold.core as and_core

import lxarnold.dcc.objects as and_dcc_objects

import lxarnold.dcc.operators as and_dcc_operators
# katana
from ... import core as ktn_core
# katana dcc
from ...dcc import objects as ktn_dcc_objects

from ...dcc import operators as ktn_dcc_operators


# noinspection PyUnusedLocal
class FncImporterForLookAssOld(gnl_fnc_abstracts.AbsFncOptionBase):
    OPTION = dict(
        file='',
        location='',
        #
        look_pass='default',
        path_lstrip=None,
        material_root='/root/materials',
        frame=None,
        #
        with_materials=True,
        with_properties=True,
        with_visibilities=True,
        # if set shader is not in includes create is ignore
        shader_includes=[
            # 'surface',
            # 'displacement',
            # 'volume'
        ],
        #
        auto_ambocc_assign=False,
        auto_white_disp_assign=False,
        auto_white_zbrush_assign=False,
    )

    @classmethod
    def _set_look_create_by_geometry_(cls, and_geometry):
        obj_universe = and_geometry.universe
        and_geometry_opt = and_dcc_operators.ShapeLookOpt(and_geometry)
        material_assigns = and_geometry_opt.get_material_assigns()
        for k, v in material_assigns.items():
            for i in v:
                pass
                # i_and_material = obj_universe.get_obj(i)

    @classmethod
    def _set_pst_run_(cls):
        for i in ktn_dcc_objects.AndShaders().get_objs():
            if i.get_port('nodeType').get() in ['ramp_float', 'ramp_rgb']:
                a = ktn_dcc_objects.AndRamp(i.path)
                a._set_ramp_dict_read_()

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

    def __init__(self, option=None):
        super(FncImporterForLookAssOld, self).__init__(option)
        #
        self._file_path = self.get('file')
        self._location = self.get('location')
        self._pass_name = self.get('look_pass')
        self._material_root = self.get('material_root')
        #
        self._convert_configure = bsc_content.Content(
            value=bsc_resource.RscExtendConfigure.get_yaml('arnold/convert')
        )
        self._convert_configure.do_flatten()
        #
        self._with_properties = self.get('with_properties') or False
        self._with_visibilities = self.get('with_visibilities') or False

        self._shader_includes = self.get('shader_includes')

        self._workspace = ktn_dcc_objects.AssetWorkspaceOld()
        self._configure = self._workspace.get_configure()

        self._material_assign_hash_stack = {}
        self._property_assign_hash_stack = {}

    def __set_obj_universe_create_(self):
        obj_scene = and_dcc_objects.Scene(
            option=dict(
                shader_rename=True,
                path_lstrip='/root/world/geo',
                look_pass=self._pass_name
            )
        )
        obj_scene.load_from_dot_ass(
            self._file_path,
            path_lstrip='/root/world/geo'
        )
        self._and_universe = obj_scene.universe

    def __set_look_create_(self, pass_name):
        self._workspace.get_look_pass_index(pass_name)
        #
        self._ramp_dcc_objs = []
        #
        self._configure = self._workspace.set_configure_create(pass_name=pass_name)
        self._configure.do_flatten()
        # geometry
        mesh_and_type = self._and_universe.get_obj_type(and_core.AndNodeTypes.QSM_MESH)
        mesh_and_objs = mesh_and_type.get_objs() if mesh_and_type is not None else []
        curve_and_type = self._and_universe.get_obj_type(and_core.AndNodeTypes.QSM_CURVE)
        curve_and_objs = curve_and_type.get_objs() if curve_and_type is not None else []
        xgen_and_type = self._and_universe.get_obj_type(and_core.AndNodeTypes.QSM_XGEN_DESCRIPTION)
        xgen_and_objs = xgen_and_type.get_objs() if xgen_and_type is not None else []
        #
        and_geometries = mesh_and_objs+curve_and_objs+xgen_and_objs
        # material
        # material_and_type = self._and_universe.get_obj_type(and_core.AndNodeTypes.QSM_MATERIAL)
        # and_materials = material_and_type.get_objs()
        #
        method_args = [
            (self.create_materials_fnc, (and_geometries,)),
            (self.create_assigns_fnc, (and_geometries,))
        ]
        if method_args:
            with bsc_log.LogProcessContext.create(maximum=len(method_args), label='execute look create method') as g_p:
                for i_method, i_args in method_args:
                    g_p.do_update()
                    #
                    i_method(*i_args)
        #
        self.__set_ramp_build_()

    #
    def __set_ramp_build_(self):
        for i in self._ramp_dcc_objs:
            i._set_ramp_dict_write0_()
            i._set_ramp_dict_read_()

    def __set_tags_add_(self, dcc_obj, and_path, parent_port_path=None):
        pass_name = self._pass_name
        tags = [
            ('lx_file', self._file_path),
            ('lx_look_pass', pass_name),
            ('lx_obj', and_path),
            ('lx_user', bsc_core.SysBaseMtd.get_user_name()),
            ('lx_time', bsc_core.SysBaseMtd.get_time())
        ]
        #
        for k, v in tags:
            if parent_port_path is not None:
                port_path = '{}.{}'.format(parent_port_path, k)
            else:
                port_path = k
            dcc_obj.get_port(port_path).set_create('string', v)

    def create_materials_fnc(self, and_geometries):
        if and_geometries:
            pass_name = self._pass_name
            with bsc_log.LogProcessContext.create(maximum=len(and_geometries), label='create material') as g_p:
                for i_gmt_seq, i_and_geometry in enumerate(and_geometries):
                    g_p.do_update()
                    self.create_material_fnc(i_and_geometry, pass_name)

    def create_material_fnc(self, and_geometry, pass_name):
        and_geometry_opt = and_dcc_operators.ShapeLookOpt(and_geometry)
        #
        and_material_paths = and_geometry.get_input_port('material').get()
        if and_material_paths:
            and_material = self._and_universe.get_obj(and_material_paths[0])
            material_group_dcc_path = self._workspace.get_ng_material_group_path_use_hash(and_geometry_opt, pass_name)
            is_material_group_create, dcc_material_group = self._workspace.get_ng_material_group_force(
                material_group_dcc_path, pass_name
                )
            if is_material_group_create is True:
                show_obj = [i for i in dcc_material_group.get_children() if i.type_name == 'NetworkMaterial'][0]
                self.__set_tags_add_(show_obj, and_material.path, parent_port_path='shaders.parameters')
            #
            material_dcc_path = self._workspace.get_ng_material_path_use_hash(and_geometry_opt, pass_name)
            is_material_create, dcc_material = self._workspace.get_ng_material_force(material_dcc_path, pass_name)
            if is_material_create is True:
                self.create_shaders_fnc(and_material, dcc_material, dcc_material.ktn_obj, material_group_dcc_path)
                dcc_material.set_source_objs_layout()

    def create_shaders_fnc(self, and_material, dcc_material, ktn_material, dcc_material_group_path):
        convert_dict = {
            'surface': 'arnoldSurface',
            'displacement': 'arnoldDisplacement',
            'volume': 'arnoldVolume'
        }
        pass_name = self._pass_name
        for i_and_bind_name in convert_dict.keys():
            if self._shader_includes:
                if i_and_bind_name not in self._shader_includes:
                    continue
            #
            i_raw = and_material.get_input_port(i_and_bind_name).get()
            if i_raw is not None:
                i_and_shader = self._and_universe.get_obj(i_raw)
                if i_and_shader is not None:
                    i_ktn_shader_type_name = i_and_shader.type.name
                    i_shader_dcc_path = '{}/{}'.format(
                        dcc_material_group_path,
                        self._workspace.get_ng_shader_name(name=i_and_shader.name, pass_name=pass_name)
                    )
                    i_dcc_shader = ktn_dcc_objects.Node(i_shader_dcc_path)
                    i_ktn_shader, is_create = i_dcc_shader.get_dcc_instance('ArnoldShadingNode')
                    #
                    i_dcc_shader.set_shader_type(i_ktn_shader_type_name)
                    i_ktn_shader.checkDynamicParameters()
                    #
                    self.create_ports_fnc(i_and_shader, i_dcc_shader)
                    #
                    dcc_material.get_input_port(
                        convert_dict.get(i_and_bind_name)
                    ).set_source(
                        i_dcc_shader.get_output_port(
                            'out'
                        )
                    )
                    #
                    self.create_node_graph_fnc(i_and_shader, dcc_material_group_path)
                    #
                    self.__set_tags_add_(i_dcc_shader, i_and_shader.path)
                else:
                    bsc_log.Log.trace_method_warning(
                        'shader create',
                        'obj="{}" is non-exists'.format(i_raw)
                    )

    def create_node_graph_fnc(self, and_shader, dcc_material_group_path):
        convert_dict = {}
        #
        pass_name = self._pass_name
        and_nodes = and_shader.get_all_source_objs()
        for seq, i_and_source_node in enumerate(and_nodes):
            i_and_node_type_name = i_and_source_node.type.name
            #
            i_dcc_node_type_name = i_and_source_node.type.name
            i_dcc_node_path = '{}/{}'.format(
                dcc_material_group_path,
                self._workspace.get_ng_shader_name(name=i_and_source_node.name, pass_name=pass_name)
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
            self.create_ports_fnc(i_and_source_node, i_dcc_node)
            #
            self.__set_tags_add_(i_dcc_node, and_shader.path)
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
                '{}/{}'.format(
                    dcc_material_group_path,
                    self._workspace.get_ng_shader_name(name=i_and_source_node.name, pass_name=pass_name)
                ),
                '{}/{}'.format(
                    dcc_material_group_path,
                    self._workspace.get_ng_shader_name(name=i_and_target_node.name, pass_name=pass_name)
                )
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

    def create_ports_fnc(self, and_obj, dcc_obj):
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

    def create_assigns_fnc(self, and_geometries):
        if and_geometries:
            pass_name = self._pass_name
            #
            key = 'material_assign'
            node_key = self._configure.get('node.{}.keyword'.format(key))
            dcc_group, ktn_group, pos = self._workspace.get_group_args(
                node_key, group_key='definition', pass_name=pass_name
                )
            dcc_group.clear_children()
            with bsc_log.LogProcessContext.create(maximum=len(and_geometries), label='create material-assign') as g_p:
                for i_gmt_seq, i_and_geometry in enumerate(and_geometries):
                    g_p.do_update()
                    self.create_material_assign_fnc(i_and_geometry)
            #
            key = 'property_assign'
            node_key = self._configure.get('node.{}.keyword'.format(key))
            dcc_group, ktn_group, pos = self._workspace.get_group_args(
                node_key, group_key='definition', pass_name=pass_name
                )
            dcc_group.clear_children()
            #
            with bsc_log.LogProcessContext.create(maximum=len(and_geometries), label='create property-assign') as g_p:
                for i_gmt_seq, i_and_geometry in enumerate(and_geometries):
                    g_p.do_update()
                    self.create_geometry_properties_fnc(i_and_geometry)

    # assign
    def create_material_assign_fnc(self, and_geometry):
        pass_name = self._pass_name
        asset_root = self._configure.get('option.asset_root')
        #
        and_geometry_opt = and_dcc_operators.ShapeLookOpt(and_geometry)
        #
        and_material_paths = and_geometry.get_input_port('material').get()
        if and_material_paths:
            dcc_material_assign_path = self._workspace.get_ng_material_assign_path_use_hash(and_geometry_opt, pass_name)

            material_dcc_path = self._workspace.get_ng_material_path_use_hash(and_geometry_opt, pass_name)
            dcc_material = ktn_dcc_objects.Node(material_dcc_path)
            #
            is_create, dcc_material_assign = self._workspace.get_ng_material_assign_force(
                dcc_material_assign_path,
                pass_name=pass_name
            )
            # cel
            material_assign_dcc_opt = ktn_dcc_operators.MaterialAssignOpt(dcc_material_assign)
            shape_path = '{}'.format('/'.join([asset_root]+and_geometry.path.split('/')[2:]))
            material_assign_dcc_opt.set_geometry_path_append(shape_path)
            if is_create is True:
                # value
                material_assign_dcc_opt.assign_material(dcc_material)
                #
                self.__set_tags_add_(dcc_material_assign, and_geometry.path)

    #
    def create_geometry_properties_fnc(self, and_geometry):
        pass_name = self._pass_name
        asset_root = self._configure.get('option.asset_root')

        and_geometry_opt = and_dcc_operators.ShapeLookOpt(and_geometry)
        dcc_path = self._workspace.get_ng_properties_assign_path_use_hash(and_geometry_opt, pass_name)
        #
        is_create, dcc_properties_assign, ktn_properties_assign = self._workspace.get_ng_property_assign_force(
            dcc_path,
            pass_name=pass_name
        )
        # cel
        shape_path = '{}'.format('/'.join([asset_root]+and_geometry.path.split('/')[2:]))
        dcc_properties_assign_opt = ktn_dcc_operators.PropertiesAssignOpt(dcc_properties_assign)
        dcc_properties_assign_opt.set_geometry_path_append(shape_path)
        if is_create is True:
            if self._with_properties is True:
                self._set_geometry_property_ports_(and_geometry_opt, dcc_properties_assign)
            #
            if self._with_visibilities is True:
                self._set_geometry_visibility_ports_(and_geometry_opt, dcc_properties_assign)
            #
            self.__set_tags_add_(dcc_properties_assign, and_geometry.path)

    @ktn_core.Modifier.undo_debug_run
    def set_run(self):
        self.__set_obj_universe_create_()
        #
        self._workspace.set_look_pass_add(self._pass_name)
        #
        self.__set_look_create_(self._pass_name)
        #
        auto_ambocc_assign = self._option['auto_ambocc_assign']
        if auto_ambocc_assign is True:
            ktn_dcc_operators.AssetWorkspaceOptOld(
                self._workspace
            ).set_auto_ambocc_assign(pass_name=self._pass_name)
        #
        auto_white_disp_assign = self._option['auto_white_disp_assign']
        if auto_white_disp_assign is True:
            ktn_dcc_operators.AssetWorkspaceOptOld(
                self._workspace
            ).set_auto_white_disp_assign(
                pass_name=self._pass_name
            )
            #
            ktn_dcc_operators.AssetWorkspaceOptOld(
                self._workspace
            ).set_auto_geometry_properties_assign(
                pass_name=self._pass_name,
                geometry_properties=ktn_dcc_operators.AssetWorkspaceOptOld.WHITE_DISP_GEOMETRY_PROPERTIES_DICT
            )

        auto_white_zbrush_assign = self._option['auto_white_zbrush_assign']
        if auto_white_zbrush_assign is True:
            ktn_dcc_operators.AssetWorkspaceOptOld(
                self._workspace
            ).set_auto_white_zbrush_assign(
                pass_name=self._pass_name
            )
            #
            ktn_dcc_operators.AssetWorkspaceOptOld(
                self._workspace
            ).set_auto_geometry_properties_assign(
                pass_name=self._pass_name,
                geometry_properties=ktn_dcc_operators.AssetWorkspaceOptOld.WHITE_ZBRUSH_GEOMETRY_PROPERTIES_DICT
            )


class FncImporterForLookYml(gnl_fnc_abstracts.AbsFncImporterForLookYmlDcc):
    def __init__(self, option):
        super(FncImporterForLookYml, self).__init__(option)
