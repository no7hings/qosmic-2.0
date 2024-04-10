# coding:utf-8
import lxbasic.log as bsc_log

import lxuniverse.objects as unr_objects
# maya
from ..core.wrap import *

from .. import core as mya_core
# maya dcc
from ..dcc import objects as mya_dcc_objects


class AttributeTranslator(object):
    def __init__(self, root_src, root_tgt):
        root_src_dag_path = unr_objects.ObjDagPath(root_src)
        self._mya_root_src_dag_path = root_src_dag_path.translate_to(mya_core.MyaUtil.OBJ_PATHSEP)
        self._mya_root_src_path = self._mya_root_src_dag_path.path

        root_tgt_dag_path = unr_objects.ObjDagPath(root_tgt)
        self._mya_root_tgt_dag_path = root_tgt_dag_path.translate_to(mya_core.MyaUtil.OBJ_PATHSEP)
        self._mya_root_tgt_path = self._mya_root_tgt_dag_path.path

    def set_uv_translate(self, clear_history=False):
        lis = []
        src_root = mya_dcc_objects.Group(self._mya_root_src_dag_path.path)
        src_mesh_obj_paths = src_root.get_all_shape_paths(include_obj_type=['mesh'])
        for src_mesh_obj_path in src_mesh_obj_paths:
            rlt_path = src_mesh_obj_path[len(self._mya_root_src_path):]
            tgt_mesh_obj_path = self._mya_root_tgt_path + rlt_path
            if mya_dcc_objects.Node(tgt_mesh_obj_path).get_is_exists() is True:
                lis.append((src_mesh_obj_path, tgt_mesh_obj_path))
        #
        for src_obj_path, tgt_obj_path in lis:
            _ = cmds.transferAttributes(
                src_obj_path, tgt_obj_path, transferUVs=2
            )
            if clear_history is True:
                cmds.delete(tgt_obj_path, constructionHistory=1)
            #
            bsc_log.Log.trace_method_result(
                'mesh-uv-translate',
                u'obj="{}"'.format(tgt_obj_path)
            )

    def set_look_translate(self):
        pass
