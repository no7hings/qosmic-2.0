# coding:utf-8
import qsm_lazy_wsp.core as lzy_wsp_core


class MayaSequenceTaskCreateOpt(lzy_wsp_core.DccTaskCreateOpt):
    RESOURCE_TYPE = 'sequence'

    STEP = 'gnl'
    TASK = 'general'

    def __init__(self, *args, **kwargs):
        super(MayaSequenceTaskCreateOpt, self).__init__(*args, **kwargs)

    def build_scene_src_fnc(self, *args, **kwargs):
        pass

    def create_groups_for(self, task):
        pass
