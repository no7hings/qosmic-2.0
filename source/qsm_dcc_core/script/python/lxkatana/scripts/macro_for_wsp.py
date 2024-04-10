# coding:utf-8
import re

import collections

import six

import lxcontent.core as ctt_core

import lxresource as bsc_resource

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.dcc.core as bsc_dcc_core

import lxgui.core as gui_core
# katana
from ..core.wrap import *

from .. import core as ktn_core

from ..dcc import objects as ktn_dcc_objects


class ScpMacro(object):
    def __init__(self, file_path):
        self._file_path = file_path
        self._cfg = ctt_core.Content(value=self._file_path)
        self._cfg.set('option.unique_name', bsc_core.TimeExtraMtd.generate_time_tag_36_(multiply=100).lower())
        #
        color_hsv = self._cfg.get('option.color_hsv')
        if color_hsv:
            h, s, v = color_hsv['h'], color_hsv['s'], color_hsv['v']
            r, g, b = bsc_core.RawColorMtd.hsv2rgb(h, s, v, maximum=1.0)
            self._cfg.set(
                'option.color.r', r
            )
            self._cfg.set(
                'option.color.g', g
            )
            self._cfg.set(
                'option.color.b', b
            )
        #
        color_use_variant = self._cfg.get('option.color_use_variant', False)
        if color_use_variant is True:
            variant_key = self._cfg.get('option.variant_key')
            r, g, b = bsc_core.RawTextOpt(variant_key).to_rgb_(maximum=1.0, s_p=25, v_p=25)
            self._cfg.set(
                'option.color.r', r
            )
            self._cfg.set(
                'option.color.g', g
            )
            self._cfg.set(
                'option.color.b', b
            )
        #
        color_use_type = self._cfg.get('option.color_use_type', False)
        if color_use_type is True:
            variant_key = self._cfg.get('option.type')
            r, g, b = bsc_core.RawTextOpt(variant_key).to_rgb_(maximum=1.0, s_p=25, v_p=25)
            self._cfg.set(
                'option.color.r', r
            )
            self._cfg.set(
                'option.color.g', g
            )
            self._cfg.set(
                'option.color.b', b
            )
        #
        auto_color = self._cfg.get('option.auto_color', default_value=True)
        if auto_color is True:
            type_name = self._cfg.get('option.type')
            r, g, b = bsc_core.RawTextOpt(type_name).to_rgb_(maximum=1.0, s_p=25, v_p=25)
            self._cfg.set(
                'option.color.r', r
            )
            self._cfg.set(
                'option.color.g', g
            )
            self._cfg.set(
                'option.color.b', b
            )
        #
        self._cfg.do_flatten()

    # @ktn_core.Modifier.undo_debug_run
    def build(self):
        self.build_main()
        self.build_nodes()
        self.gui_layout()
        #
        self.update_records()
        self.add_nodes()

    def build_main(self):
        data = self._cfg.get_as_content('main')
        ktn_obj, is_create = self._build_node_(data)
        self._obj_opt = ktn_core.NGNodeOpt(ktn_obj)
        if is_create is False:
            clear_ports = data.get('clear_ports', default_value=True)
            if clear_ports is True:
                self._obj_opt.clear_ports(
                    data.get('clear_start')
                )
            #
            self._obj_opt.create_ports_by_data(
                data.get('ports') or {}
            )
            self._obj_opt.set_parameters_by_data(
                data.get('parameters') or {}
            )
        #
        if data.get('type') in ['Group']:
            clear_children = data.get('clear_children', default_value=True)
            if clear_children is True:
                self._obj_opt.clear_children()
        #
        self._extend_kwargs = {}
        record_p = self._obj_opt.get_port('record')
        if record_p is not None:
            main_path = self._obj_opt.get_path()
            for i in ktn_core.NGNodeOpt(record_p).get_children():
                i_p_opt = ktn_core.NGPortOpt(i)
                i_key = i_p_opt.get_name()
                i_name = i_p_opt.get()
                i_path = '{}/{}'.format(main_path, i_name)
                self._extend_kwargs[i_key] = i_path

    def build_nodes(self):
        if self._cfg.get_key_is_exists('node') is False:
            return
        c = self._cfg.get_as_content('node')
        for i_key in c.get_top_keys():
            i_data = c.get_as_content(i_key)
            self._build_node_(i_data)

    @classmethod
    def _build_node_(cls, data, extend_kwargs=None):
        type_name = data['type']
        path = data['path']
        force_update = data.get('force_update', False)
        ktn_obj, is_create = ktn_core.NGNodeOpt._generate_node_create_args(path, type_name)
        obj_opt = ktn_core.NGNodeOpt(ktn_obj)
        if is_create is True or force_update is True:
            if (not type_name.endswith('_Wsp')) and (not type_name.endswith('_Wsp_Usr')):
                obj_opt.set_color(bsc_core.RawTextOpt(type_name).to_rgb_(maximum=1.0, s_p=25, v_p=25))
            #
            obj_opt.create_input_ports_by_data(
                data.get('input_ports') or []
            )
            #
            obj_opt.create_output_ports_by_data(
                data.get('output_ports') or []
            )
            #
            obj_opt.create_ports_by_data(
                data.get('ports') or {}
            )
            #
            obj_opt.set_port_hints_by_data(
                data.get('port_hints') or {},
                extend_kwargs=extend_kwargs
            )
            obj_opt.set_capsules_by_data(
                data.get('capsules') or {},
                extend_kwargs=extend_kwargs
            )
            #
            obj_opt.set_parameters_by_data(
                data.get('parameters') or {}
            )
            #
            obj_opt.set_proxy_parameters_by_data(
                data.get('proxy_parameters') or {}
            )
            #
            if type_name in ['LiveGroup']:
                ktn_obj.reloadFromSource()
            #
            obj_opt.set_arnold_geometry_properties_by_data(
                data.get('arnold_geometry_properties') or {}
            )
            #
            obj_opt.set_expressions_by_data(
                data.get('expressions') or {},
                extend_kwargs=extend_kwargs
            )
            #
            obj_opt.create_proxy_ports_by_data(
                data.get('proxy_ports') or {},
                extend_kwargs=extend_kwargs
            )
            #
            obj_opt.set_expand_groups_by_data(
                data.get('expand_groups') or [],
                extend_kwargs=extend_kwargs
            )
            #
            ktn_core.NGNodeOpt._create_connections_by_data(
                data.get('connections') or [],
                extend_kwargs=extend_kwargs
            )

            ktn_core.NGNodeOpt._create_connections_by_data(
                data.get('force_connections') or [],
                extend_kwargs=extend_kwargs, auto_create_target=True
            )
            base_type_name = data.get('base_type', None)
            #
            if type_name in {'GroupStack', 'GroupMerge'} or base_type_name in {'GroupStack', 'GroupMerge'}:
                child_type_name = data.get('child.type')
                if child_type_name is None:
                    raise RuntimeError()
                ktn_obj.setChildNodeType(child_type_name)
                child_data = data.get('child.nodes') or {}
                if child_data:
                    child_path_pattern = data.get('child.path_pattern')
                    if child_path_pattern is None:
                        raise RuntimeError()
                    #
                    for i_key, i_data in child_data.items():
                        i_var = dict(
                            parent=path,
                            key=i_key
                        )
                        i_data['type'] = child_type_name
                        i_data['path'] = child_path_pattern.format(**i_var)
                        cls._build_node_child_(i_data)

            if type_name in {'NetworkMaterialCreate'} or base_type_name in {'NetworkMaterialCreate'}:
                node_graph_data = data.get('node_graph') or {}
                if node_graph_data:
                    for i_key, i_data in node_graph_data.items():
                        i_var = dict(
                            parent=path,
                            key=i_key
                        )
                        cls._build_node_node_graph_(i_data, i_var)
        #
        obj_opt.set_attributes(
            data.get('attributes') or {}
        )
        return ktn_obj, is_create

    @classmethod
    def _build_node_child_(cls, data, extend_kwargs=None):
        type_name = data['type']
        path = data['path']
        ktn_obj, is_create = ktn_core.NGNodeOpt._generate_group_child_create_args(path, type_name)
        if is_create is True:
            obj_opt = ktn_core.NGNodeOpt(ktn_obj)
            #
            obj_opt.set_color(bsc_core.RawTextOpt(type_name).to_rgb_(maximum=1.0, s_p=25, v_p=25))
            #
            obj_opt.set_attributes(
                data.get('attributes') or {}
            )
            #
            obj_opt.set_parameters_by_data(
                data.get('parameters') or {},
            )
            obj_opt.set_arnold_geometry_properties_by_data(
                data.get('arnold_geometry_properties') or {}
            )
            #
            obj_opt.set_expressions_by_data(
                data.get('expressions') or {},
                extend_kwargs=extend_kwargs
            )
            obj_opt.create_proxy_ports_by_data(
                data.get('proxy_ports') or {},
                extend_kwargs=extend_kwargs
            )

    @classmethod
    def _build_node_node_graph_(cls, data, extend_kwargs=None):
        type_name = data['type']
        shader_type_name = data.get('shader_type')
        path = data['path']
        ktn_obj, is_create = ktn_core.NGNodeOpt._generate_material_node_graph_create_args(path, type_name, shader_type_name)
        if is_create is True:
            obj_opt = ktn_core.NGNodeOpt(ktn_obj)
            #
            obj_opt.set_attributes(
                data.get('attributes') or {}
            )
            #
            obj_opt.set_parameters_by_data(
                data.get('parameters') or {},
            )
            obj_opt.set_arnold_geometry_properties_by_data(
                data.get('arnold_geometry_properties') or {}
            )
            #
            obj_opt.set_expressions_by_data(
                data.get('expressions') or {},
                extend_kwargs=extend_kwargs
            )
            ktn_core.NGNodeOpt._create_connections_by_data(
                data.get('connections') or [],
                extend_kwargs=extend_kwargs
            )

    def update_records(self):
        if self._cfg.get_key_is_exists('record_update') is False:
            return
        c = self._cfg.get_as_content('record_update')
        for i_key in c.get_top_keys():
            i_data = c.get_as_content(i_key)
            self._update_record_(i_key, i_data)

    def _update_record_(self, key, data, extend_kwargs=None):
        port_path = 'record.{}'.format(key)
        name = self._obj_opt.get(port_path)
        obj_opt = ktn_core.NGNodeOpt(name)
        obj_opt.create_input_ports_by_data(
            data.get('input_ports') or []
        )
        #
        obj_opt.create_output_ports_by_data(
            data.get('output_ports') or []
        )
        #
        obj_opt.create_ports_by_data(
            data.get('ports') or {}
        )
        obj_opt.set_port_hints_by_data(
            data.get('port_hints') or {},
            extend_kwargs=extend_kwargs
        )
        #
        obj_opt.set_parameters_by_data(
            data.get('parameters') or {}
        )
        obj_opt.set_expressions_by_data(
            data.get('expressions') or {},
            extend_kwargs=extend_kwargs
        )
        #
        ktn_core.NGNodeOpt._create_connections_by_data(
            data.get('connections') or []
        )
        #
        obj_opt.set_attributes(
            data.get('attributes') or {}
        )

    def add_nodes(self):
        if self._cfg.get_key_is_exists('node_add') is False:
            return
        c = self._cfg.get_as_content('node_add')
        for i_key in c.get_top_keys():
            i_data = c.get_as_content(i_key)
            self._build_node_(i_data, extend_kwargs=self._extend_kwargs)

    def gui_layout(self):
        layout_gui = self._cfg.get('option.layout_gui', default_value=True)
        if layout_gui is True:
            self._obj_opt.gui_layout_node_graph(size=(240, 40))

    def get_is_changed(self):
        yaml_file_opt = bsc_storage.StgFileOpt(self._file_path)
        yaml_timestamp = yaml_file_opt.get_modify_timestamp()
        macro_file_path = '{}.macro'.format(yaml_file_opt.path_base)
        macro_file_opt = bsc_storage.StgFileOpt(macro_file_path)
        macro_timestamp = macro_file_opt.get_modify_timestamp()
        return int(yaml_timestamp) != int(macro_timestamp)

    def save(self):
        import os

        yaml_file_opt = bsc_storage.StgFileOpt(self._file_path)
        macro_file_path = '{}.macro'.format(yaml_file_opt.path_base)
        macro_file_opt = bsc_storage.StgFileOpt(macro_file_path)
        if macro_file_opt.get_is_exists() is True:
            var_dict = dict(
                directory=macro_file_opt.get_directory_path(),
                name=macro_file_opt.get_name_base(),
                ext=macro_file_opt.get_ext(),
                time_tag=bsc_core.TimestampOpt(macro_file_opt.get_modify_timestamp()).get_as_tag()
            )
            bck_file_path = '{directory}/.bck/{name}{ext}/{name}.{time_tag}{ext}'.format(
                **var_dict
            )
            macro_file_opt.copy_to_file(bck_file_path)

        self._obj_opt.save_as_macro(
            macro_file_path
        )
        os.utime(macro_file_path, (yaml_file_opt.get_modify_timestamp(), yaml_file_opt.get_modify_timestamp()))

    @classmethod
    def set_warning_show(cls, label, contents):
        if contents:
            if ktn_core.KtnUtil.get_is_ui_mode():
                gui_core.GuiDialog.create(
                    label,
                    content=u'\n'.join(contents),
                    status=gui_core.GuiDialog.ValidationStatus.Warning,
                    #
                    yes_label='Close',
                    #
                    no_visible=False, cancel_visible=False
                )
            else:
                for i in contents:
                    bsc_log.Log.trace_method_warning(
                        label, i
                    )


