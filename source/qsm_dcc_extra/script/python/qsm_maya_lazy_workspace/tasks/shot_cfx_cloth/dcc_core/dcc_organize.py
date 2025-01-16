# coding:utf-8
import qsm_maya.core as qsm_mya_core

from qsm_maya.handles import _abc


class ShotCfxRigGroupOrg(_abc.AbsGroupOpt):
    LOCATION = '|assets|cfx|cfx_rig_grp'

    def __init__(self, *args, **kwargs):
        # create force
        if qsm_mya_core.Node.is_exists(self.LOCATION) is False:
            qsm_mya_core.Group.create_dag(self.LOCATION)

        super(ShotCfxRigGroupOrg, self).__init__(
            self.LOCATION, *args, **kwargs
        )

    def add_one(self, location):
        qsm_mya_core.Group.add_one(
            self.LOCATION, location
        )
