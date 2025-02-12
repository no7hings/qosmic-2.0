# coding:utf-8
from __future__ import print_function
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ... import abc_


class MeshValidationOpt(abc_.AbsMeshOpt):
    @classmethod
    def test(cls):
        print(cls('pCube1').get_lamina_face_names())

    def __init__(self, path_or_name):
        super(MeshValidationOpt, self).__init__(path_or_name)

    def get_non_manifold_vertex_names(self):
        return [x.split('.')[-1] for x in cmds.polyInfo(self._shape_path, nonManifoldVertices=1) or []]

    def get_non_manifold_vertices(self):
        return [
            '{}.{}'.format(self._transform_path, x.split('.')[-1]) for x in
            cmds.polyInfo(self._shape_path, nonManifoldVertices=1) or []
        ]

    def get_lamina_face_names(self):
        pre_selection_paths = cmds.ls(selection=1, long=1) or []

        cmds.select(self._shape_path)
        cmds.polySelectConstraint(mode=3, type=8, topology=2)
        cmds.polySelectConstraint(mode=0, type=8, topology=0)
        _ = cmds.ls(selection=1, long=1) or []
        if pre_selection_paths:
            cmds.select(pre_selection_paths)
        else:
            cmds.select(clear=1)
        return [x.split('.')[-1] for x in _]

