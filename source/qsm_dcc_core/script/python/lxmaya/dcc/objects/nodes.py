# coding:utf-8
import re

import copy

import os

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.dcc.objects as bsc_dcc_objects
# maya
from ...core.wrap import *

from ... import core as mya_core

from ... import abstracts as mya_abstracts
# maya dcc objects
from . import node as mya_dcc_obj_node

from . import node_for_dag as mya_dcc_obj_node_for_dag

from . import node_for_xgen as mya_dcc_obj_node_for_xgen

from . import node_for_arnold as mya_dcc_obj_node_for_arnold

from . import node_for_look as mya_dcc_obj_node_for_look


class Nodes(object):
    DCC_NODE_CLS = mya_dcc_obj_node.Node

    def __init__(self, type_names):
        self._type_names = type_names

    def get_obj_paths(self):
        return cmds.ls(type=self._type_names, long=1) or []

    def get_objs(self):
        return [self.DCC_NODE_CLS(i) for i in self.get_obj_paths()]


class Sets(mya_abstracts.AbsMyaNodes):
    DCC_TYPES_INCLUDE = ['objectSet']
    DCC_PATHS_EXCLUDE = ['defaultLightSet', 'defaultObjectSet']
    DCC_NODE_CLS = mya_dcc_obj_node_for_dag.Shape

    def __init__(self, *args):
        super(Sets, self).__init__(*args)


class Cameras(mya_abstracts.AbsMyaNodes):
    DCC_TYPES_INCLUDE = ['camera']
    DCC_PATHS_EXCLUDE = ['|persp|perspShape', '|top|topShape', '|front|frontShape', '|side|sideShape']
    DCC_NODE_CLS = mya_dcc_obj_node_for_dag.Shape

    def __init__(self, *args):
        super(Cameras, self).__init__(*args)


class AnimationLayers(mya_abstracts.AbsMyaNodes):
    DCC_TYPES_INCLUDE = ['animLayer']
    DCC_PATHS_EXCLUDE = ['BaseAnimation']
    DCC_NODE_CLS = mya_dcc_obj_node.Node

    def __init__(self, *args):
        super(AnimationLayers, self).__init__(*args)


class DisplayLayers(mya_abstracts.AbsMyaNodes):
    DCC_TYPES_INCLUDE = ['displayLayer']
    DCC_PATHS_EXCLUDE = ['defaultLayer']
    DCC_NODE_CLS = mya_dcc_obj_node.DisplayLayer

    def __init__(self, *args):
        super(DisplayLayers, self).__init__(*args)


class Constrains(mya_abstracts.AbsMyaNodes):
    DCC_TYPES_INCLUDE = [
        'parentConstraint',
        'pointConstraint',
        'orientConstraint',
        'scaleConstraint'
    ]
    DCC_PATHS_EXCLUDE = []
    DCC_NODE_CLS = mya_dcc_obj_node.Node

    def __init__(self, *args):
        super(Constrains, self).__init__(*args)


class UnknownNodes(mya_abstracts.AbsMyaNodes):
    DCC_TYPES_INCLUDE = ['unknown']
    DCC_PATHS_EXCLUDE = []
    DCC_NODE_CLS = mya_dcc_obj_node.Node

    def __init__(self, *args):
        super(UnknownNodes, self).__init__(*args)


class References(mya_abstracts.AbsMyaNodes):
    DCC_TYPES_INCLUDE = ['reference']
    DCC_PATHS_EXCLUDE = [
        '_UNKNOWN_REF_NODE_',
        'sharedReferenceNode'
    ]
    DCC_NODE_CLS = mya_dcc_obj_node.Reference

    def __init__(self, *args):
        super(References, self).__init__(*args)

    def get_reference_raw(self):
        lis = []
        for i in self.get_custom_nodes():
            i_namespace = i.get_namespace()
            i_file_path = i.get_file_path()
            lis.append(
                (i, i_namespace, i_file_path)
            )
        return lis

    def get_reference_dict(self):
        dict_ = {}
        for i_obj in self.get_custom_nodes():
            i_namespace = i_obj.get_namespace()
            i_file_path = i_obj.get_file_path()
            dict_[i_namespace] = i_obj, i_file_path
        return dict_

    def get_reference_dict_(self):
        """
        get dict for maya geometry export
        use namespace of "pg_namespace" instance real namespace
        :return:
        """
        dict_ = {}
        for i_obj in self.get_custom_nodes():
            if i_obj.get_is_loaded() is True:
                i_obj_paths = i_obj.get_content_obj_paths()
                if i_obj_paths:
                    i_namespace = i_obj.get_namespace()
                    i_root = i_obj_paths[0]
                    i_namespace_real = mya_dcc_obj_node.Node(i_root).get('pg_namespace')
                    if i_namespace_real:
                        i_shot_asset = i_namespace_real
                    else:
                        i_shot_asset = i_namespace
                    dict_[i_shot_asset] = i_namespace, i_root, i_obj
        return dict_


