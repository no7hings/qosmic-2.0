# coding:utf-8
from ..abstracts import unit_for_task_manager as _abs_unit_for_task_manager

import qsm_wsp_task as qsm_dcc_wsp_task


class PrxUnitForAssetTaskManager(_abs_unit_for_task_manager.AbsPrxUnitForTaskManager):
    GUI_KEY = 'asset'

    TASK_PARSE_CLS = qsm_dcc_wsp_task.TaskParse

    RESOURCE_BRANCH = 'asset'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxUnitForAssetTaskManager, self).__init__(window, session, *args, **kwargs)


class PrxUnitForShotTaskManager(_abs_unit_for_task_manager.AbsPrxUnitForTaskManager):
    GUI_KEY = 'shot'

    TASK_PARSE_CLS = qsm_dcc_wsp_task.TaskParse

    RESOURCE_BRANCH = 'shot'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxUnitForShotTaskManager, self).__init__(window, session, *args, **kwargs)
