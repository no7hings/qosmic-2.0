# coding:utf-8


class ScpCbkGui(object):
    def __init__(self):
        pass

    @classmethod
    def refresh_tool_kit(cls):
        import lxgui.proxy.core as gui_prx_core

        w = gui_prx_core.GuiProxyUtil.find_window_proxy_by_session_name('dcc-tools/gen-tool-kit')
        if w is not None:
            w.refresh_all()

    @classmethod
    def refresh_all(cls):
        cls.refresh_tool_kit()

    # noinspection PyUnusedLocal
    def execute(self, *args, **kwargs):
        self.refresh_all()
