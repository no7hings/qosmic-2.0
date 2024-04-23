# coding:utf-8


def main(session):
    import lxgui.proxy.core as gui_prx_core

    import lxtool.comparer.gui.widgets as cpr_gui_widgets

    gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
        cpr_gui_widgets.PnlComparerForAssetGeometry, session=session
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
