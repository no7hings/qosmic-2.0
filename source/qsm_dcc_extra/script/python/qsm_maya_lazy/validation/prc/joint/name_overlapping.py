# coding:utf-8
from .. import _abc


class Main(_abc.AbsAdvValidationPrc):
    BRANCH = 'joint'
    LEAF = 'name_overlapping'

    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)

    def execute(self):
        # noinspection PyUnresolvedReferences
        import maya.cmds as cmds

        import qsm_maya.core as qsm_mya_core

        paths = self.find_all_joints()
        if not paths:
            return

        for i_path in paths:
            i_key = self.to_key(i_path)
            i_name = qsm_mya_core.DagNode.to_name(i_path)
            _ = cmds.ls(i_name, long=1)
            c = len(_)
            if c > 1:
                self._result_content.append_element(
                    self._key, (i_key, [dict(count=c)])
                )
