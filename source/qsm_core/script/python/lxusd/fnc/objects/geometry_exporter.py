# coding:utf-8
import six

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.fnc.abstracts as bsc_fnc_abstracts
# usd
from ...core.wrap import *

from ... import core as usd_core
# usd dcc
from ...dcc import operators as usd_dcc_operators


class GeometryUvMapExporter(bsc_fnc_abstracts.AbsFncOptionBase):
    OPTION = dict(
        file_0=None,
        file_1=None,
        #
        display_color=(0.25, 0.75, 0.5),
        #
        path_lstrip=None,
    )

    def __init__(self, file_path, root=None, option=None):
        self._file_path = file_path
        self._root = root
        #
        super(GeometryUvMapExporter, self).__init__(option)
        #
        self._geometry_stage_0 = Usd.Stage.CreateInMemory()
        self._geometry_stage_opt_0 = usd_core.UsdStageOpt(self._geometry_stage_0)
        self._geometry_stage_1 = Usd.Stage.CreateInMemory()
        self._geometry_stage_opt_1 = usd_core.UsdStageOpt(self._geometry_stage_1)
        #
        self._output_stage = Usd.Stage.CreateInMemory()
        self._output_stage_opt = usd_core.UsdStageOpt(self._output_stage)
        #
        self._file_path_0 = self.get('file_0')
        if self._file_path_0 is not None:
            self._geometry_stage_opt_0.append_sublayer(self._file_path_0)
            self._geometry_stage_0.Flatten()
        #
        self._file_path_1 = self.get('file_1')
        if self._file_path_1 is not None:
            self._geometry_stage_opt_1.append_sublayer(self._file_path_1)
            self._geometry_stage_1.Flatten()

    def set_uv_map_export(self):
        display_color = self.get('display_color')
        with bsc_log.LogProcessContext.create_as_bar(
                maximum=len([i for i in self._geometry_stage_0.TraverseAll()]), label='geometry look export'
                ) as l_p:
            for i_usd_prim in self._geometry_stage_0.TraverseAll():
                l_p.do_update()
                i_obj_type_name = i_usd_prim.GetTypeName()
                obj_path = i_usd_prim.GetPath().pathString
                output_prim = self._output_stage_opt.set_obj_create_as_override(obj_path)
                if i_obj_type_name == 'Mesh':
                    _ = self._geometry_stage_1.GetPrimAtPath(obj_path)
                    i_output_usd_mesh = UsdGeom.Mesh(output_prim)
                    i_output_usd_mesh_opt = usd_core.UsdMeshOpt(i_output_usd_mesh)
                    if _.IsValid() is True:
                        surface_geometry_prim = _
                        input_usd_mesh = UsdGeom.Mesh(surface_geometry_prim)
                        output_prim.CreateAttribute(
                            'userProperties:usd:logs:uv_map_from', Sdf.ValueTypeNames.Asset, custom=False
                        ).Set(self._file_path_1)
                    else:
                        input_usd_mesh = UsdGeom.Mesh(i_usd_prim)
                        output_prim.CreateAttribute(
                            'userProperties:usd:logs:uv_map_from', Sdf.ValueTypeNames.Asset, custom=False
                        ).Set(self._file_path_0)
                    #
                    input_usd_mesh_opt = usd_core.UsdMeshOpt(input_usd_mesh)
                    uv_map_names = input_usd_mesh_opt.get_uv_map_names()
                    if uv_map_names:
                        for uv_map_name in uv_map_names:
                            uv_map = input_usd_mesh_opt.get_uv_map(uv_map_name)
                            i_output_usd_mesh_opt.create_uv_map(uv_map_name, uv_map)
                    #
                    input_usd_mesh_opt.fill_display_color(
                        display_color
                    )
                    i_output_usd_mesh_opt.set_display_colors(
                        input_usd_mesh_opt.get_display_colors()
                    )
        #
        self._output_stage_opt.set_default_prim(self._root)
        # create directory
        # bsc_storage.StgFileOpt(self._file_path).create_directory()
        #
        self._output_stage_opt.export_to(self._file_path)
        #
        bsc_log.Log.trace_method_result(
            'fnc-geometry-usd-uv-map-export',
            u'file="{}"'.format(self._file_path)
        )

    def set_run(self):
        self.set_uv_map_export()


