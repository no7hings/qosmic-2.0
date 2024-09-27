# coding:utf-8
from .. import abstracts as _abstracts

from . import sub_page_for_assign as _sub_page_for_assign


class PrxSubPanelForAssign(_abstracts.AbsPrxSubPanelForAssign):
    SUB_PAGE_CLASS_DICT = dict(
        type=_sub_page_for_assign.PrxSubPageForTypeAssign,
        tag=_sub_page_for_assign.PrxSubPageForTagAssign
    )

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForAssign, self).__init__(window, session, *args, **kwargs)
