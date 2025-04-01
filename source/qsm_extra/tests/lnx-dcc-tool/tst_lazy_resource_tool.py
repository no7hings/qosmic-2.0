# coding:utf-8
import lxgui.proxy.core as gui_prx_core

import lnx_dcc_tool.resource_cfx.gui.main as m

gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    m.PrxLazyResourceCfxTool, window=None, session=None
)
