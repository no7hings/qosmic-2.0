# coding:utf-8


def main(session):
    import qsm_maya_lazy_tool.resource.gui.widgets as gui_widgets
    w = gui_widgets.PrxPanelForResourceManager(window=None, session=session)
    w.show_window_auto()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
