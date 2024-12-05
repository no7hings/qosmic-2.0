# coding:utf-8
import qsm_maya.core as qsm_mya_core

from qsm_maya.handles import _abc


class ShotAssetsAnimationGroupOrg(_abc.AbsGroupOpt):
    LOCATION = '|assets|animation'

    def __init__(self, *args, **kwargs):
        # create force
        if qsm_mya_core.Node.is_exists(self.LOCATION) is False:
            qsm_mya_core.Group.create_dag(self.LOCATION)

        super(ShotAssetsAnimationGroupOrg, self).__init__(
            self.LOCATION, *args, **kwargs
        )

    def set_frame_range(self, start_frame, end_frame):
        qsm_mya_core.NodeAttribute.create_as_time(
            self.LOCATION, 'start_frame', start_frame
        )
        qsm_mya_core.NodeAttribute.create_as_time(
            self.LOCATION, 'end_frame', end_frame
        )
    
    def set_start_frame(self, frame):
        qsm_mya_core.NodeAttribute.create_as_time(
            self.LOCATION, 'start_frame', frame
        )
    
    def get_start_frame(self):
        if qsm_mya_core.NodeAttribute.is_exists(self.LOCATION, 'start_frame') is False:
            qsm_mya_core.NodeAttribute.create_as_time(
                self.LOCATION, 'start_frame', qsm_mya_core.Frame.get_current()
            )
        return qsm_mya_core.NodeAttribute.get_value(self.LOCATION, 'start_frame')


class ShotAssetsCfxGroupOrg(_abc.AbsGroupOpt):
    LOCATION = '|assets|cfx'

    def __init__(self, *args, **kwargs):
        # create force
        if qsm_mya_core.Node.is_exists(self.LOCATION) is False:
            qsm_mya_core.Group.create_dag(self.LOCATION)

        super(ShotAssetsCfxGroupOrg, self).__init__(
            self.LOCATION, *args, **kwargs
        )

    def set_start_frame(self, frame):
        qsm_mya_core.NodeAttribute.create_as_time(
            self.LOCATION, 'start_frame', frame
        )

    def get_start_frame(self):
        if qsm_mya_core.NodeAttribute.is_exists(self.LOCATION, 'start_frame') is False:
            qsm_mya_core.NodeAttribute.create_as_time(
                self.LOCATION, 'start_frame', qsm_mya_core.Frame.get_current()
            )
        return qsm_mya_core.NodeAttribute.get_value(self.LOCATION, 'start_frame')

    def create_properties(self):
        qsm_mya_core.NodeAttribute.create_as_time(
            self.LOCATION, 'start_frame', 0
        )
