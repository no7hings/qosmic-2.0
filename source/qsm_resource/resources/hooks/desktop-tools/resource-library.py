# coding:utf-8


def main(session):
    import lxgui.proxy.core as gui_prx_core

    import lxtool.library.gui.widgets as lib_gui_widgets

    gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
        lib_gui_widgets.PnlLibraryForResource, session=session
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
