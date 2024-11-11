# coding:utf-8
import collections

import lxbasic.core as bsc_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.abstracts as prx_abstracts

import qsm_scan as qsm_scan


class PrxInputForResource(prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_widgets.QtTranslucentWidget

    class Schemes(object):
        Asset = 'asset'
        Shot = 'shot'

        All = [
            Asset,
            Shot,
        ]

    HISTORY_KEY = 'gui.input-entity-path-shot'

    def __init__(self, *args, **kwargs):
        super(PrxInputForResource, self).__init__(*args, **kwargs)

        l_0 = gui_qt_core.QtHBoxLayout(self._qt_widget)
        l_0.setContentsMargins(*[0]*4)
        l_0._set_align_as_top_()

        self._qt_scheme_input = gui_qt_widgets.QtInputForBubbleChoose()
        l_0.addWidget(self._qt_scheme_input)

        self._qt_scheme_input._set_choose_values_(
            self.Schemes.All, names=['资产', '镜头']
        )
        self._qt_scheme_input._set_value_(self.Schemes.Asset)
