# coding:utf-8
import six

import threading

import lxcontent.core as ctt_core

import lxresource as bsc_resource

import lxbasic.core as bsc_core

import lxbasic.texture as bsc_texture
# katana
from .. import core as ktn_core


# noinspection PyUnusedLocal
class ScpTextureBuildCommand(object):

    @classmethod
    def _create_shader(cls, data, extend_kwargs=None, to_view_center=False):
        type_name = data['type']
        shader_type_name = data['shader_type']
        path = data['path']
        if isinstance(extend_kwargs, dict):
            path = path.format(**extend_kwargs)
        #
        ktn_obj, is_create = ktn_core.NGNodeOpt._generate_shader_create_args(path, type_name, shader_type_name)
        if is_create is True:
            obj_opt = ktn_core.NGNodeOpt(ktn_obj)
            if to_view_center is True:
                obj_opt.move_to_view_center()
            #
            obj_opt.set_attributes(dict(ns_viewState=0.0))
            obj_opt.set_color(bsc_core.RawTextOpt(shader_type_name).to_rgb_(maximum=1.0, s_p=25, v_p=25))
            #
            obj_opt.set_shader_parameters_by_data(
                data.get('shader_parameters') or {},
                extend_kwargs=extend_kwargs
            )
            obj_opt.set_shader_expressions_by_data(
                data.get('shader_expressions') or {},
                extend_kwargs=extend_kwargs
            )
            obj_opt.set_shader_hints_by_data(
                data.get('shader_hints') or {},
                extend_kwargs=extend_kwargs
            )
            #
            ktn_core.NGNodeOpt._create_connections_by_data(
                data.get('connections') or [],
                extend_kwargs=extend_kwargs,
                auto_create_source=True,
                auto_create_target=True,
                ignore_non_exists=True

            )
        return ktn_obj

    @classmethod
    def _create_node(cls, data, extend_kwargs=None, to_view_center=False):
        type_name = data['type']
        path = data['path']
        if isinstance(extend_kwargs, dict):
            path = path.format(**extend_kwargs)
        #
        ktn_obj, is_create = ktn_core.NGNodeOpt._generate_node_create_args(path, type_name)
        if is_create is True:
            obj_opt = ktn_core.NGNodeOpt(ktn_obj)
            if to_view_center is True:
                obj_opt.move_to_view_center()
            #
            obj_opt.set_attributes(dict(ns_viewState=0.0))
            obj_opt.set_color(bsc_core.RawTextOpt(type_name).to_rgb_(maximum=1.0, s_p=25, v_p=25))
            #
            obj_opt.set_shader_parameters_by_data(
                data.get('shader_parameters') or {},
                extend_kwargs=extend_kwargs
            )
            obj_opt.set_shader_expressions_by_data(
                data.get('shader_expressions') or {},
                extend_kwargs=extend_kwargs
            )
            obj_opt.set_shader_hints_by_data(
                data.get('shader_hints') or {},
                extend_kwargs=extend_kwargs
            )
            #
            ktn_core.NGNodeOpt._create_connections_by_data(
                data.get('connections') or [],
                extend_kwargs=extend_kwargs,
                auto_create_source=True,
                auto_create_target=True,
                ignore_non_exists=True
            )
        return ktn_obj

    @classmethod
    def _update_material_collapsed(cls, mtl_grp_obj_opt, mtl_name):
        attributes_ = mtl_grp_obj_opt.get_attributes()
        if 'ns_collapsedPages' in attributes_:
            v = attributes_['ns_collapsedPages']
            if v:
                if mtl_name not in v:
                    v += '{} | '.format(mtl_name)

                mtl_grp_obj_opt.set_attributes(
                    dict(ns_collapsedPages=v)
                )
            else:
                mtl_grp_obj_opt.set_attributes(
                    dict(ns_collapsedPages='{} | '.format(mtl_name))
                )
        else:
            mtl_grp_obj_opt.set_attributes(
                dict(ns_collapsedPages='{} | '.format(mtl_name))
            )

    def __init__(self, texture_name, texture_assign):
        self._cfg = ctt_core.Content(
            value=bsc_resource.RscExtendConfigure.get_yaml('katana/node-graph/texture')
        )
        self._cfg.set(
            'option.texture_name', texture_name
        )
        self._cfg.set(
            'option.time_tag', bsc_core.TimeExtraMtd.generate_time_tag_36_(multiply=100)
        )

        self._texture_assign = texture_assign

    def get_configure(self):
        return self._cfg

    @ktn_core.Modifier.undo_debug_run
    def do_create(self):
        pass

    def create_material_group_and_material(self, to_view_center=False):
        mtl_grp_type_name = self._cfg.get('node.material_group.type')
        mtl_grp_path = self._cfg.get('node.material_group.path')
        mtl_type_name = self._cfg.get('node.material.type')
        mtl_path = self._cfg.get('node.material.path')
        mtl_grp_ktn_obj, is_create = ktn_core.NGNodeOpt._generate_node_create_args(mtl_grp_path, mtl_grp_type_name)
        if is_create is True:
            mtl_grp_obj_opt = ktn_core.NGNodeOpt(mtl_grp_ktn_obj)
            mtl_grp_obj_opt.set_color((.25, .25, .75))
            if to_view_center is True:
                mtl_grp_obj_opt.move_to_view_center()
            #
            mtl_ktn_objs = mtl_grp_obj_opt.get_children(type_includes=[mtl_type_name])
            if mtl_ktn_objs:
                mtl_obj_opt = ktn_core.NGNodeOpt(mtl_ktn_objs[-1])
                mtl_obj_opt.set_rename(bsc_core.PthNodeOpt(mtl_path).get_name())
        else:
            mtl_grp_obj_opt = ktn_core.NGNodeOpt(mtl_grp_ktn_obj)
            mtl_grp_ktn_obj.addNetworkMaterialNode()
            mtl_ktn_objs = mtl_grp_obj_opt.get_children(type_includes=[mtl_type_name])
            if mtl_ktn_objs:
                mtl_obj_opt = ktn_core.NGNodeOpt(mtl_ktn_objs[-1])
                mtl_obj_opt.set_rename(bsc_core.PthNodeOpt(mtl_path).get_name())

    def create_material(self):
        mtl_grp_path = self._cfg.get('node.material_group.path')
        #
        mtl_type_name = self._cfg.get('node.material.type')
        mtl_path = self._cfg.get('node.material.path')
        #
        mtl_grp_obj_opt = ktn_core.NGNodeOpt(mtl_grp_path)
        # create material
        mtl_grp_obj_opt._generate_material_node_graph_create_args(
            mtl_path, 'NetworkMaterial'
        )
        mtl_ktn_objs = mtl_grp_obj_opt.get_children(type_includes=[mtl_type_name])
        if mtl_ktn_objs:
            mtl_obj_opt = ktn_core.NGNodeOpt(mtl_ktn_objs[-1])
            mtl_name = bsc_core.PthNodeOpt(mtl_path).get_name()
            mtl_obj_opt.set_rename(mtl_name)
            self._update_material_collapsed(mtl_grp_obj_opt, mtl_name)

    def create_node_backdrop(self):
        data = self._cfg.get('node.node_backdrop')
        #
        node_bdp_type_name = data.get('type')
        node_bdp_path = data.get('path')
        #
        w, h = 320, 80
        #
        node_bdp_ktn_obj, is_create = ktn_core.NGNodeOpt._generate_node_create_args(node_bdp_path, node_bdp_type_name)
        if is_create is True:
            texture_name = self._cfg.get('option.texture_name')
            node_bdp_obj_opt = ktn_core.NGNodeOpt(node_bdp_ktn_obj)

            sdr_path = self._cfg.get('node.arnold_surface_shader.path')
            sdr_obj_opt = ktn_core.NGNodeOpt(sdr_path)
            x, y = sdr_obj_opt.get_position()
            r, g, b = bsc_core.RawTextOpt(texture_name).to_rgb_(maximum=1.0, s_p=25, v_p=25)
            attributes = dict(
                x=x-w,
                y=y,
                ns_sizeX=w*4,
                ns_sizeY=h*4,
                ns_colorr=r,
                ns_colorg=g,
                ns_colorb=b,
                ns_text=texture_name,
                ns_fontScale=2.0
            )
            node_bdp_obj_opt.set_attributes(
                attributes
            )

    def create_node_groups(self, to_view_center=False):
        ktn_obj = self.create_node_group('node_group')
        if to_view_center is True:
            obj_opt = ktn_core.NGNodeOpt(ktn_obj)
            obj_opt.move_to_view_center()

    def create_node_group(self, key):
        type_name = self._cfg.get('node.{}.type'.format(key))
        path = self._cfg.get('node.{}.path'.format(key))
        ktn_obj, is_create = ktn_core.NGNodeOpt._generate_node_create_args(path, type_name)
        if is_create is True:
            obj_opt = ktn_core.NGNodeOpt(ktn_obj)
            obj_opt.set_color((.25, .25, .5))
            #
            obj_opt.create_input_ports_by_data(self._cfg.get('node.{}.input_ports'.format(key)) or [])
            obj_opt.create_output_ports_by_data(self._cfg.get('node.{}.output_ports'.format(key)) or [])
            #
            ktn_core.NGNodeOpt._create_connections_by_data(
                self._cfg.get('node.{}.connections'.format(key)) or [],
                ignore_non_exists=True
            )
        return ktn_obj

    def update_node_groups(self):
        ktn_obj = self.update_node_group('node_group')

    def update_node_group(self, key):
        type_name = self._cfg.get('node.{}.type'.format(key))
        path = self._cfg.get('node.{}.path'.format(key))
        ktn_obj, is_create = ktn_core.NGNodeOpt._generate_node_create_args(path, type_name)
        obj_opt = ktn_core.NGNodeOpt(path)
        obj_opt = ktn_core.NGNodeOpt(ktn_obj)
        obj_opt.set_color((.25, .25, .5))
        #
        obj_opt.create_input_ports_by_data(self._cfg.get('node.{}.input_ports'.format(key)) or [])
        obj_opt.create_output_ports_by_data(self._cfg.get('node.{}.output_ports'.format(key)) or [])
        #
        ktn_core.NGNodeOpt._create_connections_by_data(
            self._cfg.get('node.{}.connections'.format(key)) or [],
            ignore_non_exists=True
        )
        return obj_opt.get_ktn_obj()

    def create_outer_nodes(self, to_view_center=False):
        for i_key in [
            'arnold_surface_shader',
        ]:
            self.create_shader(i_key, to_view_center=to_view_center)

    def create_inner_nodes(self, arnold=True, usd=True):
        for i_key in [
            'node_passthrough'
        ]:
            self.create_node_group(i_key)
        # create arnold node
        if arnold is True:
            for i_key in [
                'arnold_texture_basic_mode',
                #
                'arnold_texture_uv_map_proxy',
                'arnold_texture_triplanar_proxy',
                'arnold_texture_triplanar_translate',
                'arnold_texture_triplanar_rotate',
                'arnold_texture_triplanar_scale',
            ]:
                self.create_shader(i_key)
        # create usd node
        if usd is True:
            for i_key in [
                'usd_shader',
                'usd_uv_transform',
                'usd_uv',
            ]:
                self.create_shader(i_key)

    def create_shader(self, key, extend_kwargs=None, to_view_center=False):
        data = self._cfg.get('node.{}'.format(key))
        return self._create_shader(data, extend_kwargs=extend_kwargs, to_view_center=to_view_center)

    def create_textures(self, arnold=True, usd=True):
        if arnold is True:
            key = 'arnold_texture'
            all_sub_keys = self._cfg.get_key_names_at(key)
            all_sub_keys_valid = []
            for i_sub_key in all_sub_keys:
                if i_sub_key in self._texture_assign:
                    all_sub_keys_valid.append(i_sub_key)
                    i_texture = self._texture_assign[i_sub_key]
                    i_c = self._cfg.get(
                        '{}.{}'.format(key, i_sub_key)
                    )
                    self.__create_shader_node_graph(
                        key, i_sub_key,
                        extend_kwargs=dict(
                            texture=i_texture
                        )
                    )
                    #
                    ktn_core.NGNodeOpt._create_connections_by_data(
                        i_c.get('connections') or [],
                        auto_create_source=True,
                        auto_create_target=True,
                        ignore_non_exists=True
                    )
            # create connections after
            # for i_sub_key in all_sub_keys_valid:
            #     i_c = self._cfg.get(
            #         '{}.{}'.format(key, i_sub_key)
            #     )
            #     if i_c:
            #         self.__create_shader_node_graph_connections(
            #             key, i_sub_key
            #         )

        if usd is True:
            key = 'usd_texture'
            all_sub_keys = self._cfg.get_key_names_at(key)
            all_sub_keys_valid = []
            for i_sub_key in all_sub_keys:
                if i_sub_key in self._texture_assign:
                    all_sub_keys_valid.append(i_sub_key)
                    i_texture = self._texture_assign[i_sub_key]
                    i_c = self._cfg.get(
                        '{}.{}'.format(key, i_sub_key)
                    )
                    self.__create_shader_node_graph(
                        key, i_sub_key,
                        extend_kwargs=dict(
                            texture=i_texture
                        )
                    )
                    ktn_core.NGNodeOpt._create_connections_by_data(
                        i_c.get('connections') or [],
                        auto_create_source=True,
                        auto_create_target=True,
                        ignore_non_exists=True
                    )
            # create connections after
            # for i_sub_key in all_sub_keys_valid:
            #     i_c = self._cfg.get(
            #         '{}.{}'.format(key, i_sub_key)
            #     )
            #     if i_c:
            #         self.__create_shader_node_graph_connections(
            #             key, i_sub_key,
            #         )

    def __create_shader_node_graph_connections(self, key, sub_key, extend_kwargs=None):
        data = self._cfg.get('{}.{}.node_graph'.format(key, sub_key)) or {}
        for k, v in data.items():
            ktn_core.NGNodeOpt._create_connections_by_data(
                v.get('connections') or [],
                extend_kwargs=extend_kwargs,
                auto_create_source=True,
                auto_create_target=True,
                ignore_non_exists=True
            )

    def __create_shader_node_graph(self, key, sub_key, extend_kwargs=None):
        data = self._cfg.get('{}.{}.node_graph'.format(key, sub_key)) or {}
        for k, v in data.items():
            if 'shader_type' in v:
                self._create_shader(v, extend_kwargs)
            else:
                self._create_node(v, extend_kwargs)

    def gui_layout_nodes(self):
        sdr_path = self._cfg.get('node.arnold_surface_shader.path')
        ktn_core.NGNodeOpt(sdr_path).gui_layout_shader_graph(
            size=(320, 80), shader_view_state=0.0
        )


