# coding:utf-8
from qsm_lazy_tool.montage.gui import abstracts as _gui_abstracts

from . import page_for_splicing as _page_for_splicing


class PrxPanelForMontage(_gui_abstracts.AbsPrxPanelForMontage):
    PAGE_CLASSES = [
        _page_for_splicing.PrxPageForSplicing
    ]

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPanelForMontage, self).__init__(window, session, *args, **kwargs)
