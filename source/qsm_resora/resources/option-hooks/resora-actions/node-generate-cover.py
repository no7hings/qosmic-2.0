# coding:utf-8

def main(session):
    window = session.find_window()
    if not window:
        return

    import lxbasic.core as bsc_core

    import lnx_screw.core as c
    
    import lnx_screw.scripts as s

    option_opt = session.option_opt
    scr_stage_name = option_opt.get('stage_name')
    scr_entity_path = option_opt.get('entity')
    scr_stage = c.Stage(scr_stage_name)

    scr_entity = scr_stage.get_node(scr_entity_path)
    if scr_entity:
        database_name = bsc_core.BscNodePathOpt(scr_entity_path).get_name()
        result = s.ManifestStageOpt().generate_cover_for(database_name)
        if result is True:
            page = window.gui_get_current_page()
            page._gui_node_opt.gui_reload_entity(scr_entity_path, update_thumbnail=True)
        else:
            window.exec_message_dialog(
                'Generate image failed.',
                status='error'
            )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
