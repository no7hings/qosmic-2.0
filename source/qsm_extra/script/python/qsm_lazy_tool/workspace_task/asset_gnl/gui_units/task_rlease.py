# coding:utf-8
from ....workspace.gui.abstracts import unit_for_task_release as _abs_unit_for_task_release


class _GuiResourceViewOpt(_abs_unit_for_task_release.AbsGuiNodeOptForTaskRelease):
    def __init__(self, *args, **kwargs):
        super(_GuiResourceViewOpt, self).__init__(*args, **kwargs)


class PrxToolsetForGnlRelease(_abs_unit_for_task_release.AbsPrxToolsetForTaskRelease):
    GUI_KEY = 'gnl'

    GUI_RESOURCE_VIEW_CLS = _GuiResourceViewOpt

    def __init__(self, *args, **kwargs):
        super(PrxToolsetForGnlRelease, self).__init__(*args, **kwargs)
