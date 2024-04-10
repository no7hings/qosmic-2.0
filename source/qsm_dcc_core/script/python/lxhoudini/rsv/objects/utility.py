# coding:utf-8
from lxutil.rsv import utl_rsv_obj_abstract


class RsvDccUtilityHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccUtilityHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)
