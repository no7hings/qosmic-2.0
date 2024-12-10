# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from qsm_lazy_wsp.gui.abstracts import unit_for_task_tool as _abs_unit_for_task_tool

import lxgui.qt.core as gui_qt_core

import qsm_maya.core as qsm_mya_core

import qsm_maya.handles.animation.core as qsm_mya_hdl_anm_core

import qsm_maya.handles.general.core as qsm_mya_hdl_gnl_core

from ...shot_cfx_cloth import dcc_core as _shot_cfx_cloth_core

from ...shot_cfx_cloth import dcc_scripts as _shot_cfx_cloth_scripts

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

    def do_gui_refresh_all(self, force=False):
        is_changed = self._resources_query.do_update()
        if is_changed is True or force is True:
            self.gui_restore()

            for i_resource_opt in self._resources_query.get_all():
                i_cfx_asset_opt = _shot_cfx_cloth_core.ShotCfxClothAssetHandle(i_resource_opt.namespace)
                self.gui_add_resource(i_resource_opt, i_cfx_asset_opt)

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
            qt_item._item_model.set_assign_data('dcc_resource', resource_opt)

        if cfx_asset_opt.cfx_rig_is_loaded():
            qt_item._item_model.set_status(
                qt_item._item_model.Status.Correct
            )

        return qt_item

    def get_resources_query(self):
        return self._resources_query

    def gui_get_selected_resources(self):
        list_ = []
        _ = self._qt_tree_widget._view_model.get_selected_items()
        for i in _:
            i_resource = i._item_model.get_assign_data('dcc_resource')
            if i_resource is not None:
                list_.append(i_resource)
        return list_


# basic toolset
class _PrxImportToolset(_abs_unit_for_task_tool.AbsPrxToolsetForTaskTool):
    GUI_KEY = 'import'

    def get_dcc_character_args(self):
        results = []
        namespaces = qsm_mya_core.Namespaces.extract_from_selection()
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

    def on_gui_refresh_by_version_directory_changing(self):
        directory_path = self._prx_options_node.get(
            'cache_directory.version_directory'
        )
        if not directory_path:
            return

        pot = self._prx_options_node.get_port('cache_directory.file_tree')
        pot.set_root(directory_path)

        ptn = qsm_mya_hdl_gnl_core.FilePatterns.CfxClothAbcFile
        ptn_opt = bsc_core.BscStgParseOpt(
            ptn
        )
        ptn_opt.update_variants(directory=directory_path)
        abc_paths = ptn_opt.get_match_results()
        pot.set(abc_paths)

    def on_dcc_load_cloth_cache_by_checked(self):
        directory_path = self._prx_options_node.get(
            'cache_directory.version_directory'
        )
        if not directory_path:
            return

        pot = self._prx_options_node.get_port('cache_directory.file_tree')

        resources_query = self._unit._gui_resource_view_opt.get_resources_query()

        cache_paths = pot.get_all(check_only=True)
        if cache_paths:
            ptn = qsm_mya_hdl_gnl_core.FilePatterns.CfxClothAbcFile
            ptn_opt = bsc_core.BscStgParseOpt(
                ptn
            )
            with self._window.gui_progressing(
                maximum=len(cache_paths), label='load cfx clothes'
            ) as g_p:
                for i_cache_path in cache_paths:
                    if ptn_opt.check_is_matched(i_cache_path) is True:
                        i_properties = ptn_opt.get_variants(i_cache_path)
                        i_resource = resources_query.get(i_properties['namespace'])
                        if i_resource:
                            i_resource_opt = _shot_cfx_cloth_scripts.ShotCfxClothCacheOpt(i_resource)
                            i_resource_opt.load_cache(i_cache_path)

                    g_p.do_update()

    def on_dcc_remove_cloth_cache_by_selected(self):
        rig_namespaces = self.get_dcc_character_args()
        if rig_namespaces:
            with self._window.gui_progressing(
                maximum=len(rig_namespaces), label='load cfx rig'
            ) as g_p:
                for i_rig_namespace in rig_namespaces:
                    i_resource = qsm_mya_hdl_anm_core.AdvRigAsset(i_rig_namespace)
                    i_opt = _shot_cfx_cloth_scripts.ShotCfxClothCacheOpt(i_resource)
                    i_opt.remove_cache()

                g_p.do_update()

    def __init__(self, *args, **kwargs):
        super(_PrxImportToolset, self).__init__(*args, **kwargs)

        self._prx_options_node.get_port(
            'cache_directory.version_directory'
        ).connect_input_changed_to(
            self.on_gui_refresh_by_version_directory_changing
        )

        self._prx_options_node.set(
            'cache_import.load_cloth_cache',
            self.on_dcc_load_cloth_cache_by_checked
        )

        self._prx_options_node.set(
            'cache_import.remove_cloth_cache',
            self.on_dcc_remove_cloth_cache_by_selected
        )

    def do_gui_refresh_all(self):
        if self._page._task_session:
            cache_directory_path = self._page._task_session.get_file_for(
                'shot-source-maya-cfx_cache-dir', task='cfx_cloth'
            )
            if bsc_storage.StgPath.get_is_directory(cache_directory_path):
                directory_paths = bsc_storage.StgDirectoryOpt(
                    cache_directory_path
                ).get_directory_paths()
                if directory_paths:
                    self._prx_options_node.set(
                        'cache_directory.version_directory', directory_paths[-1]
                    )


class PrxToolsetForShotCfxDressingTool(_abs_unit_for_task_tool.AbsPrxUnitForTaskTool):
    GUI_KEY = 'cfx_dressing'

    GUI_RESOURCE_VIEW_CLS = _PrxNodeView

    TOOLSET_CLASSES = [
        _PrxImportToolset,
    ]

    TASK_TOOL_OPT_CLS = _gui_task_tool_opt.MayaShotCfxDressingToolOpt

    def __init__(self, *args, **kwargs):
        super(PrxToolsetForShotCfxDressingTool, self).__init__(*args, **kwargs)

