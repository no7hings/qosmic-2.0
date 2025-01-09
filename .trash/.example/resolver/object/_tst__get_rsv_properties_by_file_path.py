# coding:utf-8
if __name__ == '__main__':
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxresolver.core as rsv_core

    bsc_log.Log.RESULT_ENABLE = False

    r = rsv_core.RsvBase.generate_root()
    for i_file_path in [
        '/production/shows/nsa_dev/assets/chr/td_test/user/work.render/katana/render/groom/td_test.grm.groom.v004'
    ]:
        i_rsv_project = r.get_rsv_project_by_any_file_path(i_file_path)
        print i_rsv_project

        i_rsv_unit = i_rsv_project.get_rsv_unit(
            keyword='asset-user-app-render-image-dir'
        )
        print i_rsv_unit.pattern
        print i_rsv_unit.generate_properties_by_result(
            i_file_path
        )
