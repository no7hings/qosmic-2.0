# coding:utf-8
import os

import lxbasic.core as bsc_core

import lxbasic.dcc.objects as bsc_dcc_objects

import lxbasic.fnc.abstracts as bsc_fnc_abstracts

import lxbasic.fnc.objects as bsc_fnc_objects
# maya
from ... import core as mya_core
# maya dcc
from ...dcc import objects as mya_dcc_objects

from ...dcc import xgn_objects as mya_dcc_xgn_objects
# maya fnc
from . import geometry_exporter as mya_fnc_obj_geometry_exporter


class XgenExporter(bsc_fnc_abstracts.AbsFncOptionBase):
    OPTION = dict(
        xgen_project_directory='',
        xgen_collection_directory='',
        #
        grow_mesh_directory='',
        #
        location='',
        #
        with_grow_mesh_abc=True,
        with_xgen_collection=True,
    )

    def __init__(self, option=None):
        super(XgenExporter, self).__init__(option)

    @classmethod
    def _set_grow_mesh_abc_export_(cls, directory_path, location):
        mya_location = bsc_core.PthNodeOpt(location).translate_to('|').to_string()
        group = mya_dcc_objects.Group(mya_location)
        xgen_collection_obj_paths = group.get_all_shape_paths(include_obj_type=[mya_core.MyaNodeTypes.XgenPalette])
        for i_xgen_collection_obj_path in xgen_collection_obj_paths:
            i_xgen_palette = mya_dcc_objects.XgenPalette(
                i_xgen_collection_obj_path
            )
            i_xgen_collection_name = i_xgen_palette.name
            i_xgen_palette_opt = mya_dcc_xgn_objects.Palette(i_xgen_collection_name)
            i_xgen_collection_file_name = i_xgen_palette_opt.get_file_name()
            #
            i_grow_meshes = i_xgen_palette_opt.get_grow_meshes()
            if i_grow_meshes:
                i_abc_file_path = '{}/{}.abc'.format(directory_path, os.path.splitext(i_xgen_collection_file_name)[0])
                # i_location = i_grow_meshes[0].transform.path
                mya_fnc_obj_geometry_exporter.FncExporterForGeometryAbc(
                    file_path=i_abc_file_path,
                    root=[i.transform.path for i in i_grow_meshes],
                    attribute_prefix=['xgen'],
                    option={}
                ).set_run()

    @classmethod
    def _set_xgen_collection_export_(cls, xgen_project_directory_path_tgt, xgen_collection_directory_path_tgt, location):
        mya_location = bsc_core.PthNodeOpt(location).translate_to('|').to_string()
        group = mya_dcc_objects.Group(mya_location)
        xgen_collection_obj_paths = group.get_all_shape_paths(include_obj_type=[mya_core.MyaNodeTypes.XgenPalette])
        for i_xgen_collection_obj_path in xgen_collection_obj_paths:
            i_xgen_palette = mya_dcc_objects.XgenPalette(
                i_xgen_collection_obj_path
            )
            i_xgen_collection_name = i_xgen_palette.name
            i_xgen_palette_opt = mya_dcc_xgn_objects.Palette(i_xgen_collection_name)
            i_xgen_collection_data_directory_path_src = i_xgen_palette_opt.get_data_directory()
            # copy xgen-data
            i_xgen_collection_directory_path_tgt = '{}/{}'.format(
                xgen_collection_directory_path_tgt, i_xgen_collection_name
                )
            bsc_dcc_objects.StgDirectory(i_xgen_collection_data_directory_path_src).copy_to_directory(
                i_xgen_collection_directory_path_tgt
            )
            i_xgen_collection_file_path = i_xgen_palette_opt.get_file_path()
            bsc_fnc_objects.FncExporterForDotXgen(
                option=dict(
                    xgen_collection_file=i_xgen_collection_file_path,
                    xgen_project_directory=xgen_project_directory_path_tgt,
                    xgen_collection_directory=xgen_collection_directory_path_tgt,
                    xgen_collection_name=i_xgen_collection_name,
                )
            ).set_run()

    def set_run(self):
        option_opt = self.get_option()
        xgen_project_directory_path_tgt = option_opt.get('xgen_project_directory')
        xgen_collection_directory_path_tgt = option_opt.get('xgen_collection_directory')
        #
        grow_mesh_directory_path = option_opt.get('grow_mesh_directory')
        location = option_opt.get('location')
        # #
        with_grow_mesh_abc = option_opt.get('with_grow_mesh_abc')
        if with_grow_mesh_abc is True:
            self._set_grow_mesh_abc_export_(grow_mesh_directory_path, location)
        #
        with_xgen_collection = option_opt.get('with_xgen_collection')
        if with_xgen_collection is True:
            self._set_xgen_collection_export_(
                xgen_project_directory_path_tgt,
                xgen_collection_directory_path_tgt,
                #
                location
            )


class XgenUsdExporter(bsc_fnc_abstracts.AbsFncOptionBase):
    OPTION = dict(
        file='',
        location='',
        xgen_collection_files=[]
    )

    def __init__(self, option=None):
        super(XgenUsdExporter, self).__init__(option)

    def set_run(self):
        option_opt = self.get_option()
        location = option_opt.get('location')
        location_dag_opt = bsc_core.PthNodeOpt(location)
        mya_location_obj_path = location_dag_opt.translate_to(
            pathsep=mya_core.MyaUtil.OBJ_PATHSEP
        )
        mya_location = mya_location_obj_path.path
        #
        group = mya_dcc_objects.Group(mya_location)
        if group.get_is_exists() is True:
            mya_objs = group.get_descendants()
            print mya_objs
