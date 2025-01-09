# coding:utf-8
if __name__ == '__main__':
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxresolver.core as rsv_core

    bsc_log.Log.RESULT_ENABLE = False

    r = rsv_core.RsvBase.generate_root()

    for i_project, i_asset in [
        ('cgm', 'td_test'),
        ('nsa_dev', 'td_test'),
        ('nsa_dev', 'momo'),
    ]:
        i_rsv_project = r.get_rsv_project(project=i_project)

        print i_rsv_project.get_dcc_data('maya')

        # i_rsv_asset = i_rsv_project.get_rsv_resource(asset=i_asset)
        # print i_rsv_asset
        #
        # i_rsv_task = i_rsv_asset.get_rsv_task(step='mod', task='modeling')
        # print i_rsv_task
        #
        # print i_rsv_task._get_user_directory_path()
