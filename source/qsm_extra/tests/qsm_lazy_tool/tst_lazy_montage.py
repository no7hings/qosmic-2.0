# coding:utf-8
import lxgui.proxy.core as gui_prx_core

import qsm_lazy_tool.montage.gui.widgets as gui_widgets

gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    gui_widgets.PrxSubPanelForMontage, window=None, session=None
)
