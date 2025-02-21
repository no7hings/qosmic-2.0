# coding:utf-8
from .. import abstracts as _abstracts


class PrxSubPanelForRegister(_abstracts.AbsPrxSubPanelForRegister):

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForRegister, self).__init__(window, session, *args, **kwargs)
