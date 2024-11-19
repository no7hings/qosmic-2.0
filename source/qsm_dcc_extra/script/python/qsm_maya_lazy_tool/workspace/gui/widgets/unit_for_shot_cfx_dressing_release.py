# coding:utf-8
import os.path

from qsm_lazy_tool.workspace.gui.abstracts import unit_for_task_release as _abs_unit_for_task_publish

import qsm_general.process as qsm_dcc_process

import qsm_general.prc_task as qsm_gnl_prc_task

import qsm_maya.core as qsm_mya_core


class _GuiResourceViewOpt(_abs_unit_for_task_publish.AbsGuiNodeOptForTaskRelease):
    def on_dcc_select_node(self):
        selected_items = self._qt_tree_widget._view_model.get_selected_items()
        if selected_items:
            list_ = []
            for i in selected_items:
                i_node = i._item_model.get_assign_data('node')
                if i_node:
                    list_.append(i_node)

            qsm_mya_core.Selection.set(list_)
        else:
            qsm_mya_core.Selection.clear()

    def __init__(self, *args, **kwargs):
        super(_GuiResourceViewOpt, self).__init__(*args, **kwargs)

        self._qt_tree_widget._view.item_select_changed.connect(
            self.on_dcc_select_node
        )

    def do_gui_refresh_all(self, force=False):
        pass


class PrxToolsetForAssetCfxRigRelease(_abs_unit_for_task_publish.AbsPrxToolsetForTaskRelease):
    GUI_KEY = 'cfx_dressing'

    GUI_RESOURCE_VIEW_CLS = _GuiResourceViewOpt

    def on_release(self):
        videos = self._prx_options_node.get('videos')
        if self._task_release_opt is not None:
            args = self._task_release_opt.release_scene_src(videos=videos)
            if args:
                release_version_dir_path, release_scene_src_path, version_new = args

                method = 'shot_cfx_dressing_release'
                cmd_script = qsm_dcc_process.MayaTaskProcess.generate_cmd_script_by_option_dict(
                    method,
                    dict(
                        scene_src=release_scene_src_path
                    )
                )

                task_name = '[{}][{}]'.format(method, os.path.basename(release_version_dir_path))

                qsm_gnl_prc_task.SubprocessTaskSubmit.execute_one(
                    task_name, cmd_script, completed_fnc=None,
                    window_title='Shot CFX Dressing Release', window_title_chs='镜头解算整合发布',
                )

    def __init__(self, *args, **kwargs):
        super(PrxToolsetForAssetCfxRigRelease, self).__init__(*args, **kwargs)
