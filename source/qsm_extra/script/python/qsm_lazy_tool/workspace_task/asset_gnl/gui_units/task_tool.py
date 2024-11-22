# coding:utf-8
from ....workspace.gui.abstracts import unit_for_task_tool as _abs_unit_for_task_tool


class _GuiResourceViewOpt(_abs_unit_for_task_tool.AbsGuiResourceViewForTaskTool):
    def __init__(self, *args, **kwargs):
        super(_GuiResourceViewOpt, self).__init__(*args, **kwargs)


class _PrxBasicToolset(_abs_unit_for_task_tool.AbsPrxToolsetForTaskTool):
    GUI_KEY = 'basic'

    def __init__(self, *args, **kwargs):
        super(_PrxBasicToolset, self).__init__(*args, **kwargs)


class PrxUnitForGnlTool(_abs_unit_for_task_tool.AbsPrxUnitForTaskTool):
    GUI_KEY = 'gnl'

    GUI_RESOURCE_VIEW_CLS = _GuiResourceViewOpt

    TOOLSET_CLASSES = [
        _PrxBasicToolset
    ]

    def __init__(self, *args, **kwargs):
        super(PrxUnitForGnlTool, self).__init__(*args, **kwargs)
