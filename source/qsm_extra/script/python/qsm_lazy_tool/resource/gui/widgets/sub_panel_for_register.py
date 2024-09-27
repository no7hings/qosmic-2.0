# coding:utf-8
from .. import abstracts as _abstracts

from . import sub_page_for_register as _sub_page_for_register


class PrxSubPanelForRegister(_abstracts.AbsPrxSubPanelForRegister):
    SUB_PAGE_CLASS_DICT = dict(
        motion=_sub_page_for_register.PrxSubPageForMotionRegister,
        video=_sub_page_for_register.PrxSubPageForVideoRegister,
        audio=_sub_page_for_register.PrxSubPageForAudioRegister,
    )

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForRegister, self).__init__(window, session, *args, **kwargs)
