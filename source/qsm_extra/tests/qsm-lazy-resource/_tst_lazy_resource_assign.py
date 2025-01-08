# coding:utf-8
import lxgui.proxy.core as gui_prx_core

import qsm_lazy_rsc.gui.subpanels.assign as p

import os

os.environ['QSM_UI_LANGUAGE'] = 'chs'


def fnc(w):
    page_key = 'type'
    w.gui_setup_pages_for([page_key])
    page = w.gui_find_page(page_key)
    if page is not None:
        page.set_scr_stage_key('video_test')
        page.set_scr_node_paths(
            [
                '/3CDDDBF3-0E7A-E3B2-9289-4E382D5C0E29',
                '/3EADCB3D-FBA2-6598-4752-8BFD025D9456',
            ]
        )


gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    p.PrxSubPanelForAssign, window=None, session=None, window_process_fnc=fnc
)
