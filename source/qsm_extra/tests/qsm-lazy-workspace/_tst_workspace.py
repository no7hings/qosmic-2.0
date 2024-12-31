# coding:utf-8
import os

os.environ['QSM_UI_LANGUAGE'] = 'chs'

import lxgui.proxy.core as gui_prx_core

import qsm_lazy_wsp.gui.main as m

gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    m.PrxLazyWorkspaceTool, window=None, session=None
)
