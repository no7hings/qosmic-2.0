# coding:utf-8
import lxgui.core as gui_core


@gui_core.Verify.execute('resora', 7)
def main(session):
    window = session.find_window()
    if not window:
        return

    import six

    import re

    import lnx_screw.core as c

    option_opt = session.option_opt
    scr_stage_name = option_opt.get('stage_name')
    scr_entity_path = option_opt.get('entity')
    scr_stage = c.Stage(scr_stage_name)

    scr_entity_parent = scr_stage.get_type(scr_entity_path)

    input_result = gui_core.GuiApplication.exec_input_dialog(
        type='text',
        info='Entry Name for Create...',
        value='',
        title=window.choice_gui_name(session.gui_configure.get('window'))
    )
    if input_result:
        texts = re.split(six.u(r'[^\w\u4e00-\u9fff]+'), input_result)
        if texts:
            page = window.gui_get_current_page()
            for i_seq, i_text in enumerate(texts):
                if not i_text:
                    continue

                index_maximum = scr_stage.get_entity_index_maximum(scr_stage.EntityTypes.Type)
                if scr_entity_parent.is_root():
                    i_new_path = '/type_{}'.format(index_maximum)
                else:
                    i_new_path = '{}/type_{}'.format(scr_entity_parent.path, index_maximum)

                i_scr_entity = scr_stage.create_type(i_new_path, gui_name_chs=i_text)

                page._gui_type_opt.gui_create_entity(i_scr_entity)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
