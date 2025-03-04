# coding:utf-8


class Setup(object):
    LOG_KEY = 'maya setup'

    @classmethod
    def get_is_maya(cls):
        import os

        _ = os.environ.get('MAYA_APP_DIR')
        if _:
            return True
        return False

    @classmethod
    def setup_main_menu(cls):
        def fnc_():
            import lxbasic.log as bsc_log

            import lxmaya.startup as mya_startup

            with bsc_log.LogContext.create(cls.LOG_KEY, 'TD menu'):
                mya_startup.MenuBuild().execute()

        import lxmaya.core as mya_core

        if mya_core.MyaUtil.get_is_ui_mode():
            # noinspection PyUnresolvedReferences
            from maya import cmds

            cmds.evalDeferred(fnc_)

    @classmethod
    def setup_arnold(cls):
        def fnc_():
            import lxbasic.log as bsc_log

            import lxarnold.startup as and_startup

            with bsc_log.LogContext.create(cls.LOG_KEY, 'arnold'):
                and_startup.MayaSetup().run()

        # noinspection PyUnresolvedReferences
        from maya import cmds

        cmds.evalDeferred(fnc_)

    @classmethod
    def setup_usd(cls):
        def fnc_():
            import lxbasic.log as bsc_log

            import lxusd.startup as usd_startup

            with bsc_log.LogContext.create(cls.LOG_KEY, 'USD'):
                usd_startup.UsdSetup.build_environ()

        # noinspection PyUnresolvedReferences
        from maya import cmds

        cmds.evalDeferred(fnc_)

    @classmethod
    def setup_workspace_environment(cls):
        def fnc_():
            import lxmaya.core as mya_core

            import lxmaya.scripts as mya_scripts

            _fnc = mya_scripts.ScpCbkEnvironment().execute
            mya_core.CallbackOpt(_fnc, 'NewSceneOpened').register()
            mya_core.CallbackOpt(_fnc, 'SceneOpened').register()
            mya_core.CallbackOpt(_fnc, 'SceneSaved').register()
            cmds.evalDeferred(_fnc)

        import lxbasic.log as bsc_log
        # noinspection PyUnresolvedReferences
        from maya import cmds

        cmds.evalDeferred(fnc_)

    @classmethod
    def setup_workspace_gui(cls):
        def fnc_():
            import lxgeneral.dcc.scripts as bsd_dcc_scripts

            _fnc = bsd_dcc_scripts.ScpCbkGui().execute
            mya_core.CallbackOpt(_fnc, 'NewSceneOpened').register()
            mya_core.CallbackOpt(_fnc, 'SceneOpened').register()
            mya_core.CallbackOpt(_fnc, 'SceneSaved').register()

        import lxbasic.log as bsc_log

        import lxmaya.core as mya_core

        if mya_core.MyaUtil.get_is_ui_mode():
            # noinspection PyUnresolvedReferences
            from maya import cmds

            cmds.evalDeferred(fnc_)

    @classmethod
    def setup_shelves(cls):
        def fnc_():
            import lxbasic.log as bsc_log

            import qsm_maya.gui as qsm_mya_gui

            with bsc_log.LogContext.create(cls.LOG_KEY, 'shelf'):
                qsm_mya_gui.MainShelf().create()

        # noinspection PyUnresolvedReferences
        from maya import cmds

        cmds.evalDeferred(fnc_)

    @classmethod
    def execute(cls, *args, **kwargs):
        import lxbasic.log as bsc_log

        if cls.get_is_maya():
            with bsc_log.LogContext.create(cls.LOG_KEY, 'setup'):
                cls.setup_main_menu()
                cls.setup_shelves()


if __name__ == '__main__':
    Setup.execute()
