# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core

from . import base as _base


class JointCompleteness(_base.AdvValidationBase):
    BRANCH = 'joint'
    LEAF = 'completeness'

    def __init__(self, *args, **kwargs):
        super(JointCompleteness, self).__init__(*args, **kwargs)

    def execute(self):
        joint_keys = self._adv_cfg.get('main_joints')
        for i_main_key in joint_keys:
            i_joint = self.find_one(self._namespace, i_main_key, 'joint')
            if i_joint is None:
                self._result_content.add_element(
                    self._key, (i_main_key, [dict()])
                )


class JointNameOverlapping(_base.AdvValidationBase):
    BRANCH = 'joint'
    LEAF = 'name_overlapping'

    def __init__(self, *args, **kwargs):
        super(JointNameOverlapping, self).__init__(*args, **kwargs)

    def execute(self):
        paths = self.find_all_joints()
        if not paths:
            return

        for i_path in paths:
            i_key = self.to_key(i_path)
            i_name = qsm_mya_core.DagNode.to_name(i_path)
            _ = cmds.ls(i_name, long=1)
            c = len(_)
            if c > 1:
                self._result_content.add_element(
                    self._key, (i_key, [dict(count=c)])
                )
