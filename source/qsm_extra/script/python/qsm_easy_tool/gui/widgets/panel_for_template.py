# coding:utf-8
from .. import abstracts as _abstracts

from . import page_for_template as _page_for_node


class PrxPanelForTemplate(_abstracts.AbsPrxPanelForTemplate):
    PAGE_FOR_NODE_CLS = _page_for_node.PrxPageForTemplate

    def __init__(self, session, *args, **kwargs):
        super(PrxPanelForTemplate, self).__init__(session, *args, **kwargs)
