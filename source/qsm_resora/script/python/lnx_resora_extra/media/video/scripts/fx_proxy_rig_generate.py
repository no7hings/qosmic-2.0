# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_general.process as qsm_gnl_process

import lnx_screw.core as lnx_scr_core


class FxProxyRigGenerateOpt(object):
    TASK_KEY = 'fx_proxy_rig_generate'

    def __init__(self, scr_stage_name, scr_node_path):
        self._scr_stage_name = scr_stage_name
        self._scr_node_path = scr_node_path

    def generate_args(self):
        scr_stage = lnx_scr_core.Stage(self._scr_stage_name)

        video_path = scr_stage.get_node_parameter(self._scr_node_path, 'source')
        if video_path:
            task_name = '[{}][{}]'.format(
                self.TASK_KEY, self._scr_node_path
            )
            rig_path = scr_stage.generate_node_maya_scene_path(self._scr_node_path, 'fx_proxy_rig')
            image_sequence_path = scr_stage.generate_node_image_sequence_path(self._scr_node_path)
            if bsc_storage.StgFileOpt(rig_path).get_is_file() is False:
                cmd_script = qsm_gnl_process.MayaCacheSubprocess.generate_cmd_script_by_option_dict(
                    self.TASK_KEY,
                    dict(
                        video_path=video_path,
                        image_sequence_path=image_sequence_path,
                        rig_path=rig_path,
                    )
                )
                return task_name, cmd_script
            return task_name, None

    def register(self):
        scr_stage = lnx_scr_core.Stage(self._scr_stage_name)
        rig_path = scr_stage.generate_node_maya_scene_path(self._scr_node_path, 'fx_proxy_rig')
        if bsc_storage.StgFileOpt(rig_path).get_is_file() is True:
            scr_stage.create_or_update_node_parameter(
                self._scr_node_path, 'fx_proxy_rig', rig_path
            )
