# coding:utf-8
import qsm_lazy_wsp.core as lzy_wsp_core

import qsm_maya.core as qsm_mya_core


class MayaShotTaskToolOpt(lzy_wsp_core.DccTaskToolOpt):
    @classmethod
    def test(cls):
        pass

    def __init__(self, *args, **kwargs):
        super(MayaShotTaskToolOpt, self).__init__(*args, **kwargs)

    def create_groups_for(self, task):
        content = self._task_session._task_parse.dcc_configure.get_as_content(
            'dcc-shot-group.{}'.format(task), relative=True
        )
        if content:
            for i_key in content.get_all_keys():
                i_path = '|{}'.format(i_key.replace('.', '|'))
                qsm_mya_core.Group.create(i_path)
