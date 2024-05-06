# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class Node(object):
    class Types(object):
        Transform = 'transform'
        Mesh = 'mesh'
        GPU = 'gpuCache'

    @classmethod
    def get_type(cls, path):
        return cmds.nodeType(path)

    @classmethod
    def is_transform(cls, path):
        return cls.get_type(path) == cls.Types.Transform

    @classmethod
    def is_mesh(cls, path):
        return cls.get_type(path) == cls.Types.Mesh

    @classmethod
    def is_gpu(cls, path):
        return cls.get_type(path) == cls.Types.GPU

    @classmethod
    def is_exists(cls, path):
        return cmds.objExists(path)

    @classmethod
    def get_uuid(cls, path):
        return cmds.ls(path, uuid=1)[0]

    @classmethod
    def delete(cls, path):
        cmds.delete(path)
