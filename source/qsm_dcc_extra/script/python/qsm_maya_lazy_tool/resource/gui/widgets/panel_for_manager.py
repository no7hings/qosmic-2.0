# coding:utf-8
import qsm_lazy_tool.resource.gui.abstracts as _abstracts

from . import page_for_manager as _page_for_manager


class PrxPanelForManager(_abstracts.AbsPrxPanelForResource):
    PAGE_FOR_RESOURCE_CLS = _page_for_manager.PrxPageForManager

    def __init__(self, session, *args, **kwargs):
        super(PrxPanelForManager, self).__init__(session, *args, **kwargs)
