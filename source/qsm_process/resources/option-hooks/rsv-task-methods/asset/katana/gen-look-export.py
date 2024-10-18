# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxkatana.dcc.objects as ktn_dcc_objects

    import qsm_prc_general.rsv.objects as gnl_rsv_objects

    import qsm_prc_katana.rsv.objects as ktn_rsv_objects

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')
    if any_scene_file_path is not None:
        # get scene src file path as current application
        katana_rsv_scene_properties = gnl_rsv_objects.RsvUtilityOpt.get_dcc_args(
            any_scene_file_path, application='katana'
        )
        if katana_rsv_scene_properties:
            katana_scene_src_file_path = katana_rsv_scene_properties.get('extra.file')
            if katana_scene_src_file_path is not None:
                if bsc_storage.StgFileMtd.get_is_exists(katana_scene_src_file_path) is True:
                    ktn_dcc_objects.Scene.open_file(katana_scene_src_file_path)
                    #
                    reload_set_usd = hook_option_opt.get_as_boolean('reload_set_usd')
                    if reload_set_usd is True:
                        ktn_rsv_objects.RsvDccSceneHookOpt(
                            katana_rsv_scene_properties,
                            hook_option_opt
                        ).do_reload_asset_usd()
                    # either texture or texture-tx
                    if (
                        hook_option_opt.get_as_boolean('with_texture') is True
                        or hook_option_opt.get_as_boolean('with_texture_tx') is True
                    ):
                        ktn_rsv_objects.RsvDccTextureHookOpt(
                            katana_rsv_scene_properties,
                            hook_option_opt,
                        ).do_export_asset_render_texture()
                    #
                    if hook_option_opt.get_as_boolean('with_look_klf') is True:
                        ktn_rsv_objects.RsvDccLookHookOpt(
                            katana_rsv_scene_properties,
                            hook_option_opt,
                        ).do_export_asset_look_klf()
                    # run when is katana scheme
                    choice_scheme = hook_option_opt.get('choice_scheme')
                    if bsc_core.BscTextOpt(choice_scheme).check_is_matched('*-katana-*'):
                        if hook_option_opt.get_as_boolean('with_look_ass') is True:
                            ktn_rsv_objects.RsvDccLookHookOpt(
                                katana_rsv_scene_properties,
                                hook_option_opt,
                            ).do_export_asset_look_ass(
                                texture_use_environ_map=False, force=True
                            )
                else:
                    raise RuntimeError()
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
