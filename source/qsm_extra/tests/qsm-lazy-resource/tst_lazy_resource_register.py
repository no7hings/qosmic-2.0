# coding:utf-8
import lxgui.proxy.core as gui_prx_core

import qsm_lazy_tool.resource.gui.subpanels.register as p

import os

os.environ['QSM_UI_LANGUAGE'] = 'chs'


def fnc(w):
    scr_stage_type = 'video'
    w.gui_setup_pages_for([scr_stage_type])
    page = w.gui_find_page(scr_stage_type)
    if page is not None:
        page.set_scr_stage_key('video_test')


gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    p.PrxSubPanelForRegister, window=None, session=None, window_process_fnc=fnc
)
