# coding:utf-8
import lxgeneral.dcc.core as gnl_dcc_core

import lxgui.proxy.core as gui_prx_core

import lxgui.proxy.widgets as gui_prx_widgets


def process_fnc_(w_):
    w_.start(
        gnl_dcc_core.PythonProcess.generate_command(
            'method=test'
        )
    )


w = gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    gui_prx_widgets.PrxSprcTaskWindow, window_process_fnc=process_fnc_, show_kwargs=dict(exclusive=False)
)
