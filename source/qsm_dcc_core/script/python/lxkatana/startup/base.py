# coding:utf-8
import lxbasic.log as bsc_log

import lxgui.qt.core as gui_qt_core

import lxgui.qt.abstracts as gui_qt_abstracts


class KatanaMenuSetup(gui_qt_abstracts.AsbGuiQtDccMenuSetup):
    def __init__(self):
        super(KatanaMenuSetup, self).__init__()

    @classmethod
    def get_menu(cls, name):
        qt_menu = gui_qt_core.GuiQtKatana.get_menu(name)
        if qt_menu is not None:
            return qt_menu
        #
        qt_menu_bar = gui_qt_core.GuiQtKatana.get_menu_bar()
        if qt_menu_bar:
            # must set parent
            qt_menu = gui_qt_core.QtWidgets.QMenu(qt_menu_bar)
            qt_menu_bar.addMenu(qt_menu)
            qt_menu.setObjectName(name)
            qt_menu.setTitle(name)
            bsc_log.Log.trace_method_result(
                'menu-add',
                u'menu="{}"'.format(name)
            )
            return qt_menu

    def execute(self):
        import lxsession.commands as ssn_commands

        ssn_commands.execute_hook('dcc-menus/gen-menu')


class KatanaEventSetup(object):
    def __init__(self):
        pass

    @classmethod
    def set_run(cls):
        import lxkatana.core as ktn_core

        ktn_core.EventMtd.set_events_register()


class KatanaWorkspaceSetup(object):
    def __init__(self):
        pass

    @classmethod
    def add_environment_callback(cls):
        import lxkatana.core as ktn_core

        import lxkatana.scripts as ktn_scripts

        ktn_core.CallbackMtd.add_as_startup_complete(
            ktn_scripts.ScpCbkEnvironment().execute
        )
        ktn_core.CallbackMtd.add_as_scene_new(
            ktn_scripts.ScpCbkEnvironment().execute
        )
        ktn_core.CallbackMtd.add_as_scene_open(
            ktn_scripts.ScpCbkEnvironment().execute
        )
        ktn_core.CallbackMtd.add_as_scene_save(
            ktn_scripts.ScpCbkEnvironment().execute
        )

    @classmethod
    def add_gui_callback(cls):
        import lxkatana.core as ktn_core

        if ktn_core.KtnUtil.get_is_ui_mode():
            import lxgeneral.dcc.scripts as bsd_dcc_scripts

            fnc = bsd_dcc_scripts.ScpCbkGui().execute
            ktn_core.CallbackMtd.add_as_scene_new(fnc)
            ktn_core.CallbackMtd.add_as_scene_open(fnc)
            ktn_core.CallbackMtd.add_as_scene_save(fnc)

    @classmethod
    def execute(cls):
        cls.add_environment_callback()
        cls.add_gui_callback()


class KatanaCallbackSetup(object):
    def __init__(self):
        pass

    @classmethod
    def set_run(cls):
        import lxkatana.core as ktn_core

        ktn_core.CallbackMtd.add_arnold_callbacks()
