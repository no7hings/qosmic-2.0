# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import node_for_dag as _node_for_dag

from . import namespace as _namespace

from . import attribute as _attribute


class AssemblyDefinition(object):
    NODE_TYPE = 'assemblyDefinition'

    @classmethod
    def create(cls, location):
        name = location.split('|')[-1]
        cmds.container(type=cls.NODE_TYPE, name=name)

    @classmethod
    def add_cache(cls, path, file_path, rep_name):
        cmds.assembly(
            path,
            edit=1,
            createRepresentation='Cache',
            repName=rep_name,
            input=file_path
        )

    @classmethod
    def add_scene(cls, path, file_path, rep_name):
        cmds.assembly(
            path,
            edit=1,
            createRepresentation='Scene',
            repName=rep_name,
            input=file_path
        )

    @classmethod
    def add_locator(cls, path, file_path, rep_name):
        cmds.assembly(
            path,
            edit=1,
            createRepresentation='Locator',
            repName=rep_name,
            input=file_path
        )

    @classmethod
    def set_active(cls, path, rep_name):
        cmds.assembly(path, edit=1, active=rep_name)


class AssemblyReference(object):
    NODE_TYPE = 'assemblyReference'

    @classmethod
    def create(cls, ad_file_path, location, namespace=None):
        parent_path = '|'.join(location.split('|')[:-1])
        name = location.split('|')[-1]
        result = cmds.assembly(name=name, type=cls.NODE_TYPE)
        path_new = _node_for_dag.DagNode.parent_to(result, parent_path, relative=True)
        _attribute.NodeAttribute.set_as_string(path_new, 'definition', ad_file_path)
        if namespace is not None:
            cls.rename_namespace(path_new, namespace)
        return path_new

    @classmethod
    def get_file(cls, path):
        return _attribute.NodeAttribute.get_as_string(path, 'definition')

    @classmethod
    def get_namespace(cls, path):
        return cmds.assembly(path, query=1, repNamespace=1)

    @classmethod
    def rename_namespace(cls, path, namespace_new):
        namespace = cls.get_namespace(path)
        _namespace.Namespace.rename(namespace, namespace_new)

    @classmethod
    def set_active(cls, path, rep_name):
        cmds.assembly(
            path + '.representations', edit=1, active=rep_name
        )

    @classmethod
    def get_active(cls, path):
        return cmds.assembly(path, query=1, active=1) or 'None'