class Materials(mya_abstracts.AbsMyaNodes):
    DCC_TYPES_INCLUDE = ['shadingEngine']
    DCC_PATHS_EXCLUDE = [
        'initialShadingGroup',
        'initialParticleSE',
        'defaultLightSet',
        'defaultObjectSet'
    ]
    DCC_NODE_CLS = mya_dcc_obj_node_for_look.Material

    def __init__(self, *args):
        super(Materials, self).__init__(*args)


class TemporaryNodes(mya_abstracts.AbsMyaNodes):
    DCC_TYPES_INCLUDE = ['mesh', 'nurbsCurve', 'nurbsSurface', 'brush', 'nParticle']
    DCC_PATHS_EXCLUDE = []
    DCC_NODE_CLS = mya_dcc_obj_node.Node

    def __init__(self, *args):
        super(TemporaryNodes, self).__init__(*args)


class AbsFileReferences(object):
    DCC_NODE_CLS_DICT = {
        'custom': mya_dcc_obj_node.FileReference,
        'file': mya_dcc_obj_node.TextureReference,
        # it's right name
        'aiImage': mya_dcc_obj_node.TextureReference,
        'reference': mya_dcc_obj_node.Reference,
        #
        'xgmPalette': mya_dcc_obj_node_for_xgen.XgnPalette,
        'xgmDescription': mya_dcc_obj_node_for_xgen.XgnDescription,
        #
        'aiMaterialx': mya_dcc_obj_node_for_arnold.AndMaterialx,
        #
        'osl_file_path': mya_dcc_obj_node.TextureReference,
        'osl_window_box': mya_dcc_obj_node.TextureReference,
        'osl_window_box_s': mya_dcc_obj_node.TextureReference,
        #
        'aiJiWindowBoxArnold': mya_dcc_obj_node.TextureReference,
    }
    #
    PORT_QUERY_DICT = {
        'file': ['fileTextureName'],
        'aiImage': ['filename'],
        #
        'gpuCache': ['cacheFileName'],
        'AlembicNode': ['abc_File'],
        #
        'aiVolume': ['filename'],
        'aiMaterialx': ['filename'],
        #
        'osl_file_path': ['filename'],
        'osl_window_box': ['filename'],
        'osl_window_box_s': ['filename'],
        #
        'aiJiWindowBoxArnold': ['filename'],
    }
    #
    PORT_PATHSEP = mya_core.MyaUtil.PORT_PATHSEP
    #
    OPTION = dict(
        with_reference=True,
        includes=[]
    )

    def __init__(self, *args, **kwargs):
        self._raw = {}
        #
        self._option = copy.deepcopy(self.OPTION)
        if 'option' in kwargs:
            option = kwargs['option']
            if isinstance(option, dict):
                for k, v in option.items():
                    if k in self.OPTION:
                        self._option[k] = v

    # convert for file
    @classmethod
    def _auto_convert_file_value(cls, obj, file_path):
        if obj.type == 'file':
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            # udim
            udim_pattern = re.compile(r'.*?(<udim>).*?', re.IGNORECASE)
            udim_results = re.findall(udim_pattern, file_name)
            if udim_results:
                return file_path
            #
            tile_mode = obj.get('uvTilingMode')
            if tile_mode == 3:
                results = re.findall(r'[0-9][0-9][0-9][0-9]', file_name)
                if results:
                    return file_path.replace(results[-1], '<udim>')
            # sequence
            sequence_pattern = re.compile(r'.*?(<f>).*?', re.IGNORECASE)
            sequence_results = re.findall(sequence_pattern, file_name)
            if sequence_results:
                return file_path
            #
            sequence_enable = obj.get('useFrameExtension')
            if sequence_enable:
                results = re.findall(r'[0-9]{3,4}', file_name)
                if results:
                    return file_path.replace(results[-1], '<f>')
            return file_path
        return file_path

    @classmethod
    def _get_real_file_value(cls, port):
        obj = port.obj
        file_path = port.get()
        return cls._auto_convert_file_value(
            obj, file_path
        )

    @classmethod
    def _set_real_file_value(cls, port, new_value, remove_expression=False):
        if port.get_is_locked():
            port.set_unlock()
        #
        port.set(new_value)
        obj = port.obj
        #
        cls._auto_repair_file_value(obj)

    @classmethod
    @bsc_core.MdfBaseMtd.run_as_ignore
    def _auto_repair_file_value(cls, obj):
        if obj.type_name == 'file':
            port = obj.get_port('fileTextureName')
            file_path = port.get()
            if file_path is not None:
                file_ = bsc_dcc_objects.StgFile(file_path)
                # sequence
                if obj.get('useFrameExtension'):
                    exists_file_paths = file_.get_exists_unit_paths()
                    if port.get_is_locked():
                        port.set_unlock()
                    #
                    port.set(exists_file_paths[0])
                #
                if file_.get_is_udim():
                    if obj.get('uvTilingMode') == 3:
                        exists_file_paths = file_.get_exists_unit_paths()
                        if port.get_is_locked():
                            port.set_unlock()
                        #
                        port.set(exists_file_paths[0])
                # crash error for close
                if mya_core.MyaUtil.get_is_ui_mode():
                    mel.eval('generateUvTilePreview {}'.format(obj.path))
            else:
                bsc_log.Log.trace_method_warning(
                    'file value repair',
                    'attribute="{}" gain "None" value'.format(port.path)
                )

    @classmethod
    def repair_file_values(cls):
        fs = cmds.ls(type='file')
        for i_f in fs:
            cls._auto_repair_file_value(
                mya_dcc_obj_node.Node(i_f)
            )

    @classmethod
    def _get_obj_cls(cls, obj_type_name):
        if obj_type_name in cls.DCC_NODE_CLS_DICT:
            return cls.DCC_NODE_CLS_DICT[obj_type_name]
        return cls.DCC_NODE_CLS_DICT['custom']

    @classmethod
    def _get_type_is_valid(cls, *args):
        return True

    def __get_by_definition(self, with_reference):
        cmds.filePathEditor(refresh=1)
        directory_paths = cmds.filePathEditor(query=1, listDirectories="") or []
        for i_directory_path in directory_paths:
            raw = cmds.filePathEditor(query=1, listFiles=i_directory_path, withAttribute=1) or []
            for j in range(len(raw)/2):
                j_file_name = raw[j*2]
                j_atr_path = raw[j*2+1]
                j_search_key = cmds.filePathEditor(j_atr_path, query=1, attributeType=1)
                #
                j_search_key_s = j_search_key.split(self.PORT_PATHSEP)
                j_obj_type_name = j_search_key_s[0]
                if self._get_type_is_valid(j_obj_type_name) is False:
                    continue
                #
                j_file_path = '{}/{}'.format(i_directory_path, j_file_name)
                #
                j_atr_path_s = j_atr_path.split(self.PORT_PATHSEP)
                #
                j_obj_path = j_atr_path_s[0]
                j_port_path = self.PORT_PATHSEP.join(j_atr_path_s[1:])
                #
                if j_obj_path in self._raw:
                    j_obj = self._raw[j_obj_path]
                else:
                    j_obj_cls = self._get_obj_cls(j_obj_type_name)
                    j_obj = j_obj_cls(j_obj_path)
                    self._raw[j_obj_path] = j_obj
                #
                if with_reference is False:
                    j_is_reference = j_obj.get_is_reference()
                    if j_is_reference is True:
                        continue
                #
                j_obj.register_file(
                    j_port_path, self._auto_convert_file_value(j_obj, j_file_path)
                )

    def __get_by_custom(self, with_reference):
        all_obj_type_names = cmds.allNodeTypes()

        for i_obj_type_name, i_port_paths in self.PORT_QUERY_DICT.items():
            if self._get_type_is_valid(i_obj_type_name) is False:
                continue
            #
            if i_obj_type_name not in all_obj_type_names:
                bsc_log.Log.trace_warning(
                    'obj-type="{}" is "unknown" / "unload"'.format(i_obj_type_name)
                )
                continue
            #
            for j_port_path in i_port_paths:
                j_obj_paths = cmds.ls(type=i_obj_type_name, long=1) or []
                for k_obj_path in j_obj_paths:
                    k_atr_path = self.PORT_PATHSEP.join([k_obj_path, j_port_path])
                    k_file_path = cmds.getAttr(k_atr_path)
                    if not k_file_path:
                        bsc_log.Log.trace_warning(
                            'port="{}" is "empty"'.format(k_atr_path)
                        )
                        continue
                    if k_obj_path in self._raw:
                        k_obj = self._raw[k_obj_path]
                    else:
                        k_obj_cls = self._get_obj_cls(i_obj_type_name)
                        k_obj = k_obj_cls(k_obj_path)
                        self._raw[k_obj_path] = k_obj

                    if with_reference is False:
                        k_is_reference = k_obj.get_is_reference()
                        if k_is_reference is True:
                            continue

                    k_obj.register_file(
                        j_port_path, self._auto_convert_file_value(k_obj, k_file_path)
                    )

    def get_objs(self):
        with_reference = self._option['with_reference']
        #
        self._raw = {}
        self.__get_by_definition(with_reference)
        self.__get_by_custom(with_reference)
        return self._raw.values()

    def get_types(self):
        pass

    def get_exists_file_paths(self):
        lis = []
        path_dict = {}
        for n in self.get_objs():
            for f in n.get_stg_files():
                sub_files = f.get_exists_units()
                for sf in sub_files:
                    normcase_file_path = sf.normcase_path
                    if normcase_file_path in path_dict:
                        file_path = path_dict[normcase_file_path]
                    else:
                        file_path = sf.path
                        path_dict[normcase_file_path] = file_path
                    #
                    lis.append(file_path)
        return lis

    def get_file_paths(self):
        lis = []
        path_dict = {}
        for n in self.get_objs():
            for f in n.get_stg_files():
                normcase_file_path = f.normcase_path
                if normcase_file_path in path_dict:
                    file_path = path_dict[normcase_file_path]
                else:
                    file_path = f.path
                    path_dict[normcase_file_path] = file_path
                #
                lis.append(file_path)
        return lis

    @classmethod
    def repath_fnc(cls, obj, port_path, file_path_new, remove_expression=False):
        port = obj.get_port(port_path)
        file_path = cls._get_real_file_value(
            port
        )
        if file_path != file_path_new:
            cls._set_real_file_value(
                obj.get_port(port_path), file_path_new, remove_expression
            )


