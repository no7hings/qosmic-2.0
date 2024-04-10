# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from .wrap import *


class StageOpt(object):
    KEY = 'clarisse stage'
    PATHSEP = '/'

    class Types(object):
        Group = 'context'

    def __init__(self, pseudo_root='build://project'):
        self.__pseudo_root = pseudo_root

    def __to_crs_path_text(self, path_text):
        if path_text == self.PATHSEP:
            return self.__pseudo_root
        return self.__pseudo_root + path_text

    def get_obj_is_exists(self, path_text):
        return ix.item_exists(
            self.__to_crs_path_text(path_text)
        ) is not None

    def create_group(self, path_text):
        pass

    def create_obj(self, path_text, type_name):
        path_opt = bsc_core.PthNodeOpt(path_text)
        if type_name == self.Types.Group:
            ix.cmds.CreateContext(
                path_opt.get_name(),
                'Global',
                self.__to_crs_path_text(path_opt.get_parent_path())
            )
        else:
            ix.cmds.CreateObject(
                path_opt.get_name(),
                type_name,
                'Global',
                self.__to_crs_path_text(path_opt.get_parent_path())
            )
        bsc_log.Log.trace_method_result(
            self.KEY, 'create node: "{}"'.format(path_text)
        )

    def create_dag(self, path_text):
        path_opt = bsc_core.PthNodeOpt(path_text)
        path_texts = path_opt.get_component_paths()
        path_texts.reverse()
        for i_path_text in path_texts:
            if i_path_text != '/':
                if self.get_obj_is_exists(i_path_text) is False:
                    self.create_obj(i_path_text, self.Types.Group)

    def reference_file_to(self, path_text, file_path_text):
        file_opt = bsc_storage.StgFileOpt(file_path_text)
        if self.get_obj_is_exists(path_text) is False and file_opt.get_is_exists() is True:
            path_opt = bsc_core.PthNodeOpt(path_text)
            parent_path_text = path_opt.get_parent_path()
            self.create_dag(parent_path_text)
            ix.cmds.CreateCustomContext(
                path_opt.get_name(), 'Reference', 'Global', self.__to_crs_path_text(parent_path_text)
            )
            ix.cmds.SetReferenceFilename([ix.get_item(self.__to_crs_path_text(path_text))], file_path_text)

