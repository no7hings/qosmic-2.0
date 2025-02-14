# coding:utf-8
from ..core.adv import resource as _adv_resource


class AdvChrMotionExportOpt(object):
    """
    """
    def __init__(self, namespace):
        self._namespace = namespace

        self._adv_resource = _adv_resource.AdvResource(self._namespace)

    def test(self):
        self._adv_resource.export_to(
            'E:/myworkspace/qosmic-2.0/source/qsm_dcc_extra/resources/motion/sam_run_offset_a.json'
        )

    def export(self, file_path):
        self._adv_resource.export_to(
            file_path
        )
