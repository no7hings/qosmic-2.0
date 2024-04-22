# coding:utf-8
import collections
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import base as _base

from . import scene as _scene


class Reference(object):
    @classmethod
    def get_is_loaded(cls, path):
        # noinspection PyBroadException
        try:
            return cmds.referenceQuery(path, isLoaded=1)
        except Exception:
            return False

    @classmethod
    def get_file_path(cls, path, extend=True):
        _ = cmds.referenceQuery(path, filename=1)
        if extend is True:
            return cmds.referenceQuery(path, filename=1, withoutCopyNumber=1)
        return _

    @classmethod
    def get_namespace(cls, path):
        return cmds.referenceQuery(path, namespace=1, shortName=1)

    @classmethod
    def get_is_reference_node(cls, path):
        return cmds.referenceQuery(path, isNodeReferenced=1)

    @classmethod
    def remove(cls, path):
        # with copy number
        file_path = cmds.referenceQuery(path, filename=1)
        cmds.file(file_path, removeReference=1)

    @classmethod
    def duplicate(cls, path):
        namespace = cmds.referenceQuery(path, namespace=1, shortName=1)
        file_path = cmds.referenceQuery(path, filename=1)
        _scene.Scene.reference_file(file_path, namespace)

    @classmethod
    def reload(cls, path):
        cmds.file(loadReference=path)

    @classmethod
    def unload(cls, path):
        cmds.file(unloadReference=path)


class References(object):
    NODE_EXCLUDE = [
        '_UNKNOWN_REF_NODE_',
        'sharedReferenceNode'
    ]

    @classmethod
    def get_all_loaded(cls):
        list_ = []
        _ = [i for i in cmds.ls(type='reference', long=1) or [] if i not in cls.NODE_EXCLUDE]
        for i in _:
            if not Reference.get_is_reference_node(i):
                if Reference.get_is_loaded(i):
                    list_.append(i)
        return list_

    @classmethod
    def get_all(cls):
        list_ = []
        _ = [i for i in cmds.ls(type='reference', long=1) or [] if i not in cls.NODE_EXCLUDE]
        for i in _:
            if not Reference.get_is_reference_node(i):
                list_.append(i)
        return list_


class ReferenceNode(_base.AbsNode):
    Type = 'reference'

    def __init__(self, *args, **kwargs):
        super(ReferenceNode, self).__init__(*args, **kwargs)

    def get_namespace(self):
        return Reference.get_namespace(self._path)

    def get_file_path(self):
        return Reference.get_file_path(self._path)

    def is_loaded(self):
        return Reference.get_is_loaded(self._path)

    def do_remove(self):
        Reference.remove(self._path)

    def do_duplicate(self):
        Reference.duplicate(self._path)

    def do_reload(self):
        Reference.reload(self._path)

    def do_unload(self):
        Reference.unload(self._path)


class ReferenceNodeQuery(object):
    def __init__(self):
        self._cache_dict = collections.OrderedDict()

        self._cache_all()

    def _cache_all(self):
        _ = References.get_all()
        for i_path in _:
            i_node = ReferenceNode()
            self._cache_dict[i_path] = i_node
