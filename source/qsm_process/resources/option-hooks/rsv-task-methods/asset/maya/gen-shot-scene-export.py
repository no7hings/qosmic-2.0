# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxresolver.core as rsv_core

    import qsm_prc_maya.rsv.objects as mya_rsv_objects

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if bsc_storage.StgFile.get_is_exists(any_scene_file_path) is True:
            resolver = rsv_core.RsvBase.generate_root()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                copy_shot_scene_src = hook_option_opt.get('copy_shot_scene_src') or False
                if copy_shot_scene_src is True:
                    mya_rsv_objects.RsvDccShotSceneHookOpt(
                        rsv_scene_properties,
                        hook_option_opt
                    ).set_asset_shot_scene_src_copy()
                #
                with_shot_scene = hook_option_opt.get('with_shot_scene') or False
                if with_shot_scene is True:
                    mya_rsv_objects.RsvDccShotSceneHookOpt(
                        rsv_scene_properties,
                        hook_option_opt
                    ).set_asset_shot_scene_export()
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