class ScpTextureBuildForDrop(object):
    """
# coding:utf-8
import lxkatana

lxkatana.set_reload()

import lxbasic.core as bsc_core

import lxkatana.core as ktn_core

import lxbasic.database as bsc_database

import lxkatana.dcc.objects as ktn_dcc_objects

import lxtool.library.scripts as lib_scripts

import lxkatana.scripts as ktn_scripts

data = {
    'specular_roughness': u'/production/library/resource/all/surface/mossy_ground_umkkfcolw/v0001/texture/acescg/tx/mossy_ground_umkkfcolw.roughness.tx',
    # 'normal': u'/production/library/resource/all/surface/mossy_ground_umkkfcolw/v0001/texture/acescg/tx/mossy_ground_umkkfcolw.normal.tx',
    'diffuse_color': u'/production/library/resource/all/surface/mossy_ground_umkkfcolw/v0001/texture/acescg/tx/mossy_ground_umkkfcolw.albedo.tx',
    'displacement': u'/production/library/resource/all/surface/mossy_ground_umkkfcolw/v0001/texture/acescg/tx/mossy_ground_umkkfcolw.displacement.tx',
    # 'metalness': '',
    # 'specular': '',
    # 'opacity': '',
    # 'transmission': '',
}

tab_opt = ktn_core.GuiNodeGraphTabOpt()
ktn_group = tab_opt.get_current_group()

ktn_group_opt = ktn_core.NGNodeOpt(ktn_group)
texture_name = 'texture_name'
ktn_scripts.ScpTextureBuildForDrop(
    ktn_group_opt,
    texture_name,
    data,
).accept()
    """
    def __init__(self, obj_opt, texture_name, texture_assign):
        self._obj_opt = obj_opt
        self._command = ScpTextureBuildCommand(
            texture_name, texture_assign
        )
        self._command.get_configure().set(
            'option.root', self._obj_opt.get_path()
        )

    @ktn_core.Modifier.undo_debug_run
    def accept(self):
        def post_fnc_():
            self._command.gui_layout_nodes()

        if self._obj_opt.get_name() == 'rootNode':
            self._command.get_configure().do_flatten()
            #
            self._command.create_material_group_and_material(to_view_center=True)
            self._command.create_node_groups()
            self._command.create_outer_nodes()
            self._command.create_inner_nodes()
            self._command.create_textures()
            #
            timer = threading.Timer(.25, post_fnc_)
            timer.start()
        else:
            type_name = self._obj_opt.get_type_name()
            if type_name == 'Group':
                self._command.get_configure().do_flatten()
                #
                self._command.create_material_group_and_material(to_view_center=True)
                #
                self._command.create_node_groups()
                self._command.create_outer_nodes()
                self._command.create_inner_nodes()
                self._command.create_textures()
                #
                timer = threading.Timer(.25, post_fnc_)
                timer.start()
            elif type_name == 'NetworkMaterialCreate':
                self._command.get_configure().set(
                    'node.material_group.path', self._obj_opt.get_path()
                )
                self._command.get_configure().do_flatten()
                #
                self._command.create_material()
                self._command.create_node_groups()
                self._command.create_outer_nodes(to_view_center=True)
                self._command.create_inner_nodes()
                self._command.create_textures()
                #
                timer = threading.Timer(.25, post_fnc_)
                timer.start()


