# coding:utf-8
from ..abstracts import unit_for_task_tool as _abs_unit_for_task_tool


class GuiNodeOptForGnlTool(_abs_unit_for_task_tool.AbsGuiNodeOptForTaskTool):
    def __init__(self, *args, **kwargs):
        super(GuiNodeOptForGnlTool, self).__init__(*args, **kwargs)


class PrxToolsetForGnlTool(_abs_unit_for_task_tool.AbsPrxToolsetForTaskTool):
    UNIT_KEY = 'gnl'

    GUI_NODE_OPT_CLS = GuiNodeOptForGnlTool

    def __init__(self, *args, **kwargs):
        super(PrxToolsetForGnlTool, self).__init__(*args, **kwargs)
