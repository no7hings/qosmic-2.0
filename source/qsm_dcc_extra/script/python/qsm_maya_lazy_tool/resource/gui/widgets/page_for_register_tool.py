# coding:utf-8
import qsm_lazy_tool.resource.gui.abstracts as _abstracts

import qsm_maya.core as qsm_mya_core

import qsm_maya.preview.core as qsm_mya_prv_core

import qsm_maya_resource.rebuild as qsm_mya_rsc_rebuild


class PrxPageForRegisterTool(_abstracts.AbsPrxPageForRegisterTool):
    SCRIPT_JOB_NAME = 'lazy_resource_register_tool'

    def do_gui_update_by_dcc_selection(self):
        self._node_opt = None
        self._type_prx_tag_input.clear_all_checked()
        self._prx_options_node.set(
            'gui_name_chs', '未命名'
        )
        node_paths = qsm_mya_core.Selection.get_as_nodes()
        if node_paths:
            search_scheme = self._prx_options_node.get('search_scheme')
            stage_key = self._prx_options_node.get('stage')
            if stage_key in {'maya_node', 'maya_node_test'}:
                node_opt = qsm_mya_rsc_rebuild.Generator.generate_one(
                    node_paths[0], search_scheme=search_scheme
                )
                if node_opt is not None:
                    self._node_opt = node_opt
                    scr_type_path = self._node_opt.to_scr_type_path()
                    if scr_type_path:
                        gui_name_chs = self._scr_stage.get_entity(
                            self._scr_stage.EntityTypes.Type, scr_type_path
                        ).gui_name_chs

                        self._prx_options_node.set(
                            'gui_name_chs', gui_name_chs
                        )

                        self._type_prx_tag_input.set_node_checked(
                            scr_type_path, True
                        )
                        self._type_prx_tag_input.expand_exclusive(
                            scr_type_path
                        )
        
        self._window.gui_set_buttons_enable(self._node_opt is not None)

    def do_show_playblast_window(self):
        camera_path = qsm_mya_core.Camera.get_active()
        resolution_size = (512, 512)
        qsm_mya_prv_core.Playblast.show_window(
            camera=camera_path,
            resolution=resolution_size,
            texture_enable=True, light_enable=False, shadow_enable=False,
            show_window=True,
            hud_enable=False
        )

    def do_create_playblast(self):
        movie_path = self._generate_screenshot_file_path()
        camera_path = qsm_mya_core.Camera.get_active()
        frame_range = qsm_mya_core.Frame.get_frame_range()
        play_enable = self._prx_options_node.get('playblast.play')
        frame_step = 1
        resolution_size = (512, 512)
        qsm_mya_prv_core.Playblast.execute(
            movie_path,
            camera=camera_path,
            resolution=resolution_size,
            frame=frame_range, frame_step=frame_step,
            texture_enable=True, light_enable=False, shadow_enable=False,
            show_window=False, play_enable=play_enable,
            hud_enable=False,
            use_exists_window=True
        )
        self._prx_options_node.get_port(
            'preview'
        ).append(
            movie_path
        )

    def get_data(self):
        if self._node_opt is not None:
            return self._node_opt.get_data()

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForRegisterTool, self).__init__(window, session, *args, **kwargs)

        self._node_opt = None

