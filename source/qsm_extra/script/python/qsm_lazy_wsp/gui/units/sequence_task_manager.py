# coding:utf-8
from ... import core as _lzy_wsp_core

from ..abstracts import unit_for_task_manager as _abs_unit_for_task_manager


class PrxUnitForSequenceTaskManager(_abs_unit_for_task_manager.AbsPrxUnitForTaskManager):
    GUI_KEY = 'sequence'

    TASK_PARSE_CLS = _lzy_wsp_core.TaskParse

    RESOURCE_BRANCH = 'sequence'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxUnitForSequenceTaskManager, self).__init__(window, session, *args, **kwargs)
