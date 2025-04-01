# coding:utf-8
from . import abstracts as _abstracts

from .pages import register as _page_register

from .pages import load as _page_load


class PrxLazyResourceCfxTool(_abstracts.AbsPrxSubPanelForTool):
    PAGE_FOR_REGISTER_TOOL_CLS = _page_register.PrxPageForRegisterTool
    PAGE_FOR_LOAD_TOOL_CLS = _page_load.PrxPageForLoadTool

    def __init__(self, window, session, *args, **kwargs):
        super(PrxLazyResourceCfxTool, self).__init__(window, session, *args, **kwargs)
