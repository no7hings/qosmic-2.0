# coding:utf-8
from . import abstracts as _abstracts

from .pages import splicing as _page_splicing

from .subpanels import new_splicing as _subpanel_new_splicing


class PrxMontageTool(_abstracts.AbsPrxPanelForMontage):
    PAGE_CLASSES = [
        # _page_resource.PrxPageForResource,
        _page_splicing.PrxPageForSplicing,
    ]

    SUBPANEL_CLASSES = [
        _subpanel_new_splicing.PrxSubPanelForNewSplicing
    ]

    def __init__(self, *args, **kwargs):
        super(PrxMontageTool, self).__init__(*args, **kwargs)
