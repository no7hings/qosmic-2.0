# coding:utf-8
import os

import lxbasic.core as bsc_core

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from . import adv_motion_export as _motion_export


class StlConvertionProcess(object):

    def __init__(self, stl_animation_source_path, rig_maya_scene_path, cache_file_path):
        self._stl_animation_source_path = bsc_core.BscStorage.shit_path_auto_convert(stl_animation_source_path)
        self._rig_maya_scene_path = bsc_core.BscStorage.shit_path_auto_convert(rig_maya_scene_path)
        self._cache_file_path = cache_file_path

    def execute(self):
        with bsc_log.LogProcessContext.create(maximum=4) as l_p:
            # step 1
            qsm_mya_core.SceneFile.new()
            l_p.do_update()
            # step 2
            if os.path.isfile(self._rig_maya_scene_path) is False:
                raise RuntimeError()

            namespace = bsc_storage.StgFileOpt(self._rig_maya_scene_path).name_base
            qsm_mya_core.SceneFile.reference_file(
                self._rig_maya_scene_path, namespace=namespace
            )
            l_p.do_update()

            directory_path_tmp = '{}/{}'.format(
                bsc_storage.StgUser.get_user_temporary_directory(),
                bsc_core.BscUuid.generate_new()
            )
            stg_directory_opt = bsc_storage.StgDirectoryOpt(self._stl_animation_source_path)
            anim_directory_path_tmp = '{}/{}'.format(directory_path_tmp, stg_directory_opt.name)
            maya_scene_file_path_tmp = '{}/scene.ma'.format(directory_path_tmp)

            bsc_storage.StgDirectoryOpt(
                self._stl_animation_source_path
            ).copy_all_files_to_directory(
                anim_directory_path_tmp
            )
            # noinspection PyUnresolvedReferences
            import mutils

            anim = mutils.Animation.fromPath(anim_directory_path_tmp)
            anim.load([], option=mutils.PasteOption.Replace, startFrame=1)

            # qsm_mya_core.SceneFile.save_to(maya_scene_file_path_tmp)
            _motion_export.AdvChrMotionExportOpt(
                namespace
            ).export(self._cache_file_path)


class StlBatchConvertionProcess(object):
    pass

