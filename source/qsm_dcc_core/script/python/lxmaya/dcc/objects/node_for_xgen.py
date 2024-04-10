# coding:utf-8
import lxbasic.dcc.objects as bsc_dcc_objects
# maya
from ... import abstracts as mya_abstracts
# maya dcc objects
from . import utility as mya_dcc_obj_utility

from . import node_for_dag as mya_dcc_obj_node_for_dag


class XgnPalette(mya_abstracts.AbsMyaNodeForFileReference):
    DCC_PORT_CLS = mya_dcc_obj_utility.Port
    STG_FILE_CLS = bsc_dcc_objects.StgFile

    def __init__(self, path, file_path=None):
        super(XgnPalette, self).__init__(
            self._to_full_path(path),
            file_path
        )


class XgnDescription(
    mya_abstracts.AbsMyaNodeForFileReference,
    mya_abstracts.AbsMyaShapeDef,
):
    DCC_PORT_CLS = mya_dcc_obj_utility.Port
    STG_FILE_CLS = bsc_dcc_objects.StgFile
    TRANSFORM_CLS = mya_dcc_obj_node_for_dag.Transform

    def __init__(self, path, file_path=None):
        super(XgnDescription, self).__init__(
            self._to_full_path(path),
            file_path
        )
        self._set_ma_shape_def_init_(self.path)
