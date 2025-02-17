# coding:utf-8
import lnx_screw.core as lnx_scr_core


class Main(object):
    def __init__(self, session):
        self._session = session
        self._option_opt = self._session.option_opt

    def execute(self):
        window = self._session.find_window()
        if window is not None:
            page = window.gui_get_current_page()
            node_opt = page._gui_node_opt
            scr_stage_name = self._option_opt.get('stage_name')

            scr_entities = node_opt.gui_get_checked_or_selected_scr_entities()
            if scr_entities:
                scr_stage = lnx_scr_core.Stage(scr_stage_name)
                for i in scr_entities:
                    i_motion_path = None

                scr_stage.close()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(session).execute()
