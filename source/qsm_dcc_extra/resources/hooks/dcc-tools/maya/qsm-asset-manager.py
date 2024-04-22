# coding:utf-8


def main(session):
    import qsm_tool.manager.gui.widgets as qsm_manager_gui_widgets
    w = qsm_manager_gui_widgets.PnlAssetManager(session)

    w.set_window_show()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
