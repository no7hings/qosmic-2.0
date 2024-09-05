# coding:utf-8
import os

import qsm_general.core as qsm_gnl_core

from ...screw import core as _scr_core


class StlConvertionOpt(object):
    def __init__(self, scr_stage_key, scr_node_path):
        self._scr_stage_key = scr_stage_key
        self._scr_node_path = scr_node_path

    def generate_args(self):
        task_name = '[motion_generate][{}]'.format(self._scr_node_path)
        scr_stage = _scr_core.Stage(self._scr_stage_key)
        motion_json_path = scr_stage.generate_node_motion_json_path(self._scr_node_path, 'motion')
        if os.path.isfile(motion_json_path) is False:
            stl_animation_source_path = scr_stage.get_node_parameter(self._scr_node_path, 'stl_animation_source')
            rig_maya_scene_path = scr_stage.get_node_parameter(self._scr_node_path, 'rig_maya_scene')
            cmd_script = qsm_gnl_core.MayaCacheProcess.generate_cmd_script_by_option_dict(
                'motion_generate',
                dict(
                    stl_animation_source_path=stl_animation_source_path,
                    rig_maya_scene_path=rig_maya_scene_path,
                    cache_file_path=motion_json_path,
                ),
                packages_extend=['studio_library']
            )
            scr_stage.close()
            return task_name, cmd_script, motion_json_path
        scr_stage.close()
        return task_name, None, motion_json_path

    def register(self):
        scr_stage = _scr_core.Stage(self._scr_stage_key)
        motion_json_path = scr_stage.generate_node_motion_json_path(self._scr_node_path, 'motion')
        scr_stage.create_or_update_parameters(
            self._scr_node_path, 'motion', motion_json_path
        )
        scr_stage.close()