class AbsWsp(object):
    PRESET_DICT = {}

    def __init__(self, ktn_obj):
        if isinstance(ktn_obj, six.string_types):
            self._ktn_obj = ktn_core.NodegraphAPI.GetNode(
                ktn_obj
            )
        else:
            self._ktn_obj = ktn_obj
        self._obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)

    @classmethod
    def get_rsv_project(cls):
        pass

    @classmethod
    def get_rsv_asset(cls):
        import lxresolver.core as rsv_core

        f = ktn_dcc_objects.Scene.get_current_file_path()

        if f:
            resolver = rsv_core.RsvBase.generate_root()
            rsv_task = resolver.get_rsv_task_by_any_file_path(f)
            if rsv_task is not None:
                rsv_asset = rsv_task.get_rsv_resource()
                return rsv_asset

    @classmethod
    def _get_rsv_resource_(cls, branch, rsv_asset_path):
        import lxresolver.core as rsv_core

        #
        _ = rsv_asset_path.split('/')
        project, _, resource = _[1:]
        resolver = rsv_core.RsvBase.generate_root()
        kwargs = {
            'project': project,
            branch: resource
        }
        return resolver.get_rsv_resource(**kwargs)

    def get_rsv_task(self):
        pass

    def load_preset(self):
        key = self._obj_opt.get('preset.name')
        c = ctt_core.Content(value=self.PRESET_DICT)
        self._obj_opt.set_parameters_by_data(
            c.get('{}.parameters'.format(key)) or {}
        )
        self._obj_opt.set_proxy_parameters_by_data(
            c.get('{}.proxy_parameters'.format(key)) or {}
        )

    def get_record(self, key):
        s = ktn_core.KtnStageOpt(
            self._ktn_obj
        )
        r = s.generate_obj_opt('/root')
        return r.get('lynxi.variants.{}'.format(key))

    def get(self, key):
        return self._obj_opt.get(key)

    def set(self, key, value):
        self._obj_opt.set(key, value)


class ScpWspVariantRegister(AbsWsp):
    def __init__(self, *args, **kwargs):
        super(ScpWspVariantRegister, self).__init__(*args, **kwargs)

    def _get_key_(self):
        return self._obj_opt.get('variableName')

    @classmethod
    def _get_variant_values_(cls, obj_opt):
        list_ = []
        ktn_port = obj_opt.get_port('patterns')
        for i in ktn_core.NGPortOpt(ktn_port).get_children():
            i_variant_key = ktn_core.NGPortOpt(i).get_name()
            i_value = ktn_core.NGPortOpt(i).get()
            if obj_opt.get_input_port(i_variant_key).getConnectedPorts():
                list_.append(i_value)
        return list_

    def get_variant_values(self):
        return self._get_variant_values_(self._obj_opt)

    def register_variable(self):
        key = self._get_key_()
        values = self.get_variant_values()
        if values:
            ktn_core.VariablesSetting().register(
                key, values
            )

    def register_one(self, variant, obj_opt):
        self._obj_opt.create_input_port(variant)
        self._obj_opt.connect_input_from(
            variant, (obj_opt.get_path(), None)
        )


