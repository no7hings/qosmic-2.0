# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

from . import node as _node


class NodeDag(object):
    PATHSEP = '|'

    @classmethod
    def to_path(cls, name):
        return cmds.ls(name, long=1)[0]

    @classmethod
    def to_world(cls, path):
        parent_path = '|'.join(path.split('|')[:-1])
        if not parent_path:
            return path
        results = cmds.parent(path, world=True)
        if results:
            return cls.to_path(results[0])

    @classmethod
    def copy_to_world(cls, path):
        name = path.split('|')[-1]
        results = cmds.duplicate(
            path, name='{}_copy'.format(name),
        )
        if results:
            return cls.to_world(cls.to_path(results[0]))

    @classmethod
    def parent_to(cls, path, parent_path):
        if not parent_path:
            return path
        results = cmds.parent(path, parent_path, relative=1)
        if results:
            return cls.to_path(results[0])

    @classmethod
    def find_roots(cls, paths):
        return bsc_core.PthNodeMtd.find_dag_child_paths(
            '|', paths, '|'
        )

    @classmethod
    def find_mesh_roots(cls, paths):
        return list(set([cls.PATHSEP.join(i.split(cls.PATHSEP)[:2]) for i in paths if _node.Node.is_mesh(i)]))

    @classmethod
    def find_siblings(cls, path, type_includes):
        return cmds.ls(path, type=type_includes, dag=1, long=1) or []
