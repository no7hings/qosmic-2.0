# coding:utf-8
import lxgui
lxgui.do_reload()

import qsm_maya_lazy_tool
qsm_maya_lazy_tool.do_reload()

import lxgui.proxy.core as gui_prx_core

import qsm_maya_lazy_mtg.gui.main as m

gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    m.PrxLazyMontageTool, window=None, session=None
)
