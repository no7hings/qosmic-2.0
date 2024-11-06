# coding:utf-8
from ..abstracts import unit_for_task_release as _abs_unit_for_task_publish


class GuiNodeOptForGnlRelease(_abs_unit_for_task_publish.AbsGuiNodeOptForTaskRelease):
    def __init__(self, *args, **kwargs):
        super(GuiNodeOptForGnlRelease, self).__init__(*args, **kwargs)


class PrxToolsetForGnlRelease(_abs_unit_for_task_publish.AbsPrxToolsetForTaskRelease):
    UNIT_KEY = 'gnl'

    GUI_NODE_OPT_CLS = GuiNodeOptForGnlRelease

    def __init__(self, *args, **kwargs):
        super(PrxToolsetForGnlRelease, self).__init__(*args, **kwargs)
