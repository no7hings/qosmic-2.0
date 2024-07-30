# coding:utf-8
import random

import qsm_lazy.core as qsm_lzy_core

import qsm_lazy_tool.resource.gui.abstracts as _abstracts

import qsm_maya.core as qsm_mya_core

import qsm_maya_lazy.resource as qsm_mya_lzy_resource


class PrxPageForLoadTool(_abstracts.AbsPrxPageForLoadTool):
    SCRIPT_JOB_NAME = 'lazy_resource_load_tool'

    def do_gui_update_by_dcc_selection(self):
        self.do_gui_update_node_opt_by_dcc_selection()

        self._window.gui_set_buttons_enable(not not self._dcc_node_opt_list or self._dcc_node_graph_opt is not None)

        self._prx_options_node.get_port('automatic.create_and_apply').set_action_enable(
            not not self._dcc_node_creator_list
        )

    def do_gui_update_node_opt_by_dcc_selection(self):
        self._dcc_node_opt_list = []
        self._dcc_node_creator_list = []

        self._dcc_node_graph_opt = None

        data_file = self._prx_options_node.get('file')
        if not data_file:
            return

        data_type = self.get_resource_data_type()
        if data_type == qsm_lzy_core.DataTypes.MayaNode:
            path_map = qsm_mya_core.Selection.get_path_map()
            if not path_map:
                return

            if not self._lzy_data_for_node:
                return

            node_scheme = self._lzy_data_for_node['scheme']
            self.do_gui_update_node_opt_by_dcc_selection_for_dynamic(
                path_map, node_scheme
            )
        elif data_type == qsm_lzy_core.DataTypes.MayaNodeGraph:
            self.do_gui_update_node_graph_opt_for_any()

    def do_gui_update_node_opt_by_dcc_selection_for_dynamic(self, path_map, node_scheme):
        node_opt_list = qsm_mya_lzy_resource.DynamicGenerator.generate_node_opts(
            path_map.keys(), scheme=node_scheme
        )
        if node_opt_list:
            self._dcc_node_opt_list = node_opt_list
            return

        node_creator_list = qsm_mya_lzy_resource.DynamicGenerator.generate_node_creators(path_map, node_scheme)
        if node_creator_list:
            self._dcc_node_creator_list = node_creator_list

    def do_gui_update_node_graph_opt_for_any(self):
        node_graph_opt = qsm_mya_lzy_resource.BaseGenerator.generate_node_graph_opt([])
        if node_graph_opt is not None:
            self._dcc_node_graph_opt = node_graph_opt

    def generate_frame_offset_values(self):
        random_enable = self._prx_options_node.get('animation.frame_offset.random_enable')
        frame_offset = self._prx_options_node.get('animation.frame_offset.value')
        if random_enable is True:
            random_range = self._prx_options_node.get('animation.frame_offset.random_range')
            return range(*random_range)
        return [frame_offset]

    @qsm_mya_core.Undo.execute
    def do_apply(self):
        frame_offset_values = self.generate_frame_offset_values()
        if self._dcc_node_opt_list and self._lzy_data_file_path is not None:
            [
                x.apply_data(
                    self._lzy_data_file_path,
                    frame_offset=random.choice(frame_offset_values),
                    force=self._prx_options_node.get('animation.force'),
                    excludes=self.generate_excludes(),
                    key_includes=self.generate_key_includes()
                )
                for x in self._dcc_node_opt_list
            ]

        if self._dcc_node_graph_opt is not None:
            self._dcc_node_graph_opt.apply_data(
                self._lzy_data_file_path,
                frame_offset=random.choice(frame_offset_values)
            )

    @qsm_mya_core.Undo.execute
    def do_create_and_apply(self):
        random.seed(0)
        frame_offset_values = self.generate_frame_offset_values()
        if self._dcc_node_creator_list is not None:
            for i_creator in self._dcc_node_creator_list:
                i_opt = i_creator.do_create()
                if i_opt is not None:
                    i_opt.apply_data(
                        self._lzy_data_file_path,
                        frame_offset=random.choice(frame_offset_values),
                        force=self._prx_options_node.get('animation.force'),
                        excludes=self.generate_excludes(),
                        key_includes=self.generate_key_includes()
                    )

        self.do_gui_update_by_dcc_selection()

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForLoadTool, self).__init__(window, session, *args, **kwargs)

        random.seed(0)

    def do_gui_refresh_all(self):
        super(PrxPageForLoadTool, self).do_gui_refresh_all()
        self.do_gui_update_by_dcc_selection()