class ScpTextureBuildForCreate(object):
    """
# coding:utf-8
import lxkatana

lxkatana.set_reload()

import lxbasic.core as bsc_core

import lxkatana.core as ktn_core

import lxbasic.database as bsc_database

import lxkatana.dcc.objects as ktn_dcc_objects

import lxtool.library.scripts as lib_scripts

import lxkatana.scripts as ktn_scripts

data = {
    'specular_roughness': u'/production/library/resource/all/surface/mossy_ground_umkkfcolw/v0001/texture/acescg/tx/mossy_ground_umkkfcolw.roughness.tx',
    # 'normal': u'/production/library/resource/all/surface/mossy_ground_umkkfcolw/v0001/texture/acescg/tx/mossy_ground_umkkfcolw.normal.tx',
    'diffuse_color': u'/production/library/resource/all/surface/mossy_ground_umkkfcolw/v0001/texture/acescg/tx/mossy_ground_umkkfcolw.albedo.tx',
    'displacement': u'/production/library/resource/all/surface/mossy_ground_umkkfcolw/v0001/texture/acescg/tx/mossy_ground_umkkfcolw.displacement.tx',
    # 'metalness': '',
    # 'specular': '',
    # 'opacity': '',
    # 'transmission': '',
}

ktn_group_opt = ktn_core.NGNodeOpt('ShadingGroup')
texture_name = 'texture_name'
ktn_scripts.ScpTextureBuildForCreate(
    ktn_group_opt,
    texture_name,
    data,
).accept()
    """
    def __init__(self, node_arg, texture_name, texture_assign):
        if isinstance(node_arg, six.string_types):
            self._obj_opt = ktn_core.NGNodeOpt(node_arg)
        else:
            self._obj_opt = node_arg

        self._command = ScpTextureBuildCommand(
            texture_name, texture_assign
        )

    def accept(self):
        def post_fnc_():
            if layout_path is not None:
                ktn_core.NGNodeOpt(layout_path).gui_layout_shader_graph(
                    size=(320, 160), shader_view_state=1.0
                )

        layout_path = None
        # execute from material group
        if self._obj_opt.get_is('NetworkMaterialCreate'):
            material_group_opt = self._obj_opt
            self._command.get_configure().set(
                'option.root', material_group_opt.get_parent_opt().get_path()
            )
            self._command.get_configure().set(
                'node.material_group.path', material_group_opt.get_path()
            )
            self._command.get_configure().do_flatten()

            self._command.create_material()
            self._command.create_node_groups()
            self._command.create_outer_nodes()
            self._command.create_inner_nodes()
            self._command.create_textures()

            layout_path = self._command.get_configure().get('node.material.path')
        # execute from shader
        elif self._obj_opt.get_is('ArnoldShadingNode'):
            if self._obj_opt.get('nodeType') == 'standard_surface':
                parent_opt = self._obj_opt.get_parent_opt()
                material_group_opt = parent_opt
                self._command.get_configure().set(
                    'node.material_group.path', material_group_opt.get_path()
                )
                self._command.get_configure().set(
                    'node.arnold_surface_shader.path', self._obj_opt.get_path()
                )
                self._command.get_configure().do_flatten()
                self._command.create_node_groups()
                self._command.create_inner_nodes()
                self._command.create_textures()

                layout_path = self._obj_opt.get_path()
        # execute from node group
        elif self._obj_opt.get_is('ShadingGroup'):
            if self._obj_opt.has_children():
                return
            parent_opt = self._obj_opt.get_parent_opt()
            # if parent_opt and parent_opt.get_is('NetworkMaterialCreate'):
            material_group_opt = parent_opt
            self._command.get_configure().set(
                'node.material_group.path', material_group_opt.get_path()
            )
            self._command.get_configure().set(
                'node.node_group.path', self._obj_opt.get_path()
            )
            self._command.get_configure().do_flatten()
            self._command.update_node_groups()
            self._command.create_inner_nodes()
            self._command.create_textures()

            layout_path = self._obj_opt.get_path()

        if layout_path is not None:
            timer = threading.Timer(.25, post_fnc_)
            timer.start()


