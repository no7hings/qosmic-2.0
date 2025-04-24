# coding:utf-8
from . import abstracts as _abstracts

from .pages import manager as _page_manager

from .subpanels import register as _subpanel_register


class PrxResoraTool(_abstracts.AbsPrxResoraPanel):
    PAGE_CLASS_DICT = dict(
        manager=_page_manager.PrxPageForResourceManager
    )

    SUB_PANEL_CLASS_DICT = dict(
        register=_subpanel_register.PrxSubpanelForRegister
    )

    def __init__(self, window, session, *args, **kwargs):
        super(PrxResoraTool, self).__init__(window, session, *args, **kwargs)
