# coding:utf-8
from ..abstracts import page_for_task_manager as _abs_page_for_task_manager

import qsm_general.wsp_task as qsm_dcc_wsp_task


class PrxPageForTaskManager(_abs_page_for_task_manager.AbsPrxPageForTaskManager):
    TASK_PARSE_CLS = qsm_dcc_wsp_task.TaskParse

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForTaskManager, self).__init__(window, session, *args, **kwargs)