class ScpWspVariantSet(AbsWsp):
    def __init__(self, *args, **kwargs):
        super(ScpWspVariantSet, self).__init__(*args, **kwargs)

    def _get_key_(self):
        return self._obj_opt.get('parameters.key')

    def _get_value_(self):
        return self._obj_opt.get('parameters.value')

    def clear_variant_keys(self):
        p = 'parameters.key'
        key_pre = self._obj_opt.get(
            p
        )
        self._obj_opt.set_capsule_strings(
            p, ['None']
        )
        return key_pre

    @ktn_core.Modifier.undo_run
    def load_variant_keys(self):
        self._obj_opt.set_capsule_strings(
            'parameters.key', ['None']
        )
        node_names = self._obj_opt.get_all_source_objs_(
            inner=True, type_includes=['VariableSwitch'],
            skip_base_type_names=['SuperTool']
        )
        list_ = []
        for i_node_name in node_names:
            i_obj_opt = ktn_core.NGNodeOpt(i_node_name)
            list_.append(i_obj_opt.get('variableName'))
        #
        list__ = list(set(list_))
        list__.sort(key=list_.index)
        if list__:
            self._obj_opt.set_capsule_strings(
                'parameters.key', list__
            )

    @ktn_core.Modifier.undo_run
    def load_variant_values(self):
        key = self._get_key_()
        self._obj_opt.set_capsule_strings(
            'parameters.value', ['None']
        )
        if key != 'None':
            node_names = self._obj_opt.get_all_source_objs_(
                inner=True, type_includes=['VariableSwitch'],
                skip_base_type_names=['SuperTool']
            )
            #
            list_ = []
            for i_node_name in node_names:
                i_obj_opt = ktn_core.NGNodeOpt(i_node_name)
                if i_obj_opt.get('variableName') == key:
                    i_values = ScpWspVariantRegister._get_variant_values_(i_obj_opt)
                    list_.extend(i_values)
            #
            list__ = list(set(list_))
            list__.sort(key=list_.index)
            if list__:
                self._obj_opt.set_capsule_strings(
                    'parameters.value', list__
                )


class ScpWspVariantResolve(AbsWsp):
    def __init__(self, *args, **kwargs):
        super(ScpWspVariantResolve, self).__init__(*args, **kwargs)

    def clear_all_variants(self):
        variant_dict_pre = {}
        c = 10
        keys_p = 'parameters.keys'
        self._obj_opt.set_capsule_strings(
            keys_p, ['None']
        )
        self._obj_opt.set(
            keys_p, 'None'
        )
        for i_index in range(c):
            i_variant_key_p = 'parameters.variant.key_{}'.format(i_index)
            i_variant_value_p = 'parameters.variant.value_{}'.format(i_index)
            i_variant_key = self._obj_opt.get(i_variant_key_p)
            if i_variant_key:
                i_variant_value_pre = self._obj_opt.get(i_variant_value_p)
                variant_dict_pre[i_variant_key] = i_variant_value_pre
            self._obj_opt.set(
                i_variant_key_p, ''
            )
            self._obj_opt.set_capsule_strings(
                i_variant_value_p, ['None']
            )
            self._obj_opt.set(
                i_variant_value_p, 'None'
            )
        return variant_dict_pre

    @ktn_core.Modifier.undo_run
    def resolve_all_variants(self):
        variant_dict_pre = self.clear_all_variants()
        node_names = self._obj_opt.get_all_source_objs_(
            inner=True, type_includes=['VariableSwitch'],
            skip_base_type_names=['SuperTool']
        )
        if node_names:
            condition_keys = []
            condition_capsule_data = []
            for i_index, i_node_name in enumerate(node_names):
                i_variant_key_p = 'parameters.variant.key_{}'.format(i_index)
                i_variant_value_p = 'parameters.variant.value_{}'.format(i_index)
                #
                i_obj_opt = ktn_core.NGNodeOpt(i_node_name)
                i_variant_key = i_obj_opt.get('variableName')
                i_variant_value_pre = None
                if i_variant_key in variant_dict_pre:
                    i_variant_value_pre = variant_dict_pre[i_variant_key]
                i_condition_key = 'variant_{}'.format(i_index)
                condition_capsule_data.append(
                    (i_condition_key, bsc_core.RawStrUnderlineOpt(i_variant_key).to_prettify(word_count_limit=12))
                )
                condition_keys.append(i_condition_key)
                self._obj_opt.set(
                    i_variant_key_p, i_variant_key
                )
                i_variant_values = ScpWspVariantRegister._get_variant_values_(i_obj_opt)
                self._obj_opt.set_capsule_strings(
                    i_variant_value_p, i_variant_values
                )
                if i_variant_value_pre is not None:
                    self._obj_opt.set(
                        i_variant_value_p, i_variant_value_pre
                    )
                else:
                    self._obj_opt.set(
                        i_variant_value_p, i_variant_values[0]
                    )

            self._obj_opt.set_capsule_data(
                'parameters.keys', condition_capsule_data
            )
            self._obj_opt.set(
                'parameters.keys', ', '.join(condition_keys)
            )

    def get_variants(self):
        dict_ = collections.OrderedDict()
        node_names = self._obj_opt.get_all_source_objs_(
            inner=True, type_includes=['VariableSwitch'],
            skip_base_type_names=['SuperTool']
        )
        if node_names:
            for i_index, i_node_name in enumerate(node_names):
                i_obj_opt = ktn_core.NGNodeOpt(i_node_name)
                i_variant_key = i_obj_opt.get('variableName')
                i_variant_values = ScpWspVariantRegister._get_variant_values_(i_obj_opt)
                dict_[i_variant_key] = i_variant_values

    def set_variants(self, variant_dict):
        pass


class ScpWspShaderChecker(AbsWsp):
    def __init__(self, *args, **kwargs):
        super(ScpWspShaderChecker, self).__init__(*args, **kwargs)

    def fit_to_camera(self):
        scale_percent = self._obj_opt.get(
            'extra.camera_fit.scale_percent'
        )
        margin_percent = self._obj_opt.get(
            'extra.camera_fit.margin_percent'
        )
        camera_fov = self._obj_opt.get(
            'extra.camera_fit.camera_fov'
        )
        camera_screen_mode = self._obj_opt.get(
            'extra.camera_fit.camera_screen_mode'
        )
        render_resolution = self._obj_opt.get(
            'extra.camera_fit.render_resolution'
        )
        r_w, r_h = ktn_core.ResolutionOpt(render_resolution).get()
        (t_x, t_y, t_z), (s_x, s_y, s_z) = bsc_core.CameraMtd.compute_project_transformation(
            1, scale_percent, margin_percent, camera_fov, camera_screen_mode, (r_w, r_h)
        )
        ass_opt = ktn_core.NGNodeOpt(
            self._obj_opt.get('record.ass')
        )
        ass_opt.set(
            'transform.translate', [t_x, t_y, t_z]
        )
        ass_opt.set(
            'transform.scale', [s_x, s_y, s_z]
        )


