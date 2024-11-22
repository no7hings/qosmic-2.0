# coding:utf-8
from .. import abstracts as _abstracts


class PrxSubPageForTypeAssign(_abstracts.AbsPrxSubPageForTypeAssign):
    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(PrxSubPageForTypeAssign, self).__init__(window, session, sub_window, *args, **kwargs)


class PrxSubPageForTagAssign(_abstracts.AbsPrxSubPageForTagAssign):
    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(PrxSubPageForTagAssign, self).__init__(window, session, sub_window, *args, **kwargs)
