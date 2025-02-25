# coding:utf-8
import lxgui.core as gui_core


@gui_core.Verify.execute('resora', 7)
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

    result = gui_core.GuiApplication.exec_message_dialog(
        window.choice_gui_message(session.gui_configure.get('window')),
        title=window.choice_gui_name(session.gui_configure.get('window')),
        size=(320, 120),
        status='warning',
    )
    if result is True:
        action_result = scr_stage.set_type_trashed(scr_entity.path, True)

        if action_result is True:
            window.gui_get_current_page()._gui_type_opt.gui_remove_entity(scr_entity_path)
        else:
            window.exec_message_dialog(
                'Delete failed.',
                status='error'
            )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
