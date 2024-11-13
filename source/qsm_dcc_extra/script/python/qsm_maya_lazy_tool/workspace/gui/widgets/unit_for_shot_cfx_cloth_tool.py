# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from qsm_lazy_tool.workspace.gui.abstracts import unit_for_task_tool as _abs_unit_for_task_tool

import lxgui.qt.core as gui_qt_core

import qsm_maya.core as qsm_mya_core

import qsm_maya.tasks.animation.core as qsm_mya_tsk_anm_core

import qsm_maya.tasks.cfx_cloth.core as qsm_mya_tsk_cfx_clt_core


# cfx cloth
class GuiResourceViewForShotCfxTool(_abs_unit_for_task_tool.AbsGuiResourceViewForTaskTool):
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
        super(GuiResourceViewForShotCfxTool, self).__init__(*args, **kwargs)

        self._component_data = {}

        self._qt_tree_widget._view.item_select_changed.connect(
            self.on_dcc_select_node
        )

        self._qt_tree_widget._view_model.set_item_expand_record_enable(True)

        self._resources_query = qsm_mya_tsk_anm_core.AdvRigAssetsQuery()

    def gui_restore(self):
        return self._qt_tree_widget._view_model.restore()

    def do_gui_refresh_all(self, force=False):
        is_changed = self._resources_query.do_update()
        if is_changed is True or force is True:
            self.gui_restore()

            for i_resource_opt in self._resources_query.get_all():
                i_cfx_asset_opt = qsm_mya_tsk_cfx_clt_core.CfxClothAssetOpt(i_resource_opt.namespace)
                self.gui_add_resource(i_resource_opt, i_cfx_asset_opt)
                self.gui_add_components(i_cfx_asset_opt)

    def gui_add_resource(self, resource_opt, cfx_asset_opt):
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

        if cfx_asset_opt.get_cfx_rig_is_loaded():
            qt_item._item_model.set_status(
                qt_item._item_model.Status.Correct
            )

        return qt_item

    def gui_add_components(self, cfx_asset_opt):
        self._component_data = cfx_asset_opt.cfx_rig_group_opt.generate_component_data()
        # data_pre = self._component_data

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
                i_qt_item._item_model.set_expanded(True)

        flag, qt_item = self._qt_tree_widget._view_model.create_item(path)

        node_type = qsm_mya_core.Node.get_type(node)

        qt_icon = gui_qt_core.QtMaya.generate_qt_icon_by_name(node_type)
        qt_item._item_model.set_icon(qt_icon)
        qt_item._item_model.set_expanded(True)
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


