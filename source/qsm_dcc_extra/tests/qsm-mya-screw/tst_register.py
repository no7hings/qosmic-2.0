# coding:utf-8
import lxbasic.core as bsc_core

import lxgui

lxgui.do_reload()

bsc_core.PyReloader2(
    ['lxbasic', 'lxgui', 'qsm_general', 'qsm_maya', 'qsm_lazy_tool', 'qsm_maya_lazy_tool']
).do_reload()


import lxgui.proxy.core as gui_prx_core

import qsm_maya_lazy_tool.resource_cfx.gui.main as m

gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    m.PrxLazyResourceCfxTool, window=None, session=None
)
