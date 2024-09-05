# coding:utf-8
import collections
# noinspection PyUnresolvedReferences
from maya import cmds
# basic
import lxbasic.content as bsc_content

import lxbasic.resource as bsc_resource

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgeneral.fnc.abstracts as gnl_fnc_abstracts
# arnold
import lxarnold.core as and_core

import lxarnold.dcc.objects as and_dcc_objects

import lxarnold.dcc.operators as and_dcc_operators
# maya
from ... import core as mya_core
# maya dcc
from ...dcc import objects as mya_dcc_objects

from ...dcc import operators as mya_dcc_operators


class AssImportFnc(object):
    def __init__(self, universe, with_material=True, with_assign=True, assign_selection_enable=False):
        self._and_universe = universe
        self._with_material = with_material
        self._with_assign = with_assign
        self._assign_selection_enable = assign_selection_enable
        #
        self._convert_configure = bsc_content.Content(
            value=bsc_resource.RscExtendConfigure.get_yaml('arnold/convert')
        )
        self._convert_configure.do_flatten()

    def execute(self):
        # geometry
        mesh_and_type = self._and_universe.get_obj_type(and_core.AndNodeTypes.QSM_MESH)
        mesh_and_objs = mesh_and_type.get_objs() if mesh_and_type is not None else []
        curve_and_type = self._and_universe.get_obj_type(and_core.AndNodeTypes.QSM_CURVE)
        curve_and_objs = curve_and_type.get_objs() if curve_and_type is not None else []
        xgen_and_type = self._and_universe.get_obj_type(and_core.AndNodeTypes.QSM_XGEN_DESCRIPTION)
        xgen_and_objs = xgen_and_type.get_objs() if xgen_and_type is not None else []
        #
        geometry_and_objs = mesh_and_objs+curve_and_objs+xgen_and_objs
        # material
        material_and_type = self._and_universe.get_obj_type(and_core.AndNodeTypes.QSM_MATERIAL)
        if material_and_type is not None:
            material_and_objs = material_and_type.get_objs()
            #
            method_args = [
                (self.create_materials_fnc, (material_and_objs,), self._with_material),
                (self.create_assigns_fnc, (geometry_and_objs,), self._with_assign)
            ]
            if method_args:
                with bsc_log.LogProcessContext.create(
                    maximum=len(method_args), label='execute look create method'
                ) as g_p:
                    for i_method, i_args, i_enable in method_args:
                        g_p.do_update()
                        if i_enable is True:
                            i_method(*i_args)
        else:
            raise RuntimeError(
                bsc_log.Log.trace_method_error(
                    'look import',
                    'material(s) is not found'
                )
            )

    def create_materials_fnc(self, material_and_objs):
        if material_and_objs:
            with bsc_log.LogProcessContext.create(maximum=len(material_and_objs), label='create material') as g_p:
                for material_seq, material_and_obj in enumerate(material_and_objs):
                    g_p.do_update()
                    self.create_material_fnc(material_and_obj)

    def create_material_fnc(self, material_and_obj):
        material_and_obj_name = material_and_obj.name
        material_dcc_obj_name = material_and_obj_name
        #
        material_dcc_obj = mya_dcc_objects.Material(material_dcc_obj_name)
        if material_dcc_obj.get_is_exists() is False:
            material_dcc_obj.set_create(mya_dcc_objects.Material.OBJ_TYPE)
            #
            self.create_shaders_fnc(material_and_obj, material_dcc_obj)
            #
            mya_core.CmdObjOpt(material_dcc_obj.path).create_customize_attributes(
                dict(
                    arnold_name=material_and_obj_name
                )
            )

    def create_shaders_fnc(self, material_and_obj, material_dcc_obj):
        convert_dict = {
            'surface': 'surfaceShader',
            'displacement': 'displacementShader',
            'volume': 'volumeShader'
        }
        for i_shader_and_bind_port_name in convert_dict.keys():
            raw = material_and_obj.get_input_port(i_shader_and_bind_port_name).get()
            if raw is not None:
                shader_and_obj = self._and_universe.get_obj(raw)
                shader_dcc_obj, is_create = self.create_shader_fnc(shader_and_obj)
                if shader_dcc_obj is not None:
                    # debug
                    # do not check create, material can use same shader
                    i_shader_dcc_bind_port_name = convert_dict[i_shader_and_bind_port_name]

                    i_shader_and_source_and_port = shader_and_obj.get_output_ports()[0]
                    i_shader_and_source_and_port_path = i_shader_and_source_and_port.port_path
                    if i_shader_and_source_and_port.get_is_channel():
                        key = 'output-ports.to-maya.channels.{}'.format(i_shader_and_source_and_port_path)
                    else:
                        key = 'output-ports.to-maya.{}'.format(i_shader_and_source_and_port_path)

                    source_dcc_port_path = self._convert_configure.get(key)

                    shader_dcc_obj.get_port(source_dcc_port_path).set_target(
                        material_dcc_obj.get_port(i_shader_dcc_bind_port_name)
                    )

    def create_shader_fnc(self, shader_and_obj):
        create_args = self.create_node_fnc(shader_and_obj)
        if create_args is not None:
            shader_dcc_obj, is_create = create_args
            if is_create is True:
                self.create_ports_fnc(shader_and_obj, shader_dcc_obj)
                self.create_node_graph_fnc(shader_and_obj)
                #
                mya_core.CmdObjOpt(shader_dcc_obj.path).create_customize_attributes(
                    dict(
                        arnold_name=shader_and_obj.name
                    )
                )
            return shader_dcc_obj, is_create

    def create_node_graph_fnc(self, and_obj):
        source_and_objs = and_obj.get_all_source_objs()
        for seq, source_and_obj in enumerate(source_and_objs):
            _ = self.create_node_fnc(source_and_obj)
            if _ is not None:
                source_dcc_obj, is_create = _
                self.create_ports_fnc(source_and_obj, source_dcc_obj)
        #
        and_connections = and_obj.get_all_source_connections()
        self.create_connections_fnc(and_connections)

    def create_connections_fnc(self, and_connections):
        for i_and_connection in and_connections:
            self.create_connection_fnc(i_and_connection)

    def create_connection_fnc(self, and_connection):
        source_and_obj, target_and_obj = (
            and_connection.source_obj, and_connection.target_obj
        )
        source_and_obj_type_name, target_and_obj_type_name = (
            source_and_obj.type.name, target_and_obj.type.name
        )
        source_and_port, target_and_port = (
            and_connection.source, and_connection.target
        )
        #
        source_and_port_path, target_and_port_path = (
            source_and_port.port_path, target_and_port.port_path
        )
        if source_and_port.get_is_channel():
            key = 'output-ports.to-maya.channels.{}'.format(source_and_port_path)
        else:
            key = 'output-ports.to-maya.{}'.format(source_and_port_path)
        #
        source_dcc_port_path = self._convert_configure.get(key)
        #
        if target_and_port.get_is_channel():
            a, b = target_and_port_path.split('.')
            target_dcc_port_path = '{0}.{0}{1}'.format(a, b.upper())
        else:
            target_dcc_port_path = bsc_core.RawStrUnderlineOpt(target_and_port_path).to_camelcase()
        #
        and_obj_type_names = self._convert_configure.get_key_names_at(
            'input-ports.to-maya'
        )
        if target_and_obj_type_name in and_obj_type_names:
            and_port_names = self._convert_configure.get_key_names_at(
                'input-ports.to-maya.{}'.format(target_and_obj_type_name)
            )
            if target_and_port_path in and_port_names:
                if target_and_port.get_is_channel():
                    a, b = target_and_port_path.split('.')
                    a = self._convert_configure.get(
                        'input-ports.to-maya.{}.{}'.format(target_and_obj_type_name, target_and_port_path)
                    )
                    target_dcc_port_path = '{0}.{0}{1}'.format(a, b.upper())
                else:
                    target_dcc_port_path = self._convert_configure.get(
                        'input-ports.to-maya.{}.{}'.format(target_and_obj_type_name, target_and_port_path)
                    )

        source_and_obj_name, target_and_obj_name = (
            source_and_obj.name, target_and_obj.name
        )
        #
        source_dcc_obj_name, target_dcc_obj_name = (
            source_and_obj_name, target_and_obj_name
        )

        source_dcc_obj, target_dcc_obj = (
            mya_dcc_objects.AndShader(source_dcc_obj_name), mya_dcc_objects.AndShader(target_and_obj_name)
        )
        #
        if source_dcc_obj.get_is_exists() is False:
            bsc_log.Log.trace_method_warning(
                'connection create',
                'obj="{}" is non-exists'.format(source_and_obj.path)
            )
            return

        if target_dcc_obj.get_is_exists() is False:
            bsc_log.Log.trace_method_warning(
                'connection create',
                'obj="{}" is non-exists'.format(target_and_obj.path)
            )
            return

        if source_dcc_port_path is None:
            return

        source_dcc_port, target_dcc_port = (
            source_dcc_obj.get_port(source_dcc_port_path), target_dcc_obj.get_port(target_dcc_port_path)
        )
        if source_dcc_port.get_is_exists() is False:
            bsc_log.Log.trace_method_warning(
                'connection create', 'atr-src-path:"{}" is non-exists'.format(source_dcc_port.path)
            )
            return

        if target_dcc_port.get_is_exists() is False:
            bsc_log.Log.trace_method_warning(
                'connection create', 'atr-tgt-path:"{}" is non-exists'.format(target_dcc_port.path)
            )
            return

        source_dcc_port.set_target(target_dcc_port, validation=True)

    def create_node_fnc(self, and_obj):
        and_obj_type_name = and_obj.type.name
        all_and_obj_types = mya_dcc_objects.AndShader.CATEGORY_DICT.keys()
        dcc_type = self._convert_configure.get('shaders.to-maya.{}'.format(and_obj_type_name))
        if dcc_type is not None:
            and_obj_name = and_obj.name
            dcc_obj_name = and_obj_name
            dcc_obj = mya_dcc_objects.AndShader(dcc_obj_name)
            if dcc_obj.get_is_exists() is False:
                dcc_obj.set_create(dcc_type)
                #
                mya_core.CmdObjOpt(dcc_obj.path).create_customize_attributes(
                    dict(
                        arnold_name=and_obj.get_port('name').get()
                    )
                )
                return dcc_obj, True
            return dcc_obj, False
        else:
            if and_obj_type_name in all_and_obj_types:
                and_obj_name = and_obj.name
                dcc_obj_name = and_obj_name
                dcc_obj = mya_dcc_objects.AndShader(dcc_obj_name)
                if dcc_obj.get_is_exists() is False:
                    dcc_obj.set_create(and_obj_type_name)
                    mya_core.CmdObjOpt(dcc_obj.path).create_customize_attributes(
                        dict(
                            arnold_name=and_obj.get_port('name').get()
                        )
                    )
                    return dcc_obj, True
                return dcc_obj, False
            else:
                bsc_log.Log.trace_method_warning(
                    'shader create',
                    'obj-type="{}" is not available'.format(and_obj_type_name)
                )

    def create_ports_fnc(self, and_obj, dcc_obj):
        and_obj_type_name = and_obj.type.name
        and_obj_type_names = self._convert_configure.get_key_names_at(
            'input-ports.to-maya'
        )
        for and_port in and_obj.get_input_ports():
            if and_port.get_is_element() is False and and_port.get_is_channel() is False:
                and_port_name = and_port.port_name
                #
                dcc_port_name = bsc_core.RawStrUnderlineOpt(and_port_name).to_camelcase()
                #
                if and_obj_type_name in and_obj_type_names:
                    and_port_names = self._convert_configure.get_key_names_at(
                        'input-ports.to-maya.{}'.format(and_obj_type_name)
                    )
                    if and_port_name in and_port_names:
                        dcc_port_name = self._convert_configure.get(
                            'input-ports.to-maya.{}.{}'.format(and_obj_type_name, and_port_name)
                        )
                #
                dcc_port = dcc_obj.get_port(dcc_port_name)
                if dcc_port.get_is_exists() is True:
                    if and_port.is_enumerate():
                        raw = and_port.get_as_index()
                    else:
                        raw = and_port.get()
                    #
                    if raw is not None:
                        dcc_port.set(raw)
                elif dcc_port.get_query_is_exists():
                    raw = and_port.get()
                    if raw is not None:
                        dcc_port._set_as_array_(raw)
                else:
                    if and_port_name == 'name':
                        pass
                    else:
                        bsc_log.Log.trace_method_warning(
                            'shader-port set',
                            'attribute="{}" is non-exists'.format(dcc_port.path)
                        )

    def create_assigns_fnc(self, geometry_and_objs):
        if geometry_and_objs:
            with bsc_log.LogProcessContext.create(maximum=len(geometry_and_objs), label='create assign') as g_p:
                for geometry_seq, geometry_and_obj in enumerate(geometry_and_objs):
                    g_p.do_update()
                    #
                    geometry_and_obj_path = geometry_and_obj.path
                    geometry_dcc_dag_path = bsc_core.BscPathOpt(geometry_and_obj_path).translate_to(
                        mya_core.MyaUtil.OBJ_PATHSEP
                    )
                    geometry_dcc_obj = mya_dcc_objects.Geometry(geometry_dcc_dag_path.path)
                    self.create_assign_fnc(geometry_and_obj, geometry_dcc_obj)
            #
            if self._assign_selection_enable is True:
                self.create_assign_for_selection_fnc(geometry_and_objs)

    def create_assign_fnc(self, geometry_and_obj, geometry_dcc_obj):
        geometry_and_obj_opt = and_dcc_operators.ShapeLookOpt(geometry_and_obj)
        geometry_dcc_obj_opt = mya_dcc_operators.ShapeLookOpt(geometry_dcc_obj)
        if geometry_dcc_obj.get_is_exists() is True:
            self.create_material_assign_fnc(geometry_and_obj_opt, geometry_dcc_obj_opt)
            self.create_geometry_properties_fnc(geometry_and_obj_opt, geometry_dcc_obj_opt)
            self.create_geometry_visibilities_fnc(geometry_and_obj_opt, geometry_dcc_obj_opt)

    def create_assign_for_selection_fnc(self, geometry_and_objs):
        selection_paths = mya_dcc_objects.Selection.get_selected_paths(include=['mesh'])
        for i_geometry_path in selection_paths:
            i_and_geometry = geometry_and_objs[0]
            i_dcc_geometry = mya_dcc_objects.Mesh(i_geometry_path)
            self.create_assign_fnc(i_and_geometry, i_dcc_geometry)

    def create_material_assign_fnc(self, geometry_and_obj_opt, geometry_dcc_obj_opt):
        material_assigns = geometry_and_obj_opt.get_material_assigns()
        for k, v in material_assigns.items():
            for i in v:
                i_and_material = self._and_universe.get_obj(i)
                i_and_material_name = i_and_material.name
                i_dcc_material = i_and_material_name
                geometry_dcc_obj_opt.assign_material_to_path(i_dcc_material)

    @classmethod
    def create_geometry_properties_fnc(cls, geometry_and_obj_opt, geometry_dcc_obj_opt):
        mya_properties = geometry_and_obj_opt.convert_render_properties_to(application='maya')
        geometry_dcc_obj_opt.assign_render_properties(mya_properties)

    @classmethod
    def create_geometry_visibilities_fnc(cls, geometry_and_obj_opt, geometry_dcc_obj_opt):
        mya_visibilities = geometry_and_obj_opt.set_visibilities_convert_to(application='maya')
        geometry_dcc_obj_opt.assign_render_visibilities(mya_visibilities)


