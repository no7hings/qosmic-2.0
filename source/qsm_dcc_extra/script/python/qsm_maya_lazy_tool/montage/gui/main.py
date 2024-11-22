# coding:utf-8
from qsm_lazy_tool.montage.gui import abstracts as _gui_abstracts

from .pages import splicing as _page_splicing


class PrxLazyMontageTool(_gui_abstracts.AbsPrxPanelForMontage):
    PAGE_CLASSES = [
        _page_splicing.PrxPageForSplicing
    ]

    def __init__(self, window, session, *args, **kwargs):
        super(PrxLazyMontageTool, self).__init__(window, session, *args, **kwargs)
