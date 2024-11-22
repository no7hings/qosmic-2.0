# coding:utf-8
import lxgui.proxy.core as gui_prx_core

import qsm_lazy_tool.validation.gui.main as m

import os

os.environ['QSM_UI_LANGUAGE'] = 'chs'

gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    m.PrxLazyValidationTool, session=None
)
