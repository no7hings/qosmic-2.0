# coding:utf-8
from .... import core as _lzy_wsp_core

from ...abstracts import unit_for_task_manager as _abs_unit_for_task_manager


class GuiTaskManagerMain(_abs_unit_for_task_manager.AbsPrxUnitForTaskManager):
    TASK_PARSE_CLS = _lzy_wsp_core.TaskParse

    RESOURCE_TYPE = TASK_PARSE_CLS.ResourceTypes.Asset

    GUI_KEY = RESOURCE_TYPE

    def __init__(self, window, session, *args, **kwargs):
        super(GuiTaskManagerMain, self).__init__(window, session, *args, **kwargs)
