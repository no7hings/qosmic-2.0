# coding:utf-8
import lxbasic.resource as bsc_resource

import qsm_maya.core as qsm_mya_core

from .. import core as _core


class AdvMotionExportOpt(object):
    """
import qsm_maya_adv
reload(qsm_maya_adv)
qsm_maya_adv.do_reload()
# coding:utf-8
import qsm_maya_adv.scripts as s

s.AdvMotionExportOpt('lily_Skin').test()
    """
    def __init__(self, namespace):
        self._namespace = namespace

        self._adv_resource = _core.AdvResource(self._namespace)

    def test(self):
        self._adv_resource.export_to(
            'E:/myworkspace/qosmic-2.0/source/qsm_dcc_extra/resources/motion/sam_run_offset.json'
        )

    def export(self, name):
        self._adv_resource.export_to(
            'Z:/temporaries/adv_motion_test/motions/{}.json'.format(name)
        )
