# coding:utf-8
# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core

from . import base as _base


class MeshTriangle(_base.AdvValidationBase):
    BRANCH = 'mesh'
    LEAF = 'triangle'

    def __init__(self, *args, **kwargs):
        super(MeshTriangle, self).__init__(*args, **kwargs)

    def execute(self):
        paths = qsm_mya_core.Scene.find_all_dag_nodes(type_includes=['mesh'])
        if not paths:
            return

        options = self._validation_options.get_leaf_options_at(self.BRANCH, self.LEAF)
        limit_value = options['limit_value']

        for i_path in paths:
            i_value = qsm_mya_core.Mesh.get_face_number(i_path)
            if i_value > limit_value:
                i_key = qsm_mya_core.DagNode.to_path_without_namespace(i_path)
                self._result_content.add_element(
                    self._key, (i_key, [dict(value=i_value)])
                )
