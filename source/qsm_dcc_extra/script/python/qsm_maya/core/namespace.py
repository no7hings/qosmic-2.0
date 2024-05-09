# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class Namespace(object):
    @classmethod
    def extract_from_path(cls, path):
        """
        # etc. |A:B:C, is A:B
        """
        return ':'.join(path.split('|')[-1].split(':')[:-1])
    
    @classmethod
    def extract_root_from_path(cls, path):
        """
        # etc. |A:B:C, is A
        """
        return path.split('|')[-1].split(':')[0]

    @classmethod
    def get_is_exists(cls, namespace):
        return cmds.namespace(exists=namespace)

    @classmethod
    def find_root(cls, namespace):
        _ = cmds.ls('|{}:*'.format(namespace, long=1))
        if _:
            return _[0]

    @classmethod
    def rename(cls, namespace, new_namespace):
        cmds.namespace(rename=[namespace, new_namespace], parent=':')

    @classmethod
    def get_nodes(cls, namespace):
        return cmds.namespaceInfo(namespace, listOnlyDependencyNodes=1, dagPath=1) or []

    @classmethod
    def find_nodes(cls, namespace, type_includes):
        _ = cls.get_nodes(namespace)
        return [x for x in _ if cmds.nodeType(x) in type_includes]


class Namespaces(object):
    @classmethod
    def extract_from_selection(cls):
        paths = cmds.ls(selection=1, long=1)
        list_ = []
        for i_path in paths:
            i_namespace = Namespace.extract_from_path(i_path)
            if i_namespace:
                # must keep order
                if i_namespace not in list_:
                    list_.append(i_namespace)
        return list_

    @classmethod
    def extract_roots_from_selection(cls):
        paths = cmds.ls(selection=1, long=1)
        list_ = []
        for i_path in paths:
            i_namespace = Namespace.extract_root_from_path(i_path)
            if i_namespace:
                # must keep order
                if i_namespace not in list_:
                    list_.append(i_namespace)
        return list_

    @classmethod
    def extract_from_paths(cls, paths):
        list_ = []
        for i_path in paths:
            i_namespace = Namespace.extract_from_path(i_path)
            if i_namespace:
                # must keep order
                if i_namespace not in list_:
                    list_.append(i_namespace)
        return list_

