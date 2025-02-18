# coding:utf-8


def main(session):
    import lxgui.proxy.core as gui_prx_core

    import lnx_katana_wotrix.gui.main as m

    gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
        m.PrxWotrixTool,
        window_unique_name=session.get_gui_window_name(),
        window=None,
        session=session
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
