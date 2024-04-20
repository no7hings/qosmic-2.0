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
        # '/production/shows/nsa_dev/assets/chr/td_test/user/team.mod/katana/scenes/modeling/td_test.mod.modeling.modeling.v000_001.katana',
        # '/production/shows/nsa_dev/assets/chr/td_test/shared/mod/modeling/td_test.mod.modeling.v004/scene/td_test.ma',
        # '/production/shows/tnt/sequences/c10/c10010/user/work.fangxiaodong/katana/scenes/lighting/c10010.lgt.lighting.lighting.v000_001.katana'
    ]:

        i_rsv_scene_properties = r.get_rsv_scene_properties_by_any_scene_file_path(
            i_file_path
        )

        # print i_rsv_scene_properties

        i_rsv_task = r.get_rsv_task(
            **i_rsv_scene_properties.get_value()
        )

        # print i_rsv_task

        i_workspace = i_rsv_scene_properties.get('workspace')

        i_version = i_rsv_scene_properties.get('version')

        # if i_workspace in [i_rsv_scene_properties.get('workspaces.source'), i_rsv_scene_properties.get('workspaces.user')]:
        #     i_keyword = 'asset-source-version-dir'
        # elif i_workspace == i_rsv_scene_properties.get('workspaces.release'):
        #     i_keyword = 'asset-release-version-dir'
        # elif i_workspace == i_rsv_scene_properties.get('workspaces.temporary'):
        #     i_keyword = 'asset-temporary-version-dir'
        # else:
        #     raise RuntimeError()

        i_rsv_unit = i_rsv_task.get_rsv_unit(keyword='{branch}-user-katana-scene-src-file')

        _ = i_rsv_unit.get_result(
            version='all'
        )
        if _:

            p = i_rsv_unit.generate_properties_by_result(_[0])
            print p.get('artist')

