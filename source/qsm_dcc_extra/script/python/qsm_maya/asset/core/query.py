# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class SceneQuery(object):
    @classmethod
    def get_frame_range(cls):
        start_frame = int(cmds.playbackOptions(query=1, minTime=1))
        end_frame = int(cmds.playbackOptions(query=1, maxTime=1))
        return start_frame, end_frame


class ReferenceQuery(object):
    NODE_EXCLUDE = [
        '_UNKNOWN_REF_NODE_',
        'sharedReferenceNode'
    ]

    @classmethod
    def get_is_loaded(cls, path):
        # noinspection PyBroadException
        try:
            return cmds.referenceQuery(path, isLoaded=1)
        except Exception:
            return False

    @classmethod
    def get_is_reference_node(cls, path):
        return cmds.referenceQuery(path, isNodeReferenced=1)

    @classmethod
    def get_all_loaded(cls):
        list_ = []
        _ = [i for i in cmds.ls(type='reference', long=1) or [] if i not in cls.NODE_EXCLUDE]
        for i in _:
            if not cls.get_is_reference_node(i):
                if cls.get_is_loaded(i):
                    list_.append(i)
        return list_

    @classmethod
    def get_file(cls, path, extend=True):
        _ = cmds.referenceQuery(path, filename=1)
        if extend is True:
            return cmds.referenceQuery(path, filename=1, withoutCopyNumber=1)
        return _

    @classmethod
    def get_namespace(cls, path):
        return cmds.referenceQuery(path, namespace=1, shortName=1)


class NamespaceQuery(object):

    def __init__(self):
        self._cache_dict = dict()
        self._cache_all()

    def _cache_all(self):
        _ = ReferenceQuery.get_all_loaded()
        for i in _:
            i_namespace = ReferenceQuery.get_namespace(i)
            self._cache_dict[i_namespace] = i

    def get_file(self, namespace, extend=True):
        if namespace in self._cache_dict:
            path = self._cache_dict[namespace]
            return ReferenceQuery.get_file(path, extend)

    @classmethod
    def get_is_exists(cls, namespace):
        return cmds.namespace(exists=namespace)

    def to_valid_namespaces(self, namespaces):
        list_ = []
        for i_namespace in namespaces:
            if self.get_is_exists(i_namespace):
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


