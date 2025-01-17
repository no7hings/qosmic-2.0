# coding:utf-8
from . import abstracts as _abstracts

from .pages import splicing as _page_splicing

from .subpanels import new_splicing as _subpanel_new_splicing


class PrxLazyMontageTool(_abstracts.AbsPrxPanelForMontage):
    PAGE_CLASSES = [
        # _page_resource.PrxPageForResource,
        _page_splicing.PrxPageForSplicing,
    ]

    SUB_PANEL_CLASSES = [
        _subpanel_new_splicing.PrxSubPanelForNewSplicing
    ]

    def __init__(self, *args, **kwargs):
        super(PrxLazyMontageTool, self).__init__(*args, **kwargs)
