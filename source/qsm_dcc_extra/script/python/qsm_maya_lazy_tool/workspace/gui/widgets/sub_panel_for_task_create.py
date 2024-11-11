# coding:utf-8
from qsm_lazy_tool.workspace.gui.abstracts import sub_panel_for_task_create as _sub_panel_for_task_create

from . import sub_page_for_task_create as _sub_page_for_task_create


class PrxSubPanelForAssetTaskCreate(_sub_panel_for_task_create.AbsPrxSubPanelForTaskCreate):
    SUB_PAGE_CLASS_DICT = {
        _sub_page_for_task_create.PrxSubPageForAssetTaskCreate.PAGE_KEY:
        _sub_page_for_task_create.PrxSubPageForAssetTaskCreate
    }

    RESOURCE_BRANCH = 'asset'

    def __init__(self, *args, **kwargs):
        super(PrxSubPanelForAssetTaskCreate, self).__init__(*args, **kwargs)


class PrxSubPanelForShotTaskCreate(_sub_panel_for_task_create.AbsPrxSubPanelForTaskCreate):
    SUB_PAGE_CLASS_DICT = {
        _sub_page_for_task_create.PrxSubPageForShotTaskCreate.PAGE_KEY:
        _sub_page_for_task_create.PrxSubPageForShotTaskCreate
    }

    RESOURCE_BRANCH = 'shot'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForShotTaskCreate, self).__init__(window, session, *args, **kwargs)
