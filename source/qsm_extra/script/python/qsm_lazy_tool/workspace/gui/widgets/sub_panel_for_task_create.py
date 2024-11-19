# coding:utf-8
from ..abstracts import sub_panel_for_task_create as _sub_panel_for_task_create

from . import sub_page_for_task_create as _sub_page_for_task_create


class PrxSubPanelForTaskCreate(_sub_panel_for_task_create.AbsPrxSubPanelForTaskCreate):
    SUB_PAGE_CLASSES = [
        _sub_page_for_task_create.PrxSubPageForAssetCfxRigCreate,
        _sub_page_for_task_create.PrxSubPageForShotCfxClothCreate,
        _sub_page_for_task_create.PrxSubPageForShotCfxDressingCreate
    ]

    RESOURCE_BRANCH = 'shot'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForTaskCreate, self).__init__(window, session, *args, **kwargs)
