# coding:utf-8
from qsm_lazy_workspace.gui.abstracts import subpage_for_task_create as _sub_page_for_task_create

from ..gui_operates import task_create as _task_create_opt


# cfx rig
class PrxSubpageForAssetGnlTestingCreate(_sub_page_for_task_create.AbsPrxSubpageForTaskCreate):
    TASK_CREATE_OPT_CLS = _task_create_opt.DccAssetGnlTestingCreateOpt

    GUI_KEY = '{}/{}'.format(TASK_CREATE_OPT_CLS.RESOURCE_TYPE, TASK_CREATE_OPT_CLS.TASK)

    def __init__(self, *args, **kwargs):
        super(PrxSubpageForAssetGnlTestingCreate, self).__init__(*args, **kwargs)
