# coding:utf-8
import lxbasic.log as bsc_log

import lxgui.qt.core as gui_qt_core

import lxgui.qt.abstracts as gui_qt_abstracts


class MenuBuild(gui_qt_abstracts.AsbGuiQtDccMenuSetup):
    KEY = 'menu build'

    def __init__(self):
        super(MenuBuild, self).__init__()

    @classmethod
    def get_menu(cls, name):
        qt_menu = gui_qt_core.QtMaya.get_qt_menu(name)
        if qt_menu is not None:
            return qt_menu

        qt_menu_bar = gui_qt_core.QtMaya.get_qt_menu_bar()
        if qt_menu_bar:
            # must set parent
            qt_menu = gui_qt_core.QtWidgets.QMenu(qt_menu_bar)
            qt_menu_bar.addMenu(qt_menu)
            qt_menu.setObjectName(name)
            qt_menu.setTitle(name)
            bsc_log.Log.trace_method_result(
                cls.KEY,
                'add menu: "{}"'.format(name)
            )
            qt_menu.setTearOffEnabled(True)
            return qt_menu

    def execute(self):
        with bsc_log.LogContext.create(self.KEY):
            import lxsession.commands as ssn_commands
            ssn_commands.execute_hook('dcc-menus/gen-menu')
