# coding:utf-8
import os

import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core

import qsm_general.process as qsm_gnl_process

import qsm_screw.core as qsm_scr_core


class MoCapFbxMotionGenerateAuto(object):
    TASK_KEY = 'mocap_fbx_motion_generate_auto'

    def __init__(self, fbx_path):
        self._fbx_path = fbx_path

    def generate_args(self):
        fbx_path = self._fbx_path

        fbx_name = bsc_storage.StgFileOpt(fbx_path).name
        task_name = '[{}][{}]'.format(self.TASK_KEY, fbx_name)
        motion_json_path = qsm_gnl_core.DccCache.generate_fbx_motion_file(
            self._fbx_path, api_version=qsm_gnl_core.Montage.API_VERSION
        )

        if bsc_storage.StgPath.get_is_file(motion_json_path) is False:
            cmd_script = qsm_gnl_process.MayaCacheSubprocess.generate_cmd_script_by_option_dict(
                self.TASK_KEY,
                dict(
                    fbx_path=fbx_path,
                    motion_json_path=motion_json_path,
                )
            )
            return task_name, cmd_script, motion_json_path
        return task_name, None, motion_json_path
