# coding:utf-8

def main(session):
    import lxbasic.storage as bsc_storage

    import lnx_screw.core as c

    option_opt = session.option_opt
    scr_stage_name = option_opt.get('stage_name')
    scr_entity_path = option_opt.get('entity')
    scr_stage = c.Stage(scr_stage_name)
    scr_entity = scr_stage.get_node(scr_entity_path)
    source_path = scr_stage.get_node_parameter(scr_entity.path, 'source')
    if source_path:
        bsc_storage.StgFileOpt(source_path).start_in_system()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
