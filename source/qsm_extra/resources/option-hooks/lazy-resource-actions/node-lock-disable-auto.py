# coding:utf-8
import lxbasic.core as bsc_core

import lxgui.core as gui_core

import lxgui.qt.widgets as qt_widgets

import lxbasic.storage as bsc_storage

import qsm_lazy.screw.core as qsm_lzy_src_core


class Main(object):
    def __init__(self, session):
        self._session = session
        self._option_opt = self._session.option_opt

    def execute(self):
        window = self._session.find_window()
        if window is not None:
            result = window.exec_message_dialog(
                window.choice_tool_tip(self._session.gui_configure.get('window')),
                title=window.choice_name(self._session.gui_configure.get('window')),
                size=(320, 120),
                status='warning',
            )
            if result is True:
                page = window.gui_get_current_page()
                node_opt = page._gui_node_opt
                scr_stage_key = self._option_opt.get('stage_key')
                self._scr_stage = qsm_lzy_src_core.Stage(scr_stage_key)

                scr_entities = node_opt.gui_get_checked_or_selected_scr_entities()
                if scr_entities:
                    with window.gui_progressing(maximum=len(scr_entities)) as g_p:
                        for i_scr_entity in scr_entities:
                            self.execute_for(window, i_scr_entity, 0)

                            g_p.do_update()

    def execute_for(self, window, scr_entity, value):
        page = window.gui_get_current_page()
        # lock
        self._scr_stage.set_node_locked(scr_entity.path, value)
        page._gui_node_opt.gui_reload_entity(scr_entity.path)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(session).execute()
