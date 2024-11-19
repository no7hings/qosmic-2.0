# coding:utf-8
def main(session):
    import qsm_maya.tasks.general.scripts as qsm_prv_scripts

    option_opt = session.get_option_opt()

    qsm_prv_scripts.PlayblastOpt.execute_auto(
        **option_opt.to_dict()
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
