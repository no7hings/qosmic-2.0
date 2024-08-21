# coding:utf-8
from .. import abstracts as _abstracts

from . import page_for_rig_validation as _page_for_rig


class PrxPanelForValidation(_abstracts.AbsPrxPanelForMontage):
    PAGE_CLASSES = [
        _page_for_rig.PrxPageForRigValidation
    ]

    def __init__(self, session, *args, **kwargs):
        super(PrxPanelForValidation, self).__init__(session, window=None, *args, **kwargs)
