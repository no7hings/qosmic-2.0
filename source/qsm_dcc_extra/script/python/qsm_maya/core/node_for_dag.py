# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.api.OpenMaya as om2

import lxbasic.core as bsc_core

from . import node as _node


class DagNode(_node.Node):
    PATHSEP = '|'
    NAMESPACESEP = ':'

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
    def create_locator(cls, path):
        parent_path = '|'.join(path.split('|')[:-1])
        name = path.split('|')[-1]
        _ = cmds.spaceLocator(name=name, position=(0, 0, 0))
        return cls.parent_to(_[0], parent_path)

    @classmethod
    def create_transform(cls, path):
        return cls.create(path, 'transform')

    @classmethod
    def create_joint(cls, path):
        return cls.create(path, 'joint')

    @classmethod
    def to_name(cls, path_or_name):
        return path_or_name.split(cls.PATHSEP)[-1]

    @classmethod
    def to_name_without_namespace(cls, path_or_name):
        return cls.to_name(path_or_name).split(cls.NAMESPACESEP)[-1]

    @classmethod
    def to_path_without_namespace(cls, path_or_name):
        return cls.PATHSEP.join([x.split(cls.NAMESPACESEP)[-1] for x in cls.to_path(path_or_name).split(cls.PATHSEP)])

    @classmethod
    def to_namespace(cls, path_or_name):
        return cls.NAMESPACESEP.join(cls.to_name(path_or_name).split(cls.NAMESPACESEP)[:-1])

    @classmethod
    def to_path(cls, path_or_name):
        _ = cmds.ls(path_or_name, long=1)
        if _:
            return _[0]

    @classmethod
    def check_is_dag(cls, path_or_name):
        _ = cls.to_path(path_or_name)
        if _:
            return _.startswith('|')
        return False

    @classmethod
    def get_parent(cls, path):
        return '|'.join(cls.to_path(path).split('|')[:-1])

    @classmethod
    def to_parent_path(cls, path):
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
    def parent_to(cls, path, parent_path, relative=False):
        if not parent_path:
            return path

        results = cmds.parent(path, parent_path, relative=relative)
        if results:
            return cls.to_path(results[0])

    @classmethod
    def find_roots(cls, paths):
        return bsc_core.BscPath.find_dag_child_paths(
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
        self._name = DagNode.to_name(self._path)
        self._uuid = _node.Node.get_uuid(self._path)
        super(DagNodeOpt, self).__init__(self._name)

    @property
    def type(self):
        return _node.Node.get_type(self._path)

    @property
    def path(self):
        return self._path

    @property
    def name_or_path(self):
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

    @classmethod
    def is_visible(cls, path):
        return bool(
            cmds.getAttr(
                path+'.visibility'
            )
        )

    @classmethod
    def set_visible(cls, path, boolean):
        cmds.setAttr(
            path+'.visibility', boolean
        )

    @classmethod
    def set_outliner_visible(cls, path, boolean):
        cmds.setAttr(
            path+'.hiddenInOutliner', not boolean
        )


class NodeDrawOverride(object):
    @classmethod
    def set_enable(cls, path, boolean):
        cmds.setAttr(path+'.overrideEnabled', boolean)

    @classmethod
    def set_visible(cls, path, boolean):
        cmds.setAttr(path+'.overrideVisibility', boolean)

    @classmethod
    def set_color(cls, path, rgb, enable=True):
        cls.set_enable(path, enable)
        cmds.setAttr(path+'.overrideRGBColors', 1)
        cmds.setAttr(path+'.overrideColorRGB', *rgb)
