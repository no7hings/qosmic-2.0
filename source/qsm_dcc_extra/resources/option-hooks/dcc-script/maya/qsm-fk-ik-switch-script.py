# coding:utf-8
def main(session):
    import qsm_maya.motion as c

    option_opt = session.get_option_opt()

    c.FKIKSwitch.execute_auto(
        **option_opt.to_dict()
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
