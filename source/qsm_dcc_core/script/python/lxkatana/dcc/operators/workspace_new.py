# coding:utf-8
import fnmatch

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage
# katana
from ... import core as ktn_core
# katana dcc
from ..objects import node as ktn_dcc_obj_node

from ..objects import nodes_for_look as ktn_dcc_obj_nodes_for_look


# noinspection PyUnusedLocal
class LookOutputOpt(object):
    """
# coding:utf-8
import lxkatana

lxkatana.set_reload()

import lxkatana.core as ktn_core

import lxkatana.dcc.operators as ktn_dcc_operators

ktn_dcc_operators.LookOutputOpt(
    ktn_core.NGNodeOpt('lok_spc__LFB')
).export_ass_auto()
    """
    GEOMETRY_TYPES = [
        'subdmesh',
        'renderer procedural',
        'pointcloud',
        'polymesh',
        'curves'
    ]

    def __init__(self, obj_opt):
        self._obj_opt = obj_opt

        self._dcc_node = ktn_dcc_obj_node.Node(
            self._obj_opt.get_path()
        )

    @classmethod
    def get_look_output_nodes(cls):
        return ktn_core.NGNodesMtd.find_nodes(
            type_name='LookFileBake', ignore_bypassed=True
        )

    @classmethod
    def get_look_output_node_opts(cls):
        return [
            ktn_core.NGNodeOpt(i) for i in cls.get_look_output_nodes()
        ]

    @classmethod
    def get_all_source_nodes(cls):
        list_ = []
        _ = cls.get_look_output_node_opts()
        for i in _:
            i_nodes = cls(i).get_all_look_pass_source_nodes()
            list_.extend(i_nodes)
        return list_

    def get_all_look_pass_names(self):
        lis = []
        input_ports = self._dcc_node.get_input_ports()
        for i_input_port in input_ports:
            i_port_path = i_input_port.get_name()
            if i_port_path not in ['orig']:
                lis.append(i_port_path)
        return lis

    def get_look_pass_source_node(self, look_pass_name):
        input_port = self._dcc_node.get_input_port(look_pass_name)
        if input_port.get_is_exists() is True:
            return input_port.get_source_obj()

    def get_all_look_pass_source_nodes(self):
        list_ = []
        pass_names = self.get_all_look_pass_names()
        for i_pass_name in pass_names:
            i_node = self.get_look_pass_source_node(i_pass_name)
            if i_node is not None:
                list_.append(
                    i_node
                )
        return list_

    def get_all_dcc_geometry_materials_by_location(self, location):
        list_ = []
        query_dict = ktn_dcc_obj_nodes_for_look.Materials.get_nmc_material_dict()
        dcc_objs = self.get_all_look_pass_source_nodes()
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

    def get_all_dcc_materials(self):
        list_ = []
        query_dict = ktn_dcc_obj_nodes_for_look.Materials.get_nmc_material_dict()
        dcc_objs = self.get_all_look_pass_source_nodes()
        for i_dcc_obj in dcc_objs:
            i_material_sg_paths = ktn_core.KtnStageOpt(i_dcc_obj.ktn_obj).get_descendant_paths_at('/root/materials')
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
            i_dcc_nodes = [
                ktn_dcc_obj_node.Node(i.getName()) for i in ktn_core.NGNodeOpt(i_dcc_obj.ktn_obj).get_all_source_objs()
            ]
            list_.extend(
                i_dcc_nodes
            )
        return list_

    def get_all_dcc_shaders(self):
        list_ = []
        dcc_objs = self.get_all_dcc_materials()
        for i_dcc_obj in dcc_objs:
            i_dcc_nodes = [
                ktn_dcc_obj_node.Node(i.getName()) for i in ktn_core.NGNodeOpt(i_dcc_obj.ktn_obj).get_all_source_objs()
            ]
            list_.extend(
                i_dcc_nodes
            )
        return list_

    def get_all_look_pass_args(self):
        list_ = []
        pass_names = self.get_all_look_pass_names()
        for i_pass_name in pass_names:
            i_node = self.get_look_pass_source_node(i_pass_name)
            if i_node is not None:
                list_.append(
                    (i_pass_name, self.get_look_pass_source_node(i_pass_name))
                )
        return list_

    def get_non_material_geometry_args(self, location):
        list_ = []
        _ = self.get_all_look_pass_args()
        for i_pass_name, i_dcc_obj in _:
            i_s_opt = ktn_core.KtnStageOpt(i_dcc_obj.get_name())
            i_geometry_paths = i_s_opt.get_all_paths_at(
                location, type_includes=self.GEOMETRY_TYPES
            )
            for j_path in i_geometry_paths:
                j_obj_opt = ktn_core.KtnSGNodeOpt(i_s_opt, j_path)
                if not j_obj_opt.get('materialAssign'):
                    list_.append(
                        (i_pass_name, j_path)
                    )
        return list_

    def get_geometry_uv_map_usd_source_file(self):
        s = ktn_core.KtnStageOpt(self._obj_opt._ktn_obj)
        geometry_scheme = self.get_geometry_scheme()
        if geometry_scheme == 'asset':
            location = '/root/world/geo/master'
            _ = s.generate_obj_opt(location).get('userProperties.usd.variants.asset.surface.override.file')
            if _:
                f_opt = bsc_storage.StgFileOpt(_)
                # TODO fix this bug
                if f_opt.get_name() == 'uv_map.usda':
                    return '{}/payload.usda'.format(
                        f_opt.get_directory_path()
                    )
                return _

    def get_geometry_uv_map_usd_file(self):
        s = ktn_core.KtnStageOpt(self._obj_opt._ktn_obj)
        geometry_scheme = self.get_geometry_scheme()
        if geometry_scheme == 'asset':
            location = '/root/world/geo/master'
            _ = s.generate_obj_opt(location).get('userProperties.usd.variants.asset.surface.override.file')
            return _

    def get_geometry_scheme(self):
        s = ktn_core.KtnStageOpt(self._obj_opt._ktn_obj)
        if s.get_obj_exists('/root/world/geo/master') is True:
            return 'asset'
        elif s.get_obj_exists('/root/world/geo/assets') is True:
            return 'shot'
        return 'asset'

    def get_geometry_root(self):
        s = ktn_core.KtnStageOpt(self._obj_opt._ktn_obj)
        if s.get_obj_exists('/root/world/geo/master') is True:
            return '/root/world/geo/master'
        elif s.get_obj_exists('/root/world/geo/assets') is True:
            return '/root/world/geo/assets'
        return '/root/world/geo/master'

    def export_ass_auto(self, dynamic_override_uv_maps=False):
        node = ktn_dcc_obj_node.Node(
            self._obj_opt.get_path()
        )
        if node.get_is_exists() is True:
            parent_path = node.get_parent_path()
            look_pass_names = self.get_all_look_pass_names()
            geometry_scheme = self.get_geometry_scheme()
            geometry_root = self.get_geometry_root()
            if geometry_scheme == 'asset':
                nodes = []
                for i_look_pass_name in look_pass_names:
                    i_input_port = node.get_input_port(i_look_pass_name)
                    if i_input_port:
                        i_source_port = i_input_port.get_source()
                        if i_source_port is not None:
                            i_node = ktn_dcc_obj_node.Node(
                                '{}/asset_ass_export__{}'.format(parent_path, i_look_pass_name)
                                )
                            i_node.get_dcc_instance('AssetAssExport_Wsp', 'Group')
                            i_node.set(
                                'parameters.look_pass', i_look_pass_name
                            )
                            i_node.set(
                                'parameters.dynamic.override_uv_maps', dynamic_override_uv_maps
                            )
                            # connection
                            i_source_port.set_target(
                                i_node.get_input_port('input')
                            )
                            #
                            ktn_core.NGNodeOpt(i_node.ktn_obj).execute_port(
                                'parameters.ass.guess'
                            )
                            nodes.append(i_node)
                #
                for i_node in nodes:
                    ktn_core.NGNodeOpt(i_node.ktn_obj).execute_port(
                        'parameters.execute'
                    )
                    i_node.do_delete()

    def export_ass(self, file_path):
        pass

    def export_klf(self, file_path):
        node = ktn_dcc_obj_node.Node(
            self._obj_opt.get_path()
        )
        if node.get_is_exists() is True:
            geometry_scheme = self.get_geometry_scheme()
            geometry_root = self.get_geometry_root()
            #
            node.set('rootLocations', [geometry_root])
            #
            node.get_port('saveTo').set(file_path)
            #
            file_opt = bsc_storage.StgFileOpt(file_path)
            file_opt.create_directory()
            #
            node.ktn_obj.WriteToLookFile(None, file_path)
            #
            bsc_log.Log.trace_method_result(
                'look-klf export',
                '"{}"'.format(file_path)
            )

    def export_klf_extra(self, file_path):
        node = ktn_dcc_obj_node.Node(
            self._obj_opt.get_path()
        )
        if node.get_is_exists() is True:
            geometry_scheme = self.get_geometry_scheme()
            geometry_root = self.get_geometry_root()
            #
            dcc_shaders = self.get_all_dcc_geometry_shaders_by_location(geometry_root)
            #
            patterns = [
                # etc. '/tmp/file.%04d.ext'%frame
                '\'*.%0[0-9]d.*\'%*',
                # etc. frame/2, frame*2
                '*frame*'
            ]
            dict_ = {}
            #
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
                bsc_storage.StgFileOpt(
                    file_path
                ).set_write(
                    dict_
                )
