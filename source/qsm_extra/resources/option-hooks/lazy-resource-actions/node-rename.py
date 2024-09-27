# coding:utf-8

def main(session):
    window = session.find_window()
    if not window:
        return

    import lxgui.core as gui_core

    import qsm_lazy.screw.core as c

    option_opt = session.option_opt
    scr_stage_key = option_opt.get('stage_key')
    scr_entity_path = option_opt.get('entity')
    scr_stage = c.Stage(scr_stage_key)

    scr_entity = scr_stage.get_node(scr_entity_path)

    input_result = gui_core.GuiApplication.exec_input_dialog(
        type='string',
        info='Entry Name for Rename...',
        value=scr_entity.gui_name_chs,
        title=window.choice_name(session.gui_configure.get('window'))
    )

    if input_result:
        scr_stage.update_node(scr_entity_path, gui_name_chs=input_result)

        page = window.gui_get_current_page()
        page._gui_node_opt.gui_reload_entity(scr_entity_path)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
