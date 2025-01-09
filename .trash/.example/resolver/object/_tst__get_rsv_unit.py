# coding:utf-8
if __name__ == '__main__':
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxresolver.core as rsv_core

    bsc_log.Log.RESULT_ENABLE = False

    r = rsv_core.RsvBase.generate_root()

    for i_project, i_asset, i_step, i_task in [
        # ('cgm', 'td_test', 'mod', 'modeling'),
        ('nsa_dev', 'td_test', 'mod', 'modeling'),
        ('nsa_dev', 'momo', 'mod', 'modeling'),
        # ('nsa_dev', 'dl_creatures', 'cpt', 'concept'),
    ]:
        i_rsv_project = r.get_rsv_project(project=i_project)

        i_rsv_task = i_rsv_project.get_rsv_task(asset=i_asset, step=i_step, task=i_task)

        i_rsv_unit = i_rsv_task.get_rsv_unit(
            keyword='{branch}-user-task-dir'
        )

        print i_rsv_unit.properties

        print i_rsv_unit.get_result(
            variants_extend=dict(artist='dongchangbao')
        )

