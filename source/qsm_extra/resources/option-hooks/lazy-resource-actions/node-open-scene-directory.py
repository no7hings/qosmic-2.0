# coding:utf-8

def main(session):
    import lxbasic.storage as bsc_storage

    import qsm_lazy.screw.core as c

    option_opt = session.option_opt
    scr_stage_key = option_opt.get('stage_key')
    scr_node_path = option_opt.get('entity')
    scr_stage = c.Stage(scr_stage_key)
    scene_path = scr_stage.get_node_parameter(scr_node_path, 'scene')
    if scene_path:
        bsc_storage.StgFileOpt(scene_path).show_in_system()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)