# coding:utf-8
import lxgui.core as gui_core


@gui_core.Verify.execute('resora-admin', 7)
def main(session):
    window = session.find_window()
    if not window:
        return

    import lnx_screw.core as c

    option_opt = session.option_opt
    scr_stage_name = option_opt.get('stage_name')
    scr_entity_path = option_opt.get('entity')
    scr_stage = c.Stage(scr_stage_name)

    scr_entity = scr_stage.get_type(scr_entity_path)

    if window._language == 'chs':
        name_old = scr_entity.gui_name_chs
    else:
        name_old = scr_entity.gui_name

    name_new = gui_core.GuiApplication.exec_input_dialog(
        type='string',
        info='Entry Name for Rename...',
        value=name_old,
        title=window.choice_gui_name(session.gui_configure.get('window'))
    )
    if name_new:
        if window._language == 'chs':
            action_result = scr_stage.update_type(scr_entity_path, gui_name_chs=name_new)
        else:
            action_result = scr_stage.update_type(scr_entity_path, gui_name=name_new)

        if action_result is True:
            page = window.gui_get_current_page()
            page._gui_type_opt.gui_reload_entity(scr_entity_path)
        else:
            window.exec_message_dialog(
                'Rename failed.',
                status='error'
            )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
