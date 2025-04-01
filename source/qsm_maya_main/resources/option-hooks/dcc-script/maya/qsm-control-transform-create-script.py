# coding:utf-8
def main(session):
    import qsm_maya.handles.animation.scripts as s

    option_opt = session.get_option_opt()

    s.ControlTransformOpt.create_auto(
        **option_opt.to_dict()
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
