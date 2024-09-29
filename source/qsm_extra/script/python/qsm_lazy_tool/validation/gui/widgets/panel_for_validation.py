# coding:utf-8
from .. import abstracts as _abstracts

from . import page_for_rig as _page_for_rig

from . import page_for_scenery as _page_for_model


class PrxPanelForValidation(_abstracts.AbsPrxPanelForMontage):
    PAGE_CLASSES = [
        _page_for_rig.PrxPageForRig,
        _page_for_model.PrxPageForScenery,
    ]

    PAGE_CLASS_DICT = dict(
        rig=_page_for_rig.PrxPageForRig,
        scenery=_page_for_model.PrxPageForScenery,
    )

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPanelForValidation, self).__init__(window, session, *args, **kwargs)
