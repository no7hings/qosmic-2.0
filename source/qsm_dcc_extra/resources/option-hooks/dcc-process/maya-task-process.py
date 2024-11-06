

def cfx_rig_release(option_opt):
    import qsm_general.process as qsm_gnl_process

    import qsm_maya.steps.cfx_rig.scripts as qsm_mya_stp_cfx_rig_scripts

    kwargs = qsm_gnl_process.MayaCacheProcess.to_option_dict(
        option_opt.to_string()
    )

    qsm_mya_stp_cfx_rig_scripts.CfxRigReleaseProcess(
        **kwargs
    ).execute()


def main(session):
    # noinspection PyUnresolvedReferences
    from maya import cmds
    cmds.stackTrace(state=1)

    option_opt = session.get_option_opt()
    method = option_opt.get('method')
    
    if method == 'cfx_rig_release':
        cfx_rig_release(option_opt)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)