# coding:utf-8

def main(session):
    window = session.find_window()
    if not window:
        return

    import lxgui.core as gui_core

    import qsm_screw.core as c

    option_opt = session.option_opt
    scr_stage_key = option_opt.get('stage_key')
    scr_entity_path = option_opt.get('entity')
    scr_stage = c.Stage(scr_stage_key)

    scr_entity = scr_stage.get_node(scr_entity_path)

    if window._language == 'chs':
        name_old = scr_entity.gui_name_chs
    else:
        name_old = scr_entity.gui_name

    input_result = gui_core.GuiApplication.exec_input_dialog(
        type='string',
        info='Entry Name for Rename...',
        value=name_old,
        title=window.choice_name(session.gui_configure.get('window'))
    )

    if input_result:
        if window._language == 'chs':
            result = scr_stage.update_node(scr_entity_path, gui_name_chs=input_result)
        else:
            result = scr_stage.update_node(scr_entity_path, gui_name=input_result)

        if result is True:
            page = window.gui_get_current_page()
            page._gui_node_opt.gui_reload_entity(scr_entity_path)
        else:
            window.exec_message_dialog(
                'Rename failed.',
                status='error'
            )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
