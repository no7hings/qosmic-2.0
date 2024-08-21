# coding:utf-8
import lxbasic.resource as bsc_resource

import qsm_maya.core as qsm_mya_core

from .. import core as _core


class AdvChrMotionExportOpt(object):
    """
import qsm_maya_lazy
reload(qsm_maya_lazy)
qsm_maya_lazy.do_reload()
import qsm_maya_lazy.montage.scripts as s

s.AdvChrMotionExportOpt('lily_Skin').test()
    """
    def __init__(self, namespace):
        self._namespace = namespace

        self._adv_resource = _core.AdvResource(self._namespace)

    def test(self):
        self._adv_resource.export_to(
            'E:/myworkspace/qosmic-2.0/source/qsm_dcc_extra/resources/motion/sam_run_offset_a.json'
        )

    def export(self, file_path):
        self._adv_resource.export_to(
            file_path
        )
