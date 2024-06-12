# coding:utf-8
import copy

import functools

import six

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.pinyin as bsc_pinyin

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.abstracts as gui_prx_abstracts

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_screw.core as qsm_scr_core


class AbsPrxPageForRegister(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_widgets.QtTranslucentWidget

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForRegister, self).__init__(*args, **kwargs)

        self._window = window
        self._session = session

        self._scr_stage = qsm_scr_core.Stage(
            'Z:/libraries/screw/.database/node.db'
            # 'Z:/libraries/media/.database/video.db'
        )
        self._scr_stage.connect()

        self._window.connect_window_close_to(self._scr_stage.close)

        self.gui_setup_page()

    def gui_setup_page(self):
        qt_v_lot_0 = gui_qt_widgets.QtVBoxLayout(self._qt_widget)
        qt_v_lot_0.setContentsMargins(*[0]*4)
        qt_v_lot_0.setSpacing(2)

    def do_gui_refresh_all(self):
        pass
