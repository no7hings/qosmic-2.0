# coding:utf-8
import copy

# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import qsm_wsp_task as qsm_dcc_wsp_task

import qsm_maya.core as qsm_mya_core


class MayaAssetGnlReleaseOpt(qsm_dcc_wsp_task.DccTaskReleaseOpt):
    @classmethod
    def test(cls):
        from qsm_maya_wsp_task import task_parse

        task_parse = task_parse.TaskParse()

        task_session = task_parse.generate_task_session_by_resource_source_scene_src_auto()

        task_publish_opt = task_session.generate_task_release_opt()

        task_publish_opt.release_scene_src(
            images=[
                'C:/Users/nothings/screenshot/untitled-SMF3Y7.png',
                'C:/Users/nothings/screenshot/untitled-SMEUX4.png'
            ]
        )

    def __init__(self, *args, **kwargs):
        super(MayaAssetGnlReleaseOpt, self).__init__(*args, **kwargs)

    def release_scene_src(self, *args, **kwargs):
        result = qsm_mya_core.SceneFile.ensure_save_width_dialog()
        if result is True:
            source_scene_src_path = self._properties['result']

            properties_new = copy.copy(self._properties)

            release_scene_src_path_latest = self._task_session.get_latest_file_for(
                'asset-release-maya-scene_src-file'
            )
            if release_scene_src_path_latest:
                if bsc_storage.StgFileOpt(
                    source_scene_src_path
                ).get_timestamp_is_same_to(release_scene_src_path_latest):
                    if gui_core.GuiUtil.language_is_chs():
                        gui_core.GuiApplication.exec_message_dialog(
                            '没有修改可发布。',
                            title='任务发布',
                            size=(320, 120),
                            status='warning',
                        )
                    else:
                        gui_core.GuiApplication.exec_message_dialog(
                            'No changes to release.',
                            title='Task Release',
                            size=(320, 120),
                            status='warning',
                        )
                    return

            version_number_new = self._task_session.generate_asset_release_new_version_number()

            version_new = str(version_number_new).zfill(3)

            properties_new['version'] = str(version_number_new).zfill(3)

            # release source_src file
            release_scene_src_path_new = self._task_session.get_file_for(
                'asset-release-maya-scene_src-file', version=version_new
            )

            bsc_storage.StgFileOpt(source_scene_src_path).copy_to_file(
                release_scene_src_path_new
            )

            images = kwargs.get('images')
            if images:
                preview_path = self._task_session.get_file_for(
                    'asset-release-preview-file', version=version_new
                )
                bsc_core.BscFfmpeg.concat_images(
                    preview_path, images
                )
            return release_scene_src_path_new, version_new
