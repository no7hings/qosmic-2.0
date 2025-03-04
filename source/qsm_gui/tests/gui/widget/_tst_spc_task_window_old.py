# coding:utf-8
import os

import functools

import lxgui.proxy.core as gui_prx_core

import lxgui.proxy.widgets as gui_prx_widgets


def process_fnc_(w_):
    pass


os.environ['QSM_UI_LANGUAGE'] = 'chs'


w = gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    gui_prx_widgets.PrxSprcTaskWindow, window_process_fnc=process_fnc_
)
