# coding:utf-8

def main(session):
    window = session.find_window()
    if not window:
        return

    import lxgui.core as gui_core

    import lnx_screw.core as c

    option_opt = session.option_opt
    scr_stage_name = option_opt.get('stage_name')
    scr_entity_path = option_opt.get('entity')
    scr_stage = c.Stage(scr_stage_name)

    window.exec_message_dialog(
        scr_stage.generate_node_lock_history(scr_entity_path, window._language),
        title=window.choice_gui_name(session.gui_configure.get('window')),
        size=(320, 320)
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
