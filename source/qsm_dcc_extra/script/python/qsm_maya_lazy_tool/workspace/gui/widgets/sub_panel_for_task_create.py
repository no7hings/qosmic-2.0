# coding:utf-8
from qsm_lazy_tool.workspace.gui.abstracts import sub_panel_for_task_create as _sub_panel_for_task_create

from . import sub_page_for_task_create as _sub_page_for_task_create


class PrxSubPanelForAssetTaskCreate(_sub_panel_for_task_create.AbsPrxSubPanelForTaskCreate):
    CONFIGURE_KEY = 'lazy-workspace/gui/asset_task_create'

    SUB_PAGE_CLASS_DICT = {
        _sub_page_for_task_create.PrxSubPageForAssetCfxRigCreate.GUI_KEY:
        _sub_page_for_task_create.PrxSubPageForAssetCfxRigCreate
    }

    SUB_PAGE_KEYS = [
        _sub_page_for_task_create.PrxSubPageForAssetCfxRigCreate.GUI_KEY
    ]

    RESOURCE_BRANCH = 'asset'

    def __init__(self, *args, **kwargs):
        super(PrxSubPanelForAssetTaskCreate, self).__init__(*args, **kwargs)


class PrxSubPanelForShotTaskCreate(_sub_panel_for_task_create.AbsPrxSubPanelForTaskCreate):
    CONFIGURE_KEY = 'lazy-workspace/gui/shot_task_create'

    SUB_PAGE_CLASS_DICT = {
        _sub_page_for_task_create.PrxSubPageForShotCfxClothCreate.GUI_KEY:
        _sub_page_for_task_create.PrxSubPageForShotCfxClothCreate,
        _sub_page_for_task_create.PrxSubPageForShotCfxDressingCreate.GUI_KEY:
        _sub_page_for_task_create.PrxSubPageForShotCfxDressingCreate
    }

    SUB_PAGE_KEYS = [
        _sub_page_for_task_create.PrxSubPageForShotCfxClothCreate.GUI_KEY,
        _sub_page_for_task_create.PrxSubPageForShotCfxDressingCreate.GUI_KEY
    ]

    RESOURCE_BRANCH = 'shot'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForShotTaskCreate, self).__init__(window, session, *args, **kwargs)
