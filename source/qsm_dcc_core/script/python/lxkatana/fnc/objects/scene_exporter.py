# coding:utf-8
import lxbasic.fnc.abstracts as bsc_fnc_abstracts
# katana
# katana dcc
from ...dcc import objects as ktn_dcc_objects


class FncExporterForScene(bsc_fnc_abstracts.AbsFncOptionBase):
    OPTION = dict(
        file=''
    )

    def __init__(self, option=None):
        super(FncExporterForScene, self).__init__(option)

    def execute(self):
        ktn_dcc_objects.Scene.set_file_export_to(
            self.get('file')
        )
