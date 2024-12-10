# coding:utf-8
import copy

import functools

import six

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.resource as bsc_resource

import lxbasic.pinyin as bsc_pinyin

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.abstracts as gui_prx_abstracts

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.proxy.graphs as gui_prx_graphs

import qsm_scan as qsm_scan

import qsm_lazy.gui.proxy.widgets as lzy_gui_prx_widgets


class AbsPrxPageForSplicing(gui_prx_widgets.PrxBasePage):

    GUI_KEY = 'splicing'

    def _do_dcc_register_all_script_jobs(self):
        pass

    def _do_dcc_destroy_all_script_jobs(self):
        pass

    def _gui_add_main_tools(self, prx_tool_box):
        for i in [
            ('export', 'tool/export', 'Press to export motion', self._on_dcc_export_asset),
        ]:
            i_key, i_icon_name, i_tool_tip, i_fnc = i
            i_tool = gui_prx_widgets.PrxIconPressButton()
            prx_tool_box.add_widget(i_tool)
            i_tool.set_name(i_key)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip(i_tool_tip)
            i_tool.connect_press_clicked_to(i_fnc)

    def _gui_add_extra_tool(self, prx_tool_box):
        for i in [
            ('refresh', 'refresh', 'Press to refresh GUI', functools.partial(self.do_gui_refresh_all, force=True))
        ]:
            i_key, i_icon_name, i_tool_tip, i_fnc = i
            i_tool = gui_prx_widgets.PrxIconPressButton()
            prx_tool_box.add_widget(i_tool)
            i_tool.set_name(i_key)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip(i_tool_tip)
            i_tool.connect_press_clicked_to(i_fnc)

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForSplicing, self).__init__(window, session, *args, **kwargs)

        self.gui_page_setup_fnc()

    def gui_page_setup_fnc(self):
        self._scan_root = qsm_scan.Stage().get_root()

        self._top_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        self._qt_layout.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_align_left()
        self._top_prx_tool_bar.set_expanded(True)

        # main tool box
        self._main_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'main'
        )
        self._gui_add_main_tools(self._main_prx_tool_box)
        # load tool
        self._asset_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'load', size_mode=1
        )
        self._asset_prx_input = lzy_gui_prx_widgets.PrxInputForAssetCharacterAndProp()
        self._asset_prx_tool_box.add_widget(self._asset_prx_input)
        # self._asset_prx_input.widget.setMaximumWidth(840)

        self._asset_load_qt_button = gui_qt_widgets.QtPressButton()
        self._asset_prx_input.add_widget(self._asset_load_qt_button)
        self._asset_load_qt_button.setFixedWidth(64)
        self._asset_load_qt_button._set_name_text_(
            self._window.choice_gui_name(
                self._window._configure.get('build.{}.buttons.create'.format(self.GUI_KEY))
            )
        )
        self._asset_load_qt_button.press_clicked.connect(self._on_dcc_load_asset)
        self._asset_load_qt_button._set_action_enable_(False)

        self._asset_path = None

        self._asset_prx_input.connect_input_change_accepted_to(self._do_gui_refresh_resource_for)
        self._do_gui_refresh_resource_for(self._asset_prx_input.get_path())
        # extra
        self._extra_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'extra'
        )
        self._gui_add_extra_tool(self._extra_prx_tool_box)
        #
        self._prx_h_splitter_0 = gui_prx_widgets.PrxHSplitter()
        self._qt_layout.addWidget(self._prx_h_splitter_0.widget)
        # track
        self._motion_prx_track_widget = gui_prx_graphs.PrxTrackWidget()
        self._prx_h_splitter_0.add_widget(self._motion_prx_track_widget)

        self._motion_prx_track_widget.translate_graph_to(0, 0)
        self._motion_prx_track_widget.scale_graph_to(0.05, 1)

        self._motion_prx_track_widget.connect_stage_change_to(self.do_dcc_motion_update)
        self._motion_prx_track_widget.connect_frame_accepted_to(self.do_dcc_update_current_frame)
        # scene space
        self._scene_space_prx_unit = self.generate_unit_for('scene_space')
        self._prx_h_splitter_0.add_widget(self._scene_space_prx_unit)
        self._scene_space_prx_unit.connect_open_scene_to(self._open_scene_fnc)
        self._scene_space_prx_unit.connect_save_scene_to(self._save_scene_fnc)
        self._scene_space_prx_unit.update_scene_view()
        #
        self._prx_h_splitter_0.set_fixed_size_at(1, 240)
        # post method
        self._do_dcc_register_all_script_jobs()
        self._window.register_window_close_method(self._do_dcc_destroy_all_script_jobs)

        self._window.create_window_action_for(self._do_dcc_playback_swap, ' ')
        self._window.connect_window_activate_changed_to(self._do_check_update)

        self.do_gui_refresh_all()

    def gui_setup_post_fnc(self):
        self._top_prx_tool_bar.do_gui_refresh()

    def do_gui_refresh_all(self, force=False):
        self.gui_refresh_stage(force=force)

    def gui_refresh_stage(self, force=False):
        pass

    def gui_update_stage(self):
        pass

    @gui_qt_core.qt_slot()
    def do_dcc_motion_update(self):
        pass

    @gui_qt_core.qt_slot(int)
    def do_dcc_update_current_frame(self, frame):
        pass

    def _do_gui_update_current_frame(self, time):
        # update frame when dcc time is changed, but ignore when window is active
        if self._window.window_is_active() is False:
            self._motion_prx_track_widget.set_current_frame(int(time))

    def _do_dcc_playback_swap(self):
        pass

    def _do_check_update(self):
        pass

    def _open_scene_fnc(self, scene_path):
        return False

    def _save_scene_fnc(self, scene_path, thumbnail_path):
        return False
    
    def _do_gui_refresh_resource_for(self, path):
        self._asset_path = None
        self._asset_load_qt_button._set_action_enable_(False)
        entity = self._asset_prx_input.get_entity(path)
        if entity is not None:
            if entity.type == 'Asset':
                task = entity.task(self._scan_root.EntityTasks.Rig)
                if task is not None:
                    result = task.find_result(
                        self._scan_root.FilePatterns.MayaRigFile
                    )
                    if result is not None:
                        self._asset_path = result
                        self._asset_load_qt_button._set_action_enable_(True)

    def _on_dcc_load_asset(self):
        pass

    def _on_dcc_export_asset(self):
        pass
