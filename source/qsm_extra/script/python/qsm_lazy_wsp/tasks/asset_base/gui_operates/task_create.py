# coding:utf-8
import qsm_lazy_wsp.core as lzy_wsp_core


class DccAssetTaskCreateOpt(lzy_wsp_core.DccTaskCreateOpt):
    RESOURCE_BRANCH = 'asset'

    STEP = 'gnl'
    TASK = 'general'

    def __init__(self, *args, **kwargs):
        super(DccAssetTaskCreateOpt, self).__init__(*args, **kwargs)
