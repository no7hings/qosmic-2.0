# coding:utf-8
import lnx_wotrix.core as lnx_wtx_core


class MayaProjectTaskCreateOpt(lnx_wtx_core.DccTaskCreateOpt):
    RESOURCE_TYPE = 'project'

    STEP = 'gnl'
    TASK = 'general'

    def __init__(self, *args, **kwargs):
        super(MayaProjectTaskCreateOpt, self).__init__(*args, **kwargs)

    def build_scene_src_fnc(self, *args, **kwargs):
        pass

    def create_groups_for(self, task):
        pass
