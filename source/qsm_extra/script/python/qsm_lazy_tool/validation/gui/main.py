# coding:utf-8
from . import abstracts as _abstracts

from .pages import rig as _page_rig

from .pages import rig_batch as _page_rig_batch

from .pages import model as _page_model

from .pages import model_batch as _page_model_batch


class PrxLazyValidationTool(_abstracts.AbsPrxPanelForValidation):
    PAGE_CLASS_DICT = dict(
        rig=_page_rig.PrxPageForChrRig,
        rig_batch=_page_rig_batch.PrxPageForChrRigBatch,
        #
        scenery=_page_model.PrxPageForScnModel,
        scenery_batch=_page_model_batch.PrxPageForScnModelBatch
    )

    def __init__(self, window, session, *args, **kwargs):
        super(PrxLazyValidationTool, self).__init__(window, session, *args, **kwargs)
