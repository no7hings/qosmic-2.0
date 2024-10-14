# coding:utf-8


class Main(object):
    def __init__(self, task_prc):
        self._task_prc = task_prc

    def execute(self):
        # noinspection PyUnresolvedReferences
        import maya.cmds as cmds

        import qsm_maya.core as qsm_mya_core

        paths = self._task_prc.find_all_controls()
        for i_path in paths:
            i_key = self._task_prc.to_node_key_name(i_path)
            i_name = qsm_mya_core.DagNode.to_name(i_path)
            _ = cmds.ls(i_name, long=1)
            if len(_) > 1:
                self._task_prc._result_content.append_element(
                    self._task_prc._key, (i_key, [dict()])
                )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(task_prc).execute()
