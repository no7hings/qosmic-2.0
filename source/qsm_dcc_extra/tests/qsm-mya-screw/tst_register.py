# coding:utf-8
import lxbasic.core as bsc_core

import lxgui

lxgui.do_reload()

bsc_core.PyReloader2(
    ['lxbasic', 'lxgui', 'qsm_general', 'qsm_maya', 'qsm_lazy_tool', 'qsm_maya_lazy_tool']
).do_reload()


import lxgui.proxy.core as gui_prx_core

import qsm_maya_lazy_tool.resource.gui.widgets as gui_widgets

gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    gui_widgets.PrxSubPanelForRegister, window=None, session=None
)
