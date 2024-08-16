# coding:utf-8
import lxgui.proxy.core as gui_prx_core

import qsm_lazy_tool.validation.gui.widgets as gui_widgets

import os

os.environ['QSM_UI_LANGUAGE'] = 'chs'

gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    gui_widgets.PrxPanelForValidation, session=None
)


