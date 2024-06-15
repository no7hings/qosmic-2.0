# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_lazy_tool.resource.gui.abstracts as _abstracts

import qsm_maya.core as qsm_mya_core

import qsm_maya.preview.core as qsm_mya_prv_core

import qsm_maya_screw.core as qsm_mya_scr_core


class PrxPageForRegister(_abstracts.AbsPrxPageForRegister):
    SCRIPT_JOB_NAME = 'lazy_tool_for_resource'

    def _do_dcc_register_all_script_jobs(self):
        self._script_job = qsm_mya_core.ScriptJob(
            self.SCRIPT_JOB_NAME
        )
        self._script_job.register(
            [
                self.do_gui_update_by_dcc_selection,
            ],
            self._script_job.EventTypes.SelectionChanged
        )

    def _do_dcc_destroy_all_script_jobs(self):
        self._script_job.destroy()

    def show_playblast_window(self):
        camera_path = qsm_mya_core.Camera.get_active()
        resolution_size = (512, 512)
        qsm_mya_prv_core.Playblast.show_window(
            camera=camera_path,
            resolution=resolution_size,
            texture_enable=True, light_enable=False, shadow_enable=False,
            show_window=True,
            hud_enable=False
        )

    def create_playblast(self):
        movie_path = self._generate_screenshot_file_path()
        camera_path = qsm_mya_core.Camera.get_active()
        frame_range = qsm_mya_core.Frame.get_frame_range()
        frame_step = 1
        resolution_size = (512, 512)
        qsm_mya_prv_core.Playblast.execute(
            movie_path,
            camera=camera_path,
            resolution=resolution_size,
            frame=frame_range, frame_step=frame_step,
            texture_enable=True, light_enable=False, shadow_enable=False,
            show_window=False, play_enable=True,
            hud_enable=False
        )
        self._prx_options_node.get_port(
            'media'
        ).append(
            movie_path
        )

    def get_data(self):
        paths = cmds.ls(selection=1)
        if paths:
            qsm_mya_scr_core.Node.guess_scheme(paths[0])

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForRegister, self).__init__(window, session, *args, **kwargs)
        
        self._do_dcc_register_all_script_jobs()
        self._window.connect_window_close_to(self._do_dcc_destroy_all_script_jobs)

