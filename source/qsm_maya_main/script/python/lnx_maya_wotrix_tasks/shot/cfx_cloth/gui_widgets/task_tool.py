# coding:utf-8
import functools

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from lnx_wotrix.gui.abstracts import unit_for_task_tool as _abs_unit_for_task_tool

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import qsm_general.prc_task as qsm_gnl_prc_task

import qsm_maya.core as qsm_mya_core

import qsm_maya.preset as qsm_mya_preset

import qsm_maya.handles.animation.core as qsm_mya_hdl_anm_core

from ....asset.cfx_rig import dcc_core as _ast_cfx_rig_dcc_core

from .. import dcc_core as _task_dcc_core

from .. import dcc_scripts as _task_dcc_scripts

from ..gui_operates import task_tool as _gui_task_tool_opt


# resource view
class _PrxNodeView(
    _abs_unit_for_task_tool.AbsPrxNodeViewForTaskTool
):
    def on_dcc_select_node(self):
        selected_items = self._qt_tree_widget._view_model.get_selected_items()
        if selected_items:
            list_ = []
            for i in selected_items:
                i_node = i._item_model.get_assign_data('dcc_node')
                if i_node:
                    list_.append(i_node)

            qsm_mya_core.Selection.set(list_)
        else:
            qsm_mya_core.Selection.clear()

    def __init__(self, *args, **kwargs):
        super(_PrxNodeView, self).__init__(*args, **kwargs)

        self._component_data = {}

        self._qt_tree_widget._view.item_select_changed.connect(
            self.on_dcc_select_node
        )

        self._qt_tree_widget._view_model.set_item_expand_record_enable(True)

        self._assets_query = qsm_mya_hdl_anm_core.AdvRigAssetsQuery()

    def gui_restore(self):
        return self._qt_tree_widget._view_model.restore()

    def get_resources_query(self):
        return self._assets_query

    def do_gui_refresh_all(self, force=False):
        is_changed = self._assets_query.do_update()
        if is_changed is True or force is True:
            self.gui_restore()
            gui_task_tool_opt = self._unit._gui_task_tool_opt
            for i_resource_opt in self._assets_query.get_all():
                i_cfx_asset_hdl = _task_dcc_core.ShotCfxClothAssetHandle(i_resource_opt.namespace)
                self.gui_add_main(gui_task_tool_opt, i_resource_opt, i_cfx_asset_hdl)

    def gui_add_main(self, gui_task_tool_opt, resource_opt, asset_handle):
        path = resource_opt.path

        _ = self._qt_tree_widget._view_model.find_item(path)
        if _:
            return False, _

        path_opt = bsc_core.BscNodePathOpt(path)

        ancestor_paths = path_opt.get_ancestor_paths()
        ancestor_paths.reverse()

        for i_path in ancestor_paths:
            i_flag, i_qt_item = self._qt_tree_widget._view_model.create_item(i_path)
            if i_flag is True:
                i_qt_item._item_model.set_expanded(True)

        flag, qt_item = self._qt_tree_widget._view_model.create_item(path)

        node = resource_opt.node
        node_type = qsm_mya_core.Node.get_type(node)

        qt_icon = gui_qt_core.QtMaya.generate_qt_icon_by_name(node_type)
        qt_item._item_model.set_icon(qt_icon)
        qt_item._item_model.set_expanded(True)

        root = resource_opt.get_root()
        # loaded
        if root:
            qt_item._item_model.set_assign_data('dcc_node', root)
            qt_item._item_model.set_assign_data('dcc_node_type', 'root')
            qt_item._item_model.set_status(qt_item._item_model.Status.Normal)
        # unloaded
        else:
            qt_item._item_model.set_status(qt_item._item_model.Status.Disable)

        self.gui_add_cfx_rig(gui_task_tool_opt, asset_handle)
        self.gui_add_ani_geo_cache(gui_task_tool_opt, asset_handle)

        return qt_item

    def gui_add_cfx_rig(self, gui_task_tool_opt, asset_handle):
        gui_location, dcc_location = asset_handle.cfx_rig_handle.generate_location_args()

        path = gui_location

        _ = self._qt_tree_widget._view_model.find_item(path)
        if _:
            return False, _

        path_opt = bsc_core.BscNodePathOpt(path)

        ancestor_paths = path_opt.get_ancestor_paths()
        ancestor_paths.reverse()

        for i_path in ancestor_paths:
            i_flag, i_qt_item = self._qt_tree_widget._view_model.create_item(i_path)
            if i_flag is True:
                i_qt_item._item_model.set_expanded(True)

        flag, qt_item = self._qt_tree_widget._view_model.create_item(path)

        task_session = self._unit._page._task_session

        if dcc_location is not None:
            node_type = qsm_mya_core.Node.get_type(dcc_location)
            qt_icon = gui_qt_core.QtMaya.generate_qt_icon_by_name(node_type)
            qt_item._item_model.set_icon(qt_icon)
            qt_item._item_model.set_assign_data('dcc_node', dcc_location)

            self._refresh_cfx_rig_version(qt_item, task_session, asset_handle)
        else:
            qt_item._item_model.set_icon_name('node/default')
            qt_item._item_model.set_status(qt_item._item_model.Status.Disable)
            qt_item._item_model.set_subname('N/a')

        qt_item._item_model.set_menu_data_generate_fnc(
            functools.partial(
                self.generate_cfx_rig_version_menu_data_fnc,
                qt_item, task_session, gui_task_tool_opt, asset_handle
            )
        )

    def _refresh_cfx_rig_version(self, qt_item, task_session, asset_handle):
        rig_variant = asset_handle.cfx_rig_handle.get_rig_variant_name()
        scene_path = asset_handle.cfx_rig_handle.get_scene_path()
        if rig_variant == 'default':
            keyword = 'asset-release-maya-scene-file'
        else:
            keyword = 'asset-release-maya-scene-var-file'

        version_args = task_session.get_file_version_args(keyword, scene_path)
        if version_args:
            version, version_last = version_args
            if version == version_last:
                qt_item._item_model.set_subname('v{}@{}'.format(version, rig_variant))
                qt_item._item_model.set_status(qt_item._item_model.Status.Correct)
            else:
                qt_item._item_model.set_subname('v{}({})@{}'.format(version, version_last, rig_variant))
                qt_item._item_model.set_status(qt_item._item_model.Status.Warning)
        else:
            qt_item._item_model.set_status(qt_item._item_model.Status.Error)

        self.gui_add_components(qt_item, asset_handle)

    def generate_cfx_rig_version_menu_data_fnc(self, qt_item, task_session, gui_task_tool_opt, asset_handle):
        def fnc_(cfx_rig_path_):
            gui_task_tool_opt.load_cfx_rig_scene_auto(rig_namespace, cfx_rig_path_)

            self._refresh_cfx_rig_version(qt_item, task_session, asset_handle)

        scene_path = asset_handle.cfx_rig_handle.get_scene_path()
        rig_namespace = asset_handle.rig_namespace

        menu_data = []
        version_dict = gui_task_tool_opt.generate_cfx_rig_version_dict(rig_namespace)
        for i_rig_variant, v in version_dict.items():
            i_sub_menu_data = []
            menu_data.append(
                [
                    'Load Rig "{}"'.format(i_rig_variant), 'history',
                    i_sub_menu_data
                ]
            )
            for j_version, j_cfx_rig_path in v.items():
                if j_cfx_rig_path == scene_path:
                    i_sub_menu_data.append(
                        (j_version, 'file/version', None)
                    )
                else:
                    i_sub_menu_data.append(
                        (j_version, 'file/version', functools.partial(fnc_, j_cfx_rig_path))
                    )
        return menu_data

    def gui_add_ani_geo_cache(self, gui_task_tool_opt, asset_handle):
        gui_location, dcc_location = asset_handle.ani_geo_cache_handle.generate_location_args()

        path = gui_location

        _ = self._qt_tree_widget._view_model.find_item(path)
        if _:
            return False, _

        path_opt = bsc_core.BscNodePathOpt(path)

        ancestor_paths = path_opt.get_ancestor_paths()
        ancestor_paths.reverse()

        for i_path in ancestor_paths:
            i_flag, i_qt_item = self._qt_tree_widget._view_model.create_item(i_path)
            if i_flag is True:
                i_qt_item._item_model.set_expanded(True)

        flag, qt_item = self._qt_tree_widget._view_model.create_item(path)

        task_session = self._unit._page._task_session

        if dcc_location is not None:
            node_type = qsm_mya_core.Node.get_type(dcc_location)
            qt_icon = gui_qt_core.QtMaya.generate_qt_icon_by_name(node_type)
            qt_item._item_model.set_icon(qt_icon)
            qt_item._item_model.set_assign_data('dcc_node', dcc_location)

            self._update_ani_cache_version(qt_item, task_session, asset_handle)
        else:
            qt_item._item_model.set_icon_name('node/default')
            qt_item._item_model.set_status(qt_item._item_model.Status.Disable)

            qt_item._item_model.set_subname('N/a')

        qt_item._item_model.set_menu_data_generate_fnc(
            functools.partial(
                self.generate_ani_cache_version_menu_data_fnc,
                qt_item, task_session, gui_task_tool_opt, asset_handle
            )
        )

    def _update_ani_cache_version(self, qt_item, task_session, asset_handle):
        cache_path = asset_handle.ani_geo_cache_handle.get_cache_path()
        version_args = task_session.get_file_version_args(
            'shot-temporary-asset-cache-abc-geometry-file', cache_path
        )
        if version_args:
            version, version_last = version_args
            if version == version_last:
                qt_item._item_model.set_subname('v{}'.format(version))
                qt_item._item_model.set_status(qt_item._item_model.Status.Correct)
            else:
                qt_item._item_model.set_subname('v{}({})'.format(version, version_last))
                qt_item._item_model.set_status(qt_item._item_model.Status.Warning)
        else:
            qt_item._item_model.set_status(qt_item._item_model.Status.Error)

    def generate_ani_cache_version_menu_data_fnc(self, qt_item, task_session, gui_task_tool_opt, asset_handle):
        def fnc_(cache_path_):
            gui_task_tool_opt.load_ani_geo_cache_auto(rig_namespace, cache_path_)
            _cache_path = cache_path_.replace('geometry.abc', 'control.abc')
            gui_task_tool_opt.load_ani_ctl_cache_auto(rig_namespace, _cache_path)

            self._update_ani_cache_version(qt_item, task_session, asset_handle)

            asset_handle.unload_rig()

        cache_path = asset_handle.ani_geo_cache_handle.get_cache_path()
        rig_namespace = asset_handle.rig_namespace

        sub_menu_data = []
        menu_data = [
            [
                'Load', 'history', sub_menu_data
            ]
        ]

        version_dict = gui_task_tool_opt.generate_ani_geo_cache_version_dict(rig_namespace)
        for k, v in version_dict.items():
            if v == cache_path:
                sub_menu_data.append(
                    (k, 'file/version', None)
                )
            else:
                sub_menu_data.append(
                    (k, 'file/version', functools.partial(fnc_, v))
                )
        return menu_data

    def gui_add_components(self, resource_qt_item, asset_handle):
        resource_qt_item._item_model.clear_descendants()

        self._component_data = asset_handle.cfx_rig_handle.generate_component_data()

        for i_key, i_value in self._component_data.items():
            self.gui_add_component(i_key, i_value)

    def gui_add_component(self, path, node):
        _ = self._qt_tree_widget._view_model.find_item(path)
        if _:
            return False, _

        path_opt = bsc_core.BscNodePathOpt(path)

        ancestor_paths = path_opt.get_ancestor_paths()
        ancestor_paths.reverse()

        for i_path in ancestor_paths:
            i_flag, i_qt_item = self._qt_tree_widget._view_model.create_item(i_path)
            if i_flag is True:
                i_qt_item._item_model.set_icon_name('database/group')
                # i_qt_item._item_model.set_expanded(True)

        flag, qt_item = self._qt_tree_widget._view_model.create_item(path)

        node_type = qsm_mya_core.Node.get_type(node)

        qt_icon = gui_qt_core.QtMaya.generate_qt_icon_by_name(node_type)
        qt_item._item_model.set_icon(qt_icon)
        # qt_item._item_model.set_expanded(True)
        qt_item._item_model.set_assign_data('dcc_node', node)

        visible = qsm_mya_core.NodeDisplay.is_visible(node)
        if visible is False:
            qt_item._item_model.set_status(
                qt_item._item_model.Status.Disable
            )

    def gui_select_all_root(self):
        self._qt_tree_widget._view_model.clear_item_selection()
        for i in self._qt_tree_widget._view_model.get_all_items():
            i_dcc_node_type = i._item_model.get_assign_data('dcc_node_type')
            if i_dcc_node_type == 'root':
                i._item_model.set_selected(True)


