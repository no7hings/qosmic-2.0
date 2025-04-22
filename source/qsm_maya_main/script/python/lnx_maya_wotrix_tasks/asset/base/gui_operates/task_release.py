# coding:utf-8
import copy

# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lnx_wotrix.core as lnx_wtx_core

import qsm_maya.core as qsm_mya_core


class MayaAssetTaskReleaseOpt(lnx_wtx_core.DccTaskReleaseOpt):
    def __init__(self, *args, **kwargs):
        super(MayaAssetTaskReleaseOpt, self).__init__(*args, **kwargs)

    def release_scene_src(self, *args, **kwargs):
        # ensure source non changed to save
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

            version_dir_path_new = self._task_session.get_file_or_dir_for(
                'asset-release-version-dir', version=version_new
            )

            # release source_src file
            release_scene_src_path_new = self._task_session.get_file_or_dir_for(
                'asset-release-maya-scene_src-file', version=version_new
            )

            bsc_storage.StgFileOpt(source_scene_src_path).copy_to_file(
                release_scene_src_path_new
            )

            preview_path = self._task_session.get_file_or_dir_for(
                'asset-release-preview-mov-file', version=version_new
            )

            preview_scheme = kwargs.get('preview_scheme')
            if preview_scheme == 'image':
                images = kwargs.get('images')
                if images:
                    bsc_core.BscFfmpegVideo.concat_by_images(
                        preview_path, images
                    )
            elif preview_scheme == 'video':
                videos = kwargs.get('videos')
                if videos:
                    bsc_core.BscFfmpegVideo.concat_by_videos(
                        preview_path, videos
                    )

            return version_dir_path_new, release_scene_src_path_new, version_new
