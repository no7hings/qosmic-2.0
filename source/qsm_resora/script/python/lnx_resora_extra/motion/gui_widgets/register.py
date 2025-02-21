# coding:utf-8
from lnx_resora.gui import abstracts as lnx_rsr_abstracts


class PrxSubpageForRegister(lnx_rsr_abstracts.AbsPrxSubpageForMotionRegister):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(PrxSubpageForRegister, self).__init__(window, session, subwindow, *args, **kwargs)
