# coding:utf-8
import lnx_screw.core as lzy_src_core

import lxgui.core as gui_core


@gui_core.Verify.execute('resora', 7)
class Main(object):
    def __init__(self, session):
        self._session = session
        self._option_opt = self._session.option_opt

    def execute(self):
        window = self._session.find_window()
        if window is not None:
            result = window.exec_message_dialog(
                window.choice_gui_tool_tip(self._session.gui_configure.get('window')),
                title=window.choice_gui_name(self._session.gui_configure.get('window')),
                size=(320, 120),
                status='warning',
            )
            if result is True:
                page = window.gui_get_current_page()
                node_opt = page._gui_node_opt
                scr_stage_name = self._option_opt.get('stage_name')
                self._scr_stage = lzy_src_core.Stage(scr_stage_name)

                scr_entities = node_opt.gui_get_checked_or_selected_scr_entities()
                if scr_entities:
                    with window.gui_progressing(maximum=len(scr_entities)) as g_p:
                        for i_scr_entity in scr_entities:
                            self.execute_for(window, i_scr_entity, 1)

                            g_p.do_update()

                # update all type
                scr_node_paths = [x.path for x in scr_entities]
                scr_type_path_set = self._scr_stage.find_nodes_assign_type_path_set(
                    scr_node_paths
                )
                scr_tag_path_set = self._scr_stage.find_nodes_assign_tag_path_set(
                    scr_node_paths
                )
                page.gui_on_register_finished(list(scr_type_path_set), list(scr_tag_path_set))

    def execute_for(self, window, scr_entity, value):
        page = window.gui_get_current_page()
        # lock
        self._scr_stage.set_node_locked(scr_entity.path, value)
        page._gui_node_opt.gui_reload_entity(scr_entity.path)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(session).execute()
