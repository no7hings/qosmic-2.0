# coding:utf-8
import lxgui.core as gui_core


class Main(object):
    def __init__(self, session):
        self._session = session
        self._option_opt = self._session.option_opt

    @gui_core.Verify.execute('resora-secondary', 7)
    def execute(self):
        window = self._session.find_window()
        if window is not None:
            import lnx_resora.gui.subpanels.assign as subpanel_assign

            scr_stage_name = self._option_opt.get('stage_name')

            page = window.gui_get_current_page()
            node_opt = page._gui_node_opt
            scr_entities = node_opt.gui_get_checked_or_selected_scr_entities()
            if not scr_entities:
                return

            w = subpanel_assign.PrxSubPanelForAssign(window, self._session)

            page_key = 'type'
            w.gui_setup_pages_for([page_key])
            assign_page = w.gui_find_page(page_key)
            if assign_page is not None:
                assign_page.set_scr_stage_key(scr_stage_name)
                assign_page.set_scr_nodes(
                    scr_entities
                )
                assign_page.set_post_fnc(page._gui_type_opt.gui_update_entities_for)

            w.show_window_auto()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(session).execute()
