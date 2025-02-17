# coding:utf-8
import os

import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core

import qsm_general.process as qsm_gnl_process

import lnx_screw.core as lnx_scr_core


class MoCapDotFbxMotionGenerate(object):
    TASK_KEY = 'mocap_fbx_motion_generate'

    def __init__(self, scr_stage_name, scr_node_path):
        self._scr_stage_name = scr_stage_name
        self._scr_node_path = scr_node_path

    def generate_args(self):
        scr_stage = lnx_scr_core.Stage(self._scr_stage_name)

        fbx_path = scr_stage.get_node_parameter(self._scr_node_path, 'fbx_source')
        if not fbx_path:
            scr_stage.close()
            return

        fbx_name = bsc_storage.StgFileOpt(fbx_path).name
        task_name = '[{}][{}]'.format(self.TASK_KEY, fbx_name)
        motion_json_path = scr_stage.generate_node_motion_json_path(self._scr_node_path, 'motion')

        # check motion json file is existing, when True check API version
        if bsc_storage.StgPath.get_is_file(motion_json_path):
            data = bsc_storage.StgFileOpt(motion_json_path).set_read()
            api_version = data['metadata'].get('api_version')
            if api_version == qsm_gnl_core.Montage.API_VERSION:
                scr_stage.close()
                return task_name, None

        preview_mov_path = scr_stage.generate_node_preview_mov_path(self._scr_node_path)
        image_sequence_dir_path = scr_stage.generate_node_image_sequence_dir_path(self._scr_node_path)
        cmd_script = qsm_gnl_process.MayaCacheSubprocess.generate_cmd_script_by_option_dict(
            self.TASK_KEY,
            dict(
                fbx_path=fbx_path,
                motion_json_path=motion_json_path,
                preview_mov_path=preview_mov_path,
                image_sequence_dir_path=image_sequence_dir_path,
            )
        )
        scr_stage.close()
        return task_name, cmd_script
        # scr_stage.close()
        # return task_name, None

    def register(self):
        scr_stage = lnx_scr_core.Stage(self._scr_stage_name)
        motion_json_path = scr_stage.generate_node_motion_json_path(self._scr_node_path, 'motion')
        if bsc_storage.StgPath.get_is_file(motion_json_path) is False:
            return

        json_data = bsc_storage.StgFileOpt(motion_json_path).set_read()
        frame_count = json_data['frame_count']
        metadata = json_data['metadata']
        start_frame, end_frame = metadata['start_frame'], metadata['end_frame']
        image_sequence_dir_path = scr_stage.generate_node_image_sequence_dir_path(self._scr_node_path)
        image_sequence_path = '{}/image.%04d.jpg'.format(image_sequence_dir_path)
        scr_stage.create_or_update_node_parameter(self._scr_node_path, 'motion', motion_json_path)
        scr_stage.create_or_update_node_parameter(self._scr_node_path, 'image_sequence', image_sequence_path)
        scr_stage.create_or_update_node_parameter(self._scr_node_path, 'fps', metadata['fps'])
        scr_stage.create_or_update_node_parameter(self._scr_node_path, 'frame_count', frame_count)
        scr_stage.create_or_update_node_parameter(self._scr_node_path, 'start_frame', start_frame)
        scr_stage.create_or_update_node_parameter(self._scr_node_path, 'end_frame', end_frame)

        # remove process tag
        scr_stage.remove_assign(self._scr_node_path, '/mark/unprocessed')

        scr_stage.close()
