# coding:utf-8
from qsm_lazy_tool.workspace.gui.abstracts import page_for_task_manager as _abs_page_for_task_manager

from . import unit_for_task_manager as _unit_for_task_manager

import qsm_maya_wsp_task as qsm_mya_wsp_task


class PrxPageForTaskManager(_abs_page_for_task_manager.AbsPrxPageForTaskManager):
    TASK_PARSE_CLS = qsm_mya_wsp_task.TaskParse

    UNIT_CLASSES = [
        _unit_for_task_manager.PrxUnitForAssetTaskManager,
        _unit_for_task_manager.PrxUnitForShotTaskManager,
    ]

    def __init__(self, *args, **kwargs):
        super(PrxPageForTaskManager, self).__init__(*args, **kwargs)
