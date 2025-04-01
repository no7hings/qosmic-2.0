# coding:utf-8
import qsm_lazy_tool.resource_cfx.gui.abstracts as _abstracts

import lnx_screw.core as lnx_scr_core

import qsm_maya.core as qsm_mya_core

import qsm_maya.handles.general.scripts as qsm_mya_hdl_gnl_scripts

import lnx_maya_tool_prc.resource as mya_lzy_rcs_scripts


class PrxPageForRegisterTool(_abstracts.AbsPrxPageForRegisterTool):
    SCRIPT_JOB_NAME = 'lazy_resource_register_tool'

    def do_gui_update_by_dcc_selection(self):
        self.do_gui_update_node_opt_by_dcc_selection()
        # node
        if self._dcc_node_opt is not None:
            scr_type_path = self._dcc_node_opt.to_scr_type_path()
            if scr_type_path:
                gui_name_chs = self._scr_stage.get_entity(
                    self._scr_stage.EntityTypes.Type, scr_type_path
                ).gui_name_chs

                self._prx_options_node.set(
                    'gui_name_chs', gui_name_chs
                )

                self._type_prx_tag_view.set_node_checked_for(
                    scr_type_path, True
                )
                self._type_prx_tag_view.expand_exclusive_for_node(
                    scr_type_path
                )
            else:
                self._prx_options_node.set(
                    'gui_name_chs', '未命名节点'
                )
                self._type_prx_tag_view.uncheck_all_items()
        # node graph
        elif self._dcc_node_graph_opt is not None:
            scr_type_path = '/node_graphs/component/regular'

            self._prx_options_node.set(
                'gui_name_chs', '未命名节点网络'
            )
            self._type_prx_tag_view.set_node_checked_for(
                scr_type_path, True
            )
            self._type_prx_tag_view.set_item_expand_below('/node_graphs')
        else:
            data_type = self.get_resource_data_type()
            if data_type == lnx_scr_core.DataTypes.MayaNode:
                self._prx_options_node.set(
                    'gui_name_chs', '未命名节点'
                )
            elif data_type == lnx_scr_core.DataTypes.MayaNodeGraph:
                self._prx_options_node.set(
                    'gui_name_chs', '未命名节点网络'
                )
            self._type_prx_tag_view.expand_all_group_items()
            self._type_prx_tag_view.uncheck_all_items()

        self._window.gui_set_buttons_enable(
            self._dcc_node_opt is not None or self._dcc_node_graph_opt is not None
        )

    def do_gui_update_node_opt_by_dcc_selection(self):
        self._dcc_node_opt = None
        self._dcc_node_graph_opt = None

        self._tag_prx_tag_view.uncheck_all_items()

        node_paths = qsm_mya_core.Selection.get_as_nodes()
        if node_paths:
            data_type = self.get_resource_data_type()
            stage_name = self._prx_options_node.get('stage')
            if stage_name in {'maya_cfx'}:
                if data_type == lnx_scr_core.DataTypes.MayaNode:
                    self.do_gui_update_node_opt_by_dcc_selection_for_dynamic(node_paths[0])
                elif data_type == lnx_scr_core.DataTypes.MayaNodeGraph:
                    self.do_gui_update_node_graph_opt_by_dcc_selection_for_any(node_paths)
            elif stage_name in {'maya_layout'}:
                if data_type == lnx_scr_core.DataTypes.MayaNodeGraph:
                    self.do_gui_update_node_graph_opt_by_dcc_selection_for_any(node_paths)

    def do_gui_update_node_opt_by_dcc_selection_for_dynamic(self, node_path):
        node_opt = mya_lzy_rcs_scripts.DynamicGenerator.generate_node_opt(node_path)
        if node_opt is not None:
            self._dcc_node_opt = node_opt

    def do_gui_update_node_graph_opt_by_dcc_selection_for_any(self, node_paths):
        node_graph_opt = mya_lzy_rcs_scripts.BaseGenerator.generate_node_graph_opt(node_paths)
        if node_graph_opt is not None:
            self._dcc_node_graph_opt = node_graph_opt

    def do_gui_update_node_opt_by_dcc_selection_for_look(self, node_path):
        node_opt = mya_lzy_rcs_scripts.LookGenerator.generate_node_opt(node_path)
        if node_opt is not None:
            self._dcc_node_opt = node_opt

    def do_gui_update_node_opt_by_dcc_selection_for_motion(self, node_path):
        node_opt = mya_lzy_rcs_scripts.MotionGenerator.generate_node_opt(node_path)
        if node_opt is not None:
            self._dcc_node_opt = node_opt

    def do_gui_update_node_opt_by_dcc_selection_for_scene(self, node_path):
        node_opt = mya_lzy_rcs_scripts.SceneGenerator.generate_node_opt(node_path)
        if node_opt is not None:
            self._dcc_node_opt = node_opt

    def do_show_playblast_window(self):
        camera_path = qsm_mya_core.Camera.get_active()
        resolution_size = (512, 512)
        qsm_mya_hdl_gnl_scripts.PlayblastOpt.show_window(
            camera=camera_path,
            resolution=resolution_size,
            texture_enable=True, light_enable=False, shadow_enable=False,
            show_window=True,
            hud_enable=False,
        )

    def do_create_playblast(self):
        movie_path = self._generate_screenshot_file_path()
        camera_path = qsm_mya_core.Camera.get_active()
        frame_range = qsm_mya_core.Frame.get_frame_range()
        play_enable = self._prx_options_node.get('playblast.play')
        frame_step = 1
        resolution_size = (512, 512)
        qsm_mya_hdl_gnl_scripts.PlayblastOpt.execute(
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
        data_type = self.get_resource_data_type()
        if data_type == lnx_scr_core.DataTypes.MayaNode:
            if self._dcc_node_opt is not None:
                return self._dcc_node_opt.get_data()
        elif data_type == lnx_scr_core.DataTypes.MayaNodeGraph:
            if self._dcc_node_graph_opt is not None:
                return self._dcc_node_graph_opt.get_data()

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForRegisterTool, self).__init__(window, session, *args, **kwargs)
