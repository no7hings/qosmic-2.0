# coding:utf-8
from lnx_montage.gui.abstracts import panel_for_main as _panel_for_montage

from .pages import splicing as _page_splicing

from .subpanels import new_splicing as _subpanel_new_splicing


class PrxMontageTool(_panel_for_montage.AbsPrxPanelForMontage):
    PAGE_CLASSES = [
        _page_splicing.PrxPageForSplicing
    ]

    SUBPANEL_CLASSES = [
        _subpanel_new_splicing.PrxSubPanelForNewSplicing
    ]

    def __init__(self, window, session, *args, **kwargs):
        super(PrxMontageTool, self).__init__(window, session, *args, **kwargs)
