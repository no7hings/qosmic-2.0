# coding:utf-8


def main(session):
    import qsm_maya_easy_tool.gui.widgets as gui_widgets
    w = gui_widgets.PrxPanelForEasyPlayblast(session)

    w.set_window_show()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
