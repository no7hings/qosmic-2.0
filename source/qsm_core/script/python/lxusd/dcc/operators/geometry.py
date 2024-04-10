# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.dcc.abstracts as bsc_dcc_abstracts
# usd
from ...core.wrap import *

from ... import core as usd_core


class AbsUsdOptDef(object):
    def __init__(self, *args, **kwargs):
        self._usd_prim = args[0]

    @property
    def prim(self):
        return self._usd_prim

    def get_stage(self):
        return self.prim.GetStage()

    stage = property(get_stage)

    def get_path(self):
        return self._usd_prim.GetPath().pathString

    path = property(get_path)


class TransformOpt(AbsUsdOptDef):
    def __init__(self, *args, **kwargs):
        super(TransformOpt, self).__init__(*args, **kwargs)

    @property
    def xform(self):
        return UsdGeom.Xform(self.prim)

    def set_matrix(self, matrix):
        xform = self.xform
        op = xform.MakeMatrixXform()
        op.Set(usd_core.UsdBase.to_usd_matrix(matrix))

    def get_matrix(self):
        xform = self.xform
        op = xform.MakeMatrixXform()
        usd_matrix = op.Get()
        if usd_matrix is None:
            usd_matrix = Gf.Matrix4d()
        return usd_core.UsdBase.to_matrix(usd_matrix)

    def set_visible(self, boolean):
        usd_core.UsdTransformOpt(
            self.prim
        ).set_visible(
            boolean
        )

    def set_customize_attribute_add(self, key, value):
        usd_core.UsdPrimOpt._add_customize_attribute_(
            self.xform, key, value
        )


