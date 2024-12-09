# coding:utf-8
import functools

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from qsm_lazy_wsp.gui.abstracts import unit_for_task_tool as _abs_unit_for_task_tool

import lxgui.qt.core as gui_qt_core

import qsm_general.prc_task as qsm_gnl_prc_task

import qsm_maya.core as qsm_mya_core

import qsm_maya.preset as qsm_mya_preset

import qsm_maya.handles.animation.core as qsm_mya_hdl_anm_core

from .. import dcc_core as _task_dcc_core

from .. import dcc_scripts as _task_dcc_scripts

from ..gui_operates import task_tool as _gui_task_tool_opt


# resource view
class _PrxNodeView(_abs_unit_for_task_tool.AbsPrxNodeViewForTaskTool):
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

        self._resources_query = qsm_mya_hdl_anm_core.AdvRigAssetsQuery()

    def gui_restore(self):
        return self._qt_tree_widget._view_model.restore()

    def get_resources_query(self):
        return self._resources_query

    def do_gui_refresh_all(self, force=False):
        is_changed = self._resources_query.do_update()
        if is_changed is True or force is True:
            self.gui_restore()
            gui_task_tool_opt = self._unit._gui_task_tool_opt
            for i_resource_opt in self._resources_query.get_all():
                i_cfx_asset_hdl = _task_dcc_core.ShotCfxClothAssetHandle(i_resource_opt.namespace)
                self.gui_add_resource(gui_task_tool_opt, i_resource_opt, i_cfx_asset_hdl)

    def generate_version_switch_menu_data(
        self,
        qt_item, task_session,
        gui_task_tool_opt, asset_handle, rig_namespace
    ):
        def fnc_(scene_path_):
            gui_task_tool_opt.load_cfx_rig_scene_auto(rig_namespace, scene_path_)

            self._update_resource_version(qt_item, task_session, asset_handle)

        scene_path = asset_handle.get_cfx_rig_scene_path()

        sub_menu_data = []
        menu_data = [
            [
                'Load', 'history', sub_menu_data
            ]
        ]
        dict_ = gui_task_tool_opt.get_cfx_rig_all_version_dict(rig_namespace)
        for k, v in dict_.items():
            if v == scene_path:
                sub_menu_data.append(
                    (k, 'file/version', None)
                )
            else:
                sub_menu_data.append(
                    (k, 'file/version', functools.partial(fnc_, v))
                )
        return menu_data

    def gui_add_resource(self, gui_task_tool_opt, resource_opt, asset_handle):
        path = resource_opt.path

        _ = self._qt_tree_widget._view_model.find_item(path)
        if _:
            return False, _

        task_session = self._unit._page._task_session

        path_opt = bsc_core.BscNodePathOpt(path)

        ancestor_paths = path_opt.get_ancestor_paths()
        ancestor_paths.reverse()

        for i_path in ancestor_paths:
            i_flag, i_qt_item = self._qt_tree_widget._view_model.create_item(i_path)
            if i_flag is True:
                i_qt_item._item_model.set_icon_name('database/group')
                i_qt_item._item_model.set_expanded(True)

        flag, qt_item = self._qt_tree_widget._view_model.create_item(path)

        node = resource_opt.node
        node_type = qsm_mya_core.Node.get_type(node)

        qt_icon = gui_qt_core.QtMaya.generate_qt_icon_by_name(node_type)
        qt_item._item_model.set_icon(qt_icon)
        qt_item._item_model.set_expanded(True)

        root = resource_opt.get_root()
        if root:
            qt_item._item_model.set_assign_data('dcc_node', root)
            qt_item._item_model.set_assign_data('dcc_node_type', 'root')

        rig_namespace = asset_handle.rig_namespace

        if asset_handle.cfx_rig_is_loaded():
            self._update_resource_version(qt_item, task_session, asset_handle)

        qt_item._item_model.set_menu_data_generate_fnc(
            functools.partial(
                self.generate_version_switch_menu_data,
                qt_item, task_session, gui_task_tool_opt, asset_handle, rig_namespace
            )
        )
        return qt_item

    def _update_resource_version(self, qt_item, task_session, asset_handle):
        scene_path = asset_handle.get_cfx_rig_scene_path()
        version_args = task_session.get_file_version_args('asset-release-maya-scene-file', scene_path)
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

        self.gui_add_components(qt_item, asset_handle)

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
class _PrxBasicToolset(_abs_unit_for_task_tool.AbsPrxToolsetForTaskTool):
    GUI_KEY = 'basic'

    def __init__(self, *args, **kwargs):
        super(_PrxBasicToolset, self).__init__(*args, **kwargs)

        self._prx_options_node.set(
            'cfx_rig.load', self.on_load_cfx_rig_by_select
        )
        self._prx_options_node.get_port('cfx_rig.load').set_menu_content(
            qsm_mya_preset.NodePreset.generate_menu_content(
                'nCloth',
                atr_excludes=[
                    'displayColor', 'inputMeshAttract', 'inputAttractMethod', 'inputAttractMapType'
                ]
            )
        )
        self._prx_options_node.set(
            'cfx_rig.update', self.on_update_cfx_rig_by_select
        )

        self._prx_options_node.set(
            'cfx_rig.enable', self.on_enable_cfx_rig_by_select
        )
        self._prx_options_node.set(
            'cfx_rig.disable', self.on_disable_cfx_rig_by_select
        )

        self._prx_options_node.set(
            'simulation.solver.enable', self.on_enable_solver_by_select
        )
        self._prx_options_node.set(
            'simulation.solver.disable', self.on_disable_solver_by_select
        )

        self._prx_options_node.set(
            'simulation.select_all_asset', self.on_select_all_asset
        )

    def get_rig_namespaces_by_selected(self):
        results = []
        namespaces = qsm_mya_core.Namespaces.extract_parents_from_selection()
        if namespaces:
            results = qsm_mya_hdl_anm_core.AdvRigAsset.filter_namespaces(namespaces)

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

    def on_load_cfx_rig_by_select(self):
        if self._unit._gui_task_tool_opt is not None:
            namespaces = self.get_rig_namespaces_by_selected()
            if namespaces:
                with self._window.gui_progressing(
                    maximum=len(namespaces), label='load cfx rig'
                ) as g_p:
                    for i_rig_namespace in namespaces:
                        self._unit._gui_task_tool_opt.load_cfx_rig_for(i_rig_namespace)

                        g_p.do_update()

    def on_update_cfx_rig_by_select(self):
        if self._unit._gui_task_tool_opt is not None:
            namespaces = self.get_rig_namespaces_by_selected()
            if namespaces:
                with self._window.gui_progressing(
                    maximum=len(namespaces), label='load cfx rig'
                ) as g_p:
                    for i_rig_namespace in namespaces:
                        self._unit._gui_task_tool_opt.update_cfx_rig_for(i_rig_namespace)

                        g_p.do_update()

    def on_enable_cfx_rig_by_select(self):
        namespaces = self.get_rig_namespaces_by_selected()
        if namespaces:
            with self._window.gui_progressing(
                maximum=len(namespaces), label='enable cfx rig'
            ) as g_p:
                for i_rig_namespace in namespaces:
                    _task_dcc_core.ShotCfxClothAssetHandle(i_rig_namespace).set_cfx_rig_enable(True)

                    g_p.do_update()

    def on_disable_cfx_rig_by_select(self):
        namespaces = self.get_rig_namespaces_by_selected()
        if namespaces:
            with self._window.gui_progressing(
                maximum=len(namespaces), label='disable cfx rig'
            ) as g_p:
                for i_rig_namespace in namespaces:
                    _task_dcc_core.ShotCfxClothAssetHandle(i_rig_namespace).set_cfx_rig_enable(False)

                    g_p.do_update()

    def on_enable_solver_by_select(self):
        namespaces = self.get_rig_namespaces_by_selected()
        if namespaces:
            with self._window.gui_progressing(
                maximum=len(namespaces), label='enable cfx rig solver'
            ) as g_p:
                for i_rig_namespace in namespaces:
                    _task_dcc_core.ShotCfxClothAssetHandle(i_rig_namespace).set_all_solver_enable(True)

                    g_p.do_update()

    def on_disable_solver_by_select(self):
        namespaces = self.get_rig_namespaces_by_selected()
        if namespaces:
            with self._window.gui_progressing(
                maximum=len(namespaces), label='disable cfx rig solver'
            ) as g_p:
                for i_rig_namespace in namespaces:
                    _task_dcc_core.ShotCfxClothAssetHandle(i_rig_namespace).set_all_solver_enable(False)

                    g_p.do_update()

    def on_select_all_asset(self):
        self._unit._gui_resource_view_opt.gui_select_all_root()