# geometry
# noinspection PyUnusedLocal
class ScpWspAssetGeometry(AbsWsp):
    def __init__(self, *args, **kwargs):
        super(ScpWspAssetGeometry, self).__init__(*args, **kwargs)

    @ktn_core.Modifier.undo_run
    def load_latest_usd(self):
        import lxusd.rsv.objects as usd_rsv_objects

        import lxresolver.core as rsv_core

        contents = []

        f = ktn_dcc_objects.Scene.get_current_file_path()

        self._obj_opt.set('parameters.usd.enable', 0)

        resolver = rsv_core.RsvBase.generate_root()
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(f)
        if rsv_scene_properties:
            rsv_project = resolver.get_rsv_project(
                project=rsv_scene_properties.get('project')
            )
            rsv_asset = rsv_project.get_rsv_resource(
                asset=rsv_scene_properties.get('asset')
            )
            asset_set_usd_file_path = usd_rsv_objects.RsvUsdAssetSetCreator._generate_asset_usd_file_path_as_latest(
                rsv_asset,
                rsv_scene_properties
            )
            if asset_set_usd_file_path:
                self._obj_opt.set(
                    'parameters.usd.file', asset_set_usd_file_path
                )

                self._obj_opt.set('parameters.usd.enable', 1)

                bsc_log.Log.trace_method_result(
                    'set usd create for asset',
                    'file="{}"'.format(asset_set_usd_file_path)
                )

                self.load_usd_variant()

                ktn_core.CacheManager.flush()
        else:
            contents.append(
                u'file={} is not not available'.format(f)
            )
        ScpMacro.set_warning_show(
            'camera load', contents
        )

    @ktn_core.Modifier.undo_run
    def create_new_usd(self):
        import lxusd.rsv.objects as usd_rsv_objects

        import lxresolver.core as rsv_core

        contents = []

        f = ktn_dcc_objects.Scene.get_current_file_path()

        self._obj_opt.set('parameters.usd.enable', 0)

        resolver = rsv_core.RsvBase.generate_root()
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(f)
        if rsv_scene_properties:
            rsv_project = resolver.get_rsv_project(
                project=rsv_scene_properties.get('project')
            )
            rsv_asset = rsv_project.get_rsv_resource(
                asset=rsv_scene_properties.get('asset')
            )
            asset_set_usd_file_path = usd_rsv_objects.RsvUsdAssetSetCreator._create_asset_usd_file(
                rsv_asset,
                rsv_scene_properties
            )
            if asset_set_usd_file_path:
                self._obj_opt.set(
                    'parameters.usd.file', asset_set_usd_file_path
                )

                self._obj_opt.set('parameters.usd.enable', 1)

                bsc_log.Log.trace_method_result(
                    'set usd create for asset',
                    'file="{}"'.format(asset_set_usd_file_path)
                )

                self.load_usd_variant()

                ktn_core.CacheManager.flush()
        else:
            contents.append(
                u'file={} is not not available'.format(f)
            )

        ScpMacro.set_warning_show(
            'asset load', contents
        )

    def _clear_all_components(self):
        variant_dict_pre = {}
        p = 'parameters.usd_variant.asset_version_main.component'
        if self._obj_opt.get_port_is_exists(p):
            c = 10
            keys_p = '{}.keys'.format(p)
            self._obj_opt.set_capsule_strings(
                keys_p, ['None']
            )
            self._obj_opt.set(
                keys_p, 'None'
            )
            for i_index in range(c):
                i_variant_key_p = '{}.key_{}'.format(p, i_index)
                i_variant_value_p = '{}.value_{}'.format(p, i_index)
                i_variant_key = self._obj_opt.get(i_variant_key_p)
                if i_variant_key:
                    i_variant_value_pre = self._obj_opt.get(i_variant_value_p)
                    variant_dict_pre[i_variant_key] = i_variant_value_pre
                self._obj_opt.set(
                    i_variant_key_p, ''
                )
                self._obj_opt.set_enumerate_strings(
                    i_variant_value_p, ['None']
                )
                self._obj_opt.set(
                    i_variant_value_p, 'None'
                )
        return variant_dict_pre

    def _load_all_components(self, variant_dict):
        p = 'parameters.usd_variant.asset_version_main.component'
        prefix = 'mod_var_'
        if self._obj_opt.get_port_is_exists(p):
            variant_dict_pre = self._clear_all_components()
            condition_keys = []
            condition_capsule_data = []
            for i_index, (i_k, i_v) in enumerate(variant_dict.items()):
                i_condition_key = 'variant_{}'.format(i_index)
                condition_capsule_data.append(
                    (i_condition_key, bsc_core.RawStrUnderlineOpt(i_k[len(prefix):]).to_prettify())
                )
                condition_keys.append(i_condition_key)

                i_variant_key_p = '{}.key_{}'.format(p, i_index)
                i_variant_value_p = '{}.value_{}'.format(p, i_index)

                self._obj_opt.set(
                    i_variant_key_p, i_k
                )
                i_default = i_v['default']
                i_values = i_v['values']
                self._obj_opt.set_enumerate_strings(
                    i_variant_value_p, i_values
                )
                self._obj_opt.set(
                    i_variant_value_p, i_default
                )

            self._obj_opt.set_capsule_data(
                '{}.keys'.format(p), condition_capsule_data
            )
            self._obj_opt.set(
                '{}.keys'.format(p), ', '.join(condition_keys)
            )

    def _load_usd_variant_fnc(self, file_key, variant_group_key, mode='main'):
        import lxusd.rsv.objects as usd_rsv_objects

        contents = []

        f = self._obj_opt.get(file_key)

        if f:
            asset_variant_dict = usd_rsv_objects.RsvUsdAssetSet.generate_asset_variant_dict(
                f, mode=mode
            )
            if asset_variant_dict:
                if mode == 'main':
                    self._obj_opt.set(
                        '{}.asset_version_main.enable'.format(variant_group_key), 1
                    )
                    self._obj_opt.set(
                        '{}.asset_version_override.enable'.format(variant_group_key), 0
                    )
                elif mode == 'override':
                    self._obj_opt.set(
                        '{}.asset_version_main.enable'.format(variant_group_key), 1
                    )
                    self._obj_opt.set(
                        '{}.asset_version_override.enable'.format(variant_group_key), 1
                    )

                for i_k, i_v in asset_variant_dict.iteritems():
                    for j_k, j_v in i_v.items():
                        i_p = '{}.{}.{}'.format(variant_group_key, i_k, j_k)
                        j_default = j_v['default']
                        j_values = j_v['values']
                        self._obj_opt.set_enumerate_strings(i_p, j_values)
                        self._obj_opt.set(i_p, j_default)
                # maybe node is old style, did not have this parameters
                if self._obj_opt.get_port_is_exists('{}.asset_version_main.component'.format(variant_group_key)) is True:
                    asset_component_variant_dict = usd_rsv_objects.RsvUsdAssetSet.generate_asset_components_variant_dict(
                        f
                    )
                    if asset_component_variant_dict:
                        self._load_all_components(asset_component_variant_dict)
                    else:
                        self._clear_all_components()
            else:
                contents.append(
                    u'file={} is not not available'.format(f)
                )
        else:
            contents.append(
                u'file={} is not not available'.format(f)
            )

        ScpMacro.set_warning_show(
            'asset load', contents
        )

    @ktn_core.Modifier.undo_run
    def load_usd_variant(self):
        mode = self._obj_opt.get('parameters.usd_variant.mode')
        self._load_usd_variant_fnc(
            'parameters.usd.file', 'parameters.usd_variant', mode=mode
        )

    def reset_usd_variant(self):
        pass

    def translate_to_center(self, above_axis_y=False):
        import lxusd.core as usd_core

        file_path = self._obj_opt.get('usd.file')
        if file_path:
            root = '/master'
            sub_locations = [
                '/master/hi',
                '/master/shape',
            ]
            s_opt = usd_core.UsdStageOpt(
                file_path
            )
            [s_opt.set_active_at(i, True) for i in sub_locations]
            g = s_opt.compute_geometry_args(root)
            (x, y, z), (c_x, c_y, c_z), (w, h, d) = g
            if above_axis_y is True:
                self._obj_opt.set(
                    'parameters.extra.translate.offset', [-c_x, -y, -c_z]
                )
            else:
                self._obj_opt.set(
                    'parameters.extra.translate.offset', [-c_x, -c_y, -c_z]
                )

    def layout_all_components(self):
        pass

    def layout_visible_components(self):
        pass


