# coding:utf-8
from .. import _abc


class Main(_abc.AbsAdvValidationPrc):
    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)

    def execute(self):
        for i_name, (i_main_key, i_data) in self._task._joint_data.items():
            self._task.rotate_order_prc(self.BRANCH, self.LEAF, i_main_key, i_name, i_data)
