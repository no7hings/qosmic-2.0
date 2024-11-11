# coding:utf-8
from ..abstracts import sub_page_for_task_create as _sub_page_for_task_create


class PrxSubPageForAssetTaskCreate(_sub_page_for_task_create.AbsPrxSubPageForAssetTaskCreate):
    PAGE_KEY = 'asset'

    RESOURCE_BRANCH = 'asset'

    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(PrxSubPageForAssetTaskCreate, self).__init__(window, session, sub_window, *args, **kwargs)


class PrxSubPageForShotTaskCreate(_sub_page_for_task_create.AbsPrxSubPageForAssetTaskCreate):
    PAGE_KEY = 'shot'

    RESOURCE_BRANCH = 'shot'

    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(PrxSubPageForShotTaskCreate, self).__init__(window, session, sub_window, *args, **kwargs)
