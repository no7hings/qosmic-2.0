# coding:utf-8
import lnx_maya_tool

lnx_maya_tool.do_reload()

import lxgui.proxy.core as gui_prx_core

import lnx_maya_tool.cfx.gui.main as main

gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    main.PrxLazyCfxTool, window=None, session=None
)
