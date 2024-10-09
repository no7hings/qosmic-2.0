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
    def is_exists(cls, namespace):
        return cmds.namespace(exists=namespace)

    @classmethod
    def find_roots(cls, namespace):
        return cmds.ls('|{}:*'.format(namespace, long=1)) or []

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

    # include instanced
    @classmethod
    def get_all_dag_nodes(cls, namespace):
        list_ = []
        _ = cmds.namespaceInfo(namespace, listOnlyDependencyNodes=1, dagPath=1) or []
        for i_name in _:
            i_path = cmds.ls(i_name, long=1)[0]
            if not i_path.startswith('|'):
                continue
            # check is instance
            i_parents = cmds.listRelatives(i_path, fullPath=1, allParents=1) or []
            if len(i_parents) > 1:
                i_name = i_path.split('|')[-1]
                for j_path in i_parents:
                    j_path_shape = '{}|{}'.format(j_path, i_name)
                    list_.append(j_path_shape)
            else:
                list_.append(i_path)
        return list_

    # include instanced
    @classmethod
    def find_all_dag_nodes(cls, namespace, type_includes):
        return [x for x in cls.get_all_dag_nodes(namespace) if cmds.nodeType(x) in type_includes]

    @classmethod
    def create(cls, namespace):
        if cmds.namespace(exists=namespace) is False:
            cmds.namespace(add=namespace)

    @classmethod
    def remove(cls, namespace):
        if cmds.namespace(exists=namespace) is True:
            cmds.namespace(removeNamespace=namespace, mergeNamespaceWithRoot=1)


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

