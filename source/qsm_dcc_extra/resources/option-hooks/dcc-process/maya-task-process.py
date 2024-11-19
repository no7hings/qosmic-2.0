import sys


def asset_cfx_rig_release_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process

    import qsm_maya_wsp_task.task_release_process as p

    kwargs = qsm_gnl_process.MayaCacheProcess.to_option_dict(
        option_opt.to_string()
    )

    p.AssetCfxRigReleaseProcess(
        **kwargs
    ).execute()


def shot_cfx_dressing_release_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process

    import qsm_maya_wsp_task.task_release_process as p

    kwargs = qsm_gnl_process.MayaCacheProcess.to_option_dict(
        option_opt.to_string()
    )

    p.ShotCfxDressingReleaseProcess(
        **kwargs
    ).execute()


def main(session):
    # noinspection PyUnresolvedReferences
    from maya import cmds
    cmds.stackTrace(state=1)

    option_opt = session.get_option_opt()
    method = option_opt.get('method')
    
    if method == 'asset_cfx_rig_release':
        asset_cfx_rig_release_fnc(option_opt)
    elif method == 'shot_cfx_dressing_release':
        shot_cfx_dressing_release_fnc(option_opt)
    else:
        raise RuntimeError(
            sys.stderr.write(
                'method is not valid: {}.\n'.format(method)
            )
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
