# coding:utf-8
from .. import abstracts as _abstracts


class PrxSubpageForTypeAssign(_abstracts.AbsPrxSubpageForTypeAssign):
    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(PrxSubpageForTypeAssign, self).__init__(window, session, sub_window, *args, **kwargs)


class PrxSubpageForTagAssign(_abstracts.AbsPrxSubpageForTagAssign):
    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(PrxSubpageForTagAssign, self).__init__(window, session, sub_window, *args, **kwargs)
