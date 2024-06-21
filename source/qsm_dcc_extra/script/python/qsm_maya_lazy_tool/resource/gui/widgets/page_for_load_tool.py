# coding:utf-8
import random

import qsm_lazy_tool.resource.gui.abstracts as _abstracts

import qsm_maya.core as qsm_mya_core

import qsm_maya_resource.rebuild as qsm_mya_rsc_rebuild


class PrxPageForLoadTool(_abstracts.AbsPrxPageForLoad):
    SCRIPT_JOB_NAME = 'lazy_resource_load_tool'

    def do_gui_update_by_dcc_selection(self):
        self.do_dcc_update_node_opt()

        self._window.gui_set_buttons_enable(not not self._node_opt_list)

        self._prx_options_node.get_port('automatic.create_and_apply').set_action_enable(
            not not self._node_creator_list
        )

    def do_dcc_update_node_opt(self):
        self._node_opt_list = []
        self._node_creator_list = []

        json_path = self._prx_options_node.get('file')
        if not json_path:
            return

        stage_key = self._prx_options_node.get('stage')
        search_scheme = self._prx_options_node.get('search_scheme')
        if not self._node_rebuild_data:
            return

        path_map = qsm_mya_core.Selection.get_path_map()
        if not path_map:
            return

        if stage_key in {'maya_node', 'maya_node_test'}:
            scheme_src = self._node_rebuild_data['scheme']
            node_opt_list = qsm_mya_rsc_rebuild.Generator.generate_all(
                path_map.keys(), scheme=scheme_src, search_scheme=search_scheme
            )
            if node_opt_list:
                self._node_opt_list = node_opt_list
                return

            node_creator_list = qsm_mya_rsc_rebuild.Generator.generate_creators(path_map, scheme_src)
            if node_creator_list:
                self._node_creator_list = node_creator_list

    def generate_frame_offset_values(self):
        random_enable = self._prx_options_node.get('animation.frame_offset.random')
        frame_offset = self._prx_options_node.get('animation.frame_offset.value')
        if random_enable:
            if frame_offset != 0:
                if frame_offset < 0:
                    return range(frame_offset, 0)
                return range(frame_offset)
        return [0]

    @qsm_mya_core.Undo.execute
    def ao_apply(self):
        random.seed(0)
        frame_offset_values = self.generate_frame_offset_values()
        if self._node_opt_list and self._node_rebuild_data is not None:
            [
                x.apply_data(
                    self._node_rebuild_data,
                    frame_offset=random.choice(frame_offset_values),
                    force=self._prx_options_node.get('animation.force'),
                    excludes=self.generate_excludes(),
                    key_includes=self.generate_key_includes()
                )
                for x in self._node_opt_list
            ]

    @qsm_mya_core.Undo.execute
    def do_create_and_apply(self):
        random.seed(0)
        frame_offset_values = self.generate_frame_offset_values()
        if self._node_creator_list is not None:
            for i_creator in self._node_creator_list:
                i_opt = i_creator.do_create()
                if i_opt is not None:
                    i_opt.apply_data(
                        self._node_rebuild_data,
                        frame_offset=random.choice(frame_offset_values),
                        force=self._prx_options_node.get('animation.force'),
                        excludes=self.generate_excludes(),
                        key_includes=self.generate_key_includes()
                    )

        self.do_gui_update_by_dcc_selection()

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForLoadTool, self).__init__(window, session, *args, **kwargs)

    def do_gui_refresh_all(self):
        super(PrxPageForLoadTool, self).do_gui_refresh_all()
        self.do_gui_update_by_dcc_selection()