class MeshOpt(
    AbsUsdOptDef,
    bsc_dcc_abstracts.AbsMeshOptDef
):
    def __init__(self, *args, **kwargs):
        super(MeshOpt, self).__init__(*args, **kwargs)
        self._init_mesh_opt_def_()

    def get_usd_mesh(self):
        return UsdGeom.Mesh(self.prim)

    @property
    def usd_mesh(self):
        return self.get_usd_mesh()

    @property
    def mesh(self):
        return self.get_usd_mesh()

    def set_create(self, face_vertices, points, uv_maps=None, normal_maps=None, color_maps=None, geometry_subsets=None):
        # prim = self.prim
        # mesh = self.usd_mesh
        face_vertex_counts, face_vertex_indices = face_vertices
        self._set_face_vertex_counts_(face_vertex_counts)
        self._set_face_vertex_indices_(face_vertex_indices)
        self.set_points(points)
        if uv_maps:
            self.assign_uv_maps(uv_maps)
        if geometry_subsets is not None:
            self.create_subsets(geometry_subsets)

    def _set_face_vertex_counts_(self, raw):
        if raw:
            usd_mesh = self.usd_mesh
            if usd_mesh.GetPrim().HasAttribute('faceVertexCounts') is False:
                face_vertex_counts_attr = usd_mesh.CreateFaceVertexCountsAttr()
            else:
                face_vertex_counts_attr = usd_mesh.GetFaceVertexCountsAttr()
            face_vertex_counts_attr.Set(raw)

    def _set_face_vertex_indices_(self, raw):
        if raw:
            usd_mesh = self.usd_mesh
            if usd_mesh.GetPrim().HasAttribute("faceVertexIndices") is False:
                face_vertex_counts_attr = usd_mesh.CreateFaceVertexIndicesAttr()
            else:
                face_vertex_counts_attr = usd_mesh.GetFaceVertexIndicesAttr()
            face_vertex_counts_attr.Set(raw)

    def get_face_vertex_counts(self):
        usd_mesh = self.usd_mesh
        a = usd_mesh.GetFaceVertexCountsAttr()
        if a.GetNumTimeSamples():
            v = a.Get(0)
        else:
            v = a.Get()
        if v:
            return usd_core.UsdBase.to_integer_array(v)
        return []

    def get_face_vertex_indices(self):
        usd_mesh = self.usd_mesh
        a = usd_mesh.GetFaceVertexIndicesAttr()
        if a.GetNumTimeSamples():
            v = a.Get(0)
        else:
            v = a.Get()
        if v:
            return usd_core.UsdBase.to_integer_array(v)
        return []

    @classmethod
    def _get_face_vertex_reverse_(cls, face_vertex_counts, face_vertex_indices):
        lis = []
        index_cur = 0
        for i_count in face_vertex_counts:
            i_indices = face_vertex_indices[index_cur:index_cur+i_count]
            i_indices.reverse()
            lis.extend(i_indices)
            index_cur += i_count
        return lis

    def get_face_vertices(self):
        return self.get_face_vertex_counts(), self.get_face_vertex_indices()

    def get_points(self):
        usd_mesh = self.usd_mesh
        p = usd_mesh.GetPointsAttr()
        if p.GetNumTimeSamples():
            v = p.Get(0)
        else:
            v = p.Get()
        if v:
            return usd_core.UsdBase.to_point_array(v)
        return []

    def set_points(self, points):
        usd_mesh = self.usd_mesh
        return usd_mesh.GetPointsAttr().Set(points)

    def get_uv_map_names(self):
        list_ = []
        usd_mesh = self.usd_mesh
        usd_primvars = usd_mesh.GetAuthoredPrimvars()
        for i_p in usd_primvars:
            i_name = i_p.GetPrimvarName()
            i_a = self._usd_prim.GetAttribute('primvars:{}'.format(i_name))
            if i_a.GetNumTimeSamples():
                i_v = i_p.GetIndices(0)
            else:
                i_v = i_p.GetIndices()
            if i_v:
                list_.append(i_name)
        return list_

    def get_uv_map_coords(self, uv_map_name):
        usd_mesh = self.usd_mesh
        p = usd_mesh.GetPrimvar(uv_map_name)
        a = self._usd_prim.GetAttribute('primvars:{}'.format(uv_map_name))
        if a.GetNumTimeSamples():
            return p.Get(0)
        return p.Get()

    def get_uv_map(self, uv_map_name):
        usd_mesh = self.usd_mesh
        p = usd_mesh.GetPrimvar(uv_map_name)
        a = self._usd_prim.GetAttribute('primvars:{}'.format(uv_map_name))
        uv_face_vertex_counts = self.get_face_vertex_counts()
        if a.GetNumTimeSamples():
            uv_face_vertex_indices = p.GetIndices(0)
            uv_map_coords = p.Get(0)
        else:
            uv_face_vertex_indices = p.GetIndices()
            uv_map_coords = p.Get()
        return uv_face_vertex_counts, usd_core.UsdBase.to_integer_array(uv_face_vertex_indices), uv_map_coords

    def get_uv_maps(self, default_uv_map_name='st'):
        dic = {}
        uv_map_names = self.get_uv_map_names()
        for i_uv_map_name in uv_map_names:
            uv_map = self.get_uv_map(i_uv_map_name)
            dic[i_uv_map_name] = uv_map
        return dic

    def assign_uv_maps(self, raw):
        if raw:
            usd_mesh = self.usd_mesh
            for i_uv_map_name, v in raw.items():
                if i_uv_map_name == 'map1':
                    i_uv_map_name = 'st'
                #
                i_uv_map_name_new = bsc_core.RawTextMtd.clear_up_to(
                    i_uv_map_name
                )
                if i_uv_map_name != i_uv_map_name_new:
                    bsc_log.Log.trace_method_warning(
                        'usd uv-map set',
                        u'uv-map="{1}" in "{0}" is not available, auto convert to "{2}"'.format(
                            self.path,
                            i_uv_map_name,
                            i_uv_map_name_new
                        )
                    )
                    i_uv_map_name = i_uv_map_name_new
                #
                i_uv_map_face_vertex_counts, i_uv_map_face_vertex_indices, i_uv_map_coords = v
                if usd_mesh.HasPrimvar(i_uv_map_name) is False:
                    i_primvar = usd_mesh.CreatePrimvar(
                        i_uv_map_name,
                        Sdf.ValueTypeNames.TexCoord2fArray,
                        UsdGeom.Tokens.faceVarying
                    )
                else:
                    i_primvar = usd_mesh.GetPrimvar(
                        i_uv_map_name
                    )
                #
                i_primvar.Set(i_uv_map_coords)
                i_primvar.SetIndices(Vt.IntArray(i_uv_map_face_vertex_indices))

    def get_face_vertices_as_uuid(self):
        raw = self.get_face_vertices()
        return bsc_core.HashMtd.get_hash_value(raw, as_unique_id=True)

    def get_uv_map_face_vertices_as_uuid(self, uv_map_name='st'):
        uv_face_vertex_counts, uv_face_vertex_indices, uv_map_coords = self.get_uv_map(uv_map_name)
        raw = (uv_face_vertex_counts, uv_face_vertex_indices)
        return bsc_core.HashMtd.get_hash_value(raw, as_unique_id=True)

    def get_points_as_uuid(self, ordered=False, round_count=4):
        raw = self.get_points()
        if ordered is True:
            raw.sort()
        #
        raw = bsc_core.RawPointArrayOpt(raw).round_to(round_count)
        return bsc_core.HashMtd.get_hash_value(raw, as_unique_id=True)

    def get_uv_maps_as_uuid(self, uv_map_name='st'):
        raw = self.get_uv_maps(uv_map_name)
        return bsc_core.HashMtd.get_hash_value(raw, as_unique_id=True)

    def get_vertex_count(self):
        _ = self.get_face_vertex_indices()
        return max(_)+1

    def get_face_count(self):
        usd_mesh = self.usd_mesh
        return usd_mesh.GetFaceCount()

    def set_visible(self, boolean):
        usd_core.UsdGeometryOpt(
            self.prim
        ).set_visible(
            boolean
        )

    def fill_display_color(self, color):
        usd_core.UsdGeometryMeshOpt(
            self.prim
        ).fill_display_color(
            color
        )

    def set_customize_attribute_add(self, key, value):
        usd_core.UsdPrimOpt._add_customize_attribute_(
            self.mesh, key, value
        )

    def create_subsets(self, geometry_subsets):
        state = self.get_stage()
        for k, v in geometry_subsets.items():
            i_path = '{}/{}'.format(self.get_path(), k)
            i_prim = state.DefinePrim(i_path, usd_core.UsdNodeTypes.GeometrySubset)
            i_fnc = UsdGeom.Subset(i_prim)
            i_element_type_atr = i_fnc.CreateElementTypeAttr()
            i_element_type_atr.Set(UsdGeom.Tokens.face)
            i_indices_atr = i_fnc.CreateIndicesAttr()
            i_indices_atr.Set(v)
            i_family_name_atr = i_fnc.GetFamilyNameAttr()
            i_family_name_atr.Set(UsdShade.Tokens.materialBind)

    def assign_materials(self, material_assigns, location='/looks'):
        for key, value in material_assigns.items():
            if key == 'all':
                self.assign_material_to_path(value, location)

    def assign_material_to_path(self, path, location='/looks'):
        r = self._usd_prim.CreateRelationship('material:binding')
        if path.startswith('/'):
            path_ = location+path
        else:
            path_ = '{}/{}'.format(location, path)
        r.BlockTargets()
        r.AddTarget(path_)


