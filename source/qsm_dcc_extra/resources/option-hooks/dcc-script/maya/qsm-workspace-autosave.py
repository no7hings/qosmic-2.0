# coding:utf-8
def main(session):
    import qsm_maya_lazy_workspace.core as c
    
    c.TaskParse.autosave_source_scene_scr()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
