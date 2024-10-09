# coding:utf-8
from .. import _abc


class Main(_abc.AbsAdvValidationPrc):
    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)

    def execute(self):
        import qsm_maya.core as qsm_mya_core

        paths = self.find_all_controls()
        if not paths:
            return

        for i_path in paths:
            i_key_name = self.to_key(i_path)
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
                        # self._result_content.append_element(
                        #     self._key, (i_name, [dict(attribute=j_atr, value=j_value)])
                        # )
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
                        # self._result_content.append_element(
                        #     self._key, (i_name, [dict(attribute=j_atr, value=j_value)])
                        # )

            if i_results:
                self._result_content.append_element(
                    self._key, (i_key_name, i_results)
                )