class GeometryLookPropertyExporter(bsc_fnc_abstracts.AbsFncOptionBase):
    OPTION = dict(
        file='',
        location='',
        #
        stage_src=None,
        file_src='',
        #
        asset_name='',
        #
        color_seed=0,
        #
        with_uv_map=False,
        #
        with_object_color=False,
        with_group_color=False,
        with_asset_color=False,
        with_shell_color=False,
        #
        with_display_color=False,
        display_color=(0.25, 0.75, 0.5)
    )

    def __init__(self, *args, **kwargs):
        super(GeometryLookPropertyExporter, self).__init__(*args, **kwargs)
        #
        self._file_path = self.get('file')
        #
        file_path_src = self.get('file_src')
        stage_src = self.get('stage_src')
        #
        self._location_path = self.get('location')
        #
        self._asset_name = self.get('asset_name')
        #
        self._color_seed = self.get('color_seed')

        self._color_scheme = self.get('color_scheme')
        #
        if stage_src is not None:
            self._usd_stage_src = stage_src
        else:
            self._usd_stage_src = Usd.Stage.Open(file_path_src, Usd.Stage.LoadAll)
        #
        self._usd_stage_opt_src = usd_core.UsdStageOpt(self._usd_stage_src)
        #
        self._usd_stage_tgt = Usd.Stage.CreateInMemory()
        self._usd_stage_opt_tgt = usd_core.UsdStageOpt(self._usd_stage_tgt)

    def set_run(self):
        count = len([i for i in self._usd_stage_src.TraverseAll()])
        with bsc_log.LogProcessContext.create_as_bar(
            maximum=count,
            label='geometry look property create'
        ) as l_p:
            display_color = self.get('display_color')
            asset_color = bsc_core.RawTextOpt(self._asset_name).to_rgb_(maximum=1, seed=self._color_seed)
            for i_usd_prim_src in self._usd_stage_src.TraverseAll():
                l_p.do_update()
                #
                i_obj_type_name = i_usd_prim_src.GetTypeName()
                i_obj_path = i_usd_prim_src.GetPath().pathString
                i_obj_path_opt = bsc_core.PthNodeOpt(i_obj_path)
                #
                i_usd_prim_tgt = self._usd_stage_tgt.OverridePrim(i_obj_path)
                if i_obj_type_name in [usd_core.UsdNodeTypes.Mesh, usd_core.UsdNodeTypes.NurbsCurves]:
                    i_usd_geometry_opt_tgt = usd_core.UsdGeometryOpt(i_usd_prim_tgt)
                    #
                    if self.get('with_object_color') is True:
                        i_object_color = i_obj_path_opt.get_color_from_name(maximum=1.0, seed=self._color_seed)
                        i_usd_geometry_opt_tgt.create_customize_port_(
                            'object_color', 'color/color3', i_object_color
                        )
                    if self.get('with_group_color') is True:
                        i_group_path_opt = i_obj_path_opt.get_parent().get_parent()
                        i_group_color = i_group_path_opt.get_color_from_name(maximum=1.0, seed=self._color_seed)
                        i_usd_geometry_opt_tgt.create_customize_port_(
                            'group_color', 'color/color3', i_group_color
                        )
                    if self.get('with_asset_color') is True:
                        i_usd_geometry_opt_tgt.create_customize_port_(
                            'asset_color', 'color/color3', asset_color
                        )
                    #
                    if i_obj_type_name == usd_core.UsdNodeTypes.Mesh:
                        i_usd_mesh_src = UsdGeom.Mesh(i_usd_prim_src)
                        i_usd_mesh_opt_src = usd_core.UsdMeshOpt(i_usd_mesh_src)
                        #
                        i_usd_mesh_tgt = UsdGeom.Mesh(i_usd_prim_tgt)
                        i_usd_mesh_opt_tgt = usd_core.UsdMeshOpt(i_usd_mesh_tgt)
                        if self.get('with_uv_map') is True:
                            i_uv_map_names = i_usd_mesh_opt_src.get_uv_map_names()
                            if i_uv_map_names:
                                for j_uv_map_name in i_uv_map_names:
                                    uv_map = i_usd_mesh_opt_src.get_uv_map(j_uv_map_name)
                                    i_usd_mesh_opt_tgt.create_uv_map(j_uv_map_name, uv_map)
                        #
                        if self.get('with_shell_color') is True:
                            i_offset = bsc_core.RawTextOpt(i_obj_path_opt.name).get_index()
                            colors = i_usd_mesh_opt_src.get_colors_fom_shell(
                                offset=i_offset, seed=self._color_seed
                            )
                            i_usd_geometry_opt_tgt.create_customize_port_as_face_color(
                                'shell_color', 'array/color3', colors
                            )
                        #
                        if self.get('with_display_color') is True:
                            i_usd_mesh_opt_tgt.fill_display_color(display_color)
        #
        component_paths = bsc_core.PthNodeOpt(self._location_path).get_component_paths()
        if component_paths:
            component_paths.reverse()
            self._usd_stage_opt_tgt.set_default_prim(
                component_paths[1]
            )

        self._usd_stage_opt_tgt.export_to(self._file_path)


