# coding:utf-8
import fnmatch

import lxbasic.log as bsc_log

import lxbasic.dcc.objects as bsc_dcc_objects
# maya
from ...core.wrap import *

from ... import abstracts as mya_abstracts
# maya dcc objects
from . import utility as mya_dcc_obj_utility


class Port(mya_abstracts.AbsMyaPort):
    def __init__(self, node, name, port_assign=None):
        super(Port, self).__init__(node, name, port_assign=port_assign)


class Node(mya_abstracts.AbsMyaNode):
    DCC_PORT_CLS = mya_dcc_obj_utility.Port
    DCC_CONNECTION_CLS = mya_dcc_obj_utility.Connection

    def __init__(self, path):
        super(Node, self).__init__(path)

    # dag
    def get_child_paths(self):
        return cmds.listRelatives(self.path, children=1, fullPath=1) or []

    def get_children(self):
        return [self.__class__(i) for i in self.get_child_paths()]

    def get_descendant_paths(self, *args, **kwargs):
        def _rcs_fnc(lis_, path_):
            lis_.append(path_)
            _ = cmds.listRelatives(path_, children=1, fullPath=1) or []
            if _:
                for _i in _:
                    _rcs_fnc(lis_, _i)

        lis = []
        _rcs_fnc(lis, self.path)
        return lis

    def get_descendants(self, *args, **kwargs):
        # noinspection PyArgumentList
        return [self.__class__(i) for i in self.get_descendant_paths(*args, **kwargs)]

    def get_parent_path(self):
        if self.get_is_exists() is True:
            _ = cmds.listRelatives(self.get_path(), parent=1, fullPath=1)
            if _:
                return _[0]

    def get_parent(self):
        _ = self.get_parent_path()
        if _:
            return self.__class__(_)


class DisplayLayer(mya_abstracts.AbsMyaNode):
    DCC_PORT_CLS = mya_dcc_obj_utility.Port
    DCC_CONNECTION_CLS = mya_dcc_obj_utility.Connection
    DCC_NODE_CLS = Node

    def __init__(self, path):
        super(DisplayLayer, self).__init__(path)

    def get_objs(self):
        lis = []
        for path in self.get_node_paths():
            lis.append(self.DCC_NODE_CLS(path))
        return lis

    def get_node_paths(self):
        if cmds.objExists(self.path):
            return cmds.editDisplayLayerMembers(self.path, query=1, fullNames=1) or []
        return []


class Reference(mya_abstracts.AbsMyaNodeForFileReference):
    DCC_PORT_CLS = mya_dcc_obj_utility.Port
    STG_FILE_CLS = bsc_dcc_objects.StgFile

    def __init__(self, path):
        super(Reference, self).__init__(self._to_full_path(path))

    def get_is_loaded(self):
        # noinspection PyBroadException
        try:
            return cmds.referenceQuery(self.name, isLoaded=1)
        except Exception:
            return False

    def do_replace(self, file_path):
        cmds.file(file_path, loadReference=self.name)
        bsc_log.Log.trace_method_result(
            'reference replace',
            u'file="{}"'.format(file_path)
        )

    def set_reload(self):
        cmds.file(loadReference=self.name)

    def set_load(self):
        cmds.file(loadReference=self.name)

    def do_remove(self):
        if cmds.objExists(self.name):
            file_path = cmds.referenceQuery(self.name, filename=1)
            cmds.file(file_path, removeReference=1)

    def set_unload(self):
        cmds.file(unloadReference=self.name)

    def get_file_path(self, extend=True):
        _ = cmds.referenceQuery(self.name, filename=1)
        if extend is True:
            return cmds.referenceQuery(self.name, filename=1, withoutCopyNumber=1)
        return _

    def get_file(self):
        return bsc_dcc_objects.StgFile(self.get_file_path())

    def get_namespace_path(self):
        return cmds.referenceQuery(self.name, namespace=1)

    def get_namespace(self):
        return cmds.referenceQuery(self.name, namespace=1, shortName=1)

    def set_namespace_path(self, namespace_path):
        if cmds.namespace(exists=namespace_path) is False:
            file_path = cmds.referenceQuery(self.name, filename=1)
            cmds.file(file_path, namespace=namespace_path, edit=1)

    def get_content_obj_paths(self):
        return [cmds.ls(i, long=1)[0] for i in cmds.referenceQuery(self.name, nodes=1, dagPath=1) or []]

    def load_from_file(self, file_path, namespace):
        if cmds.objExists(self.name) is False:
            result = mya_dcc_obj_utility.SceneFile.set_reference_create(file_path, namespace)
            rn = cmds.referenceQuery(result, referenceNode=1)
            if rn != self.name:
                cmds.lockNode(rn, lock=0)
                r = cmds.rename(rn, self.name)
                cmds.lockNode(r, lock=1)

    def get_content_root_paths(self):
        paths = [cmds.ls(i, long=1)[0] for i in cmds.referenceQuery(self.name, nodes=1, dagPath=1) or []]
        return [path for path in paths if len(path.split(self.PATHSEP)) == 2]

    def _test(self):
        pass


