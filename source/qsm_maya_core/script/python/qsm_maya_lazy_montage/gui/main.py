# coding:utf-8
from qsm_lazy_montage.gui.abstracts import panel_for_main as _panel_for_montage

from .pages import splicing as _page_splicing

from .subpanels import new_splicing as _subpanel_new_splicing


class PrxLazyMontageTool(_panel_for_montage.AbsPrxPanelForMontage):
    PAGE_CLASSES = [
        _page_splicing.PrxPageForSplicing
    ]

    SUB_PANEL_CLASSES = [
        _subpanel_new_splicing.PrxSubPanelForNewSplicing
    ]

    def __init__(self, window, session, *args, **kwargs):
        super(PrxLazyMontageTool, self).__init__(window, session, *args, **kwargs)
