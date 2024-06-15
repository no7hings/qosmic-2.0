# coding:utf-8
import qsm_lazy_tool.resource.gui.abstracts as _abstracts

from . import page_for_register as _page_for_register


class PrxSubPanelForRegister(_abstracts.AbsPrxSubPanelForRegister):
    PAGE_FOR_REGISTER_CLS = _page_for_register.PrxPageForRegister

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForRegister, self).__init__(window, session, *args, **kwargs)
