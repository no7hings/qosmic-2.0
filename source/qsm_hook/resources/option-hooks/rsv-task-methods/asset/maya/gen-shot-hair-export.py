# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxresolver.core as rsv_core

    import qsm_hook_maya.rsv.objects as mya_rsv_objects
    # noinspection PyUnresolvedReferences
    import maya.cmds as cmds
    cmds.stackTrace(state=1)

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if bsc_storage.StgFileMtd.get_is_exists(any_scene_file_path) is True:
            resolver = rsv_core.RsvBase.generate_root()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                mya_rsv_objects.RsvDccShotSceneHookOpt(
                    rsv_scene_properties,
                    hook_option_opt,
                ).set_asset_shot_scene_open()
                #
                with_shot_hair_xgen = hook_option_opt.get('with_shot_hair_xgen') or False
                if with_shot_hair_xgen is True:
                    mya_rsv_objects.RsvDccShotHairHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).set_asset_shot_xgen_export()
                #
                with_shot_hair_xgen_usd = hook_option_opt.get('with_shot_hair_xgen_usd') or False
                if with_shot_hair_xgen_usd is True:
                    pass

            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
