# coding:utf-8
import os

import glob

import lxbasic.storage as bsc_storage

import lxbasic.dcc.core as bsc_dcc_core

import lxbasic.dcc.objects as bsc_dcc_objects


class AbsFncForDotXgenDef(object):
    @classmethod
    def _find_scene_xgen_collection_file_paths(cls, scene_file_path):
        d = os.path.splitext(scene_file_path)[0]
        glob_pattern = '{}__*.xgen'.format(d)
        return glob.glob(glob_pattern) or []

    @classmethod
    def _find_scene_xgen_collection_names(cls, scene_file_path):
        file_paths = cls._find_scene_xgen_collection_file_paths(scene_file_path)
        return [cls._get_xgen_collection_name(i) for i in file_paths]

    @classmethod
    def _get_xgen_collection_name(cls, xgen_collection_file_path):
        """
        :param xgen_collection_file_path: str()
        :return:
        """
        file_opt = bsc_storage.StgFileOpt(xgen_collection_file_path)
        file_name_base = file_opt.name_base
        return file_name_base.split('__')[-1]

    @classmethod
    def _copy_scene_xgen_collection_files_to(cls, scene_file_path_src, scene_file_path_tgt):
        """
        :param scene_file_path_src: str("scene_file_path")
        :param scene_file_path_tgt:
        :return:
        """
        file_paths_src = cls._find_scene_xgen_collection_file_paths(scene_file_path_src)
        file_opt_tgt = bsc_storage.StgFileOpt(scene_file_path_tgt)
        file_name_base_tgt = file_opt_tgt.name_base
        file_directory_path_tgt = file_opt_tgt.directory_path
        replace_list = []

        for i_file_path_src in file_paths_src:
            i_file_opt_src = bsc_storage.StgFileOpt(i_file_path_src)
            i_file_name_src = i_file_opt_src.name
            i_xgen_collection_name = cls._get_xgen_collection_name(i_file_path_src)
            i_file_name_tgt = '{}__{}.xgen'.format(file_name_base_tgt, i_xgen_collection_name)
            i_xgen_collection_file_path_tgt = '{}/{}'.format(file_directory_path_tgt, i_file_name_tgt)
            bsc_dcc_objects.StgFile(i_file_path_src).copy_to_file(i_xgen_collection_file_path_tgt)
            #
            cls._repair_xgen_collection_file(i_xgen_collection_file_path_tgt)
            #
            replace_list.append(
                (i_file_name_src, i_file_name_tgt)
            )
        #
        if replace_list:
            if os.path.isfile(scene_file_path_tgt):
                with open(scene_file_path_tgt) as f_r:
                    d = f_r.read()
                    for i in replace_list:
                        s, t = i
                        d = d.replace(
                            r'setAttr ".xfn" -type "string" "{}";'.format(s),
                            r'setAttr ".xfn" -type "string" "{}";'.format(t)
                        )
                        d = d.replace(
                            r'"xgFileName" " -type \"string\" \"{}\""'.format(s),
                            r'"xgFileName" " -type \"string\" \"{}\""'.format(t)
                        )
                    with open(scene_file_path_tgt, 'w') as f_w:
                        f_w.write(d)

    @classmethod
    def _repath_xgen_collection_file_to(
        cls,
        xgen_collection_file_path,
        xgen_project_directory_path_tgt, xgen_collection_directory_path_tgt, xgen_collection_name
    ):
        dot_xgen_file_reader = bsc_dcc_core.DotXgenOpt(xgen_collection_file_path)
        dot_xgen_file_reader.repath_project_directory_to(xgen_project_directory_path_tgt)
        dot_xgen_file_reader.repath_collection_directory_to(
            xgen_collection_directory_path_tgt, xgen_collection_name
        )
        #
        dot_xgen_file_reader.set_save()

    @classmethod
    def _repair_xgen_collection_file(cls, xgen_collection_file_path):
        i_dot_xgen_reader = bsc_dcc_core.DotXgenOpt(xgen_collection_file_path)
        i_dot_xgen_reader.set_repair()
        i_dot_xgen_reader.set_save()
