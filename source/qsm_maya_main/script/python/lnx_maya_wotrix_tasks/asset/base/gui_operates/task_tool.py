# coding:utf-8
import lnx_wotrix.core as lnx_wtx_core

import qsm_maya.core as qsm_mya_core


class GuiTaskToolOpt(lnx_wtx_core.DccTaskToolOpt):
    @classmethod
    def test(cls):
        pass

    def __init__(self, *args, **kwargs):
        super(GuiTaskToolOpt, self).__init__(*args, **kwargs)

    def create_groups_for(self, task):
        content = self._task_session._task_parse.dcc_configure.get_as_content(
            'dcc-asset-group.{}'.format(task), relative=True
        )
        if content:
            for i_key in content.get_all_keys():
                i_path = '|{}'.format(i_key.replace('.', '|'))
                qsm_mya_core.Group.create(i_path)
