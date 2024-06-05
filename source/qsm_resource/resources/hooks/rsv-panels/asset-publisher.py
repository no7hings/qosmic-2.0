# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxgui.qt.core as gui_qt_core

    import lxgui.proxy.core as gui_prx_core

    if bsc_core.BasApplication.get_is_dcc():
        if bsc_core.BasApplication.get_is_katana():
            import lxkatana_gui.tool.widgets as ktn_gui_tol_widgets
            gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
                ktn_gui_tol_widgets.PnlPublisherForSurface, session=session
            )
        elif bsc_core.BasApplication.get_is_maya():
            import lxmaya_gui.tool.widgets as mya_tol_widgets
            gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
                mya_tol_widgets.PnlPublisherForSurface, session=session
            )
    else:
        import lxtool.publisher.gui.widgets as pbs_gui_widgets
        gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
            pbs_gui_widgets.PnlPublisherForSurface, session=session
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
