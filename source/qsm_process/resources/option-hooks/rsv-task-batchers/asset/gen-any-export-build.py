# coding:utf-8


def main(session):
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core
    #
    import qsm_prc_general.ssn.objects as gnl_ssn_objects
    #
    import lxsession.commands as ssn_commands
    #
    hook_option_opt = session.option_opt
    #
    file_path = hook_option_opt.get('file')
    #
    bsc_core.EnvBaseMtd.set(
        'RSV_SCENE_FILE', file_path
    )
    #
    rsv_application = gnl_ssn_objects.SsnRsvApplication()
    choice_scheme = hook_option_opt.get('choice_scheme')
    version_scheme = hook_option_opt.get('version_scheme')
    bsc_log.Log.trace_method_result(
        'option-hook execute', 'choice-scheme="{}"'.format(choice_scheme)
    )
    bsc_log.Log.trace_method_result(
        'option-hook execute', 'version-scheme="{}"'.format(version_scheme)
    )
    if bsc_core.BscTextOpt(choice_scheme).get_filter_by_pattern('asset-*-publish'):
        scene_src_file_path_tgt = rsv_application.get_release_scene_src_file(
            version_scheme=version_scheme
        )
    elif bsc_core.BscTextOpt(choice_scheme).get_filter_by_pattern('asset-*-output'):
        scene_src_file_path_tgt = rsv_application.get_temporary_scene_src_file(
            version_scheme=version_scheme
        )
    else:
        raise RuntimeError()

    if scene_src_file_path_tgt:
        hook_option_opt.set(
            'file', scene_src_file_path_tgt
        )
    #
    option_hook_key = hook_option_opt.get('option_hook_key')
    batch_name = hook_option_opt.get('batch_name')
    batch_file_path = hook_option_opt.get('batch_file')
    user = hook_option_opt.get('user')
    time_tag = hook_option_opt.get('time_tag')
    td_enable = hook_option_opt.get('td_enable')
    rez_beta = hook_option_opt.get('rez_beta')
    #
    maya_scene_src_file_paths = hook_option_opt.get_as_array('maya_scene_srcs')
    if maya_scene_src_file_paths:
        main_file_path = maya_scene_src_file_paths[0]
        maya_hook_option_opt = bsc_core.ArgDictStringOpt(
            dict(
                option_hook_key='rsv-task-methods/asset/maya/gen-any-export',
                #
                batch_name=batch_name,
                #
                batch_file=batch_file_path,
                file=main_file_path,
                #
                user=user, time_tag=time_tag,
                td_enable=td_enable, rez_beta=rez_beta,
                #
                with_scene=hook_option_opt.get_as_boolean('with_scene'),
                #
                with_render_texture=hook_option_opt.get_as_boolean('with_render_texture'),
                with_preview_texture=hook_option_opt.get_as_boolean('with_preview_texture'),
                #
                with_look_yml=hook_option_opt.get_as_boolean('with_look_yml'),
                #
                with_camera_abc=hook_option_opt.get_as_boolean('with_camera_abc'),
                with_camera_usd=hook_option_opt.get_as_boolean('with_camera_usd'),
                #
                dependencies=[option_hook_key],
            )
        )
        ssn_commands.execute_option_hook_by_deadline(
            maya_hook_option_opt.to_string()
        )
    #
    katana_scene_src_file_paths = hook_option_opt.get_as_array('katana_scene_srcs')
    if katana_scene_src_file_paths:
        main_katana_file_path = katana_scene_src_file_paths[0]
    #
    ssn_commands.set_session_option_hooks_execute_by_deadline(
        session
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
