# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.resource as bsc_resource

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

from . import page_for_playblast as _page_for_playblast


class PrxPanelForEasyPlayblast(gui_prx_widgets.PrxSessionWindow):
    def __init__(self, session, *args, **kwargs):
        super(PrxPanelForEasyPlayblast, self).__init__(session, *args, **kwargs)

    def gui_setup_window(self):
        prx_sca = gui_prx_widgets.PrxVScrollArea()
        self.add_widget(prx_sca)

        self._playblast_prx_page = _page_for_playblast.PrxPageForPlayblast(
            self, self._session
        )
        prx_sca.add_widget(self._playblast_prx_page)

