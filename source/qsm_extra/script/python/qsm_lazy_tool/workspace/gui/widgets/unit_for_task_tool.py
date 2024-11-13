# coding:utf-8
from ..abstracts import unit_for_task_tool as _abs_unit_for_task_tool


class GuiNodeOptForGnlTool(_abs_unit_for_task_tool.AbsGuiResourceViewForTaskTool):
    def __init__(self, *args, **kwargs):
        super(GuiNodeOptForGnlTool, self).__init__(*args, **kwargs)
        

class PrxMainToolsetForGnlTool(_abs_unit_for_task_tool.AbsPrxToolsetForTaskTool):
    GUI_KEY = 'basic'

    def __init__(self, *args, **kwargs):
        super(PrxMainToolsetForGnlTool, self).__init__(*args, **kwargs)


class PrxUnitForGnlTool(_abs_unit_for_task_tool.AbsPrxUnitForTaskTool):
    GUI_KEY = 'gnl'

    GUI_RESOURCE_VIEW_CLS = GuiNodeOptForGnlTool
    
    TOOLSET_CLASSES = [
        PrxMainToolsetForGnlTool
    ]

    def __init__(self, *args, **kwargs):
        super(PrxUnitForGnlTool, self).__init__(*args, **kwargs)
