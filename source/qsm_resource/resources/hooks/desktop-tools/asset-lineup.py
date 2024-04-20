# coding:utf-8


def main(session):
    import lxgui.proxy.core as gui_prx_core

    import lxtool.graph.gui.widgets as grh_gui_widgets

    gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
        grh_gui_widgets.PnlAssetLineup, session=session
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
