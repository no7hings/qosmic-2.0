# coding:utf-8


def main(session):
    import qsm_maya_lazy_tool.resource.gui.main as m

    w = m.PrxLazyResourceTool(window=None, session=session)
    w.show_window_auto()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
