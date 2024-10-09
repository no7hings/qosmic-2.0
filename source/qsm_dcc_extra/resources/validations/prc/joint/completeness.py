# coding:utf-8
from .. import _abc


class Main(_abc.AbsAdvValidationPrc):
    BRANCH = 'joint'
    LEAF = 'completeness'

    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)

    def execute(self):
        joint_keys = self._adv_cfg.get('main_joints')
        for i_main_key in joint_keys:
            i_joint = self.find_one(self._namespace, i_main_key, 'joint')
            if i_joint is None:
                self._result_content.append_element(
                    self._key, (i_main_key, [dict()])
                )
