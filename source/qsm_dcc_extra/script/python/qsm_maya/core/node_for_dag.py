# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.api.OpenMaya as om2

import lxbasic.core as bsc_core

from . import node as _node


class DagNode(_node.Node):
    PATHSEP = '|'

    @classmethod
    def create(cls, path, type_name):
        parent_path = '|'.join(path.split('|')[:-1])
        name = path.split('|')[-1]
        if parent_path:
            _ = cmds.createNode(type_name, name=name, parent=parent_path, skipSelect=1)
        else:
            _ = cmds.createNode(type_name, name=name, skipSelect=1)
        return cls.to_path(_)

    @classmethod
    def path_to_name(cls, path):
        return path.split(cls.PATHSEP)[-1]

    @classmethod
    def to_path(cls, name):
        _ = cmds.ls(name, long=1)
        if not _:
            raise RuntimeError()
        return _[0]

    @classmethod
    def get_parent(cls, path):
        return '|'.join(path.split('|')[:-1])

    @classmethod
    def is_instanced(cls, path):
        dag_node = om2.MFnDagNode(om2.MGlobal.getSelectionListByName(path).getDagPath(0))
        return dag_node.isInstanced()

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

    @classmethod
    def rename(cls, path, new_name):
        _ = cmds.rename(path, new_name)
        if _:
            return cls.to_path(_)


class DagNodeOpt(_node.NodeOpt):
    def __init__(self, path):
        self._path = DagNode.to_path(path)
        print self._path
        self._name = DagNode.path_to_name(self._path)
        self._uuid = _node.Node.get_uuid(self._path)
        super(DagNodeOpt, self).__init__(self._name)

    @property
    def type(self):
        return _node.Node.get_type(self._path)

    @property
    def path(self):
        return self._path

    def update_path(self):
        if self._uuid:
            _ = cmds.ls(self._uuid, long=1)
            if _:
                self._path = _[0]
            else:
                raise RuntimeError()


class NodeDisplay(object):
    @classmethod
    def set_outliner_color(cls, path, r, g, b):
        cmds.setAttr(path+'.useOutlinerColor', 1)
        cmds.setAttr(path+'.outlinerColor', r, g, b)


class NodeDrawOverride(object):
    @classmethod
    def set_enable(cls, path, boolean):
        cmds.setAttr(path+'.overrideEnabled', boolean)

    @classmethod
    def set_visible(cls, path, boolean):
        cmds.setAttr(path+'.overrideVisibility', boolean)
