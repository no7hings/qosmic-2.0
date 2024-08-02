# coding:utf-8
from qsm_lazy_tool.montage.gui import abstracts as _gui_abstracts

from . import page_for_composition as _page_for_composition


class PrxSubPanelForMontage(_gui_abstracts.AbsPrxSubPanelForMontage):
    PAGE_FOR_COMPOSITION = _page_for_composition.PrxPageForComposition

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForMontage, self).__init__(window, session, *args, **kwargs)
