# coding:utf-8
import fnmatch

import re

import lxcontent.core as ctt_core

import lxresource as bsc_resource

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.dcc.objects as bsc_dcc_objects
# katana
from ...core.wrap import *

from ... import core as ktn_core
# katana dcc
# todo: remove this import
from ..operators import look as ktn_dcc_opt_look

from . import scene as ktn_dcc_obj_utility

from . import node as ktn_dcc_obj_node

from . import nodes_for_rfn as ktn_dcc_obj_nodes


# todo: remove this method
class AssetWorkspaceOld(object):
    CONFIGURE_FILE_PATH = bsc_resource.RscExtendConfigure.get_yaml('katana/workspace/asset-default-v1')
    GEOMETRY_TYPES = [
        'subdmesh',
        'renderer procedural',
        'pointcloud',
        'polymesh',
        'curves'
    ]

    def __init__(self, location=None):
        self._look_configure_dict = {}
        self._default_configure = self.set_configure_create()
        if location is not None:
            w, h = self._default_configure.get('option.w'), self._default_configure.get('option.h')
            x, y = ktn_dcc_obj_node.Node(location).get_position()
            #
            self._default_configure.set('option.x', x)
            self._default_configure.set('option.y', y-h/2)
        #
        self._default_configure.do_flatten()

        self._material_group_hash_stack = {}
        self._material_hash_stack = {}
        self._material_assign_hash_stack = {}
        self._property_assign_hash_stack = {}

        self._ng_material_assign_query_cache = {}
        self._ng_property_assign_query_cache = {}

    def get_configure(self, pass_name='default'):
        if pass_name in self._look_configure_dict:
            return self._look_configure_dict[pass_name]
        else:
            configure = self.set_configure_create(pass_name)
            configure.do_flatten()
            return configure

    def set_configure_create(self, pass_name='default'):
        configure = ctt_core.Content(value=self.CONFIGURE_FILE_PATH)
        configure.set('option.look_pass', pass_name)
        self._look_configure_dict[pass_name] = configure
        return configure

    def set_workspace_create(self):
        self._set_workspace_create_by_configure_(self._default_configure)

    def get_look_pass_names(self):
        return self._get_look_pass_names_()

    def get_pass_source_obj(self, pass_name):
        node_key = 'look_outputs'
        dcc_main_obj, ktn_main_obj, (x, y) = self.get_main_args(node_key)
        if dcc_main_obj.get_is_exists() is True:
            input_port = dcc_main_obj.get_input_port(pass_name)
            if input_port.get_is_exists() is True:
                return input_port.get_source_obj()

    def get_all_pass_source_obj(self):
        list_ = []
        pass_names = self.get_look_pass_names()
        for i_pass_name in pass_names:
            list_.append(
                self.get_pass_source_obj(i_pass_name)
            )
        return list_

    def get_all_pass_args(self):
        list_ = []
        pass_names = self.get_look_pass_names()
        for i_pass_name in pass_names:
            list_.append(
                (i_pass_name, self.get_pass_source_obj(i_pass_name))
            )
        return list_

    def get_all_dcc_materials(self):
        list_ = []
        query_dict = ktn_dcc_obj_nodes.Materials.get_nmc_material_dict()
        dcc_objs = self.get_all_pass_source_obj()
        for i_dcc_obj in dcc_objs:
            i_material_paths = ktn_core.KtnStageOpt(i_dcc_obj.ktn_obj).get_all_paths_at(
                '/root/materials', type_includes=['material']
            )
            for j_material_path in i_material_paths:
                if j_material_path in query_dict:
                    j_material_dcc_path = query_dict[j_material_path]
                    if j_material_dcc_path not in list_:
                        list_.append(
                            j_material_dcc_path
                        )
        return list_

    def get_all_dcc_shaders(self):
        list_ = []
        dcc_objs = self.get_all_dcc_materials()
        for i_dcc_obj in dcc_objs:
            list_.extend(
                i_dcc_obj.get_all_source_objs()
            )
        return list_

    def get_non_material_geometry_args(self, location):
        list_ = []
        _ = self.get_all_pass_args()
        for i_pass_name, i_dcc_obj in _:
            i_s_opt = ktn_core.KtnStageOpt(i_dcc_obj.ktn_obj)
            i_geometry_paths = i_s_opt.get_all_paths_at(
                location, type_includes=self.GEOMETRY_TYPES
            )
            for j_path in i_geometry_paths:
                j_obj_opt = ktn_core.KtnSGNodeOpt(i_s_opt, j_path)
                # print j_path, j_obj_opt.get('materialAssign', use_global=True), 'AAA'
                if not j_obj_opt.get('materialAssign'):
                    list_.append(
                        (i_pass_name, j_path)
                    )
        return list_

    def get_all_dcc_geometry_materials_by_location(self, location):
        list_ = []
        query_dict = ktn_dcc_obj_nodes.Materials.get_nmc_material_dict()
        dcc_objs = self.get_all_pass_source_obj()
        for i_dcc_obj in dcc_objs:
            i_material_sg_paths = ktn_core.KtnStageOpt(i_dcc_obj.ktn_obj).get_all_port_raws_at(
                location, 'materialAssign', type_includes=self.GEOMETRY_TYPES
            )
            for j_material_sg_path in i_material_sg_paths:
                if j_material_sg_path in query_dict:
                    j_material = query_dict[j_material_sg_path]
                    if j_material not in list_:
                        list_.append(
                            j_material
                        )
        return list_

    def get_all_dcc_geometry_shaders_by_location(self, location):
        list_ = []
        dcc_objs = self.get_all_dcc_geometry_materials_by_location(location)
        for i_dcc_obj in dcc_objs:
            i_dcc_nodes = [ktn_dcc_obj_node.Node(i.getName()) for i in
                           ktn_core.NGNodeOpt(i_dcc_obj.ktn_obj).get_all_source_objs()]
            list_.extend(
                i_dcc_nodes
            )
        return list_

    def get_look_pass_color(self, pass_name):
        pass_index = self.get_look_pass_index(pass_name)
        return self._get_look_pass_rgb_(
            pass_index
        )

    @classmethod
    def _get_look_pass_rgb_(cls, pass_index):
        h, s, v = 63+pass_index*15, .5, .5
        return bsc_core.RawColorMtd.hsv2rgb(
            h, s, v, maximum=1
        )

    def get_look_pass_index(self, pass_name):
        look_passes = self.get_look_pass_names()
        if pass_name in look_passes:
            return look_passes.index(pass_name)
        else:
            raise RuntimeError()

    def set_all_executes_run(self):
        configure = self._default_configure
        pass_name = configure.get('option.look_pass')
        workspace_keys = configure.get('workspace').keys()
        for i_key in workspace_keys:
            for j_sub_key in ['main']:
                j_node_path = configure.get('workspace.{}.{}.path'.format(i_key, j_sub_key))
                j_node = ktn_dcc_obj_node.Node(j_node_path)
                if j_node.get_is_exists() is True:
                    j_node_executes = configure.get('workspace.{}.{}.executes'.format(i_key, j_sub_key))
                    if j_node_executes:
                        self._set_node_executes_(j_node.ktn_obj, j_node_executes)
            #
            i_node_graph_node_dict = configure.get('workspace.{}.node_graph.nodes'.format(i_key))
            if i_node_graph_node_dict:
                for seq, (j_key, j_node_dict) in enumerate(i_node_graph_node_dict.items()):
                    j_node_path = j_node_dict['path']
                    j_node = ktn_dcc_obj_node.Node(j_node_path)
                    if j_node.get_is_exists() is True:
                        j_node_executes = j_node_dict.get('executes')
                        if j_node_executes:
                            self._set_node_executes_(j_node.ktn_obj, j_node_executes)

    def set_variables_registry(self):
        keys = ['layer', 'quality', 'camera', 'look_pass', 'light_pass']
        variable_switches = ktn_core.NGNodeTypeOpt('VariableSwitch').get_objs()
        for i in variable_switches:
            i_obj_opt = ktn_core.NGNodeOpt(i)
            i_key = i_obj_opt.get('lynxi_variants.key')
            if i_key in keys:
                i_obj_opt.execute_port('lynxi_variants.register_variable')
        #
        ktn_core.VariablesSetting().set_register_by_configure(
            {
                'variables_enable': ['on', 'off']
            }
        )

    def _get_look_pass_names_(self):
        lis = []
        node_key = 'look_outputs'
        dcc_main_obj, ktn_main_obj, (x, y) = self.get_main_args(node_key)
        if dcc_main_obj.get_is_exists() is True:
            input_ports = dcc_main_obj.get_input_ports()
            for i_input_port in input_ports:
                i_port_path = i_input_port.name
                if not i_port_path in ['orig']:
                    lis.append(i_port_path)
        return lis

    @ktn_core.Modifier.undo_debug_run
    def set_look_pass_add(self, pass_name=None):
        pass_names = self.get_look_pass_names()
        pass_count = len(pass_names)
        if pass_name is None:
            pass_name = 'pass_{}'.format(pass_count)
        #
        if pass_name not in pass_names:
            configure = self.set_configure_create(pass_name)
            r, g, b = self._get_look_pass_rgb_(pass_count+1)
            configure.set('option.look_pass_color', dict(r=r, g=g, b=b))
            w = configure.get('option.w')
            offset_x = w*pass_count*2
            configure.set('option.offset_x', offset_x)
            configure.do_flatten()
            self._set_workspace_create_by_configure_(configure)
            bsc_log.Log.trace_method_result(
                'look-pass add',
                'look-pass"{}"'.format(pass_name)
            )
        else:
            bsc_log.Log.trace_method_warning(
                'look pass add',
                'look-pass="{}" is exists'.format(pass_name)
            )

    @classmethod
    def _set_workspace_create_by_configure_(cls, configure):
        workspace_keys = configure.get('workspace').keys()
        #
        method_args = [
            cls._set_workspace_nodes_create_mtd_,
            cls._set_workspace_connections_create_mtd_,
            cls._set_workspace_node_graphs_create_mtd_
        ]
        with bsc_log.LogProcessContext.create(maximum=len(method_args), label='create workspace') as g_p:
            for i_method in method_args:
                g_p.do_update()
                i_method(configure, workspace_keys)

    @classmethod
    def _set_workspace_nodes_create_mtd_(cls, configure, workspace_keys):
        pass_name = configure.get('option.look_pass')
        with bsc_log.LogProcessContext.create(maximum=len(workspace_keys), label='crate workspace node') as g_p:
            for i_key in workspace_keys:
                g_p.do_update()
                for j_sub_key in ['main', 'backdrop', 'dot']:
                    cls._set_workspace_node_create_(configure, i_key, j_sub_key, pass_name)

    @classmethod
    def _set_workspace_node_create_(cls, configure, key, sub_key, pass_name='default'):
        variable = configure.get('workspace.{}.{}.variable'.format(key, sub_key))
        if pass_name != 'default':
            if not variable:
                return
        #
        node_obj_path = configure.get('workspace.{}.{}.path'.format(key, sub_key))
        if node_obj_path is not None:
            node_obj_type_name = configure.get('workspace.{}.{}.obj_type'.format(key, sub_key))
            node_base_obj_type = configure.get('workspace.{}.{}.base_obj_type'.format(key, sub_key))
            #
            dcc_node = ktn_dcc_obj_node.Node(node_obj_path)
            ktn_node, is_create = dcc_node.get_dcc_instance(node_obj_type_name, node_base_obj_type)
            if is_create is True:
                node_attributes = configure.get('workspace.{}.{}.attributes'.format(key, sub_key))
                if node_attributes:
                    ktn_node.setAttributes(node_attributes)
                #
                node_pos = configure.get('workspace.{}.{}.pos'.format(key, sub_key))
                if node_pos:
                    NodegraphAPI.SetNodePosition(ktn_node, node_pos)
                #
                node_parameters = configure.get('workspace.{}.{}.parameters'.format(key, sub_key))
                if node_parameters:
                    for i_parameter_port_path, parameter_value in node_parameters.items():
                        i_parameter_port_path = i_parameter_port_path.replace('/', '.')
                        dcc_node.get_port(i_parameter_port_path).set(parameter_value)
                #
                node_executes = configure.get('workspace.{}.{}.executes'.format(key, sub_key))
                if node_executes:
                    cls._set_node_executes_(ktn_node, node_executes)
                #
                child_dcc_type = configure.get('workspace.{}.{}.child_obj_type'.format(key, sub_key))
                if child_dcc_type is not None:
                    ktn_node.setChildNodeType(child_dcc_type)
            #
            node_outputs = configure.get('workspace.{}.{}.outputs'.format(key, sub_key))
            if node_outputs:
                for port_name in node_outputs:
                    ktn_port = ktn_node.getOutputPort(port_name)
                    if ktn_port is None:
                        ktn_node.addOutputPort(port_name)

    @classmethod
    def _set_workspace_connections_create_mtd_(cls, configure, workspace_keys):
        pass_name = configure.get('option.look_pass')
        with bsc_log.LogProcessContext.create(maximum=len(workspace_keys), label='crate workspace connection') as g_p:
            for key in workspace_keys:
                g_p.do_update()
                for sub_key in ['main', 'node_graph', 'dot']:
                    cls._set_workspace_connections_create_(configure, key, sub_key, pass_name)

    @classmethod
    def _set_workspace_connections_create_(cls, configure, key, sub_key, pass_name='default'):
        variable = configure.get('workspace.{}.{}.variable'.format(key, sub_key))
        if pass_name != 'default':
            if not variable:
                return
        node_connections = configure.get('workspace.{}.{}.connections'.format(key, sub_key))
        if node_connections:
            cls._set_node_connections_create_(node_connections)

    @classmethod
    def _set_workspace_node_graphs_create_mtd_(cls, configure, workspace_keys):
        pass_name = configure.get('option.look_pass')
        with bsc_log.LogProcessContext.create(maximum=len(workspace_keys), label='crate workspace node-graph') as g_p:
            for key in workspace_keys:
                g_p.do_update()
                cls._set_workspace_node_graph_create_(configure, key, pass_name)

    @classmethod
    def _set_workspace_node_graph_create_(cls, configure, key, pass_name):
        node_graph_node_dict = configure.get('workspace.{}.node_graph.nodes'.format(key))
        # dcc_main_node = configure.get('workspace.{}.main.path'.format(key))
        # backdrop_node_dcc_path = configure.get('workspace.{}.backdrop.path'.format(key))
        # d_size = configure.get('option.w'), configure.get('option.h')
        cls._set_node_graph_nodes_create_(configure, key, node_graph_node_dict, pass_name)

    @classmethod
    def _set_node_graph_nodes_create_(cls, configure, key, nodes_dict, pass_name='default'):
        if nodes_dict:
            for seq, (k, i_node_dict) in enumerate(nodes_dict.items()):
                cls._set_node_graph_node_create_(configure, key, i_node_dict, pass_name)

    @classmethod
    def _set_node_graph_node_create_(cls, configure, key, node_dict, pass_name='default'):
        variable = node_dict.get('variable')
        if pass_name != 'default':
            if not variable:
                return
        #
        node_obj_path = node_dict['path']
        node_obj_category = node_dict['obj_category']
        node_obj_type = node_dict['obj_type']
        node_base_obj_type = node_dict.get('base_obj_type')
        dcc_node = ktn_dcc_obj_node.Node(node_obj_path)
        node_ktn_obj, is_create = dcc_node.get_dcc_instance(node_obj_type, node_base_obj_type)
        if is_create is True:
            if node_obj_category == 'group':
                child_dcc_type = node_dict['child_obj_type']
                if child_dcc_type is not None:
                    node_ktn_obj.setChildNodeType(child_dcc_type)
            #
            node_attributes = node_dict.get('attributes')
            if node_attributes:
                node_ktn_obj.setAttributes(node_attributes)
            #
            insert_connections = node_dict.get('insert_connections')
            if insert_connections:
                insert_scheme = node_dict.get('insert_scheme')
                cls._set_node_insert_connections_create_(insert_connections, insert_scheme)
            #
            split_connections = node_dict.get('split_connections')
            if split_connections:
                cls._set_node_spit_connections_create_(split_connections)
            #
            connections = node_dict.get('connections')
            if connections:
                cls._set_node_connections_create_(connections)
            #
            parameters = node_dict.get('parameters')
            if parameters:
                cls._set_node_parameters_(dcc_node, parameters)
            #
            arnold_geometry_properties = node_dict.get('arnold_geometry_properties')
            if arnold_geometry_properties:
                cls._set_arnold_geometry_properties_(dcc_node, arnold_geometry_properties)
            #
            executes = node_dict.get('executes')
            if executes:
                cls._set_node_executes_(node_ktn_obj, executes)
            #
            layout_use_backdrop = configure.get('workspace.{}.option.layout_use_backdrop'.format(key)) or False
            if layout_use_backdrop is True:
                dcc_main_node = ktn_dcc_obj_node.Node(
                    configure.get('workspace.{}.main.path'.format(key))
                )
                dcc_backdrop_node = ktn_dcc_obj_node.Node(
                    configure.get('workspace.{}.backdrop.path'.format(key))
                )
                d_size = 225, 80
                cls._set_node_layout_by_backdrop_(
                    dcc_node, dcc_main_node, dcc_backdrop_node, d_size
                )

    @classmethod
    def _set_node_connections_create_(cls, node_connections, variants_extend=None):
        if variants_extend is None:
            variants_extend = {}
        for seq, i in enumerate(node_connections):
            if not (seq+1)%2:
                source_attr_path = node_connections[seq-1]
                target_attr_path = i
                if variants_extend:
                    source_attr_path = source_attr_path.format(**variants_extend)
                    target_attr_path = target_attr_path.format(**variants_extend)
                #
                source_obj_path, source_port_name = source_attr_path.split('.')
                target_obj_path, target_port_name = target_attr_path.split('.')
                #
                source_dcc_obj = ktn_dcc_obj_node.Node(source_obj_path)
                source_dcc_port = source_dcc_obj.get_output_port(source_port_name)
                source_ktn_port, _ = source_dcc_port.get_dcc_instance()
                #
                target_dcc_obj = ktn_dcc_obj_node.Node(target_obj_path)
                target_dcc_port = target_dcc_obj.get_input_port(target_port_name)
                target_ktn_port, _ = target_dcc_port.get_dcc_instance()
                #
                source_ktn_port.connect(target_ktn_port)

    @classmethod
    def _set_node_executes_(cls, ktn_obj, executes):
        for i_port_path in executes:
            ktn_core.NGNodeOpt(ktn_obj).execute_port(i_port_path)

    @classmethod
    def _set_node_layout_by_backdrop_(cls, dcc_node, dcc_main_node, dcc_backdrop_node, d_size):
        if dcc_backdrop_node.get_is_exists() is True:
            index = cls._get_node_layout_index_(dcc_node, dcc_main_node)
            x, y, w, h = cls._get_layout_backdrop_geometry_(dcc_backdrop_node, d_size)
            d_w, d_h = d_size
            d_c = int(w/d_w)+1
            column = int(index%d_c)
            row = int(index/d_c)
            x_0, y_0 = x+column*d_w, y-row*d_h
            NodegraphAPI.SetNodePosition(dcc_node.ktn_obj, (x_0, y_0))

    @classmethod
    def _get_node_layout_index_(cls, dcc_node, dcc_main_node):
        path = dcc_node.path
        paths = [i.path for i in dcc_main_node.get_source_objs()]
        if path in paths:
            return paths.index(path)
        return 0

    @classmethod
    def _get_layout_backdrop_geometry_(cls, dcc_backdrop_node, d_size):
        a = dcc_backdrop_node.ktn_obj.getAttributes()
        d_w, d_h = d_size
        x, y, w, h = a['x'], a['y'], a['ns_sizeX'], a['ns_sizeY']
        w -= d_w
        h -= d_h
        x_ = x-w/2
        y_ = y+h/2
        return x_, y_, w, h

    @classmethod
    def _set_node_insert_connections_create_(cls, node_insert_connections, insert_scheme):
        if node_insert_connections:
            for seq, i in enumerate(node_insert_connections):
                if not (seq+1)%4:
                    source_attr_path = node_insert_connections[seq-3]
                    target_attr_path = node_insert_connections[seq-2]
                    #
                    input_attr_path_ = node_insert_connections[seq-1]
                    output_attr_path_ = i
                    #
                    s_ktn_port, t_ktn_port = cls._get_node_connect_args_(source_attr_path, target_attr_path)
                    #
                    node_obj_path_, input_port_name_ = input_attr_path_.split('.')
                    node_dcc_obj_ = ktn_dcc_obj_node.Node(node_obj_path_)
                    node_ktn_obj_ = node_dcc_obj_.ktn_obj
                    #
                    node_obj_path_, output_port_name_ = output_attr_path_.split('.')
                    #
                    i_ktn_obj = node_ktn_obj_.getInputPort(input_port_name_)
                    o_ktn_obj = node_ktn_obj_.getOutputPort(output_port_name_)
                    #
                    if insert_scheme == 'TB':
                        x, y = NodegraphAPI.GetNodePosition(s_ktn_port.getNode())
                        NodegraphAPI.SetNodePosition(node_ktn_obj_, (x, y-48))
                    elif insert_scheme == 'BT':
                        x, y = NodegraphAPI.GetNodePosition(t_ktn_port.getNode())
                        NodegraphAPI.SetNodePosition(node_ktn_obj_, (x, y+48*2))
                    #
                    s_ktn_port.connect(i_ktn_obj)
                    o_ktn_obj.connect(t_ktn_port)

    @classmethod
    def _set_node_spit_connections_create_(cls, node_connections):
        if node_connections:
            for seq, i in enumerate(node_connections):
                if not (seq+1)%4:
                    source_attr_path = node_connections[seq-3]
                    target_attr_path = node_connections[seq-2]
                    #
                    input_attr_path_ = node_connections[seq-1]
                    output_attr_path_ = i
                    #
                    source_obj_path, source_port_name = source_attr_path.split('.')
                    s_ktn_port = ktn_dcc_obj_node.Node(source_obj_path).ktn_obj.getOutputPort(source_port_name)
                    target_obj_path, target_port_name = target_attr_path.split('.')
                    t_ktn_port = ktn_dcc_obj_node.Node(target_obj_path).ktn_obj.getInputPort(target_port_name)
                    #
                    node_obj_path_, input_port_name_ = input_attr_path_.split('.')
                    node_dcc_obj_ = ktn_dcc_obj_node.Node(node_obj_path_)
                    node_ktn_obj_ = node_dcc_obj_.ktn_obj
                    #
                    node_obj_path_, output_port_name_ = output_attr_path_.split('.')
                    #
                    i_ktn_obj = node_ktn_obj_.getInputPort(input_port_name_)
                    o_ktn_obj = node_ktn_obj_.getOutputPort(output_port_name_)
                    #
                    x, y = NodegraphAPI.GetNodePosition(t_ktn_port.getNode())
                    NodegraphAPI.SetNodePosition(node_ktn_obj_, (x, y+48*2))
                    #
                    s_ktn_port.connect(i_ktn_obj)
                    o_ktn_obj.connect(t_ktn_port)

    @classmethod
    def _set_node_parameters_(cls, dcc_node, parameters):
        for i_port_path, i_value in parameters.items():
            i_port_path = i_port_path.replace('/', '.')
            dcc_node.get_port(i_port_path).set(i_value)

    # geometry properties
    @classmethod
    def _set_arnold_geometry_properties_(cls, dcc_property_assign, properties_dict):
        for i_port_path, i_value in properties_dict.items():
            i_port_path = i_port_path.replace('/', '.')
            cls._set_arnold_geometry_property_(dcc_property_assign, i_port_path, i_value)

    @classmethod
    def _set_arnold_geometry_property_(cls, dcc_node, parameter_port_name, parameter_value):
        convert_dict = dict(
            subdiv_iterations='iterations',
            disp_zero_value='zero_value'
        )
        if parameter_port_name in convert_dict:
            parameter_port_name = convert_dict[parameter_port_name]
        #
        enable_ktn_port_name = 'args.arnoldStatements.{}.enable'.format(parameter_port_name)
        enable_dcc_port = dcc_node.get_port(enable_ktn_port_name)
        if enable_dcc_port.get_is_exists() is True:
            enable_dcc_port.set(True)
        else:
            bsc_log.Log.trace_warning(
                'port-name="{}" is unknown'.format(parameter_port_name)
            )
        #
        value_ktn_port_name = 'args.arnoldStatements.{}.value'.format(parameter_port_name)
        value_dcc_port = dcc_node.get_port(value_ktn_port_name)
        if value_dcc_port.get_is_exists() is True:
            value_dcc_port.set(parameter_value)

    #
    @classmethod
    def _get_node_connect_args_(cls, source_attr_path, target_attr_path):
        def rcs_fnc_(o_ktn_port_):
            _target_ktn_ports = o_ktn_port_.getConnectedPorts()
            if _target_ktn_ports:
                _target_ktn_port = _target_ktn_ports[0]
                if _target_ktn_port == i_ktn_port:
                    return o_ktn_port_
                else:
                    _target_node = _target_ktn_port.getNode()
                    _o_ktn_ports = _target_node.getOutputPorts()
                    if _o_ktn_ports:
                        _o_ktn_port = _o_ktn_ports[0]
                        return rcs_fnc_(_o_ktn_port)

        #
        source_obj_path, source_port_name = source_attr_path.split('.')
        o_ktn_port = ktn_dcc_obj_node.Node(source_obj_path).ktn_obj.getOutputPort(source_port_name)
        target_obj_path, target_port_name = target_attr_path.split('.')
        i_ktn_port = ktn_dcc_obj_node.Node(target_obj_path).ktn_obj.getInputPort(target_port_name)
        #
        s_ktn_port = rcs_fnc_(o_ktn_port)
        t_ktn_port = i_ktn_port
        #
        return s_ktn_port, t_ktn_port

    @classmethod
    def _get_main_args_(cls, configure, key):
        dcc_path = configure.get('workspace.{}.main.path'.format(key))
        dcc_obj = ktn_dcc_obj_node.Node(dcc_path)
        ktn_obj = dcc_obj.ktn_obj
        return dcc_obj, ktn_obj, NodegraphAPI.GetNodePosition(ktn_obj)

    @classmethod
    def _get_group_args_(cls, configure, key, group_key):
        dcc_path = configure.get('workspace.{}.node_graph.nodes.{}.path'.format(key, group_key))
        dcc_obj = ktn_dcc_obj_node.Node(dcc_path)
        ktn_obj = dcc_obj.ktn_obj
        return dcc_obj, ktn_obj, NodegraphAPI.GetNodePosition(ktn_obj)

    def get_main_args(self, key, pass_name='default'):
        configure = self.get_configure(pass_name=pass_name)
        return self._get_main_args_(configure, key)

    def get_main_node(self, key, pass_name='default'):
        configure = self.get_configure(pass_name=pass_name)
        dcc_path = configure.get('workspace.{}.main.path'.format(key))
        return ktn_dcc_obj_node.Node(dcc_path)

    def get_node_graph_node(self, key, sub_key, pass_name='default'):
        configure = self.get_configure(pass_name=pass_name)
        dcc_path = configure.get('workspace.{}.node_graph.nodes.{}.path'.format(key, sub_key))
        return ktn_dcc_obj_node.Node(dcc_path)

    def get_group_args(self, key, group_key, pass_name='default'):
        configure = self.get_configure(pass_name=pass_name)
        return self._get_group_args_(configure, key, group_key)

    # asset-geometry-abc
    def set_geometry_abc_import(self, file_path):
        configure = self.get_configure()
        key = 'geometry_abc'
        dcc_main_obj, dcc_node = self._set_main_node_create_(configure, key)
        if dcc_node is not None:
            file_parameter_name = configure.get('node.{}.main.file_parameter'.format(key))
            dcc_node.get_port(file_parameter_name).set(file_path)
            bsc_log.Log.trace_method_result(
                '{}-import'.format(key),
                u'file="{}"'.format(file_path)
            )

    # asset-geometry-usd
    def set_geometry_usd_import(self, file_path):
        configure = self.get_configure()
        key = 'geometry_usd'
        dcc_main_obj, dcc_node = self._set_main_node_create_(configure, key, break_source_connections=False)
        if dcc_node is not None:
            file_parameter_name = configure.get('node.{}.main.file_parameter'.format(key))
            dcc_node.get_port(file_parameter_name).set(file_path)
            bsc_log.Log.trace_method_result(
                '{}-import'.format(key),
                u'file="{}"'.format(file_path)
            )

    #
    def set_geometry_xgen_import(self, file_path, variants_extend):
        configure = self.get_configure()
        key = 'geometry_xgen'
        dcc_main_obj, dcc_node = self._set_main_node_create_(
            configure,
            key,
            variants_extend=variants_extend,
            break_source_connections=False
        )
        if dcc_node is not None:
            file_parameter_name = configure.get('node.{}.main.file_parameter'.format(key))
            dcc_node.get_port(file_parameter_name).set(file_path)
            bsc_log.Log.trace_method_result(
                '{}-import'.format(key),
                u'file="{}"'.format(file_path)
            )

    # model-usd
    def set_model_usd_import(self, file_path):
        configure = self.get_configure()
        key = 'model_usd'
        dcc_main_obj, dcc_node = self._set_main_node_create_(
            configure,
            key,
            break_source_connections=False
        )
        if dcc_node is not None:
            file_parameter_name = configure.get('node.{}.main.file_parameter'.format(key))
            dcc_node.get_port(file_parameter_name).set(file_path)
            bsc_log.Log.trace_method_result(
                '{}-import'.format(key),
                u'file="{}"'.format(file_path)
            )

    # hair-usd
    def set_groom_geometry_usd_import(self, file_path):
        configure = self.get_configure()
        key = 'groom_geometry_usd'
        dcc_main_obj, dcc_node = self._set_main_node_create_(configure, key, break_source_connections=False)
        if dcc_node is not None:
            file_parameter_name = configure.get('node.{}.main.file_parameter'.format(key))
            dcc_node.get_port(file_parameter_name).set(file_path)
            bsc_log.Log.trace_method_result(
                'hair-usd-import',
                u'file="{}"'.format(file_path)
            )

    # effect-usd
    def set_effect_usd_import(self, file_path):
        configure = self.get_configure()
        key = 'effect_usd'
        dcc_main_obj, dcc_node = self._set_main_node_create_(configure, key, break_source_connections=False)
        if dcc_node is not None:
            file_parameter_name = configure.get('node.{}.main.file_parameter'.format(key))
            dcc_node.get_port(file_parameter_name).set(file_path)
            bsc_log.Log.trace_method_result(
                '{}-import'.format(key),
                u'file="{}"'.format(file_path)
            )

    # asset-set
    def set_set_usd_import(self, file_path):
        configure = self.get_configure()
        key = 'set_usd'
        dcc_main_obj, dcc_node = self._set_main_node_create_(configure, key)
        if dcc_node is not None:
            file_parameter_name = configure.get('node.{}.main.file_parameter'.format(key))
            dcc_node.get_port(file_parameter_name).set(file_path)
            bsc_log.Log.trace_method_result(
                '{}-import'.format(key),
                u'file="{}"'.format(file_path)
            )
        #
        CacheManager.flush()

    def set_camera_persp_abc_import(self, file_path, path):
        configure = self.get_configure()
        key = 'camera_abc'
        dcc_main_obj, dcc_node = self._set_main_node_create_(configure, key, break_source_connections=False)
        camera_root = configure.get('option.camera_root')
        if dcc_node is not None:
            dcc_node.get_port('camera.file').set(file_path)
            dcc_node.get_port('camera.path').set('{}{}'.format(camera_root, path))
            bsc_log.Log.trace_method_result(
                '{}-import'.format(key),
                u'file="{}"'.format(file_path)
            )
        #
        CacheManager.flush()

    def set_render_camera(self, path):
        configure = self.get_configure()
        key_0 = 'render_settings'
        dcc_main_obj, ktn_main_obj, (x, y) = self._get_main_args_(configure, key_0)
        camera_root = configure.get('option.camera_root')
        dcc_main_obj.get_port(
            'render_settings.camera_enable'
        ).set(True)
        dcc_main_obj.get_port(
            'render_settings.camera'
        ).set(
            '{}{}'.format(camera_root, path)
        )

    def set_render_resolution(self, width, height):
        configure = self.get_configure()
        main_key = 'render_settings'
        dcc_main_obj, ktn_main_obj, (x, y) = self._get_main_args_(configure, main_key)
        #
        dcc_main_obj.get_port(
            'render_settings.resolution_enable'
        ).set(True)
        dcc_main_obj.get_port(
            'render_settings.resolution'
        ).set('{}x{}'.format(width, height))

    @classmethod
    def _get_merge_index_(cls, merge, target_port_name):
        input_port_paths = [i.port_path for i in merge.get_input_ports()]
        if target_port_name in input_port_paths:
            return input_port_paths.index(target_port_name)
        return len(input_port_paths)

    def _set_main_node_create_(self, configure, key, variants_extend=None, break_source_connections=True):
        if variants_extend is None:
            variants_extend = {}
        #
        node_key = configure.get('node.{}.keyword'.format(key))
        dcc_main_obj, ktn_main_obj, (x, y) = self._get_main_args_(configure, node_key)
        #
        if break_source_connections is True:
            dcc_main_obj.set_sources_disconnect()
        #
        if dcc_main_obj.get_is_exists() is True:
            w, h = configure.get('option.w'), configure.get('option.h')
            margin = configure.get('option.margin')
            spacing_x = configure.get('option.spacing_x')
            spacing_y = configure.get('option.spacing_y')
            #
            node_obj_path = configure.get('node.{}.main.path'.format(key))
            node_obj_path = node_obj_path.format(**variants_extend)
            node_obj_type = configure.get('node.{}.main.obj_type'.format(key))
            #
            dcc_node = ktn_dcc_obj_node.Node(node_obj_path)
            ktn_node, is_create = dcc_node.get_dcc_instance(node_obj_type)
            #
            node_parameters = configure.get('node.{}.main.parameters'.format(key))
            if node_parameters:
                for i_parameter_port_path, i_parameter_value in node_parameters.items():
                    i_parameter_port_path = i_parameter_port_path.replace('/', '.')
                    i_parameter_value = i_parameter_value.format(**variants_extend)
                    dcc_node.get_port(i_parameter_port_path).set(i_parameter_value)
            #
            node_connections = configure.get('node.{}.main.connections'.format(key))
            if node_connections:
                self._set_node_connections_create_(
                    node_connections,
                    variants_extend=variants_extend
                )
            #
            index = len([i.getName() for i in ktn_main_obj.getInputPorts()])
            if is_create is True:
                node_attributes = configure.get('node.{}.main.attributes'.format(key))
                if node_attributes:
                    ktn_node.setAttributes(node_attributes)
                NodegraphAPI.SetNodePosition(ktn_node, (x-w/2+spacing_x*index, y+margin+spacing_y*2))
            return dcc_main_obj, dcc_node

    def set_look_klf_file_export(self, file_path):
        configure = self.get_configure()
        key = 'look_outputs'
        dcc_obj = self.get_main_node(key)
        if dcc_obj.get_is_exists() is True:
            geometry_settings = self.get_main_node('geometry_settings')
            if geometry_settings.get_is_exists() is True and geometry_settings.get_is_bypassed() is False:
                scheme = self.get_geometry_scheme()
                if scheme == 'asset':
                    location = configure.get('option.asset_root')
                    dcc_obj.set('rootLocations', [location])
                elif scheme == 'shot':
                    geometry_settings_ktn_obj = geometry_settings.ktn_obj
                    geometry_settings.set('usd.override_enable', False)
                    #
                    ktn_core.NGNodeOpt(geometry_settings_ktn_obj).execute_port('usd.guess')
                    start_frame, end_frame = geometry_settings.get('usd.start_frame'), geometry_settings.get(
                        'usd.end_frame'
                        )
                    if start_frame != end_frame:
                        ktn_core.NGNodeOpt(geometry_settings_ktn_obj).execute_port('usd.shot_override.create')
                        geometry_settings.set('usd.override_enable', True)
                    #
                    location = geometry_settings.get('usd.location')
                    dcc_obj.set('rootLocations', [location])
            else:
                location = configure.get('option.asset_root')
                dcc_obj.set('rootLocations', [location])
            #
            dcc_obj.get_port('saveTo').set(file_path)
            #
            os_file = bsc_dcc_objects.StgFile(file_path)
            os_file.create_directory()
            dcc_obj.ktn_obj.WriteToLookFile(None, file_path)
            #
            if geometry_settings.get_is_exists() is True:
                geometry_settings.set('usd.override_enable', False)
            #
            bsc_log.Log.trace_method_result(
                'look-klf export',
                '"{}"'.format(file_path)
            )
        else:
            raise RuntimeError(
                bsc_log.Log.trace_method_error(
                    'look-klf export',
                    'obj="{}" is non-exists'.format(dcc_obj.path)
                )
            )

    def set_look_klf_extra_export(self, file_path):
        location = self.get_geometry_location()
        #
        dcc_shaders = self.get_all_dcc_geometry_shaders_by_location(location)
        #
        patterns = [
            # etc. '/tmp/file.%04d.ext'%frame
            '\'*.%0[0-9]d.*\'%*',
            # etc. frame/2, frame*2
            '*frame*'
        ]
        dict_ = {}

        if dcc_shaders:
            for i_dcc_shader in dcc_shaders:
                i_p = i_dcc_shader.get_port('parameters')
                if i_p.get_is_exists() is False:
                    continue
                #
                i_descendants = i_p.get_descendants()
                for j_child in i_descendants:
                    if j_child.type != 'group':
                        if j_child.port_path.endswith('.value'):
                            j_value_port = j_child
                            j_enable_port = i_dcc_shader.get_port(
                                '{}.enable'.format('.'.join(j_child.port_path.split('.')[:-1]))
                            )
                            if j_enable_port.get_is_exists() is True:
                                # ignore when enable is 0.0
                                if not j_enable_port.get():
                                    continue
                                #
                                if j_value_port.get_is_expression() is True:
                                    j_expression = j_value_port.get_expression()
                                    for k_p in patterns:
                                        if fnmatch.filter([j_expression], k_p):
                                            j_key = '{}.{}'.format(i_dcc_shader.name, j_value_port.port_path)
                                            dict_[j_key] = j_expression
                                            # match once
                                            break
        #
        if dict_:
            bsc_dcc_objects.StgJson(
                file_path
            ).set_write(dict_)

    def set_dynamic_ass_export(self, dynamic_override_uv_maps=False):
        node = self.get_main_node('look_outputs')
        geometry_scheme = self.get_geometry_scheme()
        if node.get_is_exists() is True:
            look_pass_names = self.get_look_pass_names()
            if geometry_scheme == 'asset':
                for i_look_pass_name in look_pass_names:
                    i_input_port = node.get_input_port(i_look_pass_name)
                    if i_input_port:
                        i_source_port = i_input_port.get_source()
                        if i_source_port is not None:
                            i_asset_ass_exporter = ktn_dcc_obj_node.Node(
                                '/rootNode/asset_ass_export__{}'.format(i_look_pass_name)
                                )
                            i_asset_ass_exporter.get_dcc_instance('lx_asset_ass_exporter', 'Group')
                            # i_asset_ass_exporter.set(
                            #     'export.look.pass', i_look_pass_name
                            # )
                            i_asset_ass_exporter.set(
                                'dynamic.override_uv_maps', dynamic_override_uv_maps
                            )
                            # connection
                            i_source_port.set_target(
                                i_asset_ass_exporter.get_input_port('input')
                            )
                            i_asset_ass_exporter.get_output_port(
                                'output'
                            ).set_target(
                                i_input_port
                            )
                            #
                            ktn_core.NGNodeOpt(i_asset_ass_exporter.ktn_obj).execute_port(
                                'export.guess'
                            )
                            ktn_core.NGNodeOpt(i_asset_ass_exporter.ktn_obj).execute_port(
                                'export.execute'
                            )

    def get_geometry_location(self):
        configure = self.get_configure()
        geometry_settings = self.get_main_node('geometry_settings')
        if geometry_settings.get_is_exists() is True and geometry_settings.get_is_bypassed() is False:
            geometry_scheme = self.get_geometry_scheme()
            if geometry_scheme == 'asset':
                location = configure.get('option.asset_root')
            elif geometry_scheme == 'shot':
                location = geometry_settings.get('usd.location')
            else:
                raise RuntimeError()
        else:
            location = configure.get('option.asset_root')
        #
        return location

    def get_geometry_scheme(self):
        key = 'geometry_settings'
        dcc_obj = self.get_main_node(key)
        if dcc_obj.get_is_exists() is True:
            return dcc_obj.get('options.scheme')
        else:
            return 'asset'

    @classmethod
    def _get_geometry_location_(cls, dcc_obj):
        if dcc_obj.get_is_exists() is True:
            s = ktn_core.KtnStageOpt(dcc_obj.ktn_obj)
            print s.get_obj_exists('/root/world/geo/master')

    @ktn_core.Modifier.undo_debug_run
    def set_light_rig_update(self):
        configure = self.get_configure()
        key = 'light_rigs'
        sub_key = 'main'
        node_obj_path = configure.get('workspace.{}.{}.path'.format(key, sub_key))
        node_obj_type_name = configure.get('workspace.{}.{}.obj_type'.format(key, sub_key))
        dcc_node = ktn_dcc_obj_node.Node(node_obj_path)
        source_connections = dcc_node.get_source_connections()
        target_connections = dcc_node.get_target_connections()
        dict_ = dcc_node.get_as_dict(
            [
                'user.render_quality',
                'user.Layer_Name',
                'user.Output_Path',
                'user.camera',
                'user.HDRI',
                'user.Controls.Lighting_rotation',
                'user.Show_Background'
            ]
        )
        #
        dcc_node.do_delete()
        ktn_node, is_create = dcc_node.get_dcc_instance(node_obj_type_name)
        if is_create is True:
            node_attributes = configure.get('workspace.{}.{}.attributes'.format(key, sub_key))
            if node_attributes:
                ktn_node.setAttributes(node_attributes)
            #
            node_pos = configure.get('workspace.{}.{}.pos'.format(key, sub_key))
            if node_pos:
                NodegraphAPI.SetNodePosition(ktn_node, node_pos)
        #
        for i in source_connections:
            source_ktn_port = i.source.ktn_port
            target_ktn_port = i.target.ktn_port
            source_ktn_port.connect(target_ktn_port)
        for i in target_connections:
            source_ktn_port = i.source.ktn_port
            target_ktn_port = i.target.ktn_port
            source_ktn_port.connect(target_ktn_port)
        #
        dcc_node.set_as_dict(dict_)
        return dcc_node

    def get_geometry_usd_model_hi_file_path(self):
        configure = self.get_configure()
        asset_root = configure.get('option.asset_root')
        atr_path = '{}.userProperties.geometry__model__hi'.format(asset_root)
        return self._get_stage_port_raw_(atr_path)

    def get_geometry_uv_map_usd_source_file(self):
        configure = self.get_configure()
        asset_root = configure.get('option.asset_root')
        #
        atr_path = '{}.userProperties.geometry__surface__hi'.format(asset_root)
        _ = self._get_stage_port_raw_(atr_path)
        if _:
            return _
        #
        atr_path = '{}.userProperties.usd.variants.asset.surface.override.file'.format(asset_root)
        _ = self._get_stage_port_raw_(atr_path)
        if _:
            f = bsc_dcc_objects.StgFile(_)
            # TODO fix this bug
            if f.get_is_naming_match('hi.uv_map.usd'):
                return '{}/hi.usd'.format(
                    f.directory.path
                )
            return _

    def get_geometry_usd_check_raw(self):
        raise RuntimeError('this method is removed')

    def get_asset_usd_check_raw(self):
        obj = ktn_dcc_obj_node.Node('asset_geometries')
        if obj.get_is_exists() is True:
            pass
        else:
            pass

    def _get_stage_port_raw_(self, atr_path):
        configure = self.get_configure()
        key = 'look_outputs'
        obj_path = configure.get('workspace.{}.main.path'.format(key))
        dcc_obj = ktn_dcc_obj_node.Node(obj_path)
        if dcc_obj.get_is_exists() is True:
            scene_graph_opt = ktn_core.KtnStageOpt(dcc_obj.ktn_obj)
            return scene_graph_opt.get(atr_path)
        else:
            raise RuntimeError(
                bsc_log.Log.trace_method_error(
                    'obj="{}" is non-exists'.format(dcc_obj.path)
                )
            )

    def get_sg_geometries(self, pass_name='default'):
        configure = self.get_configure(pass_name)
        geometry_location = configure.get('option.geometry_root')
        #
        root = '{}/master'.format(geometry_location)
        #
        obj_scene = ktn_dcc_obj_utility.Scene()
        obj_scene.load_from_location(
            ktn_obj='{}__material_assigns_merge'.format(pass_name),
            root=root,
        )
        obj_universe = obj_scene.universe
        lis = []
        for i_obj_type_name in ['subdmesh', 'renderer procedural']:
            obj_type = obj_universe.get_obj_type(i_obj_type_name)
            if obj_type is not None:
                lis.extend(obj_type.get_objs())
        return lis

    def get_ng_material_groups(self):
        lis = []
        node_key = 'materials'
        dcc_main_obj, ktn_main_obj, (x, y) = self.get_main_args(node_key)
        if dcc_main_obj.get_is_exists() is True:
            input_ports = dcc_main_obj.get_input_ports()
            for i_input_port in input_ports:
                lis.append(i_input_port.obj)
        return lis

    def get_ng_shader_name(self, name, pass_name='default'):
        configure = self.get_configure(pass_name)
        key = 'shader'
        dcc_name_format = configure.get('node.{}.main.name'.format(key))
        dcc_name = dcc_name_format.format(name=name)
        return dcc_name

    # material group
    def get_ng_material_group_path(self, name, pass_name='default'):
        configure = self.get_configure(pass_name)
        key = 'material_group'
        dcc_path_format = configure.get('node.{}.main.path'.format(key))
        dcc_path = dcc_path_format.format(name=name)
        return dcc_path

    def get_ng_material_group_path_use_hash(self, and_geometry_opt, pass_name='default'):
        materials = and_geometry_opt.get_material_assigns()
        hash_key = bsc_core.HashMtd.get_hash_value(
            materials, as_unique_id=True
        )
        if hash_key in self._material_group_hash_stack:
            return self._material_group_hash_stack[hash_key]
        #
        name = and_geometry_opt.obj.name
        #
        configure = self.get_configure(pass_name)
        key = 'material_group'
        #
        dcc_path_format = configure.get('node.{}.main.path'.format(key))
        dcc_path = dcc_path_format.format(name=name)
        self._material_group_hash_stack[hash_key] = dcc_path
        return dcc_path

    def get_ng_material_group_force(self, dcc_path, pass_name='default'):
        configure = self.get_configure(pass_name)
        w, h = configure.get('option.w'), configure.get('option.h')
        key = 'material_group'
        node_key = configure.get('node.{}.keyword'.format(key))
        dcc_materials_merge, ktn_materials_merge, (x, y) = self.get_main_args(
            node_key,
            pass_name=pass_name
        )
        dcc_type_name = configure.get('node.{}.main.obj_type'.format(key))
        #
        dcc_obj = ktn_dcc_obj_node.Node(dcc_path)
        #
        ktn_obj, is_create = dcc_obj.get_dcc_instance(dcc_type_name)
        target_port_name = dcc_obj.name
        if is_create is True:
            index = self._get_merge_index_(dcc_materials_merge, target_port_name)
            d = 8
            #
            _x = index%d
            _y = int(index/d)
            r, g, b = self.get_look_pass_color(pass_name)
            x, y = x+_x*w, y+h+_y*h/2
            node_attributes = configure.get_as_content('node.{}.main.attributes'.format(key))
            if node_attributes:
                node_attributes.set('x', x)
                node_attributes.set('y', y)
                node_attributes.set('ns_colorr', r)
                node_attributes.set('ns_colorg', g)
                node_attributes.set('ns_colorb', b)
                ktn_obj.setAttributes(node_attributes.value)
            #
            dcc_materials_merge.get_input_port(target_port_name).set_create()
        #
        dcc_obj.get_output_port('out').set_target(
            dcc_materials_merge.get_input_port(target_port_name)
        )
        return is_create, dcc_obj

    # material
    def get_ng_material_path_use_hash(self, and_geometry_opt, pass_name='default'):
        materials = and_geometry_opt.get_material_assigns()
        hash_key = bsc_core.HashMtd.get_hash_value(
            materials, as_unique_id=True
        )
        if hash_key in self._material_hash_stack:
            return self._material_hash_stack[hash_key]
        #
        name = and_geometry_opt.obj.name
        #
        configure = self.get_configure(pass_name)
        key = 'material'
        #
        dcc_path_format = configure.get('node.{}.main.path'.format(key))
        dcc_path = dcc_path_format.format(name=name)
        self._material_hash_stack[hash_key] = dcc_path
        return dcc_path

    def get_ng_material_force(self, dcc_path, pass_name='default'):
        # todo: fix bug to "NetworkMaterial" is exists
        def get_exists_material():
            pass

        #
        configure = self.get_configure(pass_name)
        key = 'material'
        dcc_obj = ktn_dcc_obj_node.Node(dcc_path)
        #
        dcc_nmc = dcc_obj.get_parent()
        #
        dcc_node = ktn_dcc_obj_node.Node('{}/NetworkMaterial'.format(dcc_nmc.path)).set_rename(dcc_obj.name)
        is_create = False
        if dcc_node is not None:
            is_create = True
            node_attributes = configure.get_as_content('node.{}.main.attributes'.format(key))
            if node_attributes:
                dcc_node.ktn_obj.setAttributes(node_attributes.value)
        return is_create, dcc_obj

    def get_ng_material_path(self, name, pass_name='default'):
        configure = self.get_configure(pass_name)
        group_dcc_path = self.get_ng_material_group_path(name, pass_name)
        #
        key = 'material'
        dcc_name_format = configure.get('node.{}.main.name'.format(key))
        dcc_name = dcc_name_format.format(name=name)
        #
        dcc_path = '{}/{}'.format(group_dcc_path, dcc_name)
        return dcc_path

    # material assign
    def set_ng_material_assigns_cache_update(self, pass_name='default'):
        self._ng_material_assign_query_cache = {}
        configure = self.get_configure(pass_name)
        key = 'material_assign'
        node_key = configure.get('node.{}.keyword'.format(key))
        dcc_group, ktn_group, (x, y) = self.get_group_args(
            node_key,
            group_key='definition',
            pass_name=pass_name
        )
        if dcc_group.get_is_exists() is True:
            material_assigns = dcc_group.get_children()
            for i_material_assign in material_assigns:
                i_material_assign_opt = ktn_dcc_opt_look.MaterialAssignOpt(i_material_assign)
                i_geometry_paths = i_material_assign_opt.get_geometry_paths()
                for j_geometry_path in i_geometry_paths:
                    self._ng_material_assign_query_cache[j_geometry_path] = i_material_assign

    def get_ng_material_assign_from_cache(self, sg_geometry):
        return self._ng_material_assign_query_cache.get(sg_geometry.path)

    #
    def get_ng_material_assign_path(self, name, pass_name='default'):
        configure = self.get_configure(pass_name)
        key = 'material_assign'
        node_key = configure.get('node.{}.keyword'.format(key))
        dcc_group, ktn_group, (x, y) = self.get_group_args(
            node_key,
            group_key='definition',
            pass_name=pass_name
        )
        #
        dcc_path_format = configure.get('node.{}.main.path'.format(key))
        dcc_path = dcc_path_format.format(name=name)
        return dcc_path

    def get_ng_material_assign_force(self, dcc_path, pass_name='default'):
        configure = self.get_configure(pass_name)
        key = 'material_assign'
        node_key = configure.get('node.{}.keyword'.format(key))
        dcc_group, ktn_group, (x, y) = self.get_group_args(
            node_key,
            group_key='definition',
            pass_name=pass_name
        )

        dcc_obj = ktn_dcc_obj_node.Node(dcc_path)
        ktn_obj, is_create = ktn_core.NGGroupStackOpt(ktn_group).set_child_create(
            dcc_obj.name
        )
        if is_create is True:
            node_attributes = configure.get_as_content('node.{}.main.attributes'.format(key))
            if node_attributes:
                node_attributes.update_from(ktn_obj.getAttributes())
                r, g, b = self.get_look_pass_color(pass_name)
                node_attributes.set('ns_colorr', r)
                node_attributes.set('ns_colorg', g)
                node_attributes.set('ns_colorb', b)
                ktn_obj.setAttributes(node_attributes.value)
        return is_create, dcc_obj

    #
    def get_ng_material_assign_path_use_hash(self, and_geometry_opt, pass_name='default'):
        materials = and_geometry_opt.get_material_assigns()
        hash_key = bsc_core.HashMtd.get_hash_value(
            materials, as_unique_id=True
        )
        if hash_key in self._material_assign_hash_stack:
            return self._material_assign_hash_stack[hash_key]
        #
        name = and_geometry_opt.obj.name
        #
        configure = self.get_configure(pass_name)
        key = 'material_assign'
        #
        dcc_path_format = configure.get('node.{}.main.path'.format(key))
        dcc_path = dcc_path_format.format(name=name)
        self._material_assign_hash_stack[hash_key] = dcc_path
        return dcc_path

    # property assign
    def set_ng_property_assign_create(self, name, pass_name='default'):
        configure = self.get_configure(pass_name)
        key = 'property_assign'
        node_key = configure.get('node.{}.keyword'.format(key))
        dcc_group, ktn_group, (x, y) = self.get_group_args(
            node_key,
            group_key='definition',
            pass_name=pass_name
        )
        #
        properties_path_format = configure.get('node.{}.main.path'.format(key))
        properties_path = properties_path_format.format(name=name)
        #
        dcc_properties = ktn_dcc_obj_node.Node(properties_path)
        ktn_properties, is_create = ktn_core.NGGroupStackOpt(ktn_group).set_child_create(
            dcc_properties.name
        )
        if is_create is True:
            node_attributes = configure.get_as_content('node.{}.main.attributes'.format(key))
            if node_attributes:
                node_attributes.update_from(ktn_properties.getAttributes())
                r, g, b = self.get_look_pass_color(pass_name)
                node_attributes.set('ns_colorr', r)
                node_attributes.set('ns_colorg', g)
                node_attributes.set('ns_colorb', b)
                ktn_properties.setAttributes(node_attributes.value)
        return is_create, dcc_properties, ktn_properties

    def set_ng_property_assigns_cache_update(self, pass_name='default'):
        self._ng_property_assign_query_cache = {}
        configure = self.get_configure(pass_name)
        key = 'property_assign'
        node_key = configure.get('node.{}.keyword'.format(key))
        dcc_group, ktn_group, (x, y) = self.get_group_args(
            node_key,
            group_key='definition',
            pass_name=pass_name
        )
        if dcc_group.get_is_exists() is True:
            material_assigns = dcc_group.get_children()
            for i_material_assign in material_assigns:
                i_material_assign_opt = ktn_dcc_opt_look.MaterialAssignOpt(i_material_assign)
                i_geometry_paths = i_material_assign_opt.get_geometry_paths()
                for j_geometry_path in i_geometry_paths:
                    self._ng_property_assign_query_cache[j_geometry_path] = i_material_assign

    def get_ng_property_assign_from_cache(self, sg_geometry):
        return self._ng_property_assign_query_cache.get(sg_geometry.path)

    def get_ng_property_assign_path(self, name, pass_name='default'):
        #
        configure = self.get_configure(pass_name)
        key = 'property_assign'
        node_key = configure.get('node.{}.keyword'.format(key))
        dcc_group, ktn_group, (x, y) = self.get_group_args(
            node_key,
            group_key='definition',
            pass_name=pass_name
        )
        #
        dcc_path_format = configure.get('node.{}.main.path'.format(key))
        dcc_path = dcc_path_format.format(name=name)
        return dcc_path

    def get_ng_property_assign_force(self, dcc_path, pass_name='default'):
        configure = self.get_configure(pass_name)
        key = 'property_assign'
        node_key = configure.get('node.{}.keyword'.format(key))
        dcc_group, ktn_group, (x, y) = self.get_group_args(
            node_key,
            group_key='definition',
            pass_name=pass_name
        )
        #
        dcc_properties = ktn_dcc_obj_node.Node(dcc_path)
        ktn_properties, is_create = ktn_core.NGGroupStackOpt(ktn_group).set_child_create(
            dcc_properties.name
        )
        if is_create is True:
            node_attributes = configure.get_as_content('node.{}.main.attributes'.format(key))
            if node_attributes:
                node_attributes.update_from(ktn_properties.getAttributes())
                r, g, b = self.get_look_pass_color(pass_name)
                node_attributes.set('ns_colorr', r)
                node_attributes.set('ns_colorg', g)
                node_attributes.set('ns_colorb', b)
                ktn_properties.setAttributes(node_attributes.value)
        return is_create, dcc_properties, ktn_properties

    def get_ng_properties_assign_path_use_hash(self, and_geometry_opt, pass_name='default'):
        properties = and_geometry_opt.get_properties()
        visibilities = and_geometry_opt.get_visibilities()
        properties.update(visibilities)
        hash_key = bsc_core.HashMtd.get_hash_value(
            properties, as_unique_id=True
        )
        if hash_key in self._property_assign_hash_stack:
            return self._property_assign_hash_stack[hash_key]
        #
        name = and_geometry_opt.obj.name
        #
        configure = self.get_configure(pass_name)
        key = 'property_assign'
        #
        dcc_path_format = configure.get('node.{}.main.path'.format(key))
        dcc_path = dcc_path_format.format(name=name)
        self._property_assign_hash_stack[hash_key] = dcc_path
        return dcc_path

    @classmethod
    def _set_assign_cel_value_update_(cls, dcc_node, shape_path):
        p = '[(](.*?)[)]'
        cel_port = dcc_node.get_port('CEL')
        exists_value = cel_port.get()
        if exists_value:
            _ = re.findall(p, exists_value)
            if _:
                cel_value = '({} {})'.format(_[0], shape_path)
            else:
                cel_value = '({} {})'.format(exists_value, shape_path)
        else:
            cel_value = shape_path
        cel_port.set(cel_value)

    def get_ng_look_pass(self, pass_name='default'):
        _ = '{}__look'.format(pass_name)
        dcc_obj = ktn_dcc_obj_node.Node(_)
        return dcc_obj, dcc_obj.ktn_obj

    def set_set_usd_reload(self):
        node = self.get_node_graph_node(
            'asset_geometries', 'asset'
        )
        ktn_core.NGNodeOpt(
            node.ktn_obj
        ).execute_port(
            'usd.create'
        )

    def set_asset_front_camera_fill_to_front(self):
        node = self.get_node_graph_node(
            'asset_geometries', 'asset'
        )
        ktn_core.NGNodeOpt(
            node.ktn_obj
        ).execute_port(
            'extra.transformation.translate_to_origin'
        )
        #
        node = self.get_node_graph_node(
            'cameras', 'cameras'
        )
        ktn_core.NGNodeOpt(
            node.ktn_obj
        ).execute_port(
            'cameras.front.fill_to_front'
        )

    def set_asset_front_camera_fill_to_rotation(self):
        node = self.get_node_graph_node(
            'asset_geometries', 'asset'
        )
        ktn_core.NGNodeOpt(
            node.ktn_obj
        ).execute_port(
            'extra.transformation.translate_to_origin'
        )
        #
        node = self.get_node_graph_node(
            'cameras', 'cameras'
        )
        ktn_core.NGNodeOpt(
            node.ktn_obj
        ).execute_port(
            'cameras.front.fill_to_rotation'
        )
