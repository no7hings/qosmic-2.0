# coding:utf-8


def main(session):
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxgeneral.dcc.objects as gnl_dcc_objects

    import qsm_prc_general.ssn.objects as gnl_ssn_objects

    import lxsession.commands as ssn_commands

    import lxresolver.core as rsv_core

    hook_option_opt = session.option_opt

    file_path = hook_option_opt.get('file')
    file_ = gnl_dcc_objects.StgFile(file_path)
    if file_.get_is_exists() is False:
        raise IOError(
            bsc_log.Log.trace_method_error(
                'option-hook execute',
                u'file="{}" is non-exists.'.format(file_path)
            )
        )

    bsc_core.BscEnviron.set(
        'RSV_SCENE_FILE', file_path
    )

    rsv_application = gnl_ssn_objects.SsnRsvApplication()
    choice_scheme = hook_option_opt.get('choice_scheme')
    if bsc_core.BscTextOpt(choice_scheme).get_filter_by_pattern('asset-*-output'):
        # pre export use workspace: "output"
        scene_src_file_path_tgt = rsv_application.get_temporary_scene_src_file(
            version_scheme='new'
        )
    else:
        raise RuntimeError()

    if scene_src_file_path_tgt:
        hook_option_opt.set(
            'file', scene_src_file_path_tgt
        )
    else:
        raise RuntimeError()
    #
    resolver = rsv_core.RsvBase.generate_root()
    rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(scene_src_file_path_tgt)
    rsv_task = resolver.get_rsv_task_by_any_file_path(scene_src_file_path_tgt)
    version = rsv_scene_properties.get('version')
    # render-file
    rsv_output_asset_katana_scene_file_unit = rsv_task.get_rsv_unit(
        keyword='asset-temporary-katana-scene-file'
    )
    rsv_output_asset_katana_scene_file_path = rsv_output_asset_katana_scene_file_unit.get_result(
        version=version
    )
    hook_option_opt.set('render_file', rsv_output_asset_katana_scene_file_path)
    # render-image-dir
    rsv_render_output_directory_unit = rsv_task.get_rsv_unit(
        keyword='asset-temporary-katana-render-output-dir'
    )
    rsv_render_output_directory_path = rsv_render_output_directory_unit.get_result(
        version=version
    )
    hook_option_opt.set('render_output_directory', rsv_render_output_directory_path)
    # render-info
    rsv_output_render_info_yaml_file_unit = rsv_task.get_rsv_unit(
        keyword='asset-temporary-render-info-yaml-file'
    )
    rsv_output_render_info_yaml_file_path = rsv_output_render_info_yaml_file_unit.get_result(
        version=version
    )
    bsc_storage.StgFileOpt(
        rsv_output_render_info_yaml_file_path
    ).set_write(
        hook_option_opt.get_raw()
    )

    ssn_commands.set_session_option_hooks_execute_by_deadline(
        session
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
