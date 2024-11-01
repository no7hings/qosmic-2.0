# coding:utf-8
from qsm_lazy_tool.workspace.gui.abstracts import sub_page_for_task_create as _sub_page_for_task_create


class PrxSubPageForAssetTaskCreate(_sub_page_for_task_create.AbsPrxSubPageForAssetTaskCreate):
    def __init__(self, *args, **kwargs):
        super(PrxSubPageForAssetTaskCreate, self).__init__(*args, **kwargs)