class GeometryDisplayColorExporter(bsc_fnc_abstracts.AbsFncOptionBase):
    OPTION = dict(
        file='',
        location='',
        #
        stage_src=None,
        file_src='',
        #
        asset_name='',
        #
        color_seed=0,
        # "object_color", "group_color", "asset_color", "uv_map_color", "shell_color", "enable_color"
        color_scheme='asset_color'
    )

    def __init__(self, *args, **kwargs):
        super(GeometryDisplayColorExporter, self).__init__(*args, **kwargs)
        #
        self._file_path = self.get('file')
        #
        file_path_src = self.get('file_src')
        stage_src = self.get('stage_src')
        #
        self._location_path = self.get('location')
        #
        self._asset_name = self.get('asset_name')
        #
        self._color_seed = self.get('color_seed')

        self._color_scheme = self.get('color_scheme')
        #
        if stage_src is not None:
            self._usd_stage_src = stage_src
        else:
            self._usd_stage_src = Usd.Stage.Open(file_path_src, Usd.Stage.LoadAll)
        #
        self._usd_stage_opt_src = usd_core.UsdStageOpt(self._usd_stage_src)
        #
        self._usd_stage_tgt = Usd.Stage.CreateInMemory()
        self._usd_stage_opt_tgt = usd_core.UsdStageOpt(self._usd_stage_tgt)

    def set_run(self):
        count = len([i for i in self._usd_stage_src.TraverseAll()])
        color_scheme = self.get('color_scheme')
        with bsc_log.LogProcessContext.create_as_bar(
                maximum=count,
                label='geometry display-color create'
        ) as l_p:
            asset_color = bsc_core.RawTextOpt(self._asset_name).to_rgb_(maximum=1, seed=self._color_seed)
            for i_index, i_usd_prim_src in enumerate(self._usd_stage_src.TraverseAll()):
                i_obj_type_name = i_usd_prim_src.GetTypeName()
                i_obj_path = i_usd_prim_src.GetPath().pathString
                i_obj_path_opt = bsc_core.PthNodeOpt(i_obj_path)
                #
                i_usd_prim_src = self._usd_stage_src.GetPrimAtPath(i_obj_path)
                i_usd_prim_tgt = self._usd_stage_tgt.OverridePrim(i_obj_path)
                if i_obj_type_name in [usd_core.UsdNodeTypes.Mesh, usd_core.UsdNodeTypes.NurbsCurves]:
                    #
                    i_usd_mesh_src = UsdGeom.Mesh(i_usd_prim_src)
                    i_usd_mesh_opt_src = usd_core.UsdMeshOpt(i_usd_mesh_src)
                    # all use mesh? but it is run completed
                    i_usd_mesh_tgt = UsdGeom.Mesh(i_usd_prim_tgt)
                    i_usd_mesh_opt_tgt = usd_core.UsdMeshOpt(i_usd_mesh_tgt)
                    #
                    if isinstance(color_scheme, six.string_types):
                        if color_scheme == 'object_color':
                            i_object_color = i_obj_path_opt.get_color_from_name(
                                maximum=1.0, seed=self._color_seed
                            )
                            i_usd_mesh_opt_tgt.fill_display_color(i_object_color)
                        elif color_scheme == 'group_color':
                            i_group_path_opt = i_obj_path_opt.get_parent().get_parent()
                            i_group_color = i_group_path_opt.get_color_from_name(
                                maximum=1.0, seed=self._color_seed
                            )
                            i_usd_mesh_opt_tgt.fill_display_color(i_group_color)
                        elif color_scheme == 'asset_color':
                            i_usd_mesh_opt_tgt.fill_display_color(asset_color)
                        # for mesh
                        if i_obj_type_name == usd_core.UsdNodeTypes.Mesh:
                            if color_scheme == 'uv_map_color':
                                i_color_map = i_usd_mesh_opt_src.compute_vertex_color_map_from_uv_coord('st')
                                i_usd_mesh_opt_tgt.set_display_colors_as_vertex(i_color_map)
                            elif color_scheme == 'shell_color':
                                i_colors = i_usd_mesh_opt_src.get_colors_fom_shell(
                                    offset=i_index, seed=self._color_seed
                                )
                                i_usd_mesh_opt_tgt.set_display_colors_as_uniform(i_colors)
                    elif isinstance(color_scheme, dict):
                        pass
                #
                l_p.do_update()
        #
        component_paths = bsc_core.PthNodeOpt(self._location_path).get_component_paths()
        if component_paths:
            component_paths.reverse()
            self._usd_stage_opt_tgt.set_default_prim(
                component_paths[1]
            )

        self._usd_stage_opt_tgt.export_to(self._file_path)


