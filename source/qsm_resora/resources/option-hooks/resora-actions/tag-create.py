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

    scr_entity = scr_stage.get_tag(scr_entity_path)
    index_maximum = scr_stage.get_entity_index_maximum(scr_stage.EntityTypes.Tag)

    input_result = gui_core.GuiApplication.exec_input_dialog(
        type='string',
        info='Entry Name for Create...',
        value='标签-{}'.format(index_maximum+1),
        title=window.choice_gui_name(session.gui_configure.get('window'))
    )
    if input_result:
        if scr_entity.is_root():
            new_path = '/tag_{}'.format(index_maximum)
        else:
            new_path = '{}/tag_{}'.format(scr_entity.path, index_maximum)

        scr_entity = scr_stage.create_tag(new_path, gui_name_chs=input_result)

        page = window.gui_get_current_page()
        page._gui_tag_opt.gui_create_entity(scr_entity)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
