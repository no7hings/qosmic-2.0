# coding:utf-8


def main(session):
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import qsm_prc_general.ssn.objects as gnl_ssn_objects

    import lxsession.commands as ssn_commands

    option_opt = session.option_opt

    file_path = option_opt.get('file')
    if bsc_storage.StgFileMtd.get_is_exists(file_path) is False:
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

    version_scheme = 'new'
    scene_src_file_path = rsv_application.get_release_scene_src_file(
        version_scheme=version_scheme
    )

    if scene_src_file_path:
        option_opt.set(
            'file', scene_src_file_path
        )
    #
    ssn_commands.set_session_option_hooks_execute_by_deadline(
        session
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
