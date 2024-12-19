# coding:utf-8
import qsm_lazy_wsp.core as lzy_wsp_core


class DccShotTaskCreateOpt(lzy_wsp_core.DccTaskCreateOpt):
    RESOURCE_TYPE = 'shot'

    STEP = 'gnl'
    TASK = 'general'

    def __init__(self, *args, **kwargs):
        super(DccShotTaskCreateOpt, self).__init__(*args, **kwargs)
