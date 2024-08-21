# coding:utf-8
from .. import abstracts as _abstracts

from . import sub_page_for_register as _sub_page_for_register


class PrxSubPanelForResourceRegister(_abstracts.AbsPrxSubPanelForResourceRegister):
    SUB_PAGE_CLASS_DICT = dict(
        motion=_sub_page_for_register.PrxSubPageForResourceMotionRegister
    )

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForResourceRegister, self).__init__(window, session, *args, **kwargs)
