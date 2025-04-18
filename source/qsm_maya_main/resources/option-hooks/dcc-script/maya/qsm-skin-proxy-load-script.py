# coding:utf-8
def main(session):
    import qsm_general.core as qsm_gnl_core

    if qsm_gnl_core.check_python27_lib() is False:
        return

    import qsm_maya.handles.animation.scripts as s

    option_opt = session.get_option_opt()

    s.SkinProxyOpt.execute_auto(
        **option_opt.to_dict()
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
