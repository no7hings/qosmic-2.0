# coding:utf-8
from . import abstracts as _abstracts

from .pages import rig as _page_rig

from .pages import rig_batch as _page_rig_batch

from .pages import model as _page_model

from .pages import model_batch as _page_model_batch


class PrxLazyValidationTool(_abstracts.AbsPrxPanelForValidation):
    GUI_KEY = 'lazy-validation'

    CONFIGURE_KEY = None

    PAGE_CLASSES = [
        # rig
        _page_rig.PrxPageForChrRig,
        _page_rig_batch.PrxPageForChrRigBatch,
        # model
        _page_model.PrxPageForScnModel,
        _page_model_batch.PrxPageForScnModelBatch
    ]

    def __init__(self, window, session, *args, **kwargs):
        super(PrxLazyValidationTool, self).__init__(window, session, *args, **kwargs)
