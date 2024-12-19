# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class Node(object):
    class Types(object):
        Transform = 'transform'
        Mesh = 'mesh'
        Curve = 'nurbsCurve'
        GPU = 'gpuCache'
        AssemblyReference = 'assemblyReference'
        Material = 'shadingEngine'

    @classmethod
    def create(cls, name, type_name):
        if cmds.objExists(name) is True:
            return name
        return cmds.createNode(
            type_name, name=name, skipSelect=1
        )

    @classmethod
    def create_condition(cls, name):
        return cls.create(
            name, 'condition'
        )

    @classmethod
    def get_type(cls, name):
        return cmds.nodeType(name)

    @classmethod
    def type_is(cls, name, type_name):
        return cls.get_type(name) == type_name

    @classmethod
    def is_transform_type(cls, name):
        return cls.get_type(name) == cls.Types.Transform

    @classmethod
    def is_mesh_type(cls, name):
        return cls.get_type(name) == cls.Types.Mesh

    @classmethod
    def is_curve(cls, name):
        return cls.get_type(name) == cls.Types.Curve

    @classmethod
    def is_gpu(cls, name):
        return cls.get_type(name) == cls.Types.GPU

    @classmethod
    def is_assembly_reference(cls, name):
        return cls.get_type(name) == cls.Types.AssemblyReference

    @classmethod
    def is_exists(cls, name):
        if name:
            return cmds.objExists(name)
        raise False

    @classmethod
    def get_uuid(cls, name):
        return cmds.ls(name, uuid=1)[0]

    @classmethod
    def delete(cls, name):
        cmds.delete(name)

    @classmethod
    def rename(cls, name, new_name):
        return cmds.rename(name, new_name)

    @classmethod
    def is_locked(cls, name):
        return cmds.lockNode(name, query=1, lock=1) == [True]

    @classmethod
    def unlock(cls, name):
        cmds.lockNode(name, lock=False, lockUnpublished=False)


class NodeOpt(object):
    def __init__(self, name):
        self._name_or_path = name
        self._name = name
        
        self._node_query = None

    @property
    def type(self):
        return Node.get_type(self._name)

    @property
    def name(self):
        return self._name
    
    @property
    def name_or_path(self):
        return self._name
