# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxgui.core as gui_core

import lxgui.proxy.widgets as prx_widgets

from . import unit_for_rig_resource as _unit_for_rig_resource


class PrxPnlResourceManager(prx_widgets.PrxSessionWindow):
    def __init__(self, session, *args, **kwargs):
        super(PrxPnlResourceManager, self).__init__(session, *args, **kwargs)

    def gui_setup_window(self):
        self._skin_proxy_load_args_array = []
        self._dynamic_gpu_load_args_array = []

        self.set_main_style_mode(1)
        self._tab_view = prx_widgets.PrxTabView()
        self.add_widget(self._tab_view)

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

        assembly_prx_sca = prx_widgets.PrxVScrollArea()
        self._tab_view.add_widget(
            assembly_prx_sca,
            key='assembly',
            name=gui_core.GuiUtil.choice_name(
                self._language, self._session.configure.get('build.tabs.assembly')
            ),
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._language, self._session.configure.get('build.tabs.assembly')
            )
        )

        self.connect_refresh_action_for(
            self.do_gui_refresh_all
        )

    def do_gui_refresh_all(self):
        key = self._tab_view.get_current_key()
        if key == 'rig':
            self._rig_prx_unit.do_gui_refresh_all()