# basic toolset
class _PrxBasicToolset(
    _abs_unit_for_task_tool.AbsPrxToolsetForTaskTool
):
    GUI_KEY = 'basic'

    def __init__(self, *args, **kwargs):
        super(_PrxBasicToolset, self).__init__(*args, **kwargs)

        # cfx rig
        self._prx_options_node.set(
            'cfx_rig.load_or_update', self.on_load_or_update_cfx_rig_by_selection
        )
        self._prx_options_node.get_port('cfx_rig.load_or_update').set_menu_content(
            qsm_mya_preset.NodePreset.generate_menu_content(
                'nCloth',
                key_excludes=[
                    'displayColor', 'inputMeshAttract', 'inputAttractMethod', 'inputAttractMapType'
                ]
            )
        )

        self._prx_options_node.set(
            'cfx_rig.enable', self.on_enable_cfx_rig_by_selection
        )
        self._prx_options_node.set(
            'cfx_rig.disable', self.on_disable_cfx_rig_by_selection
        )

        # rig preset
        self._prx_options_node.set(
            'cfx_rig.load_rig_preset', self.on_load_rig_preset
        )

        # animation cache
        self._prx_options_node.set(
            'ani_cache.load_or_update', self.on_load_or_update_ani_cache_by_selection
        )
        if self._window._language == 'chs':
            self._prx_options_node.get_port('ani_cache.load_or_update').set_menu_data(
                [
                    (
                        '自定义加载/更新', 'file/file', self.on_load_or_update_ani_cache_customize
                    )
                ]
            )
        else:
            self._prx_options_node.get_port('ani_cache.load_or_update').set_menu_data(
                [
                    (
                        'customize load/update', 'file/file', self.on_load_or_update_ani_cache_customize
                    )
                ]
            )

        # simulation
        self._prx_options_node.set(
            'simulation.solver.enable', self.on_enable_solver_by_selection
        )
        self._prx_options_node.set(
            'simulation.solver.disable', self.on_disable_solver_by_selection
        )

        self._prx_options_node.set(
            'simulation.select_all_asset', self.on_select_all_asset
        )

    def get_rig_namespaces_by_selection(self):
        results = []
        namespaces = qsm_mya_core.Namespaces.extract_from_selection()
        if namespaces:
            assets_query = qsm_mya_hdl_anm_core.AdvRigAssetsQuery()
            assets_query.do_update()
            for i_ns in namespaces:
                i_nss = bsc_core.BscNamespace.get_dag_component_paths(i_ns)
                i_nss.reverse()
                for j_ns in i_nss:
                    j_result = assets_query.get(j_ns)
                    if j_result:
                        results.append(j_ns)
                        break

        if not results:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._unit._configure.get(
                        'build.messages.no_characters'
                    )
                ),
                status='warning'
            )
            return
        return results
    
    # cfx rig
    def on_load_or_update_cfx_rig_by_selection(self):
        if self._unit._gui_task_tool_opt is not None:
            force = self._prx_options_node.get('cfx_rig.load_or_update_force')
            namespaces = self.get_rig_namespaces_by_selection()
            if namespaces:
                with self._window.gui_progressing(
                    maximum=len(namespaces), label='load cfx rig'
                ) as g_p:
                    for i_rig_namespace in namespaces:
                        self._unit._gui_task_tool_opt.load_cfx_rig_auto(i_rig_namespace, force=force)

                        g_p.do_update()

    def on_enable_cfx_rig_by_selection(self):
        namespaces = self.get_rig_namespaces_by_selection()
        if namespaces:
            with self._window.gui_progressing(
                maximum=len(namespaces), label='enable cfx rig'
            ) as g_p:
                for i_rig_namespace in namespaces:
                    _task_dcc_core.ShotCfxClothAssetHandle(i_rig_namespace).cfx_rig_handle.set_enable(True)

                    g_p.do_update()

    def on_disable_cfx_rig_by_selection(self):
        namespaces = self.get_rig_namespaces_by_selection()
        if namespaces:
            with self._window.gui_progressing(
                maximum=len(namespaces), label='disable cfx rig'
            ) as g_p:
                for i_rig_namespace in namespaces:
                    _task_dcc_core.ShotCfxClothAssetHandle(i_rig_namespace).cfx_rig_handle.set_enable(False)

                    g_p.do_update()

    # rig preset

    def on_load_rig_preset(self):
        namespaces = self.get_rig_namespaces_by_selection()
        if namespaces:
            rig_namespace = namespaces[-1]
            cfx_rig_namespace = _task_dcc_core.ShotCfxClothAssetHandle.to_cfx_rig_namespace(rig_namespace)
            options = _ast_cfx_rig_dcc_core.AssetCfxRigHandle.get_rig_preset_names(namespace=cfx_rig_namespace)
            name = _ast_cfx_rig_dcc_core.AssetCfxRigHandle.get_rig_preset_name(namespace=cfx_rig_namespace)

            result = gui_core.GuiApplication.exec_input_dialog(
                type='choose',
                info='Entry Name for Preset...',
                options=options,
                value=name,
                title='Mark Rig Preset'
            )
            if result:
                _ast_cfx_rig_dcc_core.AssetCfxRigHandle.load_rig_preset(result, namespace=cfx_rig_namespace)

    # animation cache
    def on_load_or_update_ani_cache_by_selection(self):
        import lnx_maya_wotrix_tasks.shot.animation.dcc_scripts as s

        namespaces = self.get_rig_namespaces_by_selection()
        if namespaces:
            properties = self._page._task_session.properties
            s.ShotAnimationCacheSync.execute_for(
                namespaces=namespaces,
                resource_properties=dict(
                    project=properties.project,
                    # episode=properties.episode,
                    sequence=properties.sequence,
                    shot=properties.shot,
                ),
                resource_fnc=s.ShotAnimationCacheSync.cfx_load_ani_cache_auto_fnc
            )

    def on_load_or_update_ani_cache_customize(self):
        namespaces = self.get_rig_namespaces_by_selection()
        if namespaces:
            scene_path = gui_core.GuiStorageDialog.open_file(
                ext_filter='All File (*.ma *.mb)',
                parent=self._window._qt_widget
            )
            if not scene_path:
                return

            import lnx_maya_wotrix_tasks.shot.animation.dcc_scripts as s

            properties = self._page._task_session.properties
            s.ShotAnimationCacheSync.execute_for(
                namespaces=namespaces,
                resource_properties=dict(
                    project=properties.project,
                    # episode=properties.episode,
                    sequence=properties.sequence,
                    shot=properties.shot,
                ),
                resource_fnc=s.ShotAnimationCacheSync.cfx_load_ani_cache_auto_fnc,
                scene_path_override=scene_path
            )

    # simulation
    def on_enable_solver_by_selection(self):
        namespaces = self.get_rig_namespaces_by_selection()
        if namespaces:
            with self._window.gui_progressing(
                maximum=len(namespaces), label='enable cfx rig solver'
            ) as g_p:
                for i_rig_namespace in namespaces:
                    _task_dcc_core.ShotCfxClothAssetHandle(i_rig_namespace).cfx_rig_handle.set_all_solver_enable(True)

                    g_p.do_update()

    def on_disable_solver_by_selection(self):
        namespaces = self.get_rig_namespaces_by_selection()
        if namespaces:
            with self._window.gui_progressing(
                maximum=len(namespaces), label='disable cfx rig solver'
            ) as g_p:
                for i_rig_namespace in namespaces:
                    _task_dcc_core.ShotCfxClothAssetHandle(i_rig_namespace).cfx_rig_handle.set_all_solver_enable(False)

                    g_p.do_update()

    def on_select_all_asset(self):
        self._unit._gui_resource_view_opt.gui_select_all_root()


