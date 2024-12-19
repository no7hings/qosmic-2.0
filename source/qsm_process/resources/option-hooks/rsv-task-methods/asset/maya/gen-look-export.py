# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxmaya.dcc.objects as mya_dcc_objects

    import qsm_prc_general.rsv.objects as gnl_rsv_objects

    import lxmaya.core as mya_core

    import qsm_prc_maya.rsv.objects as mya_rsv_objects

    mya_core.MyaUtil.set_stack_trace_enable(True)

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        maya_rsv_scene_properties = gnl_rsv_objects.RsvUtilityOpt.get_dcc_args(
            any_scene_file_path, application='maya'
        )
        if maya_rsv_scene_properties:
            maya_scene_src_file_path = maya_rsv_scene_properties.get('extra.file')
            if maya_scene_src_file_path:
                if bsc_storage.StgFile.get_is_exists(maya_scene_src_file_path) is True:
                    mya_dcc_objects.Scene.open_file(maya_scene_src_file_path)
                    # either texture or texture-tx
                    if (
                        hook_option_opt.get_as_boolean('with_texture') is True
                        or hook_option_opt.get_as_boolean('with_texture_tx') is True
                    ):
                        mya_rsv_objects.RsvDccTextureHookOpt(
                            maya_rsv_scene_properties,
                            hook_option_opt
                        ).do_export_asset_render_texture()
                    # run when is maya scheme, ass is same file
                    choice_scheme = hook_option_opt.get('choice_scheme')
                    if bsc_core.BscTextOpt(choice_scheme).check_is_matched('*-maya-*'):
                        if hook_option_opt.get_as_boolean('with_look_ass') is True:
                            mya_rsv_objects.RsvDccLookHookOpt(
                                maya_rsv_scene_properties,
                                hook_option_opt
                            ).do_export_asset_look_ass(
                                texture_use_environ_map=False
                            )
                    #
                    if hook_option_opt.get_as_boolean('with_look_yml') is True:
                        mya_rsv_objects.RsvDccLookHookOpt(
                            maya_rsv_scene_properties,
                            hook_option_opt
                        ).execute_asset_look_yml_export()
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
