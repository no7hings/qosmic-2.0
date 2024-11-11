# coding:utf-8
import os

os.environ['QSM_UI_LANGUAGE'] = 'chs'

import lxgui.proxy.core as gui_prx_core

import qsm_lazy_tool.workspace.gui.widgets as gui_widgets

gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    gui_widgets.PrxPanelForAssetWorkspace, window=None, session=None
)
