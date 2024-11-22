# coding:utf-8
import qsm_maya_lazy_tool
reload(qsm_maya_lazy_tool)
qsm_maya_lazy_tool.do_reload()

import lxgui.proxy.core as gui_prx_core

import qsm_maya_lazy_tool.cfx.gui.main as main

gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    main.PrxLazyCfxTool, window=None, session=None
)