# export toolset
class _PrxExportToolset(
    _abs_unit_for_task_tool.AbsPrxToolsetForTaskTool
):
    GUI_KEY = 'export'

    def do_gui_refresh_by_frame_scheme_changing(self):
        frame_scheme = self._prx_options_node.get('setting.frame_scheme')
        if frame_scheme == 'frame_range':
            self._prx_options_node.get_port('setting.frame_range').set_locked(False)
        else:
            self._prx_options_node.get_port('setting.frame_range').set_locked(True)
            self.do_gui_refresh_by_dcc_frame_changing()

    def do_gui_refresh_by_dcc_frame_changing(self):
        frame_scheme = self._prx_options_node.get('setting.frame_scheme')
        if frame_scheme == 'time_slider':
            frame_range = qsm_mya_core.Frame.get_frame_range()
            self._prx_options_node.get_port('setting.frame_range').set(frame_range)

    def do_gui_refresh_fps(self):
        fps = qsm_mya_core.Frame.get_fps_tag()
        self._prx_options_node.set('setting.fps', fps)

    def gui_get_frame_range(self):
        scheme = self._prx_options_node.get('setting.frame_scheme')
        if scheme == 'time_slider':
            return qsm_mya_core.Frame.get_frame_range()
        elif scheme == 'frame_range':
            return self._prx_options_node.get_port('setting.frame_range').get()

    def gui_get_frame_step(self):
        return self._prx_options_node.get('setting.frame_step')

    def do_gui_refresh_version_by_version_scheme_changing(self):
        directory_path = self._prx_options_node.get('cache_directory.directory')
        version_scheme = self._prx_options_node.get('cache_directory.version_scheme')

        options = dict(
            directory=directory_path,
            scene=bsc_storage.StgFileOpt(qsm_mya_core.SceneFile.get_current()).get_name_base()
        )

        if version_scheme == 'no_version':
            version_directory_ptn = u'{directory}/{scene}'
            version_directory_path = version_directory_ptn.format(**options)
        elif version_scheme == 'new_version':
            version_directory_ptn = u'{directory}/{scene}.v{{version}}'.format(
                **options
            )
            version_directory_path = bsc_core.BscVersion.generate_as_new_version(version_directory_ptn)
        elif version_scheme == 'specified_version':
            version_directory_ptn = u'{directory}/{scene}.v{{version}}'.format(
                **options
            )
            options['version'] = str(self._prx_options_node.get('cache_directory.specified_version')).zfill(3)
            version_directory_path = version_directory_ptn.format(**options)
        else:
            raise RuntimeError()

        self._prx_options_node.set(
            'cache_directory.version_directory', version_directory_path
        )

    def get_rig_namespaces_by_selection(self):
        results = []
        namespaces = qsm_mya_core.Namespaces.extract_from_selection()
        if namespaces:
            assets_query = qsm_mya_hdl_anm_core.AdvRigAssetsQuery()
            assets_query.do_update()
            for i_ns in namespaces:
                i_nss = bsc_core.BscNamespace.get_dag_component_paths(i_ns)
                i_nss.reverse()
                for j_ns in i_nss:
                    j_result = assets_query.get(j_ns)
                    if j_result:
                        results.append(j_ns)
                        break

        if not results:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._unit._configure.get(
                        'build.messages.no_characters'
                    )
                ),
                status='warning'
            )
            return
        return results

    @classmethod
    def get_all_rig_namespaces(cls):
        namespaces = qsm_mya_core.Namespaces.get_all()
        return qsm_mya_hdl_anm_core.AdvRigAsset.filter_namespaces(namespaces)

    def __init__(self, *args, **kwargs):
        super(_PrxExportToolset, self).__init__(*args, **kwargs)
        self._prx_options_node.get_port('setting.frame_scheme').connect_input_changed_to(
            self.do_gui_refresh_by_frame_scheme_changing
        )

        self._prx_options_node.set(
            'animation.apply_start_frame', self.on_apply_animation_start_frame
        )

        self._prx_options_node.set(
            'simulation.apply_start_frame', self.on_apply_solver_start_frame
        )

        self._prx_options_node.get_port('cache_directory.version_scheme').connect_input_changed_to(
            self.do_gui_refresh_version_by_version_scheme_changing
        )
        self._prx_options_node.get_port('cache_directory.specified_version').connect_input_changed_to(
            self.do_gui_refresh_version_by_version_scheme_changing
        )

        # playblast
        self._prx_options_node.set(
            'preview_export.playblast', self.on_playblast
        )
        if self._window._language == 'chs':
            self._prx_options_node.get_port('preview_export.playblast').set_menu_data(
                [
                    ('子进程', 'tool/subprocess', self.on_playblast_subprocess),
                    ('后台', 'tool/backstage', self.on_playblast_backstage),
                    ('农场', 'tool/farm', self.on_playblast_farm)
                ]
            )
        else:
            self._prx_options_node.get_port('preview_export.playblast').set_menu_data(
                [
                    ('subprocess', 'tool/subprocess', self.on_playblast_subprocess),
                    ('backstage', 'tool/backstage', self.on_playblast_backstage),
                    ('farm', 'tool/farm', self.on_playblast_farm)
                ]
            )

        # export cache
        self._prx_options_node.set(
            'cache_export.export_cloth_cache', self.on_export_cloth_cache_auto
        )
        if self._window._language == 'chs':
            self._prx_options_node.get_port('cache_export.export_cloth_cache').set_menu_data(
                [
                    ('子进程', 'tool/subprocess', self.on_export_cloth_cache_auto_as_subprocess),
                    ('后台', 'tool/backstage', self.on_export_cloth_cache_auto_as_backstage),
                    ('农场', 'tool/farm', self.on_export_cloth_cache_auto_as_farm)
                ]
            )
        else:
            self._prx_options_node.get_port('cache_export.export_cloth_cache').set_menu_data(
                [
                    ('subprocess', 'tool/subprocess', self.on_export_cloth_cache_auto_as_subprocess),
                    ('backstage', 'tool/backstage', self.on_export_cloth_cache_auto_as_backstage),
                    ('farm', 'tool/farm', self.on_export_cloth_cache_auto_as_farm)
                ]
            )

    def do_gui_refresh_all(self):
        if self._page._task_session:
            self.do_gui_refresh_fps()

            cache_directory_path = self._page._task_session.get_file_for(
                'shot-source-maya-cfx_cache-dir'
            )
            self._prx_options_node.set(
                'cache_directory.directory', cache_directory_path
            )

            self.do_gui_refresh_version_by_version_scheme_changing()
        
        if self._unit._gui_task_tool_opt:
            animation_start_frame = self._unit._gui_task_tool_opt.get_animation_start_frame()
            self._prx_options_node.set('animation.start_frame', animation_start_frame)

            simulation_start_frame = self._unit._gui_task_tool_opt.get_simulation_start_frame()
            self._prx_options_node.set('simulation.start_frame', simulation_start_frame)
    
    def on_apply_animation_start_frame(self):
        start_frame = self._prx_options_node.get('animation.start_frame')

        if self._unit._gui_task_tool_opt:
            self._unit._gui_task_tool_opt.apply_animation_start_frame(start_frame)
    
    @qsm_mya_core.Undo.execute
    def on_apply_solver_start_frame(self):
        start_frame = self._prx_options_node.get('simulation.start_frame')

        if self._unit._gui_task_tool_opt:
            self._unit._gui_task_tool_opt.apply_simulation_start_frame(start_frame)

    # playblast
    def on_playblast(self):
        clip_start = self._prx_options_node.get('animation.start_frame')
        with self._window.gui_minimized():
            import lxbasic.session as bsc_session
            bsc_session.OptionHook.execute(
                "option_hook_key=dcc-script/maya/qsm-playblast-script&clip_start={}".format(clip_start)
            )

    def on_playblast_subprocess(self):
        clip_start = self._prx_options_node.get('animation.start_frame')

        import lxbasic.session as bsc_session
        bsc_session.OptionHook.execute(
            "option_hook_key=dcc-script/maya/qsm-playblast-script&scheme=subprocess&clip_start={}".format(clip_start)
        )

    def on_playblast_backstage(self):
        clip_start = self._prx_options_node.get('animation.start_frame')

        import lxbasic.session as bsc_session
        bsc_session.OptionHook.execute(
            "option_hook_key=dcc-script/maya/qsm-playblast-script&scheme=backstage&clip_start={}".format(clip_start)
        )

    def on_playblast_farm(self):
        clip_start = self._prx_options_node.get('animation.start_frame')

        import lxbasic.session as bsc_session
        bsc_session.OptionHook.execute(
            "option_hook_key=dcc-script/maya/qsm-playblast-script&scheme=farm&clip_start={}".format(clip_start)
        )

    # cache export
    def on_export_cloth_cache_auto(self):
        if self._unit._gui_task_tool_opt is not None:
            export_scheme = self._prx_options_node.get('cache_export.scheme')
            include_customize_deform_geometry = self._prx_options_node.get(
                'cache_export.include_customize_deform_geometry'
            )
            if export_scheme == 'all':
                rig_namespaces = self.get_all_rig_namespaces()
            elif export_scheme == 'selected':
                rig_namespaces = self.get_rig_namespaces_by_selection()
            else:
                raise RuntimeError()

            if rig_namespaces:
                directory_path = self._prx_options_node.get('cache_directory.version_directory')
                frame_range = self.gui_get_frame_range()
                frame_step = self.gui_get_frame_step()
                with self._window.gui_progressing(
                    maximum=len(rig_namespaces), label='load cfx rig'
                ) as g_p:
                    for i_rig_namespace in rig_namespaces:
                        i_handle = _task_dcc_core.ShotCfxClothAssetHandle(i_rig_namespace)
                        if i_handle.cfx_rig_handle.get_is_enable():
                            self._unit._gui_task_tool_opt.export_cloth_cache_by_rig_namespace(
                                i_rig_namespace,
                                directory_path=directory_path,
                                frame_range=frame_range,
                                frame_step=frame_step,
                                include_customize_deform_geometry=include_customize_deform_geometry
                            )

                        g_p.do_update()

                self.do_gui_refresh_version_by_version_scheme_changing()

    def on_export_cloth_cache_auto_as_subprocess(self):
        if self._unit._gui_task_tool_opt is not None:
            export_scheme = self._prx_options_node.get('cache_export.scheme')
            include_customize_deform_geometry = self._prx_options_node.get(
                'cache_export.include_customize_deform_geometry'
            )
            if export_scheme == 'all':
                rig_namespaces = self.get_all_rig_namespaces()
            elif export_scheme == 'selected':
                rig_namespaces = self.get_rig_namespaces_by_selection()
            else:
                raise RuntimeError()

            if rig_namespaces:
                directory_path = self._prx_options_node.get('cache_directory.version_directory')
                frame_range = self.gui_get_frame_range()
                frame_step = self.gui_get_frame_step()
                cfx_rig_namespaces = []

                for i_rig_namespace in rig_namespaces:
                    i_handle = _task_dcc_core.ShotCfxClothAssetHandle(i_rig_namespace)
                    if i_handle.cfx_rig_handle.get_is_enable():
                        cfx_rig_namespaces.append(i_handle._cfx_rig_namespace)

                if cfx_rig_namespaces:
                    (
                        task_name, scene_src_path, cmd_script
                    ) = _task_dcc_scripts.ShotCfxClothCacheExportProcess.generate_subprocess_args(
                        namespaces=cfx_rig_namespaces,
                        directory_path=directory_path,
                        frame_range=frame_range,
                        frame_step=frame_step,
                        include_customize_deform_geometry=include_customize_deform_geometry
                    )

                    qsm_gnl_prc_task.SubprocessTaskSubmit.execute_one(
                        task_name, cmd_script, completed_fnc=None,
                        window_title='CFX Cloth Cache Export', window_title_chs='解算布料缓存导出',
                    )

                self.do_gui_refresh_version_by_version_scheme_changing()

    def on_export_cloth_cache_auto_as_backstage(self):
        if qsm_gnl_prc_task.BackstageTaskSubmit.check_is_valid() is False:
            return

        if self._unit._gui_task_tool_opt is not None:
            export_scheme = self._prx_options_node.get('cache_export.scheme')
            include_customize_deform_geometry = self._prx_options_node.get(
                'cache_export.include_customize_deform_geometry'
            )
            if export_scheme == 'all':
                rig_namespaces = self.get_all_rig_namespaces()
            elif export_scheme == 'selected':
                rig_namespaces = self.get_rig_namespaces_by_selection()
            else:
                raise RuntimeError()

            if rig_namespaces:
                directory_path = self._prx_options_node.get('cache_directory.version_directory')
                frame_range = self.gui_get_frame_range()
                frame_step = self.gui_get_frame_step()
                cfx_rig_namespaces = []

                for i_rig_namespace in rig_namespaces:
                    i_handle = _task_dcc_core.ShotCfxClothAssetHandle(i_rig_namespace)
                    if i_handle.cfx_rig_handle.get_is_enable():
                        cfx_rig_namespaces.append(i_handle._cfx_rig_namespace)

                if cfx_rig_namespaces:
                    (
                        task_name, scene_src_path, cmd_script
                    ) = _task_dcc_scripts.ShotCfxClothCacheExportProcess.generate_subprocess_args(
                        namespaces=cfx_rig_namespaces,
                        directory_path=directory_path,
                        frame_range=frame_range,
                        frame_step=frame_step,
                        include_customize_deform_geometry=include_customize_deform_geometry
                    )

                    qsm_gnl_prc_task.BackstageTaskSubmit.execute(
                        task_group=None, task_type='playblast', task_name=task_name,
                        cmd_script=cmd_script, icon_name='application/maya',
                        file_path=scene_src_path, output_file_path=directory_path,
                        completed_notice_dict=dict(
                            title='通知',
                            message='缓存导出结束了, 是否打开文件夹?',
                            # todo? exec must use unicode
                            ok_python_script='import os; os.startfile("{}".decode("utf-8"))'.format(
                                bsc_core.ensure_string(directory_path)
                            ),
                            status='normal'
                        )
                    )

                self.do_gui_refresh_version_by_version_scheme_changing()

    def on_export_cloth_cache_auto_as_farm(self):
        if qsm_gnl_prc_task.FarmTaskSubmit.check_is_valid() is False:
            return

        if self._unit._gui_task_tool_opt is not None:
            export_scheme = self._prx_options_node.get('cache_export.scheme')
            include_customize_deform_geometry = self._prx_options_node.get(
                'cache_export.include_customize_deform_geometry'
            )
            if export_scheme == 'all':
                rig_namespaces = self.get_all_rig_namespaces()
            elif export_scheme == 'selected':
                rig_namespaces = self.get_rig_namespaces_by_selection()
            else:
                raise RuntimeError()

            if rig_namespaces:
                directory_path = self._prx_options_node.get('cache_directory.version_directory')
                frame_range = self.gui_get_frame_range()
                frame_step = self.gui_get_frame_step()
                cfx_rig_namespaces = []

                for i_rig_namespace in rig_namespaces:
                    i_handle = _task_dcc_core.ShotCfxClothAssetHandle(i_rig_namespace)
                    if i_handle.cfx_rig_handle.get_is_enable():
                        cfx_rig_namespaces.append(i_handle._cfx_rig_namespace)

                if cfx_rig_namespaces:
                    option_hook = _task_dcc_scripts.ShotCfxClothCacheExportProcess.generate_farm_hook_option(
                        namespaces=cfx_rig_namespaces,
                        directory_path=directory_path,
                        frame_range=frame_range,
                        frame_step=frame_step,
                        include_customize_deform_geometry=include_customize_deform_geometry
                    )

                    qsm_gnl_prc_task.FarmTaskSubmit.execute_by_hook_option(
                        option_hook
                    )


class GuiTaskToolMain(
    _abs_unit_for_task_tool.AbsPrxUnitForTaskTool
):
    GUI_KEY = 'cfx_cloth'

    GUI_RESOURCE_VIEW_CLS = _PrxNodeView

    TOOLSET_CLASSES = [
        _PrxBasicToolset,
        _PrxExportToolset,
    ]

    TASK_TOOL_OPT_CLS = _gui_task_tool_opt.MayaShotCfxClothToolOpt

    def __init__(self, *args, **kwargs):
        super(GuiTaskToolMain, self).__init__(*args, **kwargs)
