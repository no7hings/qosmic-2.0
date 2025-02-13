# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.resource as bsc_resource

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_maya.core as qsm_mya_core

from .pages import character_and_prop as _page_character_and_prop

from .pages import scenery as _page_scenery


class PrxLazyAnimation(gui_prx_widgets.PrxBasePanel):
    SCRIPT_JOB_NAME = 'lazy_tool_for_animation'

    # CONFIGURE_KEY = 'lazy-animation/gui/tool'

    HST_TAB_KEY_CURRENT = 'lazy-animation-tool.page_key_current'

    def do_gui_refresh_scene_info(self):
        pass

    def _do_dcc_register_all_script_jobs(self):
        self._script_job_opt = qsm_mya_core.ScriptJobOpt(
            self.SCRIPT_JOB_NAME
        )

        self._script_job_opt.register(
            self.do_gui_refresh_scene_info,
            self._script_job_opt.EventTypes.Test
        )

    def _do_dcc_destroy_all_script_jobs(self):
        self._script_job_opt.destroy()

    def __init__(self, window, session, *args, **kwargs):
        super(PrxLazyAnimation, self).__init__(window, session, *args, **kwargs)

    # noinspection PyUnresolvedReferences
    def gui_setup_fnc(self):
        self._page_prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._page_prx_tab_tool_box)
        # rig
        rig_prx_sca = gui_prx_widgets.PrxVScrollArea()
        self._page_prx_tab_tool_box.add_widget(
            rig_prx_sca,
            key='rig',
            name=gui_core.GuiUtil.choice_gui_name(
                self._language, self._window._configure.get('build.rig.tab')
            ),
            icon_name_text='rig',
            tool_tip=gui_core.GuiUtil.choice_gui_tool_tip(
                self._language, self._window._configure.get('build.rig.tab')
            )
        )

        self._chr_and_prp_prx_page = _page_character_and_prop.PrxPageForCharacterAndProp(
            self, self._session
        )
        rig_prx_sca.add_widget(self._chr_and_prp_prx_page)
        # scenery
        scenery_prx_sca = gui_prx_widgets.PrxVScrollArea()
        self._page_prx_tab_tool_box.add_widget(
            scenery_prx_sca,
            key='scenery',
            name=gui_core.GuiUtil.choice_gui_name(
                self._language, self._window._configure.get('build.scenery.tab')
            ),
            icon_name_text='scenery',
            tool_tip=gui_core.GuiUtil.choice_gui_tool_tip(
                self._language, self._window._configure.get('build.scenery.tab')
            )
        )

        self._scenery_prx_page = _page_scenery.PrxPageForScenery(
            self, self._session
        )
        scenery_prx_sca.add_widget(self._scenery_prx_page)

        self.connect_refresh_action_for(
            lambda: self.do_gui_refresh_all(True)
        )

        self._page_prx_tab_tool_box.connect_current_changed_to(
            self.do_gui_refresh_all
        )
        self._page_prx_tab_tool_box.set_history_key('resource-manager.page_key_current')
        self._page_prx_tab_tool_box.load_history()

        self.register_window_close_method(
            self.gui_close_fnc
        )

        self._do_dcc_register_all_script_jobs()
        self._window.register_window_close_method(self._do_dcc_destroy_all_script_jobs)

        self.do_gui_refresh_all()

    def gui_setup_post_fnc(self):
        self._chr_and_prp_prx_page.gui_setup_post_fnc()
        self._scenery_prx_page.gui_setup_post_fnc()

    def do_gui_refresh_all(self, force=False):
        key = self._page_prx_tab_tool_box.get_current_key()
        if key == 'rig':
            self._chr_and_prp_prx_page.do_gui_refresh_all(force)
        elif key == 'scenery':
            self._scenery_prx_page.do_gui_refresh_all(force)

    def gui_close_fnc(self):
        self._page_prx_tab_tool_box.save_history()
        self._chr_and_prp_prx_page._page_prx_tab_tool_box.save_history()
        self._scenery_prx_page._page_prx_tab_tool_box.save_history()
