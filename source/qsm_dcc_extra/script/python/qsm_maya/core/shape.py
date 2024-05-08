# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.api.OpenMaya as om2

import lxbasic.core as bsc_core

from . import node as _node

from . import node_dag as _node_dag


class Shape(object):
    @classmethod
    def get_transform(cls, path):
        return cmds.listRelatives(path, parent=1, fullPath=1)


class ShapeOpt(object):
    def __init__(self, shape_path):
        self._shape_path = shape_path
        self._uuid = _node.Node.get_uuid(self._shape_path)

    def update_path(self):
        if self._uuid:
            _ = cmds.ls(self._uuid, long=1)
            if _:
                self._path = _[0]
            else:
                raise RuntimeError()

    @property
    def shape_path(self):
        return self._shape_path

    @property
    def shape_name(self):
        return self.shape_path.split('|')[-1]

    @property
    def transform_path(self):
        return bsc_core.PthNodeMtd.get_dag_parent_path(
            self._shape_path, _node_dag.NodeDag.PATHSEP
        )

    @property
    def transform_name(self):
        return self.transform_path.split('|')[-1]
