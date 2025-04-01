# coding:utf-8


def main(session):
    import lnx_maya_tool.motion.gui.main as m

    w = m.PrxLazyMotionTool(None, session)
    w.show_window_auto()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
