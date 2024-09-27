# coding:utf-8
from .. import abstracts as _abstracts

from . import page_for_manager as _page_for_manager

from . import sub_panel_for_register as _sub_panel_for_register


class PrxPanelForResourceManager(_abstracts.AbsPrxPanelForResourceManager):
    PAGE_CLASS_DICT = dict(
        manager=_page_for_manager.PrxPageForResourceManager
    )

    SUB_PANEL_CLASS_DICT = dict(
        register=_sub_panel_for_register.PrxSubPanelForRegister
    )

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPanelForResourceManager, self).__init__(window, session, *args, **kwargs)
