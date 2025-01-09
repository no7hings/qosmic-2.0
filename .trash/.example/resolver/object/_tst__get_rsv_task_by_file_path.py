# coding:utf-8
if __name__ == '__main__':
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxresolver.core as rsv_core

    bsc_log.Log.RESULT_ENABLE = False

    r = rsv_core.RsvBase.generate_root()
    for i_file_path in [
        # '/l/prod/cgm/work/assets/chr/ast_cg7_dad/mod/modeling/maya/scenes/ast_cg7_dad.mod.modeling.v001.ma',
        # '/production/shows/nsa_dev/assets/chr/td_test/user/team.mod/maya/scenes/modeling/td_test.mod.modeling.modeling.v000_001.ma',
        # '/production/shows/nsa_dev/assets/chr/td_test/user/work.dongchangbao/maya/scenes/modeling/td_test.mod.modeling.modeling.v000_001.ma',
        # '/production/shows/nsa_dev/assets/env/neighborhood/shared/srf/surface/neighborhood.srf.surface.v002/preview/house_test.srf.surfacing.v003.mov',
        # '/production/shows/nsa_dev/assets/chr/momo/user/work.slash/maya/scenes/modeling/momo.mod.modeling.modeling.v000_001.ma',
        # '/production/shows/nsa_dev/assets/chr/td_test/shared/set/registry/td_test.set.registry.v002/cache/usd/td_test.usda',
        '/production/shows/nsa_dev/assets/chr/nikki/user/work.dongchangbao/maya/scenes/camera/nikki.cam.camera.camera.v000_001.ma'
    ]:
        print r.get_rsv_project_by_any_file_path(i_file_path)
        i_rsv_task = r.get_rsv_task_by_any_file_path(i_file_path)
        i_rsv_task.create_directory(workspace_key='release')

        print i_rsv_task.get_rsv_project().properties