class FileReferences(AbsFileReferences):
    def __init__(self, *args, **kwargs):
        super(FileReferences, self).__init__(*args, **kwargs)


class TextureReferences(AbsFileReferences):
    INCLUDE_DCC_FILE_TYPES = [
        'file',
        'aiImage.filename',
    ]
    INCLUDE_TYPES = [
        'file',
        'aiImage',
        #
        'osl_file_path',
        'osl_window_box',
        'osl_window_box_s',
        #
        'aiJiWindowBoxArnold',
    ]

    def __init__(self, *args, **kwargs):
        super(TextureReferences, self).__init__(*args, **kwargs)

    def _get_type_is_valid(self, file_type):
        return file_type in self.INCLUDE_TYPES

    @classmethod
    def _get_objs_(cls, obj_paths):
        lis = []
        for obj_path in obj_paths:
            i_obj_type_name = cmds.nodeType(obj_path)
            if i_obj_type_name in cls.PORT_QUERY_DICT:
                i_obj_cls = cls._get_obj_cls(i_obj_type_name)
                i_obj = i_obj_cls(obj_path)
                cls._set_obj_reference_update_(i_obj)
                lis.append(i_obj)
        return lis

    @classmethod
    def _set_obj_reference_update_(cls, obj):
        obj_type_name = obj.type_name
        obj_path = obj.path
        if obj_type_name in cls.PORT_QUERY_DICT:
            port_paths = cls.PORT_QUERY_DICT[obj_type_name]
            obj.restore()
            for i_port_path in port_paths:
                atr_path = cls.PORT_PATHSEP.join([obj_path, i_port_path])
                value = cmds.getAttr(atr_path)
                obj.register_file(
                    i_port_path, cls._auto_convert_file_value(obj, value)
                )


class XgenPalettes(mya_abstracts.AbsMyaNodes):
    DCC_TYPES_INCLUDE = ['xgmPalette']
    DCC_PATHS_EXCLUDE = []
    DCC_NODE_CLS = mya_dcc_obj_node_for_xgen.XgnPalette

    def __init__(self):
        super(XgenPalettes, self).__init__(XgenPalettes)


class XgenDescriptions(mya_abstracts.AbsMyaNodes):
    DCC_TYPES_INCLUDE = ['xgmDescription']
    DCC_PATHS_EXCLUDE = []
    DCC_NODE_CLS = mya_dcc_obj_node_for_xgen.XgnDescription

    def __init__(self):
        super(XgenDescriptions, self).__init__(XgenPalettes)
