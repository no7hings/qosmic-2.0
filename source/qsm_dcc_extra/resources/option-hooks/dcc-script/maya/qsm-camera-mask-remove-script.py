# coding:utf-8
def main(session):
    import qsm_maya.scenery.scripts as qsm_scn_scripts

    option_opt = session.get_option_opt()

    qsm_scn_scripts.CameraMaskOpt.remove_auto(**option_opt.to_dict())


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