class ScpTextureBuildForPaste(object):
    def __init__(self, node_arg, scheme, texture_path):
        if isinstance(node_arg, six.string_types):
            self._obj_opt = ktn_core.NGNodeOpt(node_arg)
        else:
            self._obj_opt = node_arg

        self._scheme = scheme
        self._command = None
        m = bsc_texture.TxrMethodForBuild.generate_instance()
        all_texture_args = m.generate_all_texture_args(texture_path)
        if all_texture_args:
            texture_name, texture_data = all_texture_args
            texture_assign = {}
            for k, v in texture_data.items():
                texture_assign[k] = v[0]

            self._command = ScpTextureBuildCommand(
                texture_name, texture_assign
            )

    def accept(self):
        def post_fnc_():
            if layout_path is not None:
                ktn_core.NGNodeOpt(layout_path).gui_layout_shader_graph(
                    size=(320, 160), shader_view_state=1.0
                )
                if drop_paths:
                    ktn_core.GuiNodeGraphOpt.drop_nodes(
                        map(lambda x: ktn_core.NGNodeOpt(x).ktn_obj, drop_paths)
                    )

        import lxgui.qt.core as gui_qt_core

        with gui_qt_core.GuiQtUtil.gui_bustling():
            layout_path = None
            drop_paths = []
            if self._command is not None:
                type_name = self._obj_opt.get_type_name()
                if type_name == 'NetworkMaterialCreate':
                    if self._scheme == 'material':
                        self._command.get_configure().set(
                            'node.material_group.path', self._obj_opt.get_path()
                        )
                        self._command.get_configure().do_flatten()

                        self._command.create_material()
                        self._command.create_node_groups()
                        self._command.create_outer_nodes()
                        self._command.create_inner_nodes()
                        self._command.create_textures()

                        layout_path = self._command.get_configure().get('node.material.path')
                        drop_paths = [
                            self._command.get_configure().get('node.arnold_surface_shader.path'),
                            self._command.get_configure().get('node.node_group.path')
                        ]
                    elif self._scheme == 'shader':
                        self._command.get_configure().set(
                            'node.material_group.path', self._obj_opt.get_path()
                        )
                        self._command.get_configure().do_flatten()
                        #
                        self._command.create_node_groups()
                        self._command.create_outer_nodes()
                        self._command.create_inner_nodes()
                        self._command.create_textures()

                        layout_path = self._command.get_configure().get('node.arnold_surface_shader.path')
                        drop_paths = [
                            self._command.get_configure().get('node.arnold_surface_shader.path'),
                            self._command.get_configure().get('node.node_group.path')
                        ]
                    elif self._scheme == 'group':
                        self._command.get_configure().set(
                            'node.material_group.path', self._obj_opt.get_path()
                        )
                        self._command.get_configure().do_flatten()

                        self._command.create_node_groups()
                        self._command.create_inner_nodes()
                        self._command.create_textures()

                        layout_path = self._command.get_configure().get('node.node_group.path')
                        drop_paths = [
                            self._command.get_configure().get('node.node_group.path')
                        ]

                elif type_name == 'ShadingGroup':
                    self._command.get_configure().set(
                        'node.material_group.path', self._obj_opt.get_path()
                    )
                    self._command.get_configure().do_flatten()

                    self._command.create_node_groups()
                    self._command.create_inner_nodes()
                    self._command.create_textures()

                    layout_path = self._command.get_configure().get('node.node_group.path')
                    drop_paths = [
                        self._command.get_configure().get('node.node_group.path')
                    ]

            if layout_path is not None:
                timer = threading.Timer(.25, post_fnc_)
                timer.start()

    @classmethod
    def create_one(cls, obj_opt, texture_path):
        m = bsc_texture.TxrMethodForBuild.generate_instance()
        texture_arg = m.generate_one_texture_args(texture_path)
        if texture_arg:
            texture_name, texture_type, texture_path_ = texture_arg

            time_tag = bsc_core.TimeExtraMtd.generate_time_tag_36_(multiply=100)

            node_path = '{}/{}_{}__image__{}'.format(obj_opt.get_path(), texture_name, texture_type, time_tag)

            ktn_obj, is_create = ktn_core.NGNodeOpt._generate_shader_create_args(
                node_path, 'ArnoldShadingNode', 'image'
            )
            if is_create is True:
                obj_opt = ktn_core.NGNodeOpt(ktn_obj)
                obj_opt.set_shader_parameters_by_data(
                    {'filename': texture_path_}
                )
                ktn_core.GuiNodeGraphOpt.drop_nodes(
                    [ktn_obj]
                )
