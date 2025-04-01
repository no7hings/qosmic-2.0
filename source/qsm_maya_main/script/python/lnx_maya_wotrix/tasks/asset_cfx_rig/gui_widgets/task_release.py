# coding:utf-8
import os

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

from lnx_wotrix.gui.abstracts import unit_for_task_release as _abs_unit_for_task_release

import qsm_general.process as qsm_dcc_process

import qsm_general.prc_task as qsm_gnl_prc_task

import qsm_maya.core as qsm_mya_core

from ..gui_operates import task_release as _task_release_opt

from .. import dcc_core as _task_dcc_core


class _PrxNodeView(_abs_unit_for_task_release.AbsPrxNodeViewForTaskRelease):
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
        super(_PrxNodeView, self).__init__(*args, **kwargs)

        self._qt_tree_widget._view.item_select_changed.connect(
            self.on_dcc_select_node
        )

    def do_gui_refresh_all(self, force=False):
        pass


class PrxToolsetForAssetCfxRigRelease(_abs_unit_for_task_release.AbsPrxUnitForTaskRelease):
    GUI_KEY = 'cfx_rig'

    GUI_RESOURCE_VIEW_CLS = _PrxNodeView

    TASK_RELEASE_OPT_CLS = _task_release_opt.MayaAssetCfxRigReleaseOpt

    def on_show_release_directory(self):
        task_session = self._page._task_session
        if task_session is not None:
            task_path = task_session.get_file_for('asset-release-task-dir')
            if task_path:
                if bsc_storage.StgPath.get_is_exists(task_path):
                    bsc_storage.StgExplorer.open_directory(task_path)
                else:
                    gui_core.GuiApplication.exec_message_dialog(
                        self.choice_gui_message(
                            self._configure.get('build.messages.no_record')
                        ),
                        status='warning'
                    )

    def on_release(self):
        preview_scheme = self._prx_options_node.get('preview_scheme')
        images = self._prx_options_node.get('images')
        videos = self._prx_options_node.get('videos')

        rig_variant = self._prx_options_node.get('rig_variant')

        if self._task_release_opt is not None:
            if self._task_release_opt.check_sync_server_is_available() is False:
                return

            # release source
            args = self._task_release_opt.release_scene_src(
                preview_scheme=preview_scheme, images=images, videos=videos
            )
            if args:
                release_version_dir_path, release_scene_src_path, version_new = args

                method = 'asset_cfx_rig_release'
                cmd_script = qsm_dcc_process.MayaTaskSubprocess.generate_cmd_script_by_option_dict(
                    method,
                    dict(
                        scene_src=release_scene_src_path,
                        rig_variant=rig_variant
                    )
                )

                task_name = '[{}][{}]'.format(method, os.path.basename(release_version_dir_path))

                qsm_gnl_prc_task.SubprocessTaskSubmit.execute_one(
                    task_name, cmd_script, completed_fnc=None,
                    window_title='Asset CFX Rig Release', window_title_chs='资产解算预设发布',
                )

    def __init__(self, *args, **kwargs):
        super(PrxToolsetForAssetCfxRigRelease, self).__init__(*args, **kwargs)

        self._prx_options_node.set(
            'show_release_directory', self.on_show_release_directory
        )

    @classmethod
    def get_rig_variants(cls):
        return [_task_dcc_core.AssetCfxRigHandle.get_rig_variant_name()]

    def do_gui_refresh_all(self):
        super(PrxToolsetForAssetCfxRigRelease, self).do_gui_refresh_all()

        options = self.get_rig_variants()
        p = self._prx_options_node.get_port('rig_variant')
        p.set_options(options)
        p.set(options[0])