class NurbsCurveOpt(
    AbsUsdOptDef,
    bsc_dcc_abstracts.AbsCurveOptDef
):
    def __init__(self, *args, **kwargs):
        super(NurbsCurveOpt, self).__init__(*args, **kwargs)
        self._init_curve_opt_def_()

    def get_usd_fnc(self):
        return UsdGeom.NurbsCurves(self.prim)

    @property
    def usd_fnc(self):
        return self.get_usd_fnc()

    def set_create(self, points, knots, ranges, widths, order):
        self.set_points(points)
        self.set_knots(knots)
        self.set_ranges(ranges)
        self.set_widths(widths)
        self.set_order(order)

    def set_points(self, values):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetPointsAttr()
        if p is None:
            p = usd_fnc.CreatePointsAttr()
        #
        p.Set(values)
        p = usd_fnc.GetCurveVertexCountsAttr()
        if p is None:
            p = usd_fnc.CreateCurveVertexCountsAttr()
        p.Set([len(values)])

    def get_points(self):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetPointsAttr()
        if p.GetNumTimeSamples():
            v = p.Get(0)
        else:
            v = p.Get()
        if v:
            return usd_core.UsdBase.to_point_array(v)
        return []

    def get_point_count(self):
        return len(self.get_points())

    def set_knots(self, values):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetKnotsAttr()
        if p is None:
            p = usd_fnc.CreateKnotsAttr()
        p.Set(values)

    def set_ranges(self, values):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetRangesAttr()
        if p is None:
            p = usd_fnc.CreateRangesAttr()
        p.Set(values)

    def set_widths(self, values):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetWidthsAttr()
        if p is None:
            p = usd_fnc.CreateWidthsAttr()
        p.Set(values)

    def set_extent(self, extent):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetPrim().HasAttribute('extent')
        if p is None:
            p = usd_fnc.CreateExtentAttr()
        p.Set(extent)

    def set_order(self, order):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetOrderAttr()
        if p is None:
            p = usd_fnc.CreateOrderAttr()
        p.Set(order)

    def fill_display_color(self, color):
        usd_core.UsdGeometryMeshOpt(
            self.prim
        ).fill_display_color(
            color
        )


