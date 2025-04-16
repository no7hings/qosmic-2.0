# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.handles.animation.core as qsm_mya_hdl_anm_core


class RigAsset(qsm_mya_hdl_anm_core.AdvRigAsset):

    def __init__(self, *args, **kwargs):
        super(RigAsset, self).__init__(*args, **kwargs)
