# coding:utf-8


def main(session):
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxbasic.session as bsc_session

    import lxsession.commands as ssn_commands

    import lxgui.qt.core as gui_qt_core

    configure = session.configure

    application = session.application

    gui_name = session.gui_name
    if session.get_devlop_flag() is True:
        gui_name = '[ALPHA] {}'.format(gui_name)
    #
    if session.get_test_flag() is True:
        gui_name = '[BETA] {}'.format(gui_name)

    if application == 'maya':
        import lxmaya.core as mya_core

        import lxmaya.startup as mya_startup

        menu = mya_startup.MenuBuild.get_menu(
            gui_name
        )
        if mya_core.MyaUtil.get_is_ui_mode() is False:
            bsc_log.Log.trace_method_warning(
                'dcc menu build', 'ignore for "batch" mode'
            )
            return
    elif application == 'katana':
        import lxkatana.core as ktn_core

        import lxkatana.startup as ktn_startup

        menu = ktn_startup.KatanaMenuSetup.get_menu(
            gui_name
        )
        if ktn_core.KtnUtil.get_is_ui_mode() is False:
            bsc_log.Log.trace_method_warning(
                'dcc menu build', 'ignore for "batch" mode'
            )
            return
    else:
        raise NotImplementedError()

    menu_content = bsc_session.Hook.generate_menu_content(
        configure.get('hooks'),
        language=bsc_core.BscEnviron.get_gui_language()
    )
    menu_content.update_from(
        bsc_session.OptionHook.generate_menu_content(
            configure.get('option-hooks'),
            language=bsc_core.BscEnviron.get_gui_language(),
        )
    )

    gui_qt_core.GuiQtMenuOpt(menu).create_by_content(
        menu_content
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
