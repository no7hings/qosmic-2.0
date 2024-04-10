# coding:utf-8


if __name__ == '__main__':
    import lxgui.proxy.core as gui_prx_core

    import lxtool.converter.gui.widgets as cvt_gui_widgets

    cvt_gui_widgets.PnlTextureConverter.do_startup()

    # noinspection PyUnresolvedReferences
    gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
        cvt_gui_widgets.PnlTextureConverter, session=session
    )
