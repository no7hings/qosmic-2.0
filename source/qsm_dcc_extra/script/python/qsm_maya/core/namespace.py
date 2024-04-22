# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import reference as _reference


class Namespace(object):
    @classmethod
    def get_by_path(cls, path):
        """
        # etc. |A:B:C, is A:B
        """
        return ':'.join(path.split('|')[-1].split(':')[:-1])
    
    @classmethod
    def get_root_by_path(cls, path):
        """
        # etc. |A:B:C, is A
        """
        return path.split('|')[-1].split(':')[0]

    @classmethod
    def get_is_exists(cls, namespace):
        return cmds.namespace(exists=namespace)


class Namespaces(object):
    @classmethod
    def get_by_selection(cls):
        paths = cmds.ls(selection=1, long=1)
        list_ = []
        for i_path in paths:
            i_namespace = Namespace.get_by_path(i_path)
            if i_namespace:
                list_.append(i_namespace)
        return list(set(list_))

    @classmethod
    def get_roots_by_selection(cls):
        paths = cmds.ls(selection=1, long=1)
        list_ = []
        for i_path in paths:
            i_namespace = Namespace.get_root_by_path(i_path)
            if i_namespace:
                list_.append(i_namespace)
        return list(set(list_))


class NamespaceQuery(object):

    def __init__(self):
        self._cache_dict = dict()
        self._cache_all()

    def _cache_all(self):
        _ = _reference.References.get_all_loaded()
        for i in _:
            i_namespace = _reference.Reference.get_namespace(i)
            self._cache_dict[i_namespace] = i

    def get_file(self, namespace, extend=True):
        if namespace in self._cache_dict:
            path = self._cache_dict[namespace]
            return _reference.Reference.get_file_path(path, extend)

    def to_valid_namespaces(self, namespaces):
        list_ = []
        for i_namespace in namespaces:
            if Namespace.get_is_exists(i_namespace):
                i_file_path = self.get_file(i_namespace)
                if i_file_path:
                    list_.append(i_namespace)
        return list_

    @classmethod
    def get_root(cls, namespace):
        _ = cmds.ls('|{}:*'.format(namespace), long=1)
        if _:
            return _[0]

    @classmethod
    def find_namespaces(cls, paths):
        list_ = []
        for i_path in paths:
            i_namespace = i_path.split('|')[-1].split(':')[0]
            if i_namespace:
                list_.append(i_namespace)
        return list(set(list_))

