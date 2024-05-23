# coding:utf-8


def main(session):
    import lxgui.core as gui_core

    content = None

    application = session.application
    if application == 'maya':
        import lxmaya_gui.tool.widgets as mya_tol_widgets
        mya_tol_widgets.PnlManagerForAssetTextureDcc(session).set_window_show()
    elif application == 'katana':
        import lxkatana_gui.tool.widgets as ktn_gui_tol_widgets
        ktn_gui_tol_widgets.PnlManagerForAssetTextureDcc(session).set_window_show()
    else:
        content = u'application "{}" is not supported'.format(application)

    if content is not None:
        gui_core.GuiDialog.create(
            session.gui_name,
            content=content,
            status=gui_core.GuiDialog.ValidationStatus.Error,
            #
            ok_label='Close',
            #
            no_visible=False, cancel_visible=False
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
