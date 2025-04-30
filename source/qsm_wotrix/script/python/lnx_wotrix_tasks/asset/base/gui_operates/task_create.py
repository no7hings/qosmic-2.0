# coding:utf-8
import lnx_wotrix.core as lnx_wtx_core


class GuiTaskCreateOpt(lnx_wtx_core.DccTaskCreateOpt):
    RESOURCE_TYPE = 'asset'

    STEP = 'gnl'
    TASK = 'general'

    def __init__(self, *args, **kwargs):
        super(GuiTaskCreateOpt, self).__init__(*args, **kwargs)
