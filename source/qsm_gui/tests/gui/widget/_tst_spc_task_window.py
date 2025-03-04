# coding:utf-8
import os

import functools

import lxgui.proxy.core as gui_prx_core

import lxgui.proxy.widgets as gui_prx_widgets


def process_fnc_(w_):
    def completed_fnc(index_):
        print(index_)

    import qsm_general.process as qsm_gnl_process

    for i in range(10):
        if i%2:
            i_cmd_script = qsm_gnl_process.MayaCacheSubprocess.generate_cmd_script(
                'method=test-process&tag=error'
            )
        else:
            i_cmd_script = qsm_gnl_process.MayaCacheSubprocess.generate_cmd_script(
                'method=test-process'
            )

        w_.submit(
            'TEST',
            '测试-{}'.format(i),
            i_cmd_script,
            completed_fnc=functools.partial(
                completed_fnc, i
            ),
            application='maya'
        )


os.environ['QSM_UI_LANGUAGE'] = 'chs'


w = gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    gui_prx_widgets.PrxSpcTaskWindow, window_process_fnc=process_fnc_
)
