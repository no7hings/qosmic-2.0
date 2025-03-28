# coding:utf-8


def main(session):
    import lnx_maya_montage.gui.main as m

    w = m.PrxMontageTool(window=None, session=session)
    w.show_window_auto()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
