# coding:utf-8
if __name__ == '__main__':
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxresolver.core as rsv_core

    bsc_log.Log.RESULT_ENABLE = False

    r = rsv_core.RsvBase.generate_root()
    for i_file_path in [
        # '/production/shows/nsa_dev/assets/chr/td_test/user/work.dongchangbao/katana/scenes/surface/td_test.srf.surface.v000_002.katana',
        '/production/shows/nsa_dev/assets/chr/nikki_rnd/user/work.dongchangbao/maya/scenes/surfacing/nikki_rnd.srf.surfacing.v000_001.ma'
    ]:

        i_rsv_scene_properties = r.get_rsv_scene_properties_by_any_scene_file_path(
            i_file_path
        )

        print i_rsv_scene_properties

