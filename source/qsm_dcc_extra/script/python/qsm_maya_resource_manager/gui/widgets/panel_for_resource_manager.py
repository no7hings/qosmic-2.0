# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.resource as bsc_resource

import lxgui.core as gui_core

import lxgui.proxy.widgets as prx_widgets

from . import unit_for_rig_resource as _unit_for_rig_resource

from . import unit_for_scenery_resource as _unit_for_scenery_resource


class PrxPnlResourceManager(prx_widgets.PrxSessionWindow):
    HST_TAB_KEY_CURRENT = 'resource-manager.page_key_current'

    def __init__(self, session, *args, **kwargs):
        super(PrxPnlResourceManager, self).__init__(session, *args, **kwargs)

    def gui_setup_window(self):
        self.set_main_style_mode(1)
        self._prx_tab_view = prx_widgets.PrxTabView()
        self.add_widget(self._prx_tab_view)
        # rig
        rig_prx_sca = prx_widgets.PrxVScrollArea()
        self._prx_tab_view.add_widget(
            rig_prx_sca,
            key='rig',
            name=gui_core.GuiUtil.choice_name(
                self._language, self._session.configure.get('build.tabs.rig')
            ),
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._language, self._session.configure.get('build.tabs.rig')
            )
        )

        self._rig_prx_unit = _unit_for_rig_resource.PrxUnitForRigResource(
            self, self._session
        )
        rig_prx_sca.add_widget(self._rig_prx_unit)
        # scenery
        scenery_prx_sca = prx_widgets.PrxVScrollArea()
        self._prx_tab_view.add_widget(
            scenery_prx_sca,
            key='scenery',
            name=gui_core.GuiUtil.choice_name(
                self._language, self._session.configure.get('build.tabs.scenery')
            ),
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._language, self._session.configure.get('build.tabs.scenery')
            )
        )

        self._scenery_prx_unit = _unit_for_scenery_resource.PrxUnitForSceneryResource(
            self, self._session
        )
        scenery_prx_sca.add_widget(self._scenery_prx_unit)

        self.connect_refresh_action_for(
            lambda: self.do_gui_refresh_all(True)
        )

        self._prx_tab_view.connect_current_changed_to(
            self.do_gui_refresh_all
        )
        self._prx_tab_view.set_current_by_key(
            gui_core.GuiHistory.get_one(self.HST_TAB_KEY_CURRENT)
        )

        self.connect_window_close_to(
            self.gui_close_fnc
        )

        self.do_gui_refresh_all()

    def do_gui_refresh_all(self, force=False):
        key = self._prx_tab_view.get_current_key()
        if key == 'rig':
            self._rig_prx_unit.do_gui_refresh_all(force)
        elif key == 'scenery':
            self._scenery_prx_unit.do_gui_refresh_all(force)

    def gui_close_fnc(self):
        page_key_current = self._prx_tab_view.get_current_key()
        gui_core.GuiHistory.set_one(self.HST_TAB_KEY_CURRENT, page_key_current)

    def show_help(self):
        import os
        os.startfile(
            bsc_resource.ExtendResource.get(
                'docs/resource-manager.pdf'
            )
        )
