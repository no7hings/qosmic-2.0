# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.resource.core as qsm_mya_rsc_core

from . import dcc_handle as _dcc_handle


class RigAsset(qsm_mya_rsc_core.Asset):

    def __init__(self, *args, **kwargs):
        super(RigAsset, self).__init__(*args, **kwargs)
