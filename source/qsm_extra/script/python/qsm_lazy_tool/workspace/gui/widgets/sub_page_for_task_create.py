# coding:utf-8
from ..abstracts import sub_page_for_task_create as _sub_page_for_task_create


class PrxSubPageForAssetTaskCreate(_sub_page_for_task_create.AbsPrxSubPageForAssetTaskCreate):
    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(PrxSubPageForAssetTaskCreate, self).__init__(window, session, sub_window, *args, **kwargs)
