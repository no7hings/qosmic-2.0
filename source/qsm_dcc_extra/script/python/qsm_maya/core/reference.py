# coding:utf-8
import collections
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import base as _base

from . import scene as _scene

from . import scene_file as _scene_file

from . import namespace as _namespace


class Reference(object):
    @classmethod
    def is_loaded(cls, path):
        # noinspection PyBroadException
        try:
            return cmds.referenceQuery(path, isLoaded=1)
        except Exception:
            return False

    @classmethod
    def get_file(cls, path, extend=True):
        # noinspection PyBroadException
        try:
            _ = cmds.referenceQuery(path, filename=1)
            if extend is True:
                return cmds.referenceQuery(path, filename=1, withoutCopyNumber=1)
            return _
        except Exception:
            return None

    @classmethod
    def get_namespace(cls, path):
        # noinspection PyBroadException
        try:
            return cmds.referenceQuery(path, namespace=1, shortName=1)
        except Exception:
            return None

    @classmethod
    def get_file_args(cls, path):
        # noinspection PyBroadException
        try:
            return (
                cmds.referenceQuery(path, filename=1),
                cmds.referenceQuery(path, filename=1, withoutCopyNumber=1)
            )
        except Exception:
            return None

    @classmethod
    def get_args(cls, path):
        file_args = cls.get_file_args(path)
        if file_args is not None:
            # debug: when reference is unload, use cmd.file command to find namespace instance
            namespace = _scene_file.SceneFile.get_namespace(file_args[0])
            is_loaded = cls.is_loaded(path)
            if namespace is not None:
                return namespace, file_args[1], is_loaded
        return None

    @classmethod
    def is_from_reference(cls, path):
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
        _scene_file.SceneFile.reference_file(file_path, namespace)

    @classmethod
    def reload(cls, path):
        cmds.file(loadReference=path)

    @classmethod
    def unload(cls, path):
        cmds.file(unloadReference=path)

    @classmethod
    def replace(cls, path, file_path):
        cmds.file(file_path, loadReference=path)


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
            if not Reference.is_from_reference(i):
                if Reference.is_loaded(i):
                    list_.append(i)
        return list_

    @classmethod
    def get_all(cls):
        list_ = []
        _ = [i for i in cmds.ls(type='reference', long=1) or [] if i not in cls.NODE_EXCLUDE]
        for i in _:
            if not Reference.is_from_reference(i):
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

    def get_roots(self):
        return cmds.ls('|{}:*'.format(self.get_namespace()), long=1) or []

    def get_namespace(self):
        return Reference.get_namespace(self._path)

    def get_file(self):
        return Reference.get_file(self._path)

    def is_loaded(self):
        return Reference.is_loaded(self._path)

    def do_remove(self):
        Reference.remove(self._path)

    def do_duplicate(self):
        Reference.duplicate(self._path)

    def do_reload(self):
        Reference.reload(self._path)

    def do_unload(self):
        Reference.unload(self._path)

    def do_replace(self, file_path):
        Reference.replace(self._path, file_path)


class ReferenceQuery(object):
    def __init__(self):
        self._cache_dict = collections.OrderedDict()

        self.do_update()

    def do_update(self):
        _ = References.get_all()
        for i_path in _:
            i_opt = ReferenceOpt(i_path)
            self._cache_dict[i_path] = i_opt


class ReferenceNamespacesCache(object):

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
            return Reference.get_file(path, extend)

    def to_valid_namespaces(self, namespaces):
        list_ = []
        for i_namespace in namespaces:
            if _namespace.Namespace.is_exists(i_namespace):
                i_file_path = self.get_file(i_namespace)
                if i_file_path:
                    list_.append(i_namespace)
        return list_
