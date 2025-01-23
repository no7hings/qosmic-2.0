# coding:utf-8
from .. import abstracts as _abstracts

from ..subpages import type_assign as _subpage_type_assign

from ..subpages import tag_assign as _subpage_tag_assign


class PrxSubPanelForAssign(_abstracts.AbsPrxSubPanelForAssign):
    SUB_PAGE_CLASS_DICT = dict(
        type=_subpage_type_assign.PrxSubpageForTypeAssign,
        tag=_subpage_tag_assign.PrxSubpageForTagAssign
    )

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForAssign, self).__init__(window, session, *args, **kwargs)
