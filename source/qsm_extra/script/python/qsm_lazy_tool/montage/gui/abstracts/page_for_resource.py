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

import lxgui.qt.graph_widgets as gui_qt_graphs


class AbsPrxPageForResource(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_widgets.QtTranslucentWidget

    GUI_KEY = 'resource'

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForResource, self).__init__(*args, **kwargs)

        self._window = window
        self._session = session

        self.gui_page_setup_fnc()

    def gui_page_setup_fnc(self):
        pass

    def do_gui_refresh_all(self, force=False):
        pass
