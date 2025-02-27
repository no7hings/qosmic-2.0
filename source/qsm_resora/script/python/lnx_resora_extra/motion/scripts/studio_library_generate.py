# coding:utf-8
import os

import qsm_general.process as qsm_gnl_process

import lnx_screw.core as lnx_scr_core


class STDotAnimGenerate(object):
    def __init__(self, scr_stage_name, scr_node_path):
        self._scr_stage_name = scr_stage_name
        self._scr_node_path = scr_node_path

    def generate_args(self):
        task_name = '[motion_generate][{}]'.format(self._scr_node_path)
        scr_stage = lnx_scr_core.Stage(self._scr_stage_name)
        stl_animation_source_path = scr_stage.get_node_parameter(self._scr_node_path, 'stl_animation_source')
        if not stl_animation_source_path:
            return None

        motion_json_path = scr_stage.generate_node_motion_json_path(self._scr_node_path, 'motion')
        if os.path.isfile(motion_json_path) is False:
            rig_maya_scene_path = scr_stage.get_node_parameter(self._scr_node_path, 'rig_maya_scene')
            cmd_script = qsm_gnl_process.MayaCacheSubprocess.generate_cmd_script_by_option_dict(
                'motion_generate',
                dict(
                    stl_animation_source_path=stl_animation_source_path,
                    rig_maya_scene_path=rig_maya_scene_path,
                    cache_file_path=motion_json_path,
                ),
                packages_extend=['studio_library']
            )
            scr_stage.close()
            return task_name, cmd_script
        scr_stage.close()
        return task_name, None

    def register(self):
        scr_stage = lnx_scr_core.Stage(self._scr_stage_name)
        motion_json_path = scr_stage.generate_node_motion_json_path(self._scr_node_path, 'motion')
        scr_stage.create_or_update_node_parameter(
            self._scr_node_path, 'motion', motion_json_path
        )
        scr_stage.close()
