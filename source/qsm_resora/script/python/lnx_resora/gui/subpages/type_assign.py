# coding:utf-8
from .. import abstracts as _abstracts


class PrxSubpageForTypeAssign(_abstracts.AbsPrxSubpageForTypeAssign):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(PrxSubpageForTypeAssign, self).__init__(window, session, subwindow, *args, **kwargs)
