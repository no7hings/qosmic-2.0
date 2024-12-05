# coding:utf-8
from qsm_lazy_wsp.gui.abstracts import subpage_for_task_create as _sub_page_for_task_create

from ..gui_operates import task_create as _task_create_opt


# cfx rig
class PrxSubpageForShotGnlTestingCreate(_sub_page_for_task_create.AbsPrxSubpageForTaskCreate):
    TASK_CREATE_OPT_CLS = _task_create_opt.DccShotGnlTestingCreateOpt

    GUI_KEY = TASK_CREATE_OPT_CLS.TASK

    def __init__(self, *args, **kwargs):
        super(PrxSubpageForShotGnlTestingCreate, self).__init__(*args, **kwargs)
