# coding:utf-8
import os

from ...screw import core as _scr_core

import qsm_general.core as qsm_gnl_core


class StlConvertionOpt(object):
    def __init__(self, scr_stage_key, scr_node_path):
        self._scr_stage = _scr_core.Stage(scr_stage_key)
        self._scr_node_path = scr_node_path
        self._motion_json_path = self._scr_stage.generate_node_motion_json_path(self._scr_node_path, 'motion')

    def generate_args(self):
        task_name = '[stl-convertion][{}]'.format(self._scr_node_path)
        if os.path.isfile(self._motion_json_path) is False:
            stl_animation_source_path = self._scr_stage.get_node_parameter(self._scr_node_path, 'stl_animation_source')
            rig_maya_scene_path = self._scr_stage.get_node_parameter(self._scr_node_path, 'rig_maya_scene')
            cmd_script = qsm_gnl_core.MayaCacheProcess.generate_cmd_script_by_option_dict(
                'stl-convertion',
                dict(
                    stl_animation_source_path=stl_animation_source_path,
                    rig_maya_scene_path=rig_maya_scene_path,
                    cache_file_path=self._motion_json_path,
                ),
                packages_extend=['studio_library']
            )
            return task_name, cmd_script, self._motion_json_path
        return task_name, None, self._motion_json_path

    def register(self):
        self._scr_stage.create_or_update_parameters(
            self._scr_node_path, 'motion', self._motion_json_path
        )
