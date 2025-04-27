# coding:utf-8

def main(session):
    window = session.find_window()
    if not window:
        return

    import lxbasic.core as bsc_core

    import lnx_screw.core as c

    option_opt = session.option_opt
    scr_stage_name = option_opt.get('stage_name')
    scr_entity_path = option_opt.get('entity')
    scr_stage = c.Stage(scr_stage_name)

    scr_entity = scr_stage.get_node(scr_entity_path)
    if scr_entity:
        database_name = bsc_core.BscNodePathOpt(scr_entity.path).get_name()

        cur_scr_stage = c.Stage(database_name)
        cur_applications = cur_scr_stage.applications

        if bsc_core.BscApplication.get_is_maya():
            if 'maya' not in cur_applications:
                window.exec_message_dialog(
                    'Can not open this page in MAYA',
                    title='Open Page',
                    size=(320, 120),
                    status='error',
                )
                return

        window._gui_add_manager_page_fnc(database_name, True)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
