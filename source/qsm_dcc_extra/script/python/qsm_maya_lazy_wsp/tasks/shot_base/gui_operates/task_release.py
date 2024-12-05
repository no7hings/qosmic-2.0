# coding:utf-8
import copy

# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import qsm_lazy_wsp.core as lzy_wsp_core

import qsm_maya.core as qsm_mya_core


class MayaShotTaskReleaseOpt(lzy_wsp_core.DccTaskReleaseOpt):
    def __init__(self, *args, **kwargs):
        super(MayaShotTaskReleaseOpt, self).__init__(*args, **kwargs)

    def release_scene_src(self, *args, **kwargs):
        result = qsm_mya_core.SceneFile.ensure_save_width_dialog()
        if result is True:
            source_scene_src_path = self._properties['result']

            properties_new = copy.copy(self._properties)

            release_scene_src_path_latest = self._task_session.get_last_release_scene_src_file()
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

            version_number_new = self._task_session.generate_release_new_version_number()

            version_new = str(version_number_new).zfill(3)

            properties_new['version'] = str(version_number_new).zfill(3)

            version_dir_path_new = self._task_session.get_file_for(
                'shot-release-version-dir', version=version_new
            )

            # release source_src file
            release_scene_src_path_new = self._task_session.get_file_for(
                'shot-release-maya-scene_src-file', version=version_new
            )

            bsc_storage.StgFileOpt(source_scene_src_path).copy_to_file(
                release_scene_src_path_new
            )

            videos = kwargs.get('videos')
            if videos:
                preview_path = self._task_session.get_file_for(
                    'shot-release-preview-mov-file', version=version_new
                )
                bsc_storage.StgFileOpt(videos[0]).copy_to_file(preview_path)

            return version_dir_path_new, release_scene_src_path_new, version_new
