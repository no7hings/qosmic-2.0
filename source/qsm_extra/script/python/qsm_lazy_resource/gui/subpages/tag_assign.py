# coding:utf-8
from .. import abstracts as _abstracts


class PrxSubpageForTagAssign(_abstracts.AbsPrxSubpageForTagAssign):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(PrxSubpageForTagAssign, self).__init__(window, session, subwindow, *args, **kwargs)
