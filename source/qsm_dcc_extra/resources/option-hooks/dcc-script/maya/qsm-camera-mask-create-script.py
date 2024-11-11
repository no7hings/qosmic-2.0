# coding:utf-8
def main(session):
    import qsm_maya.tasks.scenery.scripts as s

    option_opt = session.get_option_opt()

    s.CameraMaskOpt.create_auto(
        **option_opt.to_dict()
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
