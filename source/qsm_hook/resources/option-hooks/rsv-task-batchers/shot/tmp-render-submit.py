# coding:utf-8


def main(session):
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import qsm_hook_general.ssn.objects as gnl_ssn_objects

    import lxsession.commands as ssn_commands

    hook_option_opt = session.option_opt

    file_path = hook_option_opt.get('file')
    if bsc_storage.StgFileMtd.get_is_exists(file_path) is False:
        raise IOError(
            bsc_log.Log.trace_method_error(
                'option-hook execute',
                u'file="{}" is non-exists.'.format(file_path)
            )
        )

    bsc_core.EnvBaseMtd.set(
        'RSV_SCENE_FILE', file_path
    )

    rsv_application = gnl_ssn_objects.SsnRsvApplication()
    choice_scheme = hook_option_opt.get('choice_scheme')
    if bsc_core.RawTextOpt(choice_scheme).get_filter_by_pattern('shot-*-output'):
        # pre export use workspace: "output"
        scene_src_file_path_tgt = rsv_application.get_temporary_scene_src_file(
            version_scheme='new'
        )
    elif bsc_core.RawTextOpt(choice_scheme).get_filter_by_pattern('shot-*-custom'):
        scene_src_file_path_tgt = file_path
    else:
        raise RuntimeError(
            bsc_log.Log.trace_error(
                'choice scheme="{}" is not available'.format(choice_scheme)
            )
        )

    if scene_src_file_path_tgt:
        hook_option_opt.set(
            'file', scene_src_file_path_tgt
        )
    else:
        raise RuntimeError()
    #
    ssn_commands.set_session_option_hooks_execute_by_deadline(
        session
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