class FncImporterForLookYml(gnl_fnc_abstracts.AbsFncImporterForLookYmlDcc):
    PLUG_NAMES = ['mtoa']

    def __init__(self, option):
        super(FncImporterForLookYml, self).__init__(option)
        self._obj_index = 0
        self._name_dict = {}
        self._connections = []

    @mya_core.MyaModifier.undo_debug_run
    def execute(self):
        for i_plug_name in self.PLUG_NAMES:
            is_plug_loaded = cmds.pluginInfo(i_plug_name, query=True, loaded=True)
            if is_plug_loaded is False:
                cmds.loadPlugin(i_plug_name, quiet=1)
        #
        self._look_pass_name = self.get('look_pass')
        self._auto_rename_node = self.get('auto_rename_node')
        #
        roots = self._raw.get_key_names_at('root')
        for i_root in roots:
            self.create_node_fnc(
                'root', i_root, i_root, customize=True
            )
        #
        method_args = [
            (self.create_materials_fnc, None),
            (self.create_nodes_fnc, None),
            (self.create_transforms_fnc, None),
            (self.create_geometries_fnc, None),
            (self.create_connections_fnc, None),
        ]
        with bsc_log.LogProcessContext.create(
            maximum=len(method_args), label='execute look yaml import method'
        ) as g_p:
            for i_method, i_args in method_args:
                g_p.do_update()
                if i_args:
                    i_method(*i_args)
                else:
                    i_method()

    def create_materials_fnc(self):
        materials = self._raw.get_key_names_at('material')
        for i_material in materials:
            if self._auto_rename_node is True:
                type_name = self._raw.get(
                    '{}.{}.properties.type'.format('material', i_material)
                ).split('/')[-1]
                #
                new_name = '{}__{}__{}__{}'.format(
                    self._look_pass_name, self._time_tag, type_name, len(self._name_dict)
                )
            else:
                new_name = i_material
            #
            self._name_dict[i_material] = new_name
            self.create_node_fnc(
                'material', i_material, new_name, create=True, definition=True
            )

    def create_nodes_fnc(self):
        nodes = self._raw.get_key_names_at('node-graph')
        for i_node in nodes:
            if self._auto_rename_node is True:
                type_name = self._raw.get(
                    '{}.{}.properties.type'.format('node-graph', i_node)
                ).split('/')[-1]
                #
                new_name = '{}__{}__{}__{}'.format(
                    self._look_pass_name, self._time_tag, type_name, len(self._name_dict)
                )
            else:
                new_name = i_node
            #
            self._name_dict[i_node] = new_name
            self.create_node_fnc(
                'node-graph', i_node, new_name, create=True, definition=True, clear_array_ports=True
            )

    def create_transforms_fnc(self):
        # transforms
        transforms = self._raw.get_key_names_at('transform')
        for i_transform in transforms:
            self.create_node_fnc(
                'transform', i_transform, i_transform, definition=True
            )

    def create_geometries_fnc(self):
        geometries = self._raw.get_key_names_at('geometry')
        for i_geometry in geometries:
            self.create_node_fnc(
                'geometry', i_geometry, i_geometry, assigns=True
            )

    def create_connections_fnc(self):
        for atr_path_src, atr_path_tgt in self._connections:
            obj_path_src, port_path_src = bsc_core.PthAttributeOpt(atr_path_src).to_args()
            if obj_path_src in self._name_dict:
                obj_path_src = self._name_dict[obj_path_src]
            atr_path_src = bsc_core.PthAttributeMtd.join_by(obj_path_src, port_path_src)
            mya_core.CmdPortOpt._create_connection_fnc(atr_path_src, atr_path_tgt)

    def create_node_fnc(
        self, scheme, obj_key, obj_path, create=False, definition=False, customize=False, assigns=False,
        clear_array_ports=False
    ):
        type_name = self._raw.get(
            '{}.{}.properties.type'.format(scheme, obj_key)
        ).split('/')[-1]
        if create is True:
            if mya_core.CmdObjOpt._get_is_exists_(obj_path) is True:
                mya_core.CmdObjOpt(obj_path).new_file()
            #
            mya_core.CmdObjOpt._set_create_(obj_path, type_name)
        #
        if mya_core.CmdObjOpt._get_is_exists_(obj_path) is True:
            obj = mya_core.CmdObjOpt(obj_path)
            if clear_array_ports is True:
                obj.clear_array_ports()
            #
            if definition is True:
                definition_attributes = self._raw.get(
                    '{}.{}.properties.definition-attributes'.format(scheme, obj_key),
                )
                if obj_path in self._name_dict:
                    new_name = self._name_dict[obj_path]
                    obj_path = new_name
                self.set_node_definition_properties_fnc(type_name, obj_path, definition_attributes)
            #
            if customize is True:
                customize_attributes = self._raw.get(
                    '{}.{}.properties.customize-attributes'.format(scheme, obj_key),
                )
                if obj_path in self._name_dict:
                    new_name = self._name_dict[obj_path]
                    obj_path = new_name
                self.set_node_customize_properties_fnc(type_name, obj_path, customize_attributes)

            if assigns is True:
                material_assigns = self._raw.get(
                    '{}.{}.properties.material-assigns'.format(scheme, obj_key),
                )
                self.create_node_material_assigns_fnc(obj_path, material_assigns)

    def set_node_customize_properties_fnc(self, type_name, obj_path, attributes):
        for port_path, v in attributes.items():
            type_name = v['type'].split('/')[-1]
            value = v.get('value')
            atr_path_src = v.get('connection')
            if atr_path_src is None:
                enumerate_strings = v.get(
                    'enumerate-strings'
                )
                if mya_core.CmdPortOpt._get_is_exists_(obj_path, port_path) is False:
                    mya_core.CmdPortOpt._set_create_(
                        obj_path, port_path, type_name, enumerate_strings
                    )
                #
                port = mya_core.CmdPortOpt(obj_path, port_path)
                if value is not None:
                    port.set(value, enumerate_strings)
            else:
                self._connections.append(
                    (atr_path_src, mya_core.CmdPortOpt._to_atr_path_(obj_path, port_path))
                )

    def set_node_definition_properties_fnc(self, type_name, obj_path, attributes):
        for port_path, v in attributes.items():
            value = v.get('value')
            atr_path_src = v.get('connection')
            if atr_path_src is None:
                if mya_core.CmdObjOpt._get_is_exists_(obj_path):
                    port = mya_core.CmdPortOpt(obj_path, port_path)
                    if value is not None:
                        # noinspection PyBroadException
                        try:
                            if type_name == 'file':
                                if port_path == 'fileTextureName':
                                    value = bsc_storage.StgPathMapper.map_to_current(value)
                            #
                            port.set(value)
                        except Exception:
                            bsc_core.BscException.set_print()
                            bsc_log.Log.trace_method_error(
                                'attribute-set',
                                'obj="{}", port="{}" >> value="{}"'.format(
                                    obj_path, port_path, value
                                )
                            )
            else:
                self._connections.append(
                    (atr_path_src, mya_core.CmdPortOpt._to_atr_path_(obj_path, port_path))
                )

    def create_node_material_assigns_fnc(self, obj_path, material_assigns):
        obj = mya_dcc_objects.Mesh(obj_path)
        obj_opt = mya_dcc_operators.MeshLookOpt(obj)
        #
        dic = {}
        for k, v in material_assigns.items():
            if v in self._name_dict:
                v = self._name_dict[v]
            dic[k] = v
        #
        obj_opt.assign_materials(
            dic,
            force=self._option['material_assign_force']
        )


