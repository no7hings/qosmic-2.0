# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import base as _base

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
            # result is :A, must strip ":" later
            _ = cmds.referenceQuery(path, namespace=1)
            if _:
                return _.strip(':')
            return None
            # return cmds.referenceQuery(path, namespace=1, shortName=1)
        except Exception:
            return None

    @classmethod
    def get_file_args(cls, path):
        # noinspection PyBroadException
        try:
            return (
                # with copy number, ect. /a/b.ma
                cmds.referenceQuery(path, filename=1),
                # without copy number, ect. /a/b.ma{1}
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
        file_path = cmds.referenceQuery(path, filename=1, withoutCopyNumber=1)
        result = _scene_file.SceneFile.reference_file(file_path, namespace)
        namespace_new = _scene_file.SceneFile.get_namespace(result)
        return namespace_new

    @classmethod
    def reload(cls, path):
        cmds.file(loadReference=path, force=1)

    @classmethod
    def load(cls, path, load_no_references=False):
        kwargs = dict(loadReference=path, force=1)
        if load_no_references is True:
            kwargs['loadNoReferences'] = True
        cmds.file(**kwargs)

    @classmethod
    def unload(cls, path):
        cmds.file(unloadReference=path)

    @classmethod
    def replace(cls, path, file_path):
        cmds.file(file_path, loadReference=path, force=1)

    @classmethod
    def get_nodes(cls, path):
        return [cmds.ls(x, long=1)[0] for x in cmds.referenceQuery(path, nodes=1, dagPath=1) or []]


class References(object):
    NODE_EXCLUDE = [
        '_UNKNOWN_REF_NODE_',
        'sharedReferenceNode'
    ]

    @classmethod
    def get_all_loaded(cls, nested=False):
        list_ = []
        _ = [i for i in cmds.ls(type='reference', long=1) or [] if i not in cls.NODE_EXCLUDE]
        for i in _:
            if not Reference.is_from_reference(i):
                if Reference.is_loaded(i):
                    list_.append(i)
            else:
                if nested is True:
                    list_.append(i)
        return list_

    @classmethod
    def get_all(cls, nested=False):
        list_ = []
        _ = [x for x in cmds.ls(type='reference', long=1) or [] if x not in cls.NODE_EXCLUDE]
        for i in _:
            if not Reference.is_from_reference(i):
                list_.append(i)
            else:
                if nested is True:
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


class ReferencesCache(object):
    INSTANCE = None

    def __init__(self):
        self._dict = dict()
        self.do_update()

    def get_data(self):
        pass

    def do_update(self):
        _ = References.get_all(nested=True)
        for i_reference in _:
            i_namespace = Reference.get_namespace(i_reference)
            self._dict[i_namespace] = i_reference

    def get_file(self, namespace, extend=True):
        if namespace in self._dict:
            reference = self._dict[namespace]
            return Reference.get_file(reference, extend)

    def get(self, namespace):
        return self._dict.get(namespace)

    def to_valid_namespaces(self, namespaces):
        list_ = []
        for i_namespace in namespaces:
            if _namespace.Namespace.is_exists(i_namespace):
                i_file_path = self.get_file(i_namespace)
                if i_file_path:
                    list_.append(i_namespace)
        return list_

    def find_from_selection(self):
        list_ = []
        namespaces = _namespace.Namespaces.extract_from_selection()
        for i_namespace in namespaces:
            i_reference_node = self.get(i_namespace)
            if i_reference_node:
                list_.append(i_reference_node)
        return list_
