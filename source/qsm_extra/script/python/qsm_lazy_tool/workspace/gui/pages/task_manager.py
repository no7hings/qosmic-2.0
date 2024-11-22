# coding:utf-8
from ..abstracts import page_for_task_manager as _abs_page_for_task_manager

from ..toolsets import task_manager as _toolset_task_manager

import qsm_wsp_task as qsm_dcc_wsp_task


class PrxPageForTaskManager(_abs_page_for_task_manager.AbsPrxPageForTaskManager):
    TASK_PARSE_CLS = qsm_dcc_wsp_task.TaskParse

    UNIT_CLASSES = [
        _toolset_task_manager.PrxUnitForAssetTaskManager,
        _toolset_task_manager.PrxUnitForShotTaskManager,
    ]

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskManager, self).__init__(*args, **kwargs)