# noinspection PyUnusedLocal
class ScpComponentLayout(AbsWsp):
    def __init__(self, *args, **kwargs):
        super(ScpComponentLayout, self).__init__(*args, **kwargs)

    def generate_cache(self):
        force = True

        file_paths = ['test']
        cache_file_name = bsc_core.UuidMtd.generate_by_files(file_paths)
        cache_json_directory_path = bsc_storage.StgTmpBaseMtd.get_cache_directory('json-cache')
        cache_json_file_path = '{}/{}.json'.format(cache_json_directory_path, bsc_core.UuidMtd.generate_new())

        if bsc_storage.StgFileOpt(cache_json_file_path).get_is_exists() is False or force is True:
            paths = ktn_core.CEL(
                self._ktn_obj, self._obj_opt.get('CEL')
            ).parse()
            paths_leaf = bsc_core.PthNodeMtd.to_leaf_paths(paths)
            if paths_leaf:
                keys = []
                bboxes = []
                points = []
                xywh_array = []
                colors = []
                c_o = bsc_core.RawColorChoiceOpt()

                stage_opt = ktn_core.KtnStageOpt(self._ktn_obj)

                spacing = self._obj_opt.get('user.setting.spacing')

                move_to_floor = self._obj_opt.get('user.setting.move_to_floor')

                for i_path in paths_leaf:
                    i_g = stage_opt.compute_geometry_args(i_path)
                    (i_x, i_y, i_z), _, (i_w, i_h, i_d) = i_g
                    i_b = stage_opt.compute_bbox_args(i_path)
                    (i_b_x_0, i_b_y_0, i_b_z_0), (i_b_x_1, i_b_y_1, i_b_z_1) = i_b
                    keys.append(i_path)
                    bboxes.append((i_b_x_0, i_b_x_1, i_b_y_0, i_b_y_1, i_b_z_0, i_b_z_1))
                    points.append((i_x, i_y, i_z))
                    xywh_array.append((0, 0, i_w, i_d))
                    i_rgb = c_o.generate(maximum=1.0)
                    colors.append(i_rgb)

                if xywh_array:
                    dict_ = {}
                    l_opt = bsc_core.RectLayoutOpt(xywh_array, spacing=spacing)
                    rects = l_opt.generate()
                    layout_rect = l_opt.layout_rect
                    layout_rect_exact = layout_rect.exact_rect
                    center = layout_rect_exact.center
                    for i_rect in rects:
                        i_index = i_rect.index
                        i_key = keys[i_index]
                        i_bbox = bboxes[i_index]
                        i_point = points[i_index]
                        i_c_x, i_c_y, i_c_z = i_point
                        i_rgb = colors[i_index]
                        i_x, i_y, i_z = i_rect.x-i_c_x-center.x, 0, i_rect.y-i_c_z-center.y
                        if move_to_floor:
                            i_y = -i_c_y

                        dict_[i_key] = [(i_x, i_y, i_z), i_bbox, i_rgb]

                    bsc_storage.StgFileOpt(cache_json_file_path).set_write(dict_)

            self._obj_opt.set('user.cache.json', cache_json_file_path)

            CacheManager.flush()


class ScpWspGeometry(AbsWsp):
    CFG_YAML = bsc_resource.RscExtendConfigure.get_yaml(
        'katana/script/macro/geometry'
    )

    def __init__(self, *args, **kwargs):
        super(ScpWspGeometry, self).__init__(*args, **kwargs)
        self._cfg = ctt_core.Content(value=self.CFG_YAML)
        self.PRESET_DICT = self._cfg.get('preset')


class ScpWspGeometrySpace(AbsWsp):
    class Records(object):
        variant_register = 'record.variant_register'

    class Keys(object):
        node_name = 'record.variant_register'
        #
        default_name = 'extra.default_name'
        customize_name = 'extra.customize_name'

    def __init__(self, *args, **kwargs):
        super(ScpWspGeometrySpace, self).__init__(*args, **kwargs)

    def add_default(self):
        pass

    def add_customize(self):
        pass

    def _add_(self, key):
        pass

    def register_variable(self):
        node_name = self._obj_opt.get(
            self.Records.variant_register
        )
        ScpWspVariantRegister(node_name).register_variable()


class ScpWspUtilityCamera(AbsWsp):
    def __init__(self, *args, **kwargs):
        super(ScpWspUtilityCamera, self).__init__(*args, **kwargs)

    def refresh_abc(self):
        sg_opt = ktn_core.KtnStageOpt(
            self._obj_opt.ktn_obj
        )
        location = self._obj_opt.get('option.location')
        element = self._obj_opt.get('parameters.setting.abc.element')
        _ = sg_opt.get_all_paths_at(
            '{}/abc'.format(location), type_includes=['camera']
        )
        if _:
            self._obj_opt.set_enumerate_strings(
                'parameters.setting.abc.element', _
            )
            if element in _:
                self._obj_opt.set('parameters.setting.abc.element', element)
        else:
            self._obj_opt.set_enumerate_strings(
                'parameters.setting.abc.element', ['None']
            )


# camera
class ScpWspAssetCamera(AbsWsp):
    def __init__(self, *args, **kwargs):
        super(ScpWspAssetCamera, self).__init__(*args, **kwargs)

    def load_latest_abc(self):
        self.load_all_abc()

    def load_all_abc(self):
        import lxresolver.core as rsv_core

        contents = []

        f = ktn_dcc_objects.Scene.get_current_file_path()
        if f:
            resolver = rsv_core.RsvBase.generate_root()
            rsv_task = resolver.get_rsv_task_by_any_file_path(f)
            if rsv_task is not None:
                rsv_entity = rsv_task.get_rsv_resource()
                rsv_camera_task = rsv_entity.get_rsv_task(
                    step='cam',
                    task='camera'
                )
                if rsv_camera_task is not None:
                    rsv_unit = rsv_camera_task.get_rsv_unit(
                        keyword='asset-camera-main-abc-file'
                    )
                    file_paths = rsv_unit.get_result(version='all')
                    if file_paths:
                        self._obj_opt.set_enumerate_strings(
                            'parameters.setting.abc.file',
                            file_paths
                        )
                        self._obj_opt.set(
                            'parameters.setting.abc.file',
                            file_paths[-1]
                        )
                else:
                    contents.append(
                        u'asset="{}" camera task is non-exists'.format(rsv_entity.path)
                    )
            else:
                contents.append(
                    u'file={} is not not available'.format(f)
                )
        else:
            contents.append(
                u'file={} is not not available'.format(f)
            )

        ScpMacro.set_warning_show(
            'camera load', contents
        )

    def refresh_abc(self):
        sg_opt = ktn_core.KtnStageOpt(
            self._obj_opt.ktn_obj
        )
        location = self._obj_opt.get('option.location')
        element = self._obj_opt.get('parameters.setting.abc.element')
        _ = sg_opt.get_all_paths_at(
            '{}/abc'.format(location), type_includes=['camera']
        )
        if _:
            self._obj_opt.set_enumerate_strings(
                'parameters.setting.abc.element', _
            )
            if element in _:
                self._obj_opt.set('parameters.setting.abc.element', element)
        else:
            self._obj_opt.set_enumerate_strings(
                'parameters.setting.abc.element', ['None']
            )


class ScpWspCamera(AbsWsp):
    PRESET_DICT = {
        'test_0': {
            'cache/asset_abc/enable': True,
            'cache/asset_abc/file': '/l/prod/cgm/publish/assets/chr/nn_4y/cam/camera/nn_4y.cam.camera.v001/camera/abc/main.abc',
            'cache/asset_abc/copy_from': '/root/world/cam/cam_fullbody/cam_fullbodyShape'
        }
    }

    def __init__(self, *args, **kwargs):
        super(ScpWspCamera, self).__init__(*args, **kwargs)


class ScpWspSpace(AbsWsp):
    class Records(object):
        variant_register = 'record.variant_register'

    #
    def __init__(self, *args, **kwargs):
        super(ScpWspSpace, self).__init__(*args, **kwargs)

    def add_default(self):
        pass

    def add_customize(self):
        pass

    def _add_(self, key):
        pass

    def register_variable(self):
        obj_name = self._obj_opt.get(
            self.Records.variant_register
        )
        ScpWspVariantRegister(obj_name).register_variable()
        ktn_core.NGNodeOpt(obj_name).execute_port('variant.register')

    def get_variant_values(self):
        n = self._obj_opt.get('record.variant_register')
        return ScpWspVariantRegister(n).get_variant_values()


