# coding:utf-8


def main(session):
    import lxgui.proxy.core as gui_prx_core

    import lxtool.publisher.gui.widgets as pbs_gui_widgets

    gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
        pbs_gui_widgets.PnlGeneralPublish, session=session
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
