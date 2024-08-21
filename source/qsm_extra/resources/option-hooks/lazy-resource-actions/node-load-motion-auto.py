# coding:utf-8
import qsm_lazy.screw.core as qsm_scr_core


class Main(object):
    def __init__(self, session):
        self._session = session
        self._option_opt = self._session.option_opt

    def execute(self):
        window = self._session.find_window()
        if window is not None:
            page = window.gui_get_current_page()
            node_opt = page._gui_node_opt
            scr_stage_key = self._option_opt.get('stage_key')

            src_entities = node_opt.gui_get_checked_or_selected_scr_entities()
            if src_entities:
                scr_stage = qsm_scr_core.Stage(scr_stage_key)
                for i in src_entities:
                    i_motion_path = None


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(session).execute()
