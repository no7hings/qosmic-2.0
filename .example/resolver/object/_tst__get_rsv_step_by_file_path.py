# coding:utf-8
if __name__ == '__main__':
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxresolver.core as rsv_core

    bsc_log.Log.RESULT_ENABLE = False

    r = rsv_core.RsvBase.generate_root()
    for i_file_path in [
        '/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/surface/set/scene/v001/td_test.usda'
    ]:
        print r.get_rsv_project_by_any_file_path(i_file_path)