class ScpWspCameraSpace(AbsWsp):
    class Records(object):
        variant_register = 'record.variant_register'

    class Keys(object):
        #
        default_name = 'extra.default_name'
        customize_name = 'extra.customize_name'

    def __init__(self, *args, **kwargs):
        super(ScpWspCameraSpace, self).__init__(*args, **kwargs)

    def add_default(self):
        pass

    def add_customize(self):
        pass

    def _add_(self, key):
        pass

    def register_variable(self):
        node_name = self._obj_opt.get(
            self.Records.variant_register
        )
        ScpWspVariantRegister(node_name).register_variable()


# look
class AbsSpcWspLookGroup(AbsWsp):
    def __init__(self, *args, **kwargs):
        super(AbsSpcWspLookGroup, self).__init__(*args, **kwargs)

    @ktn_core.Modifier.undo_run
    def load_latest_ass_file(self):
        import lxresolver.core as rsv_core

        import lxresolver.scripts as rsv_scripts

        env_data = rsv_scripts.ScpEnvironment.get_as_dict()

        resolver = rsv_core.RsvBase.generate_root()

        rsv_task = resolver.get_rsv_task(
            **env_data
        )
        if rsv_task is not None:
            version_cur = env_data.get('version') or None
            workspace_key = env_data.get('workspace_key')
            if workspace_key in {resolver.WorkspaceKeys.Source, resolver.WorkspaceKeys.User}:
                keyword = 'asset-source-look-ass-file'
                version = 'latest'
            elif workspace_key in {resolver.WorkspaceKeys.Release}:
                keyword = 'asset-look-ass-file'
                version = version_cur
            elif workspace_key in {resolver.WorkspaceKeys.Temporary}:
                keyword = 'asset-temporary-look-ass-file'
                version = version_cur
            else:
                raise RuntimeError()

            rsv_unit = rsv_task.get_rsv_unit(
                keyword=keyword
            )
            result = rsv_unit.get_result(version=version)
            if result:
                self._obj_opt.set(
                    'user.parameters.ass.file', result
                )


class SpcWspMaterialGroup(AbsSpcWspLookGroup):
    def __init__(self, *args, **kwargs):
        super(SpcWspMaterialGroup, self).__init__(*args, **kwargs)

    def build_from_ass_file(self):
        from . import look as ktn_scp_look

        f = self._obj_opt.get('user.parameters.ass.file')
        if f:
            ktn_scp_look.ScpLookMaterialImport(
                self._obj_opt
            ).import_from_ass_file(
                f
            )


class SpcWspMaterialAssignGroup(AbsSpcWspLookGroup):
    def __init__(self, *args, **kwargs):
        super(SpcWspMaterialAssignGroup, self).__init__(*args, **kwargs)

    def build_from_ass_file(self):
        from . import look as ktn_scp_look

        f = self._obj_opt.get('user.parameters.ass.file')
        if f:
            ktn_scp_look.ScpLookMaterialAssignImport(
                self._obj_opt
            ).import_from_ass_file(
                f
            )


class SpcWspGeometryPropertiesAssignGroup(AbsSpcWspLookGroup):
    def __init__(self, *args, **kwargs):
        super(SpcWspGeometryPropertiesAssignGroup, self).__init__(*args, **kwargs)

    def build_from_ass_file(self):
        from . import look as ktn_scp_look

        f = self._obj_opt.get('user.parameters.ass.file')
        if f:
            ktn_scp_look.ScpLookGeometryPropertiesAssignImport(
                self._obj_opt
            ).import_from_ass_file(
                f
            )


class ScpWspLookSpace(AbsWsp):
    class Records(object):
        variant_register = 'record.variant_register'

        #
        default_name = 'extra.default_name'
        customize_name = 'extra.customize_name'

    def __init__(self, *args, **kwargs):
        super(ScpWspLookSpace, self).__init__(*args, **kwargs)

    def add_default(self):
        pass

    def add_customize(self):
        pass

    def _add_(self, key):
        pass

    def register_variable(self):
        node_name = self._obj_opt.get(
            self.Records.variant_register
        )
        ScpWspVariantRegister(node_name).register_variable()


# light
class ScpWspAssetLightRig(AbsWsp):
    def __init__(self, *args, **kwargs):
        super(ScpWspAssetLightRig, self).__init__(*args, **kwargs)

    @classmethod
    def _get_light_args_(cls, project):
        import lxbasic.extra.methods as bsc_etr_methods

        import lxresolver.core as rsv_core

        import lxshotgun.rsv.scripts as stg_rsv_scripts

        if project == 'current':
            project = bsc_etr_methods.EtrBase.get_project()
        elif project == 'default':
            project = 'cgm'
        #
        resolver = rsv_core.RsvBase.generate_root()
        #
        rsv_project = resolver.get_rsv_project(project=project)
        if rsv_project is None:
            return
        #
        defaults, currents = stg_rsv_scripts.RsvStgProjectOpt(
            rsv_project
        ).get_light_args()
        return ['/{}/{}'.format(project, i) for i in defaults], ['/{}/{}'.format(project, i) for i in currents]

    def guess_option(self):
        pass

    def load_resource(self, project='default'):
        args = self._get_light_args_(project)
        if args:
            defaults, currents = args
            #
            key_1 = 'parameters.resource.name'
            name_pre = self._obj_opt.get(key_1)
            if currents:
                self._obj_opt.set_enumerate_strings(key_1, currents)
                if name_pre != 'None':
                    self._obj_opt.set(key_1, name_pre)
                else:
                    if defaults:
                        self._obj_opt.set(key_1, defaults[0])
            else:
                self._obj_opt.set_enumerate_strings(
                    key_1, ['None']
                )

    def _get_live_group_results_(self):
        import lxresolver.core as rsv_core

        name = self._obj_opt.get('parameters.resource.name')
        if name == 'None':
            return
        #
        project, asset = name.split('/')[1:]
        #
        resolver = rsv_core.RsvBase.generate_root()
        #
        rsv_project = resolver.get_rsv_project(project=project)
        if rsv_project is None:
            return
        #
        properties = rsv_project.properties
        role = properties.get('roles.light_rig')
        step = properties.get('asset_steps.light_rig')
        task = properties.get('asset_tasks.light_rig')
        rsv_task = rsv_project.get_rsv_task(
            role=role, asset=asset, step=step, task=task
        )
        if rsv_task is None:
            return
        #
        rsv_unit = rsv_task.get_rsv_unit(
            keyword='asset-live_group-file'
        )
        if rsv_unit is None:
            return
        #
        return rsv_unit.get_result(
            version='all'
        )

    def load_latest_light_rig(self):
        self.load_all_light_rig()

    def load_all_light_rig(self):
        results = self._get_live_group_results_()
        if results:
            key = 'parameters.live_group.file'
            file_path = results[-1]
            self._obj_opt.set_enumerate_strings(
                key, results
            )
            self._obj_opt.set(
                key, file_path
            )
            self.reload_live_group()

    def reload_live_group(self, ):
        file_path = self._obj_opt.get('parameters.live_group.file')
        name = self._obj_opt.get('record.live_group')
        obj_opt = ktn_core.NGNodeOpt(
            name
        )
        obj_opt.set(
            'source', file_path
        )
        obj_opt.get_ktn_obj().reloadFromSource()


