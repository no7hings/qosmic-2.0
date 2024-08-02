# coding:utf-8
from .. import abstracts as _abstracts

from . import page_for_composition as _page_for_composition


class PrxSubPanelForMontage(_abstracts.AbsPrxSubPanelForMontage):
    PAGE_FOR_COMPOSITION = _page_for_composition.PrxPageForComposition

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForMontage, self).__init__(window, session, *args, **kwargs)
