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


class AbsPrxPageForComposition(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_widgets.QtTranslucentWidget

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForComposition, self).__init__(*args, **kwargs)
        
        self._window = window
        self._session = session
        
        self.gui_setup_page()

    def gui_build_stage(self):
        pass
    
    def do_gui_update_current_frame(self):
        pass

    @gui_qt_core.qt_slot()
    def do_dcc_motion_update(self):
        pass

    @gui_qt_core.qt_slot(int)
    def do_dcc_update_current_frame(self, frame):
        pass
    
    def gui_setup_page(self):
        v_qt_lot = gui_qt_widgets.QtVBoxLayout(self._qt_widget)
        v_qt_lot.setContentsMargins(*[0]*4)
        v_qt_lot.setSpacing(2)

        self._motion_prx_track_view = gui_prx_graphs.PrxTrackView()
        v_qt_lot.addWidget(self._motion_prx_track_view.widget)

        self._motion_prx_track_view.translate_graph_to(0, 0)
        self._motion_prx_track_view.scale_graph_to(0.05, 1)

        self._motion_prx_track_view.connect_stage_change_to(self.do_dcc_motion_update)
        self._motion_prx_track_view.connect_frame_accepted_to(self.do_dcc_update_current_frame)

        self.do_gui_refresh_all()

    def do_gui_refresh_all(self):
        self.gui_build_stage()
