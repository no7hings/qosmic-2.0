# coding:utf-8
# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core

from . import base as _base


class MeshFaceCount(_base.AdvValidationBase):
    BRANCH = 'mesh'
    LEAF = 'face_count'

    def __init__(self, *args, **kwargs):
        super(MeshFaceCount, self).__init__(*args, **kwargs)

    def execute(self):
        paths = self.find_all_meshes()
        if not paths:
            return

        counts = []
        for i in paths:
            counts.append(qsm_mya_core.Mesh.get_face_number(i))

        if counts:
            options = self._validation_options.get_leaf_options_at(self.BRANCH, self.LEAF)
            limit_value = options['limit_value']
            value = sum(counts)
            if value > limit_value:
                self._result_content.add_element(
                    self._key, ('all', [dict(value=value)])
                )
