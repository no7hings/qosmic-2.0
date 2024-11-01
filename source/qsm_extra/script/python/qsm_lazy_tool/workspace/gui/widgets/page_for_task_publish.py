# coding:utf-8
from ..abstracts import page_for_task_publish as _abs_page_for_task_publish


class PrxPageForTaskPublish(_abs_page_for_task_publish.AbsPrxPageForTaskPublish):
    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForTaskPublish, self).__init__(window, session, *args, **kwargs)