# export toolset
class _PrxExportToolset(_abs_unit_for_task_tool.AbsPrxToolsetForTaskTool):
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

    def get_rig_namespaces_by_selected(self):
        results = []
        namespaces = qsm_mya_core.Namespaces.extract_parents_from_selection()
        if namespaces:
            results = qsm_mya_hdl_anm_core.AdvRigAsset.filter_namespaces(namespaces)

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
            if export_scheme == 'all':
                rig_namespaces = self.get_all_rig_namespaces()
            elif export_scheme == 'selected':
                rig_namespaces = self.get_rig_namespaces_by_selected()
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
                        i_opt = _task_dcc_core.ShotCfxClothAssetHandle(i_rig_namespace)
                        if i_opt.get_cfx_rig_is_enable():
                            self._unit._gui_task_tool_opt.export_cloth_cache_by_rig_namespace(
                                i_rig_namespace,
                                directory_path=directory_path,
                                frame_range=frame_range,
                                frame_step=frame_step
                            )

                        g_p.do_update()

                self.do_gui_refresh_version_by_version_scheme_changing()

    def on_export_cloth_cache_auto_as_subprocess(self):
        if self._unit._gui_task_tool_opt is not None:
            export_scheme = self._prx_options_node.get('cache_export.scheme')
            if export_scheme == 'all':
                rig_namespaces = self.get_all_rig_namespaces()
            elif export_scheme == 'selected':
                rig_namespaces = self.get_rig_namespaces_by_selected()
            else:
                raise RuntimeError()

            if rig_namespaces:
                directory_path = self._prx_options_node.get('cache_directory.version_directory')
                frame_range = self.gui_get_frame_range()
                frame_step = self.gui_get_frame_step()
                cfx_rig_namespaces = []

                for i_rig_namespace in rig_namespaces:
                    i_opt = _task_dcc_core.ShotCfxClothAssetHandle(i_rig_namespace)
                    if i_opt.get_cfx_rig_is_enable():
                        cfx_rig_namespaces.append(i_opt._cfx_rig_namespace)

                if cfx_rig_namespaces:
                    (
                        task_name, scene_src_path, cmd_script
                    ) = _task_dcc_scripts.ShotCfxClothCacheProcess.generate_subprocess_args(
                        namespaces=cfx_rig_namespaces,
                        directory_path=directory_path,
                        frame_range=frame_range,
                        frame_step=frame_step
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
            if export_scheme == 'all':
                rig_namespaces = self.get_all_rig_namespaces()
            elif export_scheme == 'selected':
                rig_namespaces = self.get_rig_namespaces_by_selected()
            else:
                raise RuntimeError()

            if rig_namespaces:
                directory_path = self._prx_options_node.get('cache_directory.version_directory')
                frame_range = self.gui_get_frame_range()
                frame_step = self.gui_get_frame_step()
                cfx_rig_namespaces = []

                for i_rig_namespace in rig_namespaces:
                    i_opt = _task_dcc_core.ShotCfxClothAssetHandle(i_rig_namespace)
                    if i_opt.get_cfx_rig_is_enable():
                        cfx_rig_namespaces.append(i_opt._cfx_rig_namespace)

                if cfx_rig_namespaces:
                    (
                        task_name, scene_src_path, cmd_script
                    ) = _task_dcc_scripts.ShotCfxClothCacheProcess.generate_subprocess_args(
                        namespaces=cfx_rig_namespaces,
                        directory_path=directory_path,
                        frame_range=frame_range,
                        frame_step=frame_step
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
            if export_scheme == 'all':
                rig_namespaces = self.get_all_rig_namespaces()
            elif export_scheme == 'selected':
                rig_namespaces = self.get_rig_namespaces_by_selected()
            else:
                raise RuntimeError()

            if rig_namespaces:
                directory_path = self._prx_options_node.get('cache_directory.version_directory')
                frame_range = self.gui_get_frame_range()
                frame_step = self.gui_get_frame_step()
                cfx_rig_namespaces = []

                for i_rig_namespace in rig_namespaces:
                    i_opt = _task_dcc_core.ShotCfxClothAssetHandle(i_rig_namespace)
                    if i_opt.get_cfx_rig_is_enable():
                        cfx_rig_namespaces.append(i_opt._cfx_rig_namespace)

                if cfx_rig_namespaces:
                    option_hook = _task_dcc_scripts.ShotCfxClothCacheProcess.generate_farm_hook_option(
                        namespaces=cfx_rig_namespaces,
                        directory_path=directory_path,
                        frame_range=frame_range,
                        frame_step=frame_step
                    )

                    qsm_gnl_prc_task.FarmTaskSubmit.execute_by_hook_option(
                        option_hook
                    )


class PrxToolsetForShotCfxClothTool(_abs_unit_for_task_tool.AbsPrxUnitForTaskTool):
    GUI_KEY = 'cfx_cloth'

    GUI_RESOURCE_VIEW_CLS = _PrxNodeView

    TOOLSET_CLASSES = [
        _PrxBasicToolset,
        _PrxExportToolset,
    ]

    TASK_TOOL_OPT_CLS = _gui_task_tool_opt.MayaShotCfxClothToolOpt

    def __init__(self, *args, **kwargs):
        super(PrxToolsetForShotCfxClothTool, self).__init__(*args, **kwargs)
