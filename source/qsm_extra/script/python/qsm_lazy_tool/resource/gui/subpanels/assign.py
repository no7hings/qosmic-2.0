# coding:utf-8
from .. import abstracts as _abstracts

from ..subpages import assign as _subpage_assign


class PrxSubPanelForAssign(_abstracts.AbsPrxSubPanelForAssign):
    SUB_PAGE_CLASS_DICT = dict(
        type=_subpage_assign.PrxSubPageForTypeAssign,
        tag=_subpage_assign.PrxSubPageForTagAssign
    )

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForAssign, self).__init__(window, session, *args, **kwargs)
