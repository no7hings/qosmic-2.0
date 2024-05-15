# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.resource as bsc_resource

import lxgui.core as gui_core

import lxgui.proxy.widgets as prx_widgets

from . import unit_for_rig_resource as _unit_for_rig_resource

from . import unit_for_scenery_resource as _unit_for_scenery_resource


class PrxPnlResourceManager(prx_widgets.PrxSessionWindow):
    def __init__(self, session, *args, **kwargs):
        super(PrxPnlResourceManager, self).__init__(session, *args, **kwargs)

    def gui_setup_window(self):
        self.set_main_style_mode(1)
        self._tab_view = prx_widgets.PrxTabView()
        self.add_widget(self._tab_view)
        # rig
        rig_prx_sca = prx_widgets.PrxVScrollArea()
        self._tab_view.add_widget(
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
        self._tab_view.add_widget(
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

        self._tab_view.connect_current_changed_to(
            self.do_gui_refresh_all
        )
        self._tab_view.set_current_by_key('scenery')

    def do_gui_refresh_all(self, force=False):
        key = self._tab_view.get_current_key()
        if key == 'rig':
            self._rig_prx_unit.do_gui_refresh_all(force)
        elif key == 'scenery':
            self._scenery_prx_unit.do_gui_refresh_all(force)

    def show_help(self):
        import os
        os.startfile(
            bsc_resource.ExtendResource.get(
                'docs/resource-manager.pdf'
            )
        )
