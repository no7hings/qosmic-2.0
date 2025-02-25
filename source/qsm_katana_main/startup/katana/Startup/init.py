# coding:utf-8
import sys
# noinspection PyUnresolvedReferences
from Katana import Callbacks


class Setup(object):
    LOG_KEY = 'katana setup'

    @classmethod
    def build_menu(cls):
        import lxbasic.log as bsc_log

        import lxkatana.core as ktn_core

        import lxkatana.startup as ktn_startup

        if ktn_core.KtnUtil.get_is_ui_mode():
            with bsc_log.LogContext.create(cls.LOG_KEY, 'register menu'):
                ktn_startup.KatanaMenuSetup().execute()

    @classmethod
    def build_lua(cls):
        import lxbasic.resource as bsc_resource

        import lxbasic.core as bsc_core

        bsc_core.BscEnvironExtra.append_lua_path(
            '{}/?.lua'.format(
                bsc_resource.BscExtendResource.get(
                    'lua-scripts'
                )
            )
        )

    @classmethod
    def build_workspace(cls):
        import lxbasic.log as bsc_log

        import lxkatana.startup as ktn_startup

        with bsc_log.LogContext.create(cls.LOG_KEY, 'register workspace'):
            ktn_startup.KatanaWorkspaceSetup().execute()

    @classmethod
    def build_hot_key(cls):
        import lxbasic.log as bsc_log

        import lxkatana.core as ktn_core

        import lxkatana.scripts as ktn_scripts

        if ktn_core.KtnUtil.get_is_ui_mode():
            with bsc_log.LogContext.create(cls.LOG_KEY, 'register hot key'):
                ktn_scripts.ScpHotKeyForNodeGraphLayout().register()
                ktn_scripts.ScpHotKeyForNodeGraphPaste().register()

    @classmethod
    def set_run(cls, *args, **kwargs):
        import lxbasic.log as bsc_log

        with bsc_log.LogContext.create(cls.LOG_KEY, 'all'):
            cls.build_menu()
            cls.build_lua()
            # cls.build_hot_key()
            # cls.build_workspace()


class ArnoldSetup(object):
    LOG_KEY = 'arnold setup'

    @classmethod
    def set_events_register(cls):
        import lxbasic.log as bsc_log

        import lxkatana.core as ktn_core

        import lxkatana.scripts as ktn_scripts

        with bsc_log.LogContext.create(cls.LOG_KEY, 'register event'):

            ss = [
                (ktn_scripts.ScpEventForArnold.on_material_create, ktn_core.EventOpt.EventType.NodeCreate),
                (ktn_scripts.ScpEventForArnold.on_node_group_create, ktn_core.EventOpt.EventType.NodeCreate),
                (ktn_scripts.ScpEventForArnold.on_shader_create, ktn_core.EventOpt.EventType.NodeCreate),
                (ktn_scripts.ScpEventForArnold.on_image_create, ktn_core.EventOpt.EventType.NodeCreate),
            ]
            #
            for handler, event_type in ss:
                event_opt = ktn_core.EventOpt(
                    handler=handler, event_type=event_type
                )
                event_opt.register()

    @classmethod
    def set_callbacks_register(cls):
        pass

    @classmethod
    def set_run(cls, *args, **kwargs):
        import lxbasic.log as bsc_log

        with bsc_log.LogContext.create(cls.LOG_KEY, 'all'):
            cls.set_events_register()
            cls.set_callbacks_register()


Callbacks.addCallback(
    callbackType=Callbacks.Type.onStartupComplete,
    callbackFcn=Setup.set_run
)

Callbacks.addCallback(
    callbackType=Callbacks.Type.onStartupComplete,
    callbackFcn=ArnoldSetup.set_run
)
