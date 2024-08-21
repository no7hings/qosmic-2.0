# coding:utf-8
from .. import abstracts as _abstracts

from . import page_for_resource as _page_for_resource

from . import page_for_splicing as page_for_splicing


class PrxPanelForMontage(_abstracts.AbsPrxPanelForMontage):
    PAGE_CLASSES = [
        # _page_for_resource.PrxPageForResource,
        page_for_splicing.PrxPageForSplicing,
    ]

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPanelForMontage, self).__init__(window, session, *args, **kwargs)
