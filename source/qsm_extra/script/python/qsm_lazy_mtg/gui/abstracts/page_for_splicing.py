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
            # ('refresh', 'refresh', 'Press to refresh GUI', functools.partial(self.do_gui_refresh_all, force=True)),
            ('delete', 'montage/delete', 'Press to delete splicing', self._on_dcc_delete),
            ('bake', 'montage/bake-keyframe', 'Press to bake splicing', self._on_dcc_bake),
            ('look_from_persp_cam', 'tool/camera', 'Press Look from Persp Camera', self._on_dcc_look_from_persp_cam)
        ]:
            i_key, i_icon_name, i_tool_tip, i_fnc = i
            i_tool = gui_prx_widgets.PrxIconPressButton()
            prx_tool_box.add_widget(i_tool)
            i_tool.set_name(i_key)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip(i_tool_tip)
            i_tool.connect_press_clicked_to(i_fnc)

    def _gui_add_export_import_tools(self, prx_tool_box):
        for i in [
            ('export', 'montage/splicing-export', 'Press to export track', self._on_dcc_export),
            ('import', 'montage/splicing-import', 'Press to import track', self._on_dcc_import),
        ]:
            i_key, i_icon_name, i_tool_tip, i_fnc = i
            i_tool = gui_prx_widgets.PrxIconPressButton()
            prx_tool_box.add_widget(i_tool)
            i_tool.set_name(i_key)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip(i_tool_tip)
            i_tool.connect_press_clicked_to(i_fnc)

    def _gui_add_rig_switch_tools(self, prx_tool_box):
        self._rig_namespace_switch_qt_button = gui_qt_widgets.QtIconPressButton()
        prx_tool_box.add_widget(self._rig_namespace_switch_qt_button)
        self._rig_namespace_switch_qt_button._set_name_text_('rig namespace switch')
        self._rig_namespace_switch_qt_button._set_icon_name_('montage/layers')
        self._rig_namespace_switch_qt_button.press_clicked.connect(self._on_gui_switch_rig_namespace)

        self._rig_namespace_qt_info_bubble = gui_qt_widgets.QtInfoBubble()
        prx_tool_box.add_widget(self._rig_namespace_qt_info_bubble)
        self._rig_namespace_qt_info_bubble._set_style_(
            self._rig_namespace_qt_info_bubble.Style.Frame
        )
        self._rig_namespace_qt_info_bubble._set_text_(self._rig_namespace or 'N/a')

    def _dcc_get_rig_namespaces(self):
        return []

    def _dcc_set_current_rig_namespace(self, rig_namespace):
        pass

    def _dcc_get_current_rig_namespace(self):
        pass

    def _on_gui_switch_rig_namespace(self):
        options = self._dcc_get_rig_namespaces()
        if options:
            result = gui_core.GuiApplication.exec_input_dialog(
                type='choose',
                options=options,
                info='Choose Rig Namespace...',
                value=self._rig_namespace or options[0],
                title='Switch Namespace'
            )
            if result:
                self._gui_switch_rig_namespace(result)

    def _gui_switch_rig_namespace(self, rig_namespace):
        if rig_namespace != self._rig_namespace:
            self._rig_namespace = rig_namespace
            self._rig_namespace_qt_info_bubble._set_text_(self._rig_namespace)
            # gui_core.GuiHistory.set_one(self._artist_history_key, self._artist)

            self.do_gui_refresh_all(force=True)

            self._dcc_set_current_rig_namespace(self._rig_namespace)
            self._on_dcc_look_from_persp_cam()

            self._window.popup_message(
                self._window.choice_gui_message(
                    self._window._configure.get('build.messages.switch_rig_namespace')
                ).format(rig_namespace=self._rig_namespace)
            )

    def _gui_add_new_tool(self, prx_tool_box):
        self._new_splicing_qt_button = gui_qt_widgets.QtPressButton()
        prx_tool_box.add_widget(self._new_splicing_qt_button)
        self._new_splicing_qt_button._set_auto_width_(True)

        self._new_splicing_qt_button._set_name_text_(
            self._window.choice_gui_name(
                self._window._configure.get('build.buttons.new_splicing')
            )
        )
        self._new_splicing_qt_button._set_icon_name_('montage/splicing-new')
        self._new_splicing_qt_button.press_clicked.connect(
            self._on_gui_show_new_splicing_window
        )

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForSplicing, self).__init__(window, session, *args, **kwargs)

        self._rig_namespace = None

        self.gui_page_setup_fnc()

    def gui_page_setup_fnc(self):
        self._scan_root = qsm_scan.Stage().get_root()

        self._top_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        self._qt_layout.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_align_left()
        self._top_prx_tool_bar.set_expanded(True)

        # extra
        self._new_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'new'
        )
        self._gui_add_new_tool(self._new_prx_tool_box)

        # main tool box
        self._main_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'main'
        )
        self._gui_add_main_tools(self._main_prx_tool_box)

        self._export_import_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'export import'
        )
        self._gui_add_export_import_tools(self._export_import_prx_tool_box)

        self._rig_switch_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'rig switch'
        )
        self._gui_add_rig_switch_tools(self._rig_switch_prx_tool_box)
        # track
        self._motion_prx_track_widget = gui_prx_graphs.PrxTrackWidget()
        self._qt_layout.addWidget(self._motion_prx_track_widget.widget)

        self._motion_prx_track_widget.translate_graph_to(0, 0)
        self._motion_prx_track_widget.scale_graph_to(0.05, 1)

        self._motion_prx_track_widget.connect_stage_change_to(self.on_dcc_stage_update)
        self._motion_prx_track_widget.connect_frame_accepted_to(self.do_dcc_update_current_frame)

        self._motion_prx_track_widget._qt_widget.refresh.connect(
            functools.partial(self.do_gui_refresh_all, force=True)
        )
        # post method
        self._do_dcc_register_all_script_jobs()
        self._window.register_window_close_method(self._do_dcc_destroy_all_script_jobs)

        self._window.create_window_action_for(self._do_dcc_playback_swap, ' ')
        self._window.connect_window_activate_changed_to(self._do_check_update)

        self.do_gui_refresh_all()

    def gui_setup_post_fnc(self):
        self._top_prx_tool_bar.do_gui_refresh()

    def do_gui_refresh_all(self, force=False):
        self.gui_refresh_fnc(force=force)

    def gui_restore(self):
        self._rig_namespace = None

        self._rig_namespace_qt_info_bubble._set_text_(self._rig_namespace or 'N/a')

        self._motion_prx_track_widget.restore()

    def gui_refresh_fnc(self, force=False):
        pass

    @gui_qt_core.qt_slot()
    def on_dcc_stage_update(self):
        pass

    @gui_qt_core.qt_slot(int)
    def do_dcc_update_current_frame(self, frame):
        pass

    def _do_gui_update_current_frame(self, time):
        # update frame when dcc time is changed, but ignore when window is active
        if self._window.window_is_active() is False:
            self._motion_prx_track_widget.set_current_frame(int(time))

    def _do_dcc_playback_swap(self):
        self._motion_prx_track_widget._qt_widget._track_timeline._swap_autoplaying_()

    def _do_check_update(self):
        pass

    def _on_dcc_export(self):
        pass

    def _on_dcc_import(self):
        pass

    def _on_dcc_delete(self):
        pass

    def _on_dcc_bake(self):
        pass

    def _on_dcc_look_from_persp_cam(self):
        pass

    def _on_gui_show_new_splicing_window(self):
        w = self._window.gui_generate_sub_panel_for('new_splicing')
        w.do_gui_refresh_all()
        w.show_window_auto()
