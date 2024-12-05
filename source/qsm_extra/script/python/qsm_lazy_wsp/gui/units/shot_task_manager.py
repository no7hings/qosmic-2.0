# coding:utf-8
from ... import core as _lzy_wsp_core

from ..abstracts import unit_for_task_manager as _abs_unit_for_task_manager


class PrxUnitForShotTaskManager(_abs_unit_for_task_manager.AbsPrxUnitForTaskManager):
    GUI_KEY = 'shot'

    TASK_PARSE_CLS = _lzy_wsp_core.TaskParse

    RESOURCE_BRANCH = 'shot'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxUnitForShotTaskManager, self).__init__(window, session, *args, **kwargs)
