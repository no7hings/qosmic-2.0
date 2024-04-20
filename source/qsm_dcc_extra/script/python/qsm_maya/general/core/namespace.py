# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


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
