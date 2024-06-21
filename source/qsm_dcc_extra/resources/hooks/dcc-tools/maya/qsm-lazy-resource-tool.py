# coding:utf-8


def main(session):
    import qsm_maya_lazy_tool.resource.gui.widgets as gui_widgets

    w = gui_widgets.PrxSubPanelForTool(None, session)
    w.set_window_show()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
