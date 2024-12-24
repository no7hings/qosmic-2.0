# coding:utf-8
import qsm_lazy_wsp.core as lzy_wsp_core


class MayaProjectTaskCreateOpt(lzy_wsp_core.DccTaskCreateOpt):
    RESOURCE_TYPE = 'project'

    STEP = 'gnl'
    TASK = 'general'

    def __init__(self, *args, **kwargs):
        super(MayaProjectTaskCreateOpt, self).__init__(*args, **kwargs)

    def build_scene_src_fnc(self, *args, **kwargs):
        pass

    def create_groups_for(self, task):
        pass
