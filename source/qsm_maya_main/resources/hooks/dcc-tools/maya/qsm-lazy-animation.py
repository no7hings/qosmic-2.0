# coding:utf-8


def main(session):
    import lnx_maya_tool.animation.gui.main as m

    w = m.PrxLazyAnimation(window=None, session=None)
    w.show_window_auto()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
