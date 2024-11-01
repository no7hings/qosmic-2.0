# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.qt.view_widgets as gui_qt_view_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_gui.proxy.widgets as qsm_gui_prx_widgets

import qsm_lazy.workspace.core as qsm_lzy_wsp_core


class AbsPrxPageForTaskPublish(gui_prx_widgets.PrxBasePage):
    PAGE_KEY = 'task_publish'

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForTaskPublish, self).__init__(window, session, *args, **kwargs)

        self._entity_properties = {}