class GeometryDebugger(bsc_fnc_abstracts.AbsFncOptionBase):
    OPTION = dict(
        input_file='',
        output_file='',
        location=''
    )

    def __init__(self, option):
        super(GeometryDebugger, self).__init__(option)

    def set_face_vertex_indices_reverse_create(self):
        input_file_path = self.get('input_file')
        output_file_path = self.get('output_file')
        #
        self._input_stage_opt = usd_core.UsdStageOpt(input_file_path)

        self._output_stage_opt = usd_core.UsdStageOpt()

        with bsc_log.LogProcessContext.create_as_bar(
            maximum=self._input_stage_opt.get_count(), label='face vertex indices reverse create'
        ) as l_p:
            for i_input_prim in self._input_stage_opt.usd_instance.TraverseAll():
                l_p.do_update()
                #
                i_obj_type_name = i_input_prim.GetTypeName()
                if i_obj_type_name == 'Mesh':
                    i_input_mesh = UsdGeom.Mesh(i_input_prim)
                    i_input_mesh_opt = usd_core.UsdMeshOpt(i_input_mesh)
                    print i_input_mesh_opt.get_face_vertex_indices()


class FncGeometryExporter(bsc_fnc_abstracts.AbsFncOptionBase):
    OPTION = dict(
        file='',
        location='',
        #
        default_prim_path=None,
        with_usda=False,
        #
        path_lstrip=None,
    )

    def __init__(self, *args, **kwargs):
        super(FncGeometryExporter, self).__init__(*args, **kwargs)
        #
        self._file_path = self.get('file')
        self._location_path = self.get('location')
        #
        self._output_stage = Usd.Stage.CreateInMemory()
        self._output_stage_opt = usd_core.UsdStageOpt(self._output_stage)
        #
        self._create_location_fnc_(self._output_stage, self._location_path)

    @classmethod
    def _create_location_fnc_(cls, stage, location):
        dag_path_comps = bsc_core.PthNodeMtd.get_dag_component_paths(location, pathsep=usd_core.UsdNodes.PATHSEP)
        if dag_path_comps:
            dag_path_comps.reverse()
        #
        stage.GetPseudoRoot()
        for i in dag_path_comps:
            if i != usd_core.UsdNodes.PATHSEP:
                stage.DefinePrim(
                    i, usd_core.UsdNodeTypes.Xform
                )
        #
        default_prim_path = stage.GetPrimAtPath(dag_path_comps[1])
        stage.SetDefaultPrim(default_prim_path)

    def create_transform_opt(self, obj_path, use_override=False):
        if use_override is True:
            prim = self._output_stage.OverridePrim(obj_path, usd_core.UsdNodeTypes.Xform)
        else:
            prim = self._output_stage.DefinePrim(obj_path, usd_core.UsdNodeTypes.Xform)
        obj_opt = usd_dcc_operators.TransformOpt(prim)
        return obj_opt

    def create_mesh_opt(self, obj_path, use_override=False):
        if use_override is True:
            prim = self._output_stage.OverridePrim(obj_path, usd_core.UsdNodeTypes.Mesh)
        else:
            prim = self._output_stage.DefinePrim(obj_path, usd_core.UsdNodeTypes.Mesh)
        #
        obj_opt = usd_dcc_operators.MeshOpt(prim)
        return obj_opt

    def create_nurbs_curve_opt(self, obj_path, use_override=False):
        if use_override is True:
            prim = self._output_stage.OverridePrim(obj_path, usd_core.UsdNodeTypes.NurbsCurves)
        else:
            prim = self._output_stage.DefinePrim(obj_path, usd_core.UsdNodeTypes.NurbsCurves)
        #
        obj_opt = usd_dcc_operators.NurbsCurveOpt(prim)
        return obj_opt

    def create_basis_curves_opt(self, obj_path, use_override=False):
        if use_override is True:
            prim = self._output_stage.OverridePrim(obj_path, usd_core.UsdNodeTypes.BasisCurves)
        else:
            prim = self._output_stage.DefinePrim(obj_path, usd_core.UsdNodeTypes.BasisCurves)
        #
        obj_opt = usd_dcc_operators.BasisCurveOpt(prim)
        return obj_opt

    def _get_geometry_fnc_(self, obj_path):
        prim = self._output_stage.GetPrimAtPath(obj_path)
        if prim.IsValid() is True:
            return UsdGeom.Xform(prim)

    def _set_export_run_(self):
        default_prim_path = self.get('default_prim_path')
        if default_prim_path is not None:
            self._output_stage_opt.set_default_prim(
                default_prim_path
            )
        #
        self._output_stage_opt.export_to(self._file_path)

    def execute(self):
        self._set_export_run_()
