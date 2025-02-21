# coding:utf-8

def main(session):
    import lxgui.qt.core as gui_qt_core

    import lnx_screw.core as c

    option_opt = session.option_opt
    scr_stage_name = option_opt.get('stage_name')
    scr_node_path = option_opt.get('entity')
    scr_stage = c.Stage(scr_stage_name)
    source_path = scr_stage.get_node_parameter(scr_node_path, 'source')
    if source_path:
        gui_qt_core.QtUtil.set_text_to_clipboard(source_path)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
