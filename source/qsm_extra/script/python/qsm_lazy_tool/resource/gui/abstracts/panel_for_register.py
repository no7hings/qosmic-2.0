# coding:utf-8
import lxgui.proxy.widgets as gui_prx_widgets

from . import page_for_resource as _page_for_resource


class AbsPanelForRegister(gui_prx_widgets.PrxBaseWindow):
    PAGE_FOR_NODE_CLS = _page_for_resource.AbsPrxPageForResource

    def __init__(self, *args, **kwargs):
        super(AbsPanelForRegister, self).__init__(*args, **kwargs)

    def gui_setup_window(self):
        prx_sca = gui_prx_widgets.PrxVScrollArea()
        self.add_widget(prx_sca)

