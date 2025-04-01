# coding:utf-8


class Main(object):
    def __init__(self, task_prc):
        self._task_prc = task_prc

    def execute(self):
        joint_keys = self._task_prc._adv_cfg.get('main_joints')
        for i_main_key in joint_keys:
            i_joint = self._task_prc.find_one(self._task_prc._namespace, i_main_key, 'joint')
            if i_joint is None:
                self._task_prc._result_content.append_element(
                    self._task_prc._key, (i_main_key, [dict()])
                )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(task_prc).execute()
