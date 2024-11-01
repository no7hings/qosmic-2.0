# coding:utf-8


def main(session):
    import lxgui.proxy.core as gui_prx_core

    import qsm_lazy_tool.prc_task.gui.widgets as gui_widgets

    gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
        gui_widgets.PrxPanelForTaskManager,
        window_unique_name=session.get_gui_window_name(),
        window_ask_for_close=True,
        session=session
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
