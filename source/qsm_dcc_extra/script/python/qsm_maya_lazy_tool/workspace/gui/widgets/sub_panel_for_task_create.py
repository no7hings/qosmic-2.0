# coding:utf-8
from qsm_lazy_tool.workspace.gui.abstracts import sub_panel_for_task_create as _sub_panel_for_task_create

from . import sub_page_for_task_create as _sub_page_for_task_create


class PrxSubPanelForTaskCreate(_sub_panel_for_task_create.AbsPrxSubPanelForTaskCreate):
    SUB_PAGE_CLASS_DICT = {
        _sub_page_for_task_create.PrxSubPageForAssetTaskCreate.PAGE_KEY:
        _sub_page_for_task_create.PrxSubPageForAssetTaskCreate
    }

    def __init__(self, *args, **kwargs):
        super(PrxSubPanelForTaskCreate, self).__init__(*args, **kwargs)
