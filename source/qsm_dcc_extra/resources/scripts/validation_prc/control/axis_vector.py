# coding:utf-8

class Main(object):
    def __init__(self, task_prc):
        self._task_prc = task_prc

    def execute(self):
        for i_name, (i_main_key, i_data) in self._task_prc._task._control_data.items():
            self._task_prc._task.axis_vector_prc(
                self._task_prc.BRANCH, self._task_prc.LEAF, i_main_key, i_name, i_data
            )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(task_prc).execute()
