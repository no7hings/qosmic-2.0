# coding:utf-8
import qsm_lazy_tool.resource.gui.abstracts as _abstracts

from . import page_for_resource as _page_for_resource


class PrxPanelForResource(_abstracts.AbsPrxPanelForResource):
    PAGE_FOR_RESOURCE_CLS = _page_for_resource.PrxPageForResource

    def __init__(self, session, *args, **kwargs):
        super(PrxPanelForResource, self).__init__(session, *args, **kwargs)