class FileReference(mya_abstracts.AbsMyaNodeForFileReference):
    DCC_PORT_CLS = mya_dcc_obj_utility.Port
    STG_FILE_CLS = bsc_dcc_objects.StgFile

    def __init__(self, path, file_path=None):
        super(FileReference, self).__init__(self._to_full_path(path))
        self._init_dcc_node_file_reference_def_(file_path)


class TextureReference(mya_abstracts.AbsMyaNodeForFileReference):
    DCC_PORT_CLS = mya_dcc_obj_utility.Port
    STG_FILE_CLS = bsc_dcc_objects.StgTexture

    def __init__(self, path, file_path=None):
        super(TextureReference, self).__init__(self._to_full_path(path), file_path)

    def get_color_space(self):
        return self.get_port('colorSpace').get()

    def set_color_space(self, color_space):
        if self.get_color_space() != color_space:
            self.get_port('ignoreColorSpaceFileRules').set(True)
            self.get_port('colorSpace').set(color_space)
            bsc_log.Log.trace_method_result(
                'color-space switch',
                'obj="{}", color-space="{}"'.format(self.path, color_space)
            )


class Alembic(mya_abstracts.AbsMyaNodeForFileReference):
    DCC_PORT_CLS = mya_dcc_obj_utility.Port
    STG_FILE_CLS = bsc_dcc_objects.StgFile

    def __init__(self, path):
        super(Alembic, self).__init__(path)


class Set(mya_abstracts.AbsMyaNode):
    DCC_PORT_CLS = mya_dcc_obj_utility.Port
    DCC_CONNECTION_CLS = mya_dcc_obj_utility.Connection

    def __init__(self, path):
        super(Set, self).__init__(path)

    def set_create(self, *args, **kwargs):
        if self.get_is_exists() is False:
            cmds.sets(name=self.path, empty=1)

    def add_element(self, path):
        cmds.sets(path, addElement=self.path, edit=1)
        bsc_log.Log.trace_method_result(
            'set-element-add',
            'connection="{}" >> "{}"'.format(path, self.path)
        )

    def get_element_exists(self, path):
        pass

    def get_elements(self):
        return cmds.sets(self.path, query=1) or []

    def set_element_remove(self, path):
        cmds.sets(path, remove=self.path, edit=1)
        bsc_log.Log.trace_method_result(
            'set-element-remove',
            'connection="{}" >> "{}"'.format(path, self.path)
        )

    def set_elements_clear(self):
        _ = self.get_elements()
        [self.set_element_remove(i) for i in _]

    def get_elements_match(self, pattern):
        return fnmatch.filter(
            [cmds.ls(i, long=1)[0] for i in self.get_elements()], pattern
        )
