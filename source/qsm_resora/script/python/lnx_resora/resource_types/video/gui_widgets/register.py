# coding:utf-8
from ....gui import abstracts as _abstracts


class PrxSubpageForRegister(_abstracts.AbsPrxSubpageForVideoRegister):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(PrxSubpageForRegister, self).__init__(window, session, subwindow, *args, **kwargs)
