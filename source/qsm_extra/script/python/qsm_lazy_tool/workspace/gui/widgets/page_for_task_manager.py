# coding:utf-8
from ..abstracts import page_for_task_manager as _abs_page_for_task_manager

import qsm_lazy.workspace.core as qsm_lzy_wsp_core


class PrxPageForTaskManager(_abs_page_for_task_manager.AbsPrxPageForTaskManager):
    TASK_PARSE_CLS = qsm_lzy_wsp_core.TaskParse

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForTaskManager, self).__init__(window, session, *args, **kwargs)
