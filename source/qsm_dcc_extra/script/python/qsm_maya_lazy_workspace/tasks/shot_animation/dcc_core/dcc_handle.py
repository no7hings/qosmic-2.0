# coding:utf-8
import json
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core

import qsm_maya.adv as qsm_mya_adv

import qsm_maya.handles.animation.core as qsm_mya_hdl_anm_core

from ...asset_cfx_rig import dcc_core as _asset_cfx_rig_core


class ShotAnimationAssetHandle(object):
    def __init__(self, rig_namespace):
        self._rig_namespace = rig_namespace

    @property
    def rig_namespace(self):
        return self._rig_namespace
