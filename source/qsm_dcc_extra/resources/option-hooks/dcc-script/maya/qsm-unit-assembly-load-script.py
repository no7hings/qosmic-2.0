# coding:utf-8
def main(session):
    import qsm_general.core as qsm_gnl_core

    if qsm_gnl_core.check_python_lib() is False:
        return

    import qsm_maya.tasks.scenery.scripts as s

    option_opt = session.get_option_opt()

    s.UnitAssemblyOpt.execute_auto(
        **option_opt.to_dict()
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
