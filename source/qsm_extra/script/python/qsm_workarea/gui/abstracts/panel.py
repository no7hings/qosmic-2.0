# coding:utf-8
import lxgui.proxy.widgets as prx_widgets


class AbsPrxPnlWorkarea(prx_widgets.PrxSessionWindow):
    def __init__(self, session, *args, **kwargs):
        super(AbsPrxPnlWorkarea, self).__init__(session, *args, **kwargs)

    def gui_setup_window(self):
        pass
