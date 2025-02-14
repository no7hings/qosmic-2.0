# coding:utf-8
import lxgeneral.dcc.core as gnl_dcc_core

import lxgeneral.dcc.objects as gnl_dcc_objects
# maya
from ... import abstracts as mya_abstracts

from . import utility as _utility


class AndMaterialx(mya_abstracts.AbsMyaNodeForFileReference):
    DCC_PORT_CLS = _utility.Port
    STG_FILE_CLS = gnl_dcc_objects.StgFile

    def __init__(self, path):
        super(AndMaterialx, self).__init__(path)

    def get_stg_files(self):
        lis = []
        for port_dcc_path, file_path in self._reference_raw.items():
            lis.append(
                self._create_stg_file_fnc(file_path, port_dcc_path)
            )
            mtx_reader = gnl_dcc_core.DotMtlxOpt(file_path)
            for i in mtx_reader.texture_paths:
                lis.append(
                    self._create_stg_file_fnc(i)
                )
        return lis


class AndStringReplace(mya_abstracts.AbsMyaNode):
    DCC_PORT_CLS = _utility.Port

    def __init__(self, path):
        super(AndStringReplace, self).__init__(path)
