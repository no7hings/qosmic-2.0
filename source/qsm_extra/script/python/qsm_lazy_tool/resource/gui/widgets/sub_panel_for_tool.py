# coding:utf-8
from .. import abstracts as _abstracts

from . import page_for_register_tool as _page_for_register_tool

from . import page_for_load_tool as _page_for_load_tool


class PrxSubPanelForTool(_abstracts.AbsPrxSubPanelForRegister):
    PAGE_FOR_REGISTER_CLS = _page_for_register_tool.PrxPageForRegisterTool
    PAGE_FOR_LOAD_CLS = _page_for_load_tool.PrxPageForLoadTool

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForTool, self).__init__(window, session, *args, **kwargs)
