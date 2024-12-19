# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxkatana.dcc.objects as ktn_dcc_objects

    import qsm_prc_katana.rsv.objects as ktn_rsv_objects

    import lxresolver.core as rsv_core

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if bsc_storage.StgFile.get_is_exists(any_scene_file_path) is True:
            ktn_dcc_objects.Scene.open_file(any_scene_file_path)
            #
            resolver = rsv_core.RsvBase.generate_root()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                # lock first
                with_workspace_texture_lock = hook_option_opt.get_as_boolean('with_workspace_texture_lock')
                if with_workspace_texture_lock is True:
                    pass
                    # ktn_rsv_objects.RsvDccTextureHookOpt(
                    #     rsv_scene_properties,
                    #     hook_option_opt,
                    # ).do_lock_asset_texture_workspace()
                # texture
                with_texture = hook_option_opt.get_as_boolean('with_texture')
                if with_texture is True:
                    ktn_rsv_objects.RsvDccTextureHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).do_export_asset_render_texture()
                else:
                    # texture-tx
                    with_texture_tx = hook_option_opt.get('with_texture_tx') or False
                    if with_texture_tx is True:
                        ktn_rsv_objects.RsvDccTextureHookOpt(
                            rsv_scene_properties,
                            hook_option_opt,
                        ).do_export_asset_render_texture()
                #
                with_scene = hook_option_opt.get_as_boolean('with_scene')
                if with_scene is True:
                    ktn_rsv_objects.RsvDccSceneHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).do_export_asset_scene()
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
