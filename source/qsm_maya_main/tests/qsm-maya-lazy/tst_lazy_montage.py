# coding:utf-8
import lxgui
lxgui.do_reload()

import lnx_maya_montage
lnx_maya_montage.do_reload()

import lxgui.proxy.core as gui_prx_core

import lnx_maya_montage.gui.main as m

gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    m.PrxMontageTool, window=None, session=None
)
