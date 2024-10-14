# coding:utf-8


class Main(object):
    def __init__(self, task_prc):
        self._task_prc = task_prc

    def execute(self):
        import qsm_maya.core as qsm_mya_core

        paths = self._task_prc.find_all_transform_controls()
        if not paths:
            return

        for i_path in paths:
            i_key_name = self._task_prc.to_node_key_name(i_path)
            i_results = []
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
                        i_results.append(dict(attribute=j_atr, value=j_value))
            for j_atr in [
                'scaleX',
                'scaleY',
                'scaleZ',
            ]:
                if qsm_mya_core.NodeAttribute.get_channel_box_enable(i_path, j_atr) is True:
                    j_value = qsm_mya_core.NodeAttribute.get_value(i_path, j_atr)
                    j_value = round(j_value, 3)
                    if j_value != 1.0:
                        i_results.append(dict(attribute=j_atr, value=j_value))

            if i_results:
                self._task_prc._result_content.append_element(
                    self._task_prc._key, (i_key_name, i_results)
                )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(task_prc).execute()
