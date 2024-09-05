# coding:utf-8
import lxgeneral.dcc.core as gnl_dcc_core

import lxgui.proxy.core as gui_prx_core

import lxgui.proxy.widgets as gui_prx_widgets


def process_fnc_(w_):
    import qsm_general.core as qsm_gnl_core

    w_.start(
        qsm_gnl_core.MayaCacheProcess.generate_command(
            'method=test-process'
        )
    )


w = gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    gui_prx_widgets.PrxSprcTaskWindow, window_process_fnc=process_fnc_
)



