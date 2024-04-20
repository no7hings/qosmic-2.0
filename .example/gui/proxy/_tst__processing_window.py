# coding:utf-8
import lxbasic.dcc.core as bsc_dcc_core

import lxgui.proxy.core as gui_prx_core

import lxgui.proxy.widgets as prx_widgets


def process_fnc_(w_):
    w_.start(
        bsc_dcc_core.PythonProcess.generate_command(
            'method=test'
        )
    )


w = gui_prx_core.GuiProxyUtil.show_window_proxy_auto(prx_widgets.PrxProcessingWindow, process_fnc=process_fnc_)


