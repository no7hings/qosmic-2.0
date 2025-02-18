# coding:utf-8
import lnx_wotrix.core as lnx_wtx_core


class DccShotTaskCreateOpt(lnx_wtx_core.DccTaskCreateOpt):
    RESOURCE_TYPE = 'shot'

    STEP = 'gnl'
    TASK = 'general'

    def __init__(self, *args, **kwargs):
        super(DccShotTaskCreateOpt, self).__init__(*args, **kwargs)
