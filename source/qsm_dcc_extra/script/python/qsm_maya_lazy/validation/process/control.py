# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core

from . import base as _base

_BRANCH = 'control'


class ControlResetTransformations(_base.AdvValidationBase):
    BRANCH = _BRANCH
    LEAF = 'reset_transformations'

    def __init__(self, *args, **kwargs):
        super(ControlResetTransformations, self).__init__(*args, **kwargs)

    def execute(self):
        paths = self.find_all_controls()
        if not paths:
            return

        for i_path in paths:
            i_name = self.to_key(i_path)
            for j_atr in [
                'translateX',
                'translateY',
                'translateZ',
                'rotateX',
                'rotateY',
                'rotateZ',
            ]:
                if qsm_mya_core.NodeAttribute.get_channel_box_enable(i_path, j_atr) is True:
                    j_value = qsm_mya_core.NodeAttribute.get_value(i_path, j_atr)
                    j_value = round(j_value, 3)
                    if j_value != 0:
                        self._result_content.add_element(
                            self._key, (i_name, [dict(attribute=j_atr, value=j_value)])
                        )
            for j_atr in [
                'scaleX',
                'scaleY',
                'scaleZ',
            ]:
                if qsm_mya_core.NodeAttribute.get_channel_box_enable(i_path, j_atr) is True:
                    j_value = qsm_mya_core.NodeAttribute.get_value(i_path, j_atr)
                    j_value = round(j_value, 3)
                    if j_value != 1.0:
                        self._result_content.add_element(
                            self._key, (i_name, [dict(attribute=j_atr, value=j_value)])
                        )


class ControlNameOverlapping(_base.AdvValidationBase):
    BRANCH = _BRANCH
    LEAF = 'name_overlapping'

    def __init__(self, *args, **kwargs):
        super(ControlNameOverlapping, self).__init__(*args, **kwargs)

    def execute(self):
        paths = self.find_all_controls()
        for i_path in paths:
            i_key = self.to_key(i_path)
            i_name = qsm_mya_core.DagNode.to_name(i_path)
            _ = cmds.ls(i_name, long=1)
            if len(_) > 1:
                self._result_content.add_element(
                    self._key, (i_key, [dict()])
                )
