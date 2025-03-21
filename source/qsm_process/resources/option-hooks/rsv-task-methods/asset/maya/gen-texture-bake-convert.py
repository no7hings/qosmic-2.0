# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxmaya.dcc.objects as mya_dcc_objects

    import lxresolver.core as rsv_core

    import qsm_prc_maya.rsv.objects as mya_rsv_objects

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        resolver = rsv_core.RsvBase.generate_root()
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
        if rsv_scene_properties:
            if bsc_storage.StgFile.get_is_exists(any_scene_file_path) is True:
                mya_dcc_objects.Scene.open_file(any_scene_file_path)
                with_texture_bake_convert = hook_option_opt.get('with_texture_bake_convert', as_array=True) or []
                if with_texture_bake_convert:
                    mya_rsv_objects.RsvDccSceneHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).set_asset_texture_bake_convert()
                #
                with_work_scene_src_link = hook_option_opt.get('with_work_scene_src_link') or False
                if with_work_scene_src_link is True:
                    mya_rsv_objects.RsvDccSceneHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).set_asset_work_scene_src_link()
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
