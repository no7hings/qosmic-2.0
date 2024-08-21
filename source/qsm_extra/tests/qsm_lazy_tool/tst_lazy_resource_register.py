# coding:utf-8
import lxgui.proxy.core as gui_prx_core

import qsm_lazy_tool.resource.gui.widgets as gui_widgets

import os

os.environ['QSM_UI_LANGUAGE'] = 'chs'


def fnc(w):
    w.gui_setup_pages_for(['motion'])


gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    gui_widgets.PrxSubPanelForResourceRegister, window=None, session=None, window_process_fnc=fnc
)
