# coding:utf-8
import lxgui.proxy.core as gui_prx_core

import lxgui.proxy.widgets as gui_prx_widgets


def process_fnc_(w_):
    import qsm_general.process as qsm_gnl_process

    w_.start(
        qsm_gnl_process.MayaCacheProcess.generate_cmd_script(
            'method=test-process'
        )
    )


w = gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    gui_prx_widgets.PrxSprcTaskWindow, window_process_fnc=process_fnc_
)



