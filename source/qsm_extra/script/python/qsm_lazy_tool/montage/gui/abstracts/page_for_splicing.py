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

import lxgui.qt.graphs as gui_qt_graphs


class AbsPrxPageForSplicing(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_widgets.QtTranslucentWidget

    PAGE_KEY = 'splicing'

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForSplicing, self).__init__(*args, **kwargs)
        
        self._window = window
        self._session = session

        self.gui_setup_page()

    def gui_refresh_stage(self, force=False):
        pass

    @gui_qt_core.qt_slot()
    def do_dcc_motion_update(self):
        pass

    @gui_qt_core.qt_slot(int)
    def do_dcc_update_current_frame(self, frame):
        pass

    def _gui_add_main_tools(self):
        for i in [
            ('create', 'file/add-file', '', self._create_master_layer)
        ]:
            i_key, i_icon_name, i_tool_tip, i_fnc = i
            i_tool = gui_prx_widgets.PrxIconPressButton()
            self._main_prx_tool_box.add_widget(i_tool)
            i_tool.set_name(i_key)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip(i_tool_tip)
            i_tool.connect_press_clicked_to(i_fnc)

    def _create_master_layer(self):
        pass
    
    def gui_setup_page(self):
        qt_v_lot = gui_qt_widgets.QtVBoxLayout(self._qt_widget)
        qt_v_lot.setContentsMargins(*[0]*4)
        qt_v_lot.setSpacing(2)

        self._top_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        qt_v_lot.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_align_left()
        self._top_prx_tool_bar.set_expanded(True)
        
        # main tool box
        self._main_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'main'
        )

        self._gui_add_main_tools()

        self._motion_prx_track_view = gui_prx_graphs.PrxTrackView()
        qt_v_lot.addWidget(self._motion_prx_track_view.widget)

        self._motion_prx_track_view.translate_graph_to(0, 0)
        self._motion_prx_track_view.scale_graph_to(0.05, 1)

        self._motion_prx_track_view.connect_stage_change_to(self.do_dcc_motion_update)
        self._motion_prx_track_view.connect_frame_accepted_to(self.do_dcc_update_current_frame)

        self.do_gui_refresh_all()

    def do_gui_refresh_all(self, force=False):
        self.gui_refresh_stage(force=force)