class BasisCurveOpt(
    AbsUsdOptDef,
    bsc_dcc_abstracts.AbsCurveOptDef
):
    def __init__(self, *args, **kwargs):
        super(BasisCurveOpt, self).__init__(*args, **kwargs)
        self._init_curve_opt_def_()

    def get_usd_fnc(self):
        return UsdGeom.BasisCurves(self.prim)

    @property
    def usd_fnc(self):
        return self.get_usd_fnc()

    def set_create(self, counts, points, widths):
        self.set_curve_basis(
            UsdGeom.Tokens.catmullRom
        )
        self.set_curve_type(
            UsdGeom.Tokens.cubic
        )
        self.set_curve_vertex_counts(counts)
        self.set_points(points)
        self.set_widths(widths)

    def set_curve_type(self, value):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetTypeAttr()
        if p is not None:
            p = usd_fnc.CreateTypeAttr()

        p.Set(value)

    def set_curve_basis(self, value):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetBasisAttr()
        if p is not None:
            p = usd_fnc.CreateBasisAttr()

        p.Set(value)

    def set_curve_vertex_counts(self, values):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetCurveVertexCountsAttr()
        if p is None:
            p = usd_fnc.CreateCurveVertexCountsAttr()
        p.Set(values)

    def set_points(self, values):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetPointsAttr()
        if p is None:
            p = usd_fnc.CreatePointsAttr()
        p.Set(values)

    def get_points(self):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetPointsAttr()
        if p.GetNumTimeSamples():
            v = p.Get(0)
        else:
            v = p.Get()
        if v:
            return usd_core.UsdBase.to_point_array(v)
        return []

    def set_widths(self, values):
        usd_fnc = self.get_usd_fnc()
        p = usd_fnc.GetWidthsAttr()
        if p is None:
            p = usd_fnc.CreateWidthsAttr()
        p.Set(values)

    def fill_display_color(self, color):
        usd_fnc = self.get_usd_fnc()
        usd_core.UsdGeometryOpt(
            usd_fnc
        ).fill_display_color(
            color
        )
