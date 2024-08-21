# coding:utf-8
import qsm_lazy_tool.resource.gui.abstracts as _abstracts

from . import page_for_manager as _page_for_manager


class PrxPanelForResourceManager(_abstracts.AbsPrxPanelForResourceManager):
    PAGE_CLASS_DICT = dict(
        manager=_page_for_manager.PrxPageForResourceManager
    )

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPanelForResourceManager, self).__init__(window, session, *args, **kwargs)
