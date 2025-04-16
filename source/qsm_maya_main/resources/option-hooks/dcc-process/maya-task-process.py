import sys


# cache export
def shot_animation_cache_export_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process

    import lnx_maya_wotrix_tasks.shot.animation.dcc_scripts as s

    kwargs = qsm_gnl_process.MayaCacheSubprocess.to_option_dict(
        option_opt.to_string()
    )

    s.ShotAnimationCacheProcess(
        **kwargs
    ).execute()


def shot_cfx_cloth_cache_export_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process

    import lnx_maya_wotrix_tasks.shot.cfx_cloth.dcc_scripts as s

    kwargs = qsm_gnl_process.MayaCacheSubprocess.to_option_dict(
        option_opt.to_string()
    )

    s.ShotCfxClothCacheExportProcess(
        **kwargs
    ).execute()


def asset_cfx_rig_release_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process

    import lnx_maya_wotrix_tasks.asset.cfx_rig.dcc_processes.task_release as p

    kwargs = qsm_gnl_process.MayaCacheSubprocess.to_option_dict(
        option_opt.to_string()
    )

    p.AssetCfxRigReleaseProcess(
        **kwargs
    ).execute()


# release
def shot_cfx_dressing_release_fnc(option_opt):
    import qsm_general.process as qsm_gnl_process

    import lnx_maya_wotrix_tasks.shot.cfx_dressing.dcc_processes.task_release as p

    kwargs = qsm_gnl_process.MayaCacheSubprocess.to_option_dict(
        option_opt.to_string()
    )

    p.ShotCfxDressingReleaseProcess(
        **kwargs
    ).execute()


def main(session):
    # noinspection PyUnresolvedReferences
    from maya import cmds
    cmds.stackTrace(state=1)
    
    import qsm_general.process.maya_task_process as task_prc

    option_opt = session.get_option_opt()
    method = option_opt.get('method')
    # cache export
    # animation
    if method == task_prc.MayaTaskSubprocess.TaskKeys.ShotAnimationCacheExport:
        shot_animation_cache_export_fnc(option_opt)
    # cfx cloth
    elif method == task_prc.MayaTaskSubprocess.TaskKeys.ShotCfxClothCacheExport:
        shot_cfx_cloth_cache_export_fnc(option_opt)
    # release
    # cfx rig
    elif method == task_prc.MayaTaskSubprocess.TaskKeys.AssetCfxRigRelease:
        asset_cfx_rig_release_fnc(option_opt)
    # cfx dressing
    elif method == task_prc.MayaTaskSubprocess.TaskKeys.ShotCfxDressingRelease:
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
