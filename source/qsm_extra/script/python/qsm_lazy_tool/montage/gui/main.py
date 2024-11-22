# coding:utf-8
from . import abstracts as _abstracts

from .pages import resource as _page_resource

from .pages import splicing as _page_splicing


class PrxLazyMontageTool(_abstracts.AbsPrxPanelForMontage):
    PAGE_CLASSES = [
        _page_resource.PrxPageForResource,
        _page_splicing.PrxPageForSplicing,
    ]

    def __init__(self, *args, **kwargs):
        super(PrxLazyMontageTool, self).__init__(*args, **kwargs)