# noinspection PyUnusedLocal,PyMethodMayBeStatic
class ScpWspWorkspace(AbsWsp):
    CFG_YAML = bsc_resource.RscExtendConfigure.get_yaml(
        'katana/script/macro/workspace'
    )

    def __init__(self, *args, **kwargs):
        super(ScpWspWorkspace, self).__init__(*args, **kwargs)
        self._cfg = ctt_core.Content(value=self.CFG_YAML)

        self._cfg.set(
            'option.path', self._obj_opt.get_path(),
        )
        self._cfg.set(
            'option.root', self._obj_opt.get_parent_opt().get_path(),
        )
        exists_time_tag = self._obj_opt.get('workspace.time_tag')
        if not exists_time_tag:
            exists_time_tag = bsc_core.TimeExtraMtd.generate_time_tag_36_(multiply=100)
            self._obj_opt.set('workspace.time_tag', exists_time_tag)
        #
        self._cfg.set(
            'option.time_tag', exists_time_tag
        )
        x, y = self._obj_opt.get_position()
        self._cfg.set(
            'option.position.x', x
        )
        self._cfg.set(
            'option.position.y', y
        )
        self._cfg.do_flatten()

        self.PRESET_DICT = self._cfg.get('preset')

    def guess_option(self):
        pass

    def register_all_variable(self):
        keys = self._obj_opt.get('workspace.keys')
        valid_keys = keys.split(', ')
        for i_key in valid_keys:
            i_record = self.get_record(
                '{}.space'.format(i_key)
            )
            if i_record is not None:
                ktn_core.NGNodeOpt(i_record).execute_port('variant.register')

    @ktn_core.Modifier.undo_run
    def build(self):
        keys = self._obj_opt.get('workspace.keys')
        valid_keys = keys.split(', ')
        c = len(valid_keys)
        x, y = self._obj_opt.get_position()
        w_s, h_s = self._cfg.get('option.size.w_s'), self._cfg.get('option.size.h_s')
        self._record_dict = dict(
            workspace=self._obj_opt.get_name()
        )
        if valid_keys:
            for i_index, i_key in enumerate(valid_keys):
                i_scheme = self._obj_opt.get('workspace.spaces.{}'.format(i_key))
                i_cfg_key = 'build.{}.{}'.format(i_key, i_scheme)
                if self._cfg.get_key_is_exists(i_cfg_key):
                    i_data = self._cfg.get_as_content(i_cfg_key)
                    i_record = self.get_record('{}.space'.format(i_key))
                    if not i_record:
                        i_main_data = i_data.get_as_content('main')
                        i_obj_opt = self._build_main_(i_key, i_main_data)
                        i_node_data = i_data.get('node') or {}
                        self._build_nodes_(i_node_data)
                    else:
                        i_obj_opt = ktn_core.NGNodeOpt(i_record)
                    #
                    self._record_dict[i_key] = i_obj_opt.get_name()
                    #
                    i_index_y = c-i_index

                    i_attributes = dict(
                        y=y+h_s*i_index_y
                    )
                    i_obj_opt.set_attributes(
                        i_attributes
                    )
        #
        connections = []
        for i_index, i_key_src in enumerate(valid_keys):
            i_obj_name_src = self._record_dict[i_key_src]
            i_obj_opt_src = ktn_core.NGNodeOpt(i_obj_name_src)
            i_src = '{}.{}'.format(i_obj_name_src, i_obj_opt_src.get_output_port_names()[0])
            if i_index == c-1:
                i_obj_key_tgt = 'workspace'
            else:
                i_obj_key_tgt = valid_keys[i_index+1]
            i_obj_name_tgt = self._record_dict[i_obj_key_tgt]
            i_obj_opt_tgt = ktn_core.NGNodeOpt(i_obj_name_tgt)
            i_output_names = i_obj_opt_tgt.get_input_port_names()
            if 'join_upstream' in i_output_names:
                i_output_name = 'join_upstream'
            else:
                i_output_name = i_output_names[0]
            i_tgt = '{}.{}'.format(i_obj_name_tgt, i_output_name)
            connections.extend(
                [i_src, i_tgt]
            )

        for i_index, i_key in enumerate(valid_keys):
            i_scheme = self._obj_opt.get('workspace.spaces.{}'.format(i_key))
            i_cfg_key = 'build.{}.{}'.format(i_key, i_scheme)
            i_data = self._cfg.get_as_content(i_cfg_key)
            main_post_connections = i_data.get('main.post_connections')
            if main_post_connections:
                connections.extend(main_post_connections)

        ktn_core.NGNodeOpt._create_connections_by_data(connections, extend_kwargs=self._record_dict)

        # self._create_nodes_()

    def _build_main_(self, key, data):
        ktn_obj, is_create = ScpMacro._build_node_(data)
        obj_opt = ktn_core.NGNodeOpt(ktn_obj)
        if is_create is True:
            self._obj_opt.set_expression(
                'record.{}'.format(key),
                'getNode(\'{}\').getNodeName()'.format(
                    obj_opt.get_name()
                )
            )
        return obj_opt

    def _build_nodes_(self, data):
        for k, v in data.items():
            pass
            # print k, v
            ktn_obj, is_create = ScpMacro._build_node_(v)

    def _create_nodes_(self, key, data):
        pass


class ScpWspRenderLayer(AbsWsp):
    def __init__(self, *args, **kwargs):
        super(ScpWspRenderLayer, self).__init__(*args, **kwargs)

    def load_all_variant_value(self):
        keys = self._obj_opt.get('variant.keys')
        valid_keys = keys.split(', ')
        for i_key in valid_keys:
            i_record = self.get_record(
                '{}.space'.format(i_key)
            )
            if i_record is not None:
                i_port_path = 'variant.{}'.format(i_key)
                i_values = ScpWspSpace(i_record).get_variant_values()
                i_value = self._obj_opt.get(i_port_path)
                self._obj_opt.set_capsule_strings(
                    i_port_path, i_values
                )
                if i_value in i_values:
                    self._obj_opt.set(i_port_path, i_value)

    def get_variants(self):
        dict_ = {}
        name = self._obj_opt.get(
            'record.render_properties'
        )
        if ktn_core.NGNodeOpt._get_is_exists_(name) is True:
            obj_opt = ktn_core.NGNodeOpt(name)
            v = obj_opt.get('user.output.variants')
            if v:
                for i in v.split('\n'):
                    i_k, i_v = i.split('=')[:2]
                    i_r = re.findall(re.compile(r'\$(.*)', re.S), i_v)
                    if i_r:
                        i_v = bsc_core.EnvBaseMtd.get(i_r[0])
                    dict_[i_k] = i_v
        return dict_


