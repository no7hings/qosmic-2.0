# coding:utf-8


def main(session):
    import lxgui.proxy.core as gui_prx_core

    import qsm_lazy_tool.resource.gui.widgets as gui_widgets

    gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
        gui_widgets.PrxPanelForResource,
        window_unique_name=session.get_gui_window_name(),
        session=session
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
