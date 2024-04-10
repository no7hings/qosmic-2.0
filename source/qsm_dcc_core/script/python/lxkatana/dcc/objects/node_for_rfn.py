# coding:utf-8
import lxbasic.dcc.objects as bsc_dcc_objects
# katana
from ... import abstracts as ktn_abstracts
# katana dcc
from . import node as ktn_dcc_obj_node


class FileReference(ktn_abstracts.AbsKtnFileReferenceObj):
    DCC_PORT_CLS = ktn_dcc_obj_node.Port
    DCC_CONNECTION_CLS = ktn_dcc_obj_node.Connection
    STG_FILE_CLS = bsc_dcc_objects.StgFile

    def __init__(self, path):
        super(FileReference, self).__init__(path)


class TextureReference(ktn_abstracts.AbsKtnFileReferenceObj):
    DCC_PORT_CLS = ktn_dcc_obj_node.Port
    DCC_CONNECTION_CLS = ktn_dcc_obj_node.Connection
    STG_FILE_CLS = bsc_dcc_objects.StgTexture

    def __init__(self, path):
        super(TextureReference, self).__init__(path)

    # noinspection PyMethodMayBeStatic
    def get_color_space(self):
        return 'auto'

    def set_color_space(self, color_space):
        pass