class ScpAssetAssExport(AbsWsp):
    RENDER_MODE = 'previewRender'

    def __init__(self, *args, **kwargs):
        super(ScpAssetAssExport, self).__init__(*args, **kwargs)

    @classmethod
    def _get_input_dynamic_usd_file_(cls, rsv_asset):
        rsv_task = rsv_asset.get_rsv_task(
            step='mod', task='mod_dynamic'
        )
        if rsv_task is not None:
            keyword = 'asset-geometry-usd-var-file'
            usd_file_rsv_unit = rsv_task.get_rsv_unit(
                keyword=keyword
            )
            return usd_file_rsv_unit.get_exists_result(
                version='latest', variants_extend=dict(var='hi')
            )

    @classmethod
    def _get_output_ass_file_(cls, rsv_scene_properties, rsv_task, look_pass_name):
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        if workspace in [rsv_scene_properties.get('workspaces.user'), rsv_scene_properties.get('workspaces.source')]:
            keyword = 'asset-source-look-ass-dir'
            rsv_unit = rsv_task.get_rsv_unit(keyword=keyword)
            new_version = rsv_unit.get_new_version()
            version = new_version
            #
            keyword_0 = 'asset-source-look-ass-file'
            keyword_1 = 'asset-source-look-ass-sub-file'
        elif workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-look-ass-file'
            keyword_1 = 'asset-look-ass-sub-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-look-ass-file'
            keyword_1 = 'asset-temporary-look-ass-sub-file'
        else:
            raise TypeError()
        #
        if look_pass_name == 'default':
            look_ass_file_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_0)
            look_ass_file_path = look_ass_file_rsv_unit.get_result(
                version=version
            )
        else:
            look_ass_file_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_1)
            look_ass_file_path = look_ass_file_rsv_unit.get_result(
                version=version,
                variants_extend=dict(look_pass=look_pass_name)
            )
        return look_ass_file_path

    @ktn_core.Modifier.undo_run
    def set_guess(self):
        import lxusd.core as usd_core

        import lxresolver.core as rsv_core

        contents = []

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)

        any_scene_file_path = ktn_dcc_objects.Scene.get_current_file_path()
        resolver = rsv_core.RsvBase.generate_root()
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
        if rsv_scene_properties:
            rsv_task = resolver.get_rsv_task(**rsv_scene_properties.value)

            input_dynamic_usd_file_path = self._get_input_dynamic_usd_file_(
                rsv_task.get_rsv_resource()
            )
            if input_dynamic_usd_file_path is not None:
                guess_frame_range = usd_core.UsdStageOpt(
                    input_dynamic_usd_file_path
                ).get_frame_range()
                #
                obj_opt.set(
                    'parameters.mode', 'dynamic'
                )
                obj_opt.set(
                    'parameters.start_frame', guess_frame_range[0]
                )
                obj_opt.set(
                    'parameters.end_frame', guess_frame_range[1]
                )
                obj_opt.set('parameters.dynamic.input_usd_file', input_dynamic_usd_file_path)
            else:
                obj_opt.set(
                    'parameters.mode', 'static'
                )
            #
            look_pass_name = obj_opt.get('parameters.look_pass')
            #
            mode = obj_opt.get('parameters.mode')
            #
            output_ass_file_path = self._get_output_ass_file_(
                rsv_scene_properties, rsv_task, look_pass_name
            )
            if mode == 'static':
                obj_opt.set_expression_enable('parameters.ass.file', False)
                obj_opt.set(
                    'parameters.ass.file', output_ass_file_path
                )
            elif mode == 'dynamic':
                output_ass_file = bsc_storage.StgFileOpt(output_ass_file_path)
                path_base = output_ass_file.path_base
                ext = output_ass_file.ext
                file_path = '{}.####{}'.format(path_base, ext)
                obj_opt.set(
                    'parameters.ass.file', file_path
                )
        else:
            contents.append(
                'current scene is not available'
            )

    def set_ass_export(self):
        # noinspection PyUnresolvedReferences
        from UI4 import Manifest

        obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)
        #
        mode = obj_opt.get('parameters.mode')
        look_pass_name = obj_opt.get('parameters.look_pass')
        camera_path = obj_opt.get('option.camera_path')
        ass_file_path = obj_opt.get('parameters.ass.file')
        if not ass_file_path:
            return
        #
        bsc_storage.StgFileOpt(ass_file_path).create_directory()
        #
        rss = RenderManager.RenderingSettings()
        rss.ignoreROI = True
        rss.asynch = False
        rss.interactiveOutputs = True
        rss.interactiveMode = True
        #
        if not ktn_core.KtnUtil.get_is_ui_mode():
            # noinspection PyUnresolvedReferences
            from UI4.Manifest import Nodes2DAPI
            Nodes2DAPI.CreateExternalRenderListener(15900)
        #
        if mode == 'static':
            rss.frame = ktn_core.NGNodeOpt(
                NodegraphAPI.GetRootNode()
            ).get('currentTime')
            RenderManager.StartRender(
                self.RENDER_MODE,
                node=self._ktn_obj,
                views=[camera_path],
                settings=rss
            )
        elif mode == 'dynamic':
            stat_frame, end_frame = obj_opt.get('parameters.start_frame'), obj_opt.get('parameters.end_frame')
            if stat_frame != end_frame:
                frames = range(int(stat_frame), int(end_frame)+1)
                with bsc_log.LogProcessContext.create_as_bar(maximum=len(frames), label='ass sequence export') as l_p:
                    for i_frame in frames:
                        ktn_core.NGNodeOpt(
                            NodegraphAPI.GetRootNode()
                        ).set('currentTime', i_frame)
                        rss.frame = i_frame
                        RenderManager.StartRender(
                            self.RENDER_MODE,
                            node=self._ktn_obj,
                            views=[camera_path],
                            settings=rss
                        )
                        l_p.do_update()
                        bsc_log.Log.trace_method_result(
                            'ass sequence export',
                            'look-pass="{}", frame="{}"'.format(look_pass_name, i_frame)
                        )


class ScpInstanceColorMap(object):
    def __init__(self, ktn_obj):
        if isinstance(ktn_obj, six.string_types):
            self._ktn_obj = ktn_core.NodegraphAPI.GetNode(
                ktn_obj
            )
        else:
            self._ktn_obj = ktn_obj
        self._obj_opt = ktn_core.NGNodeOpt(self._ktn_obj)

    def get_location(self):
        return self._obj_opt.get('parameters.setting.location')

    def get_grow_usd_file_path(self):
        return self._obj_opt.get('parameters.grow.usd')

    def get_instance_usd_file_path(self):
        return self._obj_opt.get('parameters.instance.usd')

    def get_grow_image_file_path(self):
        return self._obj_opt.get('parameters.grow.image')

    def get_grow_map_name(self):
        return self._obj_opt.get('parameters.grow.uv_map_name')

    def get_grow_op(self):
        return self._obj_opt.get('parameters.op.grow')

    def generate_grow_cache(self):
        self._obj_opt.set('parameters.grow.preview', False)
        force = bool(self._obj_opt.get('parameters.grow.force'))

        grow_usd_file_path = self.get_grow_usd_file_path()
        image_file_path = self.get_grow_image_file_path()
        uv_map_name = self.get_grow_map_name()
        cache_file_name = bsc_core.UuidMtd.generate_by_files(
            [grow_usd_file_path]+bsc_storage.StgTextureMtd.get_unit_paths(image_file_path),
            [uv_map_name]
        )
        cache_usd_directory_path = bsc_storage.StgTmpBaseMtd.get_cache_directory('usd-cache')
        cache_usd_file_path = '{}/{}.usd'.format(cache_usd_directory_path, cache_file_name)
        self._obj_opt.set('parameters.grow.cache.usd', cache_usd_file_path)
        if bsc_storage.StgPathMtd.get_is_exists(cache_usd_file_path) is False or force is True:
            import lxgui.proxy.widgets as prx_widgets

            w = prx_widgets.PrxProcessingWindow()
            w.set_window_title('Generator Grow Cache')
            w.set_window_show(exclusive=False)

            w.start(
                bsc_dcc_core.PythonProcess.generate_command(
                    'method=generator-grow-cache&grow_usd={}&image={}&uv_map_name={}&cache_usd={}'.format(
                        grow_usd_file_path, image_file_path, uv_map_name, cache_usd_file_path
                    )
                )
            )

    def generate_instance_cache(self):
        self._obj_opt.set('parameters.instance.preview', False)
        force = bool(self._obj_opt.get('parameters.instance.force'))

        grow_usd_file_path = self.get_grow_usd_file_path()
        instance_usd_file_path = self.get_instance_usd_file_path()
        image_file_path = self.get_grow_image_file_path()
        uv_map_name = self.get_grow_map_name()
        cache_file_name = bsc_core.UuidMtd.generate_by_files(
            [grow_usd_file_path, instance_usd_file_path]+bsc_storage.StgTextureMtd.get_unit_paths(image_file_path),
            [uv_map_name]
        )
        cache_usd_directory_path = bsc_storage.StgTmpBaseMtd.get_cache_directory('usd-cache')
        cache_usd_file_path = '{}/{}.usd'.format(cache_usd_directory_path, cache_file_name)
        self._obj_opt.set('parameters.instance.cache.usd', cache_usd_file_path)
        cache_json_directory_path = bsc_storage.StgTmpBaseMtd.get_cache_directory('json-cache')
        cache_json_file_path = '{}/{}.json'.format(cache_json_directory_path, cache_file_name)
        self._obj_opt.set('parameters.instance.cache.json', cache_json_file_path)
        if bsc_storage.StgPathMtd.get_is_exists(cache_usd_file_path) is False or force is True:
            import lxgui.proxy.widgets as prx_widgets

            w = prx_widgets.PrxProcessingWindow()
            w.set_window_title('Generator Instance Cache')
            w.set_window_show(exclusive=False)

            w.start(
                bsc_dcc_core.PythonProcess.generate_command(
                    (
                        'method=generator-instance-cache'
                        '&grow_usd={}&instance_usd={}&image={}&uv_map_name={}&cache_usd={}&cache_json={}'
                    ).format(
                        grow_usd_file_path, instance_usd_file_path, image_file_path, uv_map_name,
                        cache_usd_file_path, cache_json_file_path
                    )
                )
            )
