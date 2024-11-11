# coding:utf-8
from ..abstracts import page_for_task_manager as _abs_page_for_task_manager

import qsm_general.wsp_task as qsm_dcc_wsp_task


class PrxPageForAssetTaskManager(_abs_page_for_task_manager.AbsPrxPageForTaskManager):
    TASK_PARSE_CLS = qsm_dcc_wsp_task.TaskParse

    RESOURCE_BRANCH = 'asset'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForAssetTaskManager, self).__init__(window, session, *args, **kwargs)


class PrxPageForShotTaskManager(_abs_page_for_task_manager.AbsPrxPageForTaskManager):
    TASK_PARSE_CLS = qsm_dcc_wsp_task.TaskParse

    RESOURCE_BRANCH = 'shot'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForShotTaskManager, self).__init__(window, session, *args, **kwargs)