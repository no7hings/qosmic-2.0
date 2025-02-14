# coding:utf-8
import re

import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from . import node as _node

from . import attribute as _attribute


class FileReferences(object):
    QUERY = {
        'file': ['fileTextureName'],
        #
        'gpuCache': ['cacheFileName'],
        'AlembicNode': ['abc_File']
    }

    PLUGIN_NAMES = [
        'AbcImport',
        'AbcExport',
        'gpuCache'
    ]

    @classmethod
    def search_from(cls, paths, directory_paths):
        pass

    @classmethod
    def _auto_convert_file_value(cls, path, file_path):
        pass

    @classmethod
    def get_file(cls, path, atr_name):
        node_type = _node.Node.get_type(path)
        file_path = _attribute.NodeAttribute.get_as_string(path, atr_name)
        if node_type == 'file':
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            # udim
            udim_pattern = re.compile(r'.*?(<udim>).*?', re.IGNORECASE)
            udim_results = re.findall(udim_pattern, file_name)
            if udim_results:
                return file_path

            tile_mode = _attribute.NodeAttribute.get_value(path, 'uvTilingMode')
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
            sequence_enable = _attribute.NodeAttribute.get_value(path, 'useFrameExtension')
            if sequence_enable:
                results = re.findall(r'[0-9]{3,4}', file_name)
                if results:
                    return file_path.replace(results[-1], '<f>')
            return file_path
        return file_path

    @classmethod
    def set_file_path(cls, path, atr_name, file_path):
        if file_path is None:
            return
        node_type = _node.Node.get_type(path)
        if node_type == 'file':
            stg_file = bsc_storage.StgFileOpt(file_path)
            if bsc_core.BscFileTiles.is_valid(stg_file.name_base) is True:
                unit_paths = bsc_storage.StgFileTiles.get_tiles(
                    file_path
                )
                # sequence
                if _attribute.NodeAttribute.get_value(path, 'useFrameExtension'):
                    _attribute.NodeAttribute.set_as_string(path, atr_name, unit_paths[0])
                # udim
                elif _attribute.NodeAttribute.get_value(path, 'uvTilingMode') == 3:
                    _attribute.NodeAttribute.set_as_string(path, atr_name, unit_paths[0])
            else:
                _attribute.NodeAttribute.set_as_string(path, atr_name, file_path)
        else:
            _attribute.NodeAttribute.set_as_string(path, atr_name, file_path)

    @classmethod
    def load_plugins(cls):
        for i in cls.PLUGIN_NAMES:
            cmds.loadPlugin(i, quiet=1)

    @classmethod
    def search_all_from(cls, directory_paths, ignore_exists=False):
        cls.load_plugins()

        search_opt = bsc_storage.StgFileSearchOpt(
            ignore_name_case=True, ignore_ext_case=True
        )
        search_opt.set_search_directories(
            directory_paths, recursion_enable=True
        )
        paths = cmds.ls(type=cls.QUERY.keys(), long=1)
        for i_path in paths:
            i_node_type = _node.Node.get_type(i_path)
            i_atr_names = cls.QUERY[i_node_type]
            for j_atr_name in i_atr_names:
                j_file_path = cls.get_file(i_path, j_atr_name)
                if ignore_exists is True:
                    if bsc_storage.StgFileTiles.get_is_exists(j_file_path) is True:
                        continue

                j_file_path_new = search_opt.get_result(j_file_path)
                cls.set_file_path(i_path, j_atr_name, j_file_path_new)
