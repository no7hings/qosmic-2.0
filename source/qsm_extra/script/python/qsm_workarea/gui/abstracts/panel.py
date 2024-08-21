# coding:utf-8
import lxgui.proxy.widgets as gui_prx_widgets


class AbsPrxPnlWorkarea(gui_prx_widgets.PrxSessionWindow):
    def __init__(self, session, *args, **kwargs):
        super(AbsPrxPnlWorkarea, self).__init__(session, *args, **kwargs)

    def gui_setup_fnc(self):
        pass
