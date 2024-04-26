# coding:utf-8
import lxgui.proxy.widgets as prx_widgets


class AbsPnlWorkarea(prx_widgets.PrxSessionWindow):
    def __init__(self, session, *args, **kwargs):
        super(AbsPnlWorkarea, self).__init__(session, *args, **kwargs)

    def set_all_setup(self):
        pass
