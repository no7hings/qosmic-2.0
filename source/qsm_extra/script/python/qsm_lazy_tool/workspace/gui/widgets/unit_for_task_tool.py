# coding:utf-8
from ..abstracts import unit_for_task_tool as _abs_unit_for_task_tool


class GuiNodeOptForGeneral(_abs_unit_for_task_tool.AbsGuiNodeOpt):
    def __init__(self, *args, **kwargs):
        super(GuiNodeOptForGeneral, self).__init__(*args, **kwargs)


class PrxToolsetForGeneral(_abs_unit_for_task_tool.AbsPrxToolset):
    GUI_NODE_OPT_CLS = GuiNodeOptForGeneral

    def __init__(self, *args, **kwargs):
        super(PrxToolsetForGeneral, self).__init__(*args, **kwargs)
