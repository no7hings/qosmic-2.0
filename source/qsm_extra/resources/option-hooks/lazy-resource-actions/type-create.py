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

    scr_entity = scr_stage.get_type(scr_entity_path)
    index_maximum = scr_stage.get_entity_index_maximum(scr_stage.EntityTypes.Type)

    input_result = gui_core.GuiApplication.exec_input_dialog(
        type='string',
        info='Entry Name for Create...',
        value='分类-{}'.format(index_maximum+1),
        title=window.choice_name(session.gui_configure.get('window'))
    )
    if input_result:
        if scr_entity.is_root():
            new_path = '/type_{}'.format(index_maximum)
        else:
            new_path = '{}/type_{}'.format(scr_entity.path, index_maximum)

        scr_entity = scr_stage.create_type(new_path, gui_name_chs=input_result)

        page = window.gui_get_current_page()
        page._gui_type_opt.gui_create_entity(scr_entity)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
