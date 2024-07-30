# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.resource as bsc_resource

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_maya.core as qsm_mya_core

from . import page_for_character_and_prop as _unit_for_rig_resource

from . import page_for_scenery as _unit_for_scenery_resource


class PrxPanelForAnimationTool(gui_prx_widgets.PrxSessionWindow):
    SCRIPT_JOB_NAME = 'lazy_tool_for_animation'

    def do_gui_refresh_scene_info(self):
        print "AAA"

    def _do_dcc_register_all_script_jobs(self):
        self._script_job = qsm_mya_core.ScriptJob(
            self.SCRIPT_JOB_NAME
        )

        self._script_job.register(
            self.do_gui_refresh_scene_info,
            self._script_job.EventTypes.Test
        )

    def _do_dcc_destroy_all_script_jobs(self):
        self._script_job.destroy()

    def __init__(self, session, *args, **kwargs):
        super(PrxPanelForAnimationTool, self).__init__(session, *args, **kwargs)

    # noinspection PyUnresolvedReferences
    def gui_setup_window(self):
        self._window = self
        self._configure = bsc_resource.RscExtendConfigure.get_as_content(
            'lazy-animation/gui/tool'
        )

        self.set_main_style_mode(1)
        self._prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._prx_tab_tool_box)
        # rig
        rig_prx_sca = gui_prx_widgets.PrxVScrollArea()
        self._prx_tab_tool_box.add_widget(
            rig_prx_sca,
            key='rig',
            name=gui_core.GuiUtil.choice_name(
                self._language, self._window._configure.get('build.rig.tab')
            ),
            icon_name_text='rig',
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._language, self._window._configure.get('build.rig.tab')
            )
        )

        self._rig_prx_page = _unit_for_rig_resource.PrxPageForCharacterAndProp(
            self, self._session
        )
        rig_prx_sca.add_widget(self._rig_prx_page)
        # scenery
        scenery_prx_sca = gui_prx_widgets.PrxVScrollArea()
        self._prx_tab_tool_box.add_widget(
            scenery_prx_sca,
            key='scenery',
            name=gui_core.GuiUtil.choice_name(
                self._language, self._window._configure.get('build.scenery.tab')
            ),
            icon_name_text='scenery',
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._language, self._window._configure.get('build.scenery.tab')
            )
        )

        self._scenery_prx_page = _unit_for_scenery_resource.PrxPageForSceneryResource(
            self, self._session
        )
        scenery_prx_sca.add_widget(self._scenery_prx_page)

        self.connect_refresh_action_for(
            lambda: self.do_gui_refresh_all(True)
        )

        self._prx_tab_tool_box.connect_current_changed_to(
            self.do_gui_refresh_all
        )
        self._prx_tab_tool_box.set_history_key('resource-manager.page_key_current')
        self._prx_tab_tool_box.load_history()

        self.register_window_close_method(
            self.gui_close_fnc
        )

        self._do_dcc_register_all_script_jobs()
        self._window.register_window_close_method(self._do_dcc_destroy_all_script_jobs)

        self.do_gui_refresh_all()

    def do_gui_refresh_all(self, force=False):
        key = self._prx_tab_tool_box.get_current_key()
        if key == 'rig':
            self._rig_prx_page.do_gui_refresh_all(force)
        elif key == 'scenery':
            self._scenery_prx_page.do_gui_refresh_all(force)

    def gui_close_fnc(self):
        self._prx_tab_tool_box.save_history()
        self._rig_prx_page._page_prx_tab_tool_box.save_history()
        self._scenery_prx_page._page_prx_tab_tool_box.save_history()

    def show_help(self):
        import os

        _0 = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
        if os.path.isfile(_0):
            cmd_script = '"{}" "{}"'.format(
                _0,
                bsc_resource.ExtendResource.get(
                    'docs/resource-manager.pdf'
                )
            )

            bsc_core.BscProcess.execute_use_thread(
                cmd_script
            )
        else:
            _1 = 'C:/Program Files (x86)/Adobe/Reader 11.0/Reader/AcroRd32.exe'
            if os.path.isfile(_1):
                cmd_script = '"{}" "{}"'.format(
                    _1,
                    bsc_resource.ExtendResource.get(
                        'docs/resource-manager.pdf'
                    )
                )

                bsc_core.BscProcess.execute_use_thread(
                    cmd_script
                )
