# coding:utf-8
import qsm_wsp_task as qsm_dcc_wsp_task

import qsm_maya.core as qsm_mya_core


class MayaAssetGnlToolOpt(qsm_dcc_wsp_task.DccTaskToolOpt):
    @classmethod
    def test(cls):
        pass

    def __init__(self, *args, **kwargs):
        super(MayaAssetGnlToolOpt, self).__init__(*args, **kwargs)

    def create_groups_for(self, task):
        content = self._task_session._task_parse.dcc_configure.get_as_content(
            'dcc-asset-group.{}'.format(task), relative=True
        )
        if content:
            for i_key in content.get_all_keys():
                i_path = '|{}'.format(i_key.replace('.', '|'))
                qsm_mya_core.Group.create(i_path)
