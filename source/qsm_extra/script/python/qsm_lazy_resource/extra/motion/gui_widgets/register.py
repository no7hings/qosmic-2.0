# coding:utf-8
from ....gui import abstracts as _abstracts


class PrxSubpageForMotionRegister(_abstracts.AbsPrxSubpageForMotionRegister):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(PrxSubpageForMotionRegister, self).__init__(window, session, subwindow, *args, **kwargs)
