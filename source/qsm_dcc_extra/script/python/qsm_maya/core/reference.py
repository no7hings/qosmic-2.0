# coding:utf-8
import collections
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import base as _base

from . import scene as _scene

from . import namespace as _namespace


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
    def get_is_from_reference(cls, path):
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
            if not Reference.get_is_from_reference(i):
                if Reference.get_is_loaded(i):
                    list_.append(i)
        return list_

    @classmethod
    def get_all(cls):
        list_ = []
        _ = [i for i in cmds.ls(type='reference', long=1) or [] if i not in cls.NODE_EXCLUDE]
        for i in _:
            if not Reference.get_is_from_reference(i):
                list_.append(i)
        return list_


class ReferenceOpt(_base.AbsNodeOpt):
    Type = 'reference'

    def __init__(self, *args, **kwargs):
        super(ReferenceOpt, self).__init__(*args, **kwargs)

    def get_root(self):
        _ = cmds.ls('|{}:*'.format(self.get_namespace()), long=1)
        if _:
            return _[0]

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


class ReferenceQuery(object):
    def __init__(self):
        self._cache_dict = collections.OrderedDict()

        self.do_update()

    def do_update(self):
        _ = References.get_all()
        for i_path in _:
            i_opt = ReferenceOpt(i_path)
            self._cache_dict[i_path] = i_opt


class ReferenceNamespaceQuery(object):

    def __init__(self):
        self._cache_dict = dict()
        self.do_update()

    def do_update(self):
        _ = References.get_all_loaded()
        for i in _:
            i_namespace = Reference.get_namespace(i)
            self._cache_dict[i_namespace] = i

    def get_file(self, namespace, extend=True):
        if namespace in self._cache_dict:
            path = self._cache_dict[namespace]
            return Reference.get_file_path(path, extend)

    def to_valid_namespaces(self, namespaces):
        list_ = []
        for i_namespace in namespaces:
            if _namespace.Namespace.get_is_exists(i_namespace):
                i_file_path = self.get_file(i_namespace)
                if i_file_path:
                    list_.append(i_namespace)
        return list_