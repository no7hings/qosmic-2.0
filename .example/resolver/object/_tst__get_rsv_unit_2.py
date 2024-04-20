# coding:utf-8
if __name__ == '__main__':
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxresolver.core as rsv_core

    bsc_log.Log.RESULT_ENABLE = False

    r = rsv_core.RsvBase.generate_root()

    rsv_project = r.get_rsv_project(project='nsa_dev')

    rsv_task = rsv_project.get_rsv_task(
        asset='nikki', step='mod', task='modeling'
    )

    rsv_unit = rsv_task.get_rsv_unit(
        keyword='{branch}-user-task-dir'
    )

    print rsv_unit.get_exists_result(
        variants_extend=dict(artist='dongchangbao')
    )
