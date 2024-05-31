# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.resource as bsc_resource

import lxgui.core as gui_core

import lxgui.proxy.widgets as prx_widgets

from . import page_for_playblast as _page_for_playblast


class PrxPanelForEasyPlayblast(prx_widgets.PrxSessionWindow):
    HST_TAB_KEY_CURRENT = 'resource-manager.page_key_current'

    def __init__(self, session, *args, **kwargs):
        super(PrxPanelForEasyPlayblast, self).__init__(session, *args, **kwargs)

    def gui_setup_window(self):
        prx_sca = prx_widgets.PrxVScrollArea()
        self.add_widget(prx_sca)

        self.playblast_prx_page = _page_for_playblast.PrxPageForRigResource(
            self, self._session
        )
        prx_sca.add_widget(self.playblast_prx_page)

