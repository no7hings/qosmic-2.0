# coding:utf-8
import lxgui.proxy.widgets as gui_prx_widgets

from . import page_for_template as _page_for_node_template


class AbsPrxPanelForTemplate(gui_prx_widgets.PrxSessionWindow):
    PAGE_FOR_NODE_CLS = _page_for_node_template.AbsPrxPageForTemplate

    def __init__(self, session, *args, **kwargs):
        super(AbsPrxPanelForTemplate, self).__init__(session, *args, **kwargs)

    def gui_setup_window(self):
        prx_sca = gui_prx_widgets.PrxVScrollArea()
        self.add_widget(prx_sca)

        self.playblast_prx_page = self.PAGE_FOR_NODE_CLS(
            self, self._session
        )
        prx_sca.add_widget(self.playblast_prx_page)
