# coding:utf-8


def main(session):
    import lxgui.proxy.core as gui_prx_core

    import qsm_prc_task.gui.widgets as task_gui_widgets

    gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
        task_gui_widgets.PnlTaskMonitor, session=session
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
