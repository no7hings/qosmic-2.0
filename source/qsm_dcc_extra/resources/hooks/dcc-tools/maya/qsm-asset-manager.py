# coding:utf-8


def main(session):
    import qsm_maya_tool.resource_manager.gui.widgets as qsm_rsc_mng_gui_widgets
    w = qsm_rsc_mng_gui_widgets.PnlAssetManager(session)

    w.set_window_show()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
