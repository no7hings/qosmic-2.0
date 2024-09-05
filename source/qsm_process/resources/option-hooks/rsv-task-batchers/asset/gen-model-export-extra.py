# coding:utf-8


def main(session):
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core
    #
    import lxgeneral.dcc.objects as gnl_dcc_objects
    #
    import qsm_prc_general.ssn.objects as gnl_ssn_objects
    #
    import lxsession.commands as ssn_commands
    #
    hook_option_opt = session.option_opt
    #
    file_path = hook_option_opt.get('file')
    file_ = gnl_dcc_objects.StgFile(file_path)
    if file_.get_is_exists() is False:
        raise IOError(
            bsc_log.Log.trace_method_error(
                'option-hook execute',
                u'file="{}" is non-exists.'.format(file_path)
            )
        )
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
    if bsc_core.BscTextOpt(choice_scheme).get_filter_by_pattern('asset-*-output'):
        scene_src_file_path_tgt = rsv_application.get_temporary_scene_src_file(
            version_scheme=version_scheme
        )
    elif bsc_core.BscTextOpt(choice_scheme).get_filter_by_pattern('asset-*-publish'):
        scene_src_file_path_tgt = rsv_application.get_release_scene_src_file(
            version_scheme=version_scheme
        )
    else:
        raise RuntimeError()

    if scene_src_file_path_tgt:
        hook_option_opt.set(
            'file', scene_src_file_path_tgt
        )
    #
    ssn_commands.set_session_option_hooks_execute_by_deadline(
        session
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
