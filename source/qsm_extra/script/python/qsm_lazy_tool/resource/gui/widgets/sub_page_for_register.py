# coding:utf-8
from .. import abstracts as _abstracts


class PrxSubPageForResourceMotionRegister(_abstracts.AbsPrxSubPageForResourceMotionRegister):
    PAGE_KEY = 'motion'

    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(PrxSubPageForResourceMotionRegister, self).__init__(window, session, sub_window, *args, **kwargs)
