# coding:utf-8
from .. import abstracts as _abstracts

from . import page_for_rig as _page_for_rig

from . import page_for_rig_batch as _page_for_rig_batch

from . import page_for_scenery as _page_for_model

from . import page_for_scenery_batch as _page_for_scenery_batch


class PrxPanelForValidation(_abstracts.AbsPrxPanelForValidation):
    PAGE_CLASS_DICT = dict(
        rig=_page_for_rig.PrxPageForRig,
        rig_batch=_page_for_rig_batch.PrxPageForRigBatch,
        scenery=_page_for_model.PrxPageForScenery,
        scenery_batch=_page_for_scenery_batch.PrxPageForSceneryBatch
    )

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPanelForValidation, self).__init__(window, session, *args, **kwargs)
