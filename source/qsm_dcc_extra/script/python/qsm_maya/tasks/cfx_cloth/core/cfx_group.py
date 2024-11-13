# coding:utf-8
import collections

import lxbasic.core as bsc_core

import lxbasic.log as bsc_log

from .... import core as _mya_core

from ... import _abc

from . import cfx_cloth_asset_operate as _cfx_rig_operate


class ShotCfxRigGroupOpt(_abc.AbsGroupOpt):
    LOCATION = '|assets|cfx|cfx_rig_grp'

    def __init__(self, *args, **kwargs):
        # create force
        if _mya_core.Node.is_exists(self.LOCATION) is False:
            _mya_core.Group.create_dag(self.LOCATION)

        super(ShotCfxRigGroupOpt, self).__init__(
            self.LOCATION, *args, **kwargs
        )

    def generate_cfx_rig_opt(self, rig_namespace):
        return _cfx_rig_operate.CfxClothAssetOpt(rig_namespace)

    def add_one(self, location):
        _mya_core.Group.add_one(
            self.LOCATION, location
        )