class FncLookAssImporterNew(gnl_fnc_abstracts.AbsFncOptionBase):
    PLUG_NAME = 'mtoa'
    #
    OPTION = dict(
        file='',
        location='/master',
        look_pass='default',
        #
        path_lstrip='/root/world/geo',
        path_mapper=[
            # source >> target
            # renderable
            #   model
            ('/master/hi', '/master/mod/hi'),
            ('/master/lo', '/master/mod/lo'),
            # auxiliary
            ('/master/aux/grm', '/master/grm'),
            ('/master/aux/cfx', '/master/cfx'),
            ('/master/aux/efx', '/master/efx'),
            ('/master/aux/misc', '/master/misc')
        ],
        #
        with_material=True,
        with_assign=True,
        #
        assign_selection=False,
        #
        name_join_time_tag=True
    )

    def __init__(self, option=None):
        super(FncLookAssImporterNew, self).__init__(option)

    @mya_core.MyaModifier.undo_run
    def execute(self):
        file_path = self.get('file')
        is_plug_loaded = cmds.pluginInfo(self.PLUG_NAME, query=True, loaded=True)
        if is_plug_loaded is False:
            cmds.loadPlugin(self.PLUG_NAME, quiet=1)
        #
        if self.get('name_join_time_tag') is True:
            time_tag = bsc_core.TimestampOpt(bsc_storage.StgFileOpt(file_path).get_mtime()).get_as_tag_36()
        else:
            time_tag = None
        #
        s = and_dcc_objects.Scene(option=dict(shader_rename=True))
        s.load_from_dot_ass(
            file_path=self.get('file'),
            path_lstrip=self.get('path_lstrip'),
            path_mapper=collections.OrderedDict(
                [
                    # source >> target
                    # renderable
                    #   model
                    ('/master/hi', '/master/mod/hi'),
                    ('/master/lo', '/master/mod/lo'),
                    # auxiliary
                    ('/master/aux/grm', '/master/grm'),
                    ('/master/aux/cfx', '/master/cfx'),
                    ('/master/aux/efx', '/master/efx'),
                    ('/master/aux/misc', '/master/misc'),
                ]
            ),
            time_tag=time_tag
        )
        AssImportFnc(
            s.universe, self.get('with_material'), self.get('with_assign')
        ).execute()