# main toolset
class PrxMainToolsetForShotCfxTool(_abs_unit_for_task_tool.AbsPrxToolsetForTaskTool):
    GUI_KEY = 'basic'

    def __init__(self, *args, **kwargs):
        super(PrxMainToolsetForShotCfxTool, self).__init__(*args, **kwargs)

        self._prx_options_node.set(
            'cfx_rig.load', self.on_load_cfx_rig_by_select
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
            'simulation.enable_solver', self.on_enable_cfx_rig_solver_by_select
        )
        self._prx_options_node.set(
            'simulation.disable_solver', self.on_disable_cfx_rig_solver_by_select
        )

        self._prx_options_node.set(
            'simulation.select_all', self.on_select_all
        )

    def get_dcc_character_args(self):
        results = []
        namespaces = qsm_mya_core.Namespaces.extract_parents_from_selection()
        if namespaces:
            results = qsm_mya_tsk_anm_core.AdvRigAsset.filter_namespaces(namespaces)

        if not results:
            self._window.exec_message_dialog(
                self._window.choice_message(
                    self._window._configure.get(
                        'build.{}.{}.messages.no_characters'.format(self._page.GUI_KEY, self._unit.GUI_KEY)
                    )
                ),
                status='warning'
            )
            return
        return results

    def on_load_cfx_rig_by_select(self):
        if self._unit._task_tool_opt is not None:
            namespaces = self.get_dcc_character_args()
            if namespaces:
                with self._window.gui_progressing(
                    maximum=len(namespaces), label='load cfx rig'
                ) as g_p:
                    for i_rig_namespace in namespaces:
                        self._unit._task_tool_opt.load_cfx_rig_for(i_rig_namespace)

                        g_p.do_update()

    def on_update_cfx_rig_by_select(self):
        if self._unit._task_tool_opt is not None:
            namespaces = self.get_dcc_character_args()
            if namespaces:
                with self._window.gui_progressing(
                    maximum=len(namespaces), label='load cfx rig'
                ) as g_p:
                    for i_rig_namespace in namespaces:
                        self._unit._task_tool_opt.update_cfx_rig_for(i_rig_namespace)

                        g_p.do_update()

    def on_enable_cfx_rig_by_select(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            with self._window.gui_progressing(
                maximum=len(namespaces), label='enable cfx rig'
            ) as g_p:
                for i_rig_namespace in namespaces:
                    qsm_mya_tsk_cfx_clt_core.CfxClothAssetOpt(i_rig_namespace).set_cfx_rig_enable(True)

                    g_p.do_update()

    def on_disable_cfx_rig_by_select(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            with self._window.gui_progressing(
                maximum=len(namespaces), label='disable cfx rig'
            ) as g_p:
                for i_rig_namespace in namespaces:
                    qsm_mya_tsk_cfx_clt_core.CfxClothAssetOpt(i_rig_namespace).set_cfx_rig_enable(False)

                    g_p.do_update()

    def on_enable_cfx_rig_solver_by_select(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            with self._window.gui_progressing(
                maximum=len(namespaces), label='enable cfx rig solver'
            ) as g_p:
                for i_rig_namespace in namespaces:
                    qsm_mya_tsk_cfx_clt_core.CfxClothAssetOpt(i_rig_namespace).set_cfx_rig_solver_enable(True)

                    g_p.do_update()

    def on_disable_cfx_rig_solver_by_select(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            with self._window.gui_progressing(
                maximum=len(namespaces), label='disable cfx rig solver'
            ) as g_p:
                for i_rig_namespace in namespaces:
                    qsm_mya_tsk_cfx_clt_core.CfxClothAssetOpt(i_rig_namespace).set_cfx_rig_solver_enable(False)

                    g_p.do_update()

    def on_select_all(self):
        self._unit._gui_resource_view_opt.gui_select_all_root()


# export toolset
class PrxExportToolsetForShotCfxTool(_abs_unit_for_task_tool.AbsPrxToolsetForTaskTool):
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
            version_directory_ptn = '{directory}/{scene}'
            version_directory_path = version_directory_ptn.format(**options)
        elif version_scheme == 'new_version':
            version_directory_ptn = '{directory}/{scene}.v{{version}}'.format(
                **options
            )
            version_directory_path = bsc_core.BscVersion.generate_as_new_version(version_directory_ptn)
        elif version_scheme == 'specified_version':
            version_directory_ptn = '{directory}/{scene}.v{{version}}'.format(
                **options
            )
            options['version'] = str(self._prx_options_node.get('cache_directory.specified_version')).zfill(3)
            version_directory_path = version_directory_ptn.format(**options)
        else:
            raise RuntimeError()

        self._prx_options_node.set(
            'cache_directory.version_directory', version_directory_path
        )

    def get_dcc_character_args(self):
        results = []
        namespaces = qsm_mya_core.Namespaces.extract_parents_from_selection()
        if namespaces:
            results = qsm_mya_tsk_anm_core.AdvRigAsset.filter_namespaces(namespaces)

        if not results:
            self._window.exec_message_dialog(
                self._window.choice_message(
                    self._window._configure.get(
                        'build.{}.{}.messages.no_characters'.format(self._page.GUI_KEY, self._unit.GUI_KEY)
                    )
                ),
                status='warning'
            )
            return
        return results

    def __init__(self, *args, **kwargs):
        super(PrxExportToolsetForShotCfxTool, self).__init__(*args, **kwargs)
        self._prx_options_node.get_port('setting.frame_scheme').connect_input_changed_to(
            self.do_gui_refresh_by_frame_scheme_changing
        )

        self._prx_options_node.get_port('cache_directory.version_scheme').connect_input_changed_to(
            self.do_gui_refresh_version_by_version_scheme_changing
        )
        self._prx_options_node.get_port('cache_directory.specified_version').connect_input_changed_to(
            self.do_gui_refresh_version_by_version_scheme_changing
        )

        self._prx_options_node.set(
            'preview_export.playblast', self.on_playblast
        )
        self._prx_options_node.set(
            'preview_export.playblast_subprocess', self.on_playblast_subprocess
        )
        self._prx_options_node.set(
            'preview_export.playblast_backstage', self.on_playblast_backstage
        )
        self._prx_options_node.set(
            'preview_export.playblast_farm', self.on_playblast_farm
        )

        self._prx_options_node.set(
            'cache_export.export_cloth_cache', self.on_export_cloth_cache_by_select
        )

    def do_gui_refresh_all(self):
        if self._page._task_session:
            self.do_gui_refresh_fps()

            cache_directory_path = self._page._task_session.get_file_for(
                'shot-source-maya-cloth_cache-dir'
            )
            self._prx_options_node.set(
                'cache_directory.directory', cache_directory_path
            )

            self.do_gui_refresh_version_by_version_scheme_changing()

    def on_playblast(self):
        with self._window.gui_minimized():
            import lxbasic.session as bsc_session
            bsc_session.OptionHook.execute("option_hook_key=dcc-script/maya/qsm-playblast-script")

    @staticmethod
    def on_playblast_subprocess():
        import lxbasic.session as bsc_session
        bsc_session.OptionHook.execute("option_hook_key=dcc-script/maya/qsm-playblast-script&scheme=subprocess")

    @staticmethod
    def on_playblast_backstage():
        import lxbasic.session as bsc_session
        bsc_session.OptionHook.execute("option_hook_key=dcc-script/maya/qsm-playblast-script&scheme=backstage")

    @staticmethod
    def on_playblast_farm():
        import lxbasic.session as bsc_session
        bsc_session.OptionHook.execute("option_hook_key=dcc-script/maya/qsm-playblast-script&scheme=farm")

    def on_export_cloth_cache_by_select(self):
        if self._unit._task_tool_opt is not None:
            namespaces = self.get_dcc_character_args()
            if namespaces:
                with self._window.gui_progressing(
                    maximum=len(namespaces), label='load cfx rig'
                ) as g_p:
                    directory_path = self._prx_options_node.get('cache_directory.version_directory')
                    frame_range = self.gui_get_frame_range()
                    frame_step = self.gui_get_frame_step()
                    for i_rig_namespace in namespaces:
                        self._unit._task_tool_opt.load_cfx_rig_for(i_rig_namespace)
                        self._unit._task_tool_opt.export_cloth_cache_for(
                            i_rig_namespace,
                            directory_path=directory_path,
                            frame_range=frame_range,
                            frame_step=frame_step
                        )

                    g_p.do_update()

                self.do_gui_refresh_version_by_version_scheme_changing()


class PrxToolsetForShotCfxClothTool(_abs_unit_for_task_tool.AbsPrxUnitForTaskTool):
    GUI_KEY = 'cfx_cloth'

    GUI_RESOURCE_VIEW_CLS = GuiResourceViewForShotCfxTool

    TOOLSET_CLASSES = [
        PrxMainToolsetForShotCfxTool,
        PrxExportToolsetForShotCfxTool,
    ]

    def __init__(self, *args, **kwargs):
        super(PrxToolsetForShotCfxClothTool, self).__init__(*args, **kwargs)

