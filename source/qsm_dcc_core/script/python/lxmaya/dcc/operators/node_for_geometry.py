# coding:utf-8
from random import choice

import json

import fnmatch

import parse

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.dcc.core as bsc_dcc_core

import lxbasic.dcc.abstracts as bsc_dcc_abstracts

import lxuniverse.core as unr_core
# maya
from ...core.wrap import *

from ... import core as mya_core


class AbsOm2FncDef(object):
    @property
    def obj(self):
        raise NotImplementedError()

    def _set_om2_fnc_def_init_(self):
        pass

    def get_om2_fnc(self):
        raise NotImplementedError()

    @property
    def om2_obj(self):
        return self.get_om2_fnc()

    def get_is_invalid(self):
        return self.om2_obj.object().isNull()


# noinspection PyUnusedLocal
class TransformOpt(bsc_dcc_abstracts.AbsNodeOpt):
    def __init__(self, *args, **kwargs):
        super(TransformOpt, self).__init__(*args, **kwargs)

    @property
    def om2_obj(self):
        return self.get_om2_fnc()

    def get_om2_fnc(self):
        return mya_core.Om2Base._get_om2_transform_(self.obj.path)

    def set_create(self, matrix=None):
        if self.obj.get_is_exists() is False:
            path = self.obj.get_path()
            path_opt = bsc_core.PthNodeOpt(path)
            parent_path = path_opt.get_parent_path()
            name = path_opt.get_name()
            if parent_path != mya_core.MyaUtil.OBJ_PATHSEP:
                if cmds.objExists(parent_path) is True:
                    om2_obj = mya_core.Om2Base._get_om2_transform_()
                    om2_obj.create(
                        mya_core.Om2Base._get_om2_dag_obj_(parent_path)
                    )
                    om2_obj.setName(name)
                    #
                    bsc_log.Log.trace_method_result(
                        'transform-obj-create',
                        'obj="{}"'.format(self.obj.path)
                    )
                    return True
            else:
                om2_obj = mya_core.Om2Base._get_om2_transform_()
                om2_obj.create()
                #
                om2_obj.setName(name)
                #
                bsc_log.Log.trace_method_result(
                    'transform-obj-create',
                    'obj="{}"'.format(self.obj.path)
                )
                return True

    def get_transformation(self):
        om2_obj = self.om2_obj
        return om2_obj.transformation()

    def get_matrix(self):
        om2_obj = self.om2_obj
        return mya_core.Om2Base._to_float_array_(
            om2_obj.transformation().asMatrix()
        )

    def set_matrix(self, matrix):
        om2_obj = self.om2_obj
        om2_obj.setTransformation(
            mya_core.Om2Base._get_om2_transformation_matrix_(matrix)
        )


# noinspection PyUnusedLocal
class MeshOpt(
    bsc_dcc_abstracts.AbsNodeOpt,
    bsc_dcc_abstracts.AbsMeshOptDef,
    AbsOm2FncDef
):
    COMPONENT_PATHSEP = '.'

    def __init__(self, *args, **kwargs):
        super(MeshOpt, self).__init__(*args, **kwargs)
        self._set_om2_fnc_def_init_()

    def get_om2_fnc(self):
        return mya_core.Om2Base._get_om2_mesh_fnc_(self.obj.path)

    def set_create(self, face_vertices, points, uv_map_coords=None, normal_maps=None, color_maps=None):
        transform_path = self._obj.transform.path
        shape_path = self.obj.path
        if self._obj.get_is_exists() is False:
            if cmds.objExists(transform_path) is True:
                shape_name = self._obj.name
                shape_path = self._obj.path
                om2_obj = om2.MFnMesh()
                face_vertex_counts, face_vertex_indices = face_vertices
                om2_obj.create(
                    mya_core.Om2Base._to_om2_point_array_(points),
                    face_vertex_counts, face_vertex_indices,
                    parent=mya_core.Om2Base._get_om2_dag_obj_(transform_path)
                )
                #
                om2_obj.setName(shape_name)
                #
                _om2_obj = mya_core.Om2Base._get_om2_mesh_fnc_(shape_path)
                #
                bsc_log.Log.trace_method_result(
                    'mesh-obj-create',
                    u'obj="{}"'.format(shape_path)
                )
                return True

    def get_face_vertex_counts(self):
        """
        :return:
            list(
                int(count)
                )
        """
        return [self.om2_obj.polygonVertexCount(i) for i in xrange(self.om2_obj.numPolygons)]

    def get_face_vertex_indices(self, reverse=False):
        om2_obj = self.om2_obj
        if reverse is True:
            face_vertex_indices = []
            for i_face_index in xrange(om2_obj.numPolygons):
                i_om2_indices = self.om2_obj.getPolygonVertices(i_face_index)
                i_indices = list(i_om2_indices)
                if reverse is True:
                    i_indices.reverse()
                face_vertex_indices.extend(i_indices)
            return face_vertex_indices
        face_vertex_counts, face_vertex_indices = om2_obj.getVertices()
        return list(face_vertex_indices)

    def get_face_vertices(self, reverse=False):
        """
        :param reverse: bool
        :return:
            tuple(
                list(
                    int(count),
                    ...
                ),
                list(
                    int(index),
                    ...
                )
            )
        """
        om2_obj = self.om2_obj
        if reverse is True:
            face_vertex_counts = []
            face_vertex_indices = []
            for i_face_index in xrange(om2_obj.numPolygons):
                i_count = om2_obj.polygonVertexCount(i_face_index)
                face_vertex_counts.append(i_count)
                i_om2_indices = om2_obj.getPolygonVertices(i_face_index)
                i_indices = list(i_om2_indices)
                if reverse is True:
                    i_indices.reverse()
                face_vertex_indices.extend(i_indices)

            return face_vertex_counts, face_vertex_indices
        face_vertex_counts, face_vertex_indices = om2_obj.getVertices()
        return list(face_vertex_counts), list(face_vertex_indices)

    def set_vertex_delete(self, vertex_index):
        om2_obj = self.om2_obj
        om2_obj.deleteVertex(vertex_index)

    def get_points(self):
        """
        :return:
            list(
                tuple(float(x), float(y), float(z)),
                ...
            )
        """
        return mya_core.Om2Base.to_point_array(self.om2_obj.getPoints())

    def set_points(self, points):
        om2_obj = mya_core.Om2Base._get_om2_mesh_fnc_(self._obj.transform.path)
        om2_obj.setPoints(mya_core.Om2Base._to_om2_point_array_(points))
        om2_obj.updateSurface()

    def get_uv_map_names(self):
        """
        :return:
            list(
                str(uv_map_name),
                ...
            )
        """
        return self.om2_obj.getUVSetNames()

    def get_default_uv_map_index(self):
        uv_map_names = self.om2_obj.getUVSetNames()
        default_uv_map = mya_core.Om2Base.DEFAULT_MAP_NAME
        if default_uv_map in uv_map_names:
            return uv_map_names.index(default_uv_map)

    def get_default_uv_map_is_exists(self):
        return mya_core.Om2Base.DEFAULT_MAP_NAME in self.get_uv_map_names()

    def set_uv_map_repair(self):
        # uv-map-name
        uv_map_name_default = mya_core.Om2Base.DEFAULT_MAP_NAME
        uv_map_names = self.get_uv_map_names()
        if uv_map_name_default not in uv_map_names:
            self.om2_obj.copyUVSet(uv_map_names[0], uv_map_name_default)

        uv_map_names = self.get_uv_map_names()
        if uv_map_name_default in uv_map_names:
            index_default = uv_map_names.index(uv_map_name_default)
            if index_default != 0:
                name_0 = uv_map_names[0]
                name_bck = '{}_bck'.format(uv_map_name_default)
                self.om2_obj.copyUVSet(uv_map_name_default, name_0)
                self.om2_obj.renameUVSet(uv_map_name_default, name_bck)
                self.om2_obj.renameUVSet(name_0, uv_map_name_default)
                self.om2_obj.deleteUVSet(name_bck)

    @mya_core.MyaModifier.undo_debug_run
    def _get_map_face_non_uv_comp_names_(self):
        path = self.obj.path
        pre_selection_paths = cmds.ls(selection=1, long=1) or []
        #
        cmds.select(path)
        #
        cmds.polySelectConstraint(mode=3, type=8, textured=2)
        cmds.polySelectConstraint(mode=0, type=8, textured=0)
        #
        _ = cmds.ls(selection=1, long=1) or []
        if pre_selection_paths:
            cmds.select(pre_selection_paths)
        else:
            cmds.select(clear=1)
        return [i.split(self.COMPONENT_PATHSEP)[-1] for i in _]

    def get_uv_map_check_error_result(self):
        if mya_core.Om2Base.DEFAULT_MAP_NAME in self.get_uv_map_names():
            om2_obj = self.get_om2_fnc()
            om2_obj.setCurrentUVSetName(mya_core.Om2Base.DEFAULT_MAP_NAME)
            return self._get_map_face_non_uv_comp_names_()

    def get_uv_map_error_comp_names(self, uv_map_name):
        om2_obj = self.get_om2_fnc()
        om2_obj.setCurrentUVSetName(uv_map_name)
        return self._get_map_face_non_uv_comp_names_()

    def get_uv_map_face_vertex_counts(self, uv_map_name):
        uv_face_vertex_counts, uv_face_vertex_indices = self.om2_obj.getAssignedUVs(uv_map_name)
        return list(uv_face_vertex_counts)

    def get_uv_map_face_vertex_indices(self, uv_map_name):
        uv_face_vertex_counts, uv_face_vertex_indices = self.om2_obj.getAssignedUVs(uv_map_name)
        return list(uv_face_vertex_indices)

    def get_uv_map_coords(self, uv_map_name):
        """
        :param uv_map_name: str(uv_map_name)
        :return:
            list(
                tuple(float(u), float(v)),
                ...
            )
        """
        u_coords, v_coords = self.om2_obj.getUVs(uv_map_name)
        coords = zip(u_coords, v_coords)
        return coords

    def get_uv_map(self, uv_map_name):
        if uv_map_name in self.get_uv_map_names():
            uv_face_vertex_counts, uv_face_vertex_indices = self.om2_obj.getAssignedUVs(uv_map_name)
            u_coords, v_coords = self.om2_obj.getUVs(uv_map_name)
            coords = zip(u_coords, v_coords)
            return list(uv_face_vertex_counts), list(uv_face_vertex_indices), coords

    def get_uv_maps(self):
        """
        :return:
            dict(
                str(uv_map_name): self.get_uv_map_coords(*args),
                ...
            )
        """
        dic = {}
        uv_map_names = self.get_uv_map_names()
        # check first map name is default
        if mya_core.Om2Base.DEFAULT_MAP_NAME not in uv_map_names:
            self.om2_obj.copyUVSet(uv_map_names[0], mya_core.Om2Base.DEFAULT_MAP_NAME)
            uv_map_names = self.get_uv_map_names()
        if uv_map_names:
            for uv_map_name in uv_map_names:
                i_uv_face_vertex_counts, i_uv_face_vertex_indices = self.om2_obj.getAssignedUVs(uv_map_name)
                i_coords = self.get_uv_map_coords(uv_map_name)
                dic[uv_map_name] = (
                    list(i_uv_face_vertex_counts),
                    list(i_uv_face_vertex_indices),
                    i_coords
                )
        return dic

    @staticmethod
    def _get_uv_map_face_vertex_indices_(uv_map_coords):
        """
        :param uv_map_coords:
            list(
                tuple(float(u), float(v)),
                ...
            )
        :return:
        """
        uv_face_vertex_indices = []
        new_uv_map_coords = sorted(set(uv_map_coords), key=uv_map_coords.index)
        for i in uv_map_coords:
            uv_face_vertex_indices.append(new_uv_map_coords.index(i))
        return new_uv_map_coords, uv_face_vertex_indices

    def set_uv_coords(self, uv_map_name, uv_map_coords):
        """
        :param uv_map_name: str(uv_map_name)
        :param uv_map_coords: self.get_uv_map_coords(*args)
        :return: None
        """
        uv_face_vertex_counts = self.get_face_vertex_counts()
        new_uv_map_coords, uv_face_vertex_indices = self._get_uv_map_face_vertex_indices_(uv_map_coords)
        uv_map_u_coords, uv_map_v_coords = zip(*new_uv_map_coords)

        self.om2_obj.setUVs(uv_map_u_coords, uv_map_v_coords, uv_map_name)
        self.om2_obj.assignUVs(uv_face_vertex_counts, uv_face_vertex_indices, uv_map_name)

    @classmethod
    def _set_uvs_reduce_(cls):
        pass

    @classmethod
    def _get_maya_uv_face_vertex_indices_(cls, om2_obj, uv_face_vertex_indices, interpolation, unauthored_values_index):
        valueIds = om2.MIntArray(om2_obj.numFaceVertices, -1)
        #
        itFV = om2.MItMeshFaceVertex(om2_obj.object())
        itFV.reset()
        size = max(uv_face_vertex_indices)
        fvi = 0
        while not itFV.isDone():
            valueId = 0
            if interpolation == 'constant':
                valueId = 0
            elif interpolation == 'uniform':
                valueId = itFV.faceId()
            elif interpolation == 'vertex':
                valueId = itFV.vertexId()
            elif interpolation == 'faceVarying':
                valueId = fvi
            #
            if valueId < size:
                valueId = uv_face_vertex_indices[valueId]
                # if valueId == unauthored_values_index:
                #     continue
            #
            valueIds[fvi] = valueId
            #
            fvi += 1
            itFV.next()
        return valueIds

    def assign_uv_map(self, uv_map_name, uv_map):
        om2_obj = self.get_om2_fnc()
        #
        if uv_map_name == 'st':
            uv_map_name = 'map1'
        #
        uv_map_names = self.get_uv_map_names()
        if uv_map_name not in uv_map_names:
            om2_obj.createUVSet(uv_map_name)
            bsc_log.Log.trace_method_result(
                'uv-map-create',
                u'uv-map-name="{}"'.format(uv_map_name)
            )
        #
        current_uv_map_name = om2_obj.currentUVSetName()
        om2_obj.setCurrentUVSetName(current_uv_map_name)
        # noinspection PyBroadException
        try:
            uv_face_vertex_counts, uv_face_vertex_indices, uv_map_coords = uv_map
            if uv_face_vertex_counts:
                u_coords, v_coords = zip(*uv_map_coords)
                #
                om2_obj.setUVs(u_coords, v_coords, uv_map_name)
                om2_obj.assignUVs(uv_face_vertex_counts, uv_face_vertex_indices, uv_map_name)
                #
                bsc_log.Log.trace_method_result(
                    'mesh uv-map assign',
                    u'obj="{}"; uv-map-name="{}"'.format(self.obj.path, uv_map_name)
                )
        except Exception:
            bsc_core.ExceptionMtd.set_print()
            bsc_log.Log.trace_method_error(
                'mesh uv-map assign',
                'obj="{}"'.format(self.obj.path)
            )

    def assign_uv_maps(self, uv_maps, clear=False):
        """
        :param uv_maps: see self.get_uv_maps()
        :param clear: bool
        :return: None
        """
        if clear is True:
            om2_obj = self.get_om2_fnc()
            om2_obj.clearUVs()
        #
        for uv_map_name, uv_map in uv_maps.items():
            self.assign_uv_map(uv_map_name, uv_map)

    def get_normals(self):
        """
        :return: list(
            (float, float, float),
            ...
        )
        """
        lis = []
        for vertex_id in xrange(self.om2_obj.numVertices):
            om2_float_vector = self.om2_obj.getVertexNormal(vertex_id, True)
            lis.append(
                mya_core.Om2Base._get_float_vector_(om2_float_vector)
            )
        return lis

    def get_color_map_names(self):
        """
        :return:
            list(
                str(uv_map_name),
                ...
            )
        """
        return self.om2_obj.getColorSetNames()

    def get_color_map(self, uv_map_name):
        """
        :param uv_map_name: str(uv_map_name)
        :return:
            list(
                tuple(float(r), float(g), float(b), float(a)),
                ...
            )
        """
        lis = []
        om2_color_array = self.om2_obj.getVertexColors(uv_map_name)
        return mya_core.Om2Base._get_rgba_array_(om2_color_array)

    def get_color_maps(self):
        """
        :return:
            dict(
                str(uv_map_name): self.get_color_map(*args),
                ...
            )
        """
        dic = {}
        uv_map_names = self.get_color_map_names()
        if uv_map_names:
            for uv_map_name in uv_map_names:
                dic[uv_map_name] = self.get_color_map(uv_map_name)
        return dic

    def set_color_map_create(self):
        face_vertex_counts = []
        face_vertex_indices = []
        om2_obj = self.om2_obj
        for i_face_index in xrange(om2_obj.numPolygons):
            i_count = om2_obj.polygonVertexCount(i_face_index)
            face_vertex_counts.append(i_count)
            color_range = [i/100.0 for i in range(0, 100)]
            r, g, b = choice(color_range), choice(color_range), choice(color_range)
            for i in range(i_count):
                om2_color = om2.MColor()
                om2_color.r, om2_color.g, om2_color.b, om2_color.a = (r, g, b, 1)
                om2_obj.setFaceVertexColor(om2_color, i_face_index, i)

    def get_bounding_box(self):
        omt_bounding_box = self.om2_obj.boundingBox
        return mya_core.Om2Base.to_point_array([omt_bounding_box.max, omt_bounding_box.min])

    def get_name(self):
        # use transform name
        return mya_core.MyaUtil.get_name_with_namespace_clear(
            self._obj.get_transform().get_name()
        )

    def get_path(self, lstrip=None):
        # remove namespace, use transform path
        raw = mya_core.MyaUtil.get_path_with_namespace_clear(
            self._obj.get_transform().get_name()
        )
        # replace pathsep
        raw = raw.replace(self._obj.PATHSEP, unr_core.UnrObj.PATHSEP)
        # strip path
        if lstrip is not None:
            if raw.startswith(lstrip):
                raw = raw[len(lstrip):]
        return raw

    def get_path_as_uuid(self, lstrip=None):
        return bsc_core.HashMtd.get_hash_value(self.get_path(lstrip), as_unique_id=True)

    def get_name_as_uuid(self):
        return bsc_core.HashMtd.get_hash_value(self.get_name(), as_unique_id=True)

    def get_points_as_uuid(self, ordered=False, round_count=4):
        raw = self.get_points()
        if ordered is True:
            raw.sort()
        raw = bsc_core.RawPointArrayOpt(raw).round_to(round_count)
        return bsc_core.HashMtd.get_hash_value(raw, as_unique_id=True)

    def get_face_vertices_as_uuid(self):
        raw = self.get_face_vertices()
        return bsc_core.HashMtd.get_hash_value(raw, as_unique_id=True)

    def get_geometry_as_uuid(self):
        face_vertices = self.get_face_vertices()
        points = self.get_points()
        return bsc_core.HashMtd.get_hash_value((face_vertices, points), as_unique_id=True)

    def get_uv_map_face_vertices_as_uuid(self, uv_map_name='map1'):
        uv_map = self.get_uv_map(uv_map_name)
        if uv_map:
            uv_face_vertex_counts, uv_face_vertex_indices, uv_map_coords = uv_map
            raw = uv_face_vertex_counts, uv_face_vertex_indices
            return bsc_core.HashMtd.get_hash_value(raw, as_unique_id=True)
        return bsc_core.UuidMtd.generate_new()

    def mark_uuids(self):
        # use transform
        dic = {}
        port = self._obj.transform.get_port(bsc_dcc_core.DccPort.GEOMETRY_UUIDS)
        if port.get_is_exists() is False:
            port.set_create(raw_type='string')
        #
        dic[bsc_dcc_core.DccMeshData.FaceVertices] = self.get_face_vertices_as_uuid()
        dic[bsc_dcc_core.DccMeshData.Points] = self.get_points_as_uuid()

        port.set(json.dumps(dic))

    def get_changed(self):
        pass

    def get_maximum_face_index(self):
        om2_obj = self.get_om2_fnc()
        count = om2_obj.numPolygons
        return count-1

    def get_comp_name_is_whole(self, comp_name):
        if fnmatch.filter([comp_name], 'f?*:*?'):
            p = parse.parse(
                'f[{start_index}:{end_index}]', comp_name
            )
            if p:
                variants = p.named
                start_index, end_index = int(variants['start_index']), int(variants['end_index'])
                if start_index == 0:
                    maximum_face_index = self.get_maximum_face_index()
                    if end_index == maximum_face_index:
                        return True
        return False

    def get_override_face_vertices(self):
        dic = {}
        for i_face_index in xrange(self.om2_obj.numPolygons):
            i_om2_indices = self.om2_obj.getPolygonVertices(i_face_index)
            _ = list(i_om2_indices)
            _.sort()
            key = str(_)
            dic.setdefault(key, []).append(i_face_index)
        #
        lis = []
        face_comp_names = mya_core.Om2Base._get_mesh_face_comp_names_([i_0 for i_0, i_1 in dic.values()])
        for face_comp_name in face_comp_names:
            lis.append('{}.{}'.format(self.obj.path, face_comp_name))
        return lis

    def get_shell_count(self):
        return cmds.polyEvaluate(
            self.obj.path,
            shell=1
        )

    def set_uv_map_rename(self, uv_map_name, new_uv_map_name):
        om2_obj = self.get_om2_fnc()
        om2_obj.renameUVSet(uv_map_name, new_uv_map_name)

    def get_face_count(self):
        om2_obj = self.get_om2_fnc()
        return om2_obj.numPolygons


class MeshChecker(
    bsc_dcc_abstracts.AbsNodeOpt
):
    def __init__(self, *args, **kwargs):
        super(MeshChecker, self).__init__(*args, **kwargs)

    def get_om2_fnc(self):
        return mya_core.Om2Base._get_om2_mesh_fnc_(self.obj.path)

    @property
    def om2_obj(self):
        return self.get_om2_fnc()

    def get_unused_vertex_comp_names(self):
        lis = []
        om2_obj_fnc = self.om2_obj
        om2_vertex_itr = om2.MItMeshVertex(om2_obj_fnc.object())
        for i_vertex_index in range(om2_obj_fnc.numVertices):
            om2_vertex_itr.setIndex(i_vertex_index)
            if not om2_vertex_itr.numConnectedFaces():
                lis.append(i_vertex_index)
        return mya_core.Om2Base._get_mesh_vertex_comp_names_(lis)

    def set_unused_vertices_delete(self):
        cs = self.get_unused_vertex_comp_names()
        for i_c in mya_core.Om2Base._get_mesh_vertex_comp_names_(cs):
            p = '{}.{}'.format(self.obj.path, i_c)
            cmds.delete(p)


# noinspection PyUnusedLocal
class NurbsCurveOpt(
    bsc_dcc_abstracts.AbsNodeOpt,
    AbsOm2FncDef,
):
    def __init__(self, *args):
        """
        :param args:
            1.str(path)
        """
        super(NurbsCurveOpt, self).__init__(*args)
        self._om2_obj_fnc = self.get_om2_fnc()

    def get_om2_fnc(self):
        return mya_core.Om2Base._get_om2_nurbs_curve_fnc_(self.obj.path)

    def get_knots(self):
        return mya_core.Om2CurveOpt(
            self.obj.path
        ).get_knots()

    def get_knots_as_uuid(self):
        raw = self.get_knots()
        return bsc_core.HashMtd.get_hash_value(raw, as_unique_id=True)

    def get_points(self):
        return mya_core.Om2CurveOpt(
            self.obj.path
        ).get_points()

    def get_degree(self):
        return mya_core.Om2CurveOpt(
            self.obj.path
        ).get_degree()

    def get_usd_data(self):
        points = self.get_points()
        degree = self.get_degree()
        form = 1
        count = len(points)
        knots = mya_core.Om2Base._get_curve_knots_(count, degree)
        span = count-3
        ranges = [(0, 1)]
        widths = [0.1]
        order = [degree]
        return points, knots, ranges, widths, order

    def get_usd_basis_curve_data(self):
        points = self.get_points()
        counts = [len(points)]
        widths = [0.003]*len(counts)
        return counts, points, widths


class Om2SurfaceOpt(
    bsc_dcc_abstracts.AbsNodeOpt,
    AbsOm2FncDef,
):
    def __init__(self, *args):
        """
        :param args:
            1.str(path)
        """
        super(Om2SurfaceOpt, self).__init__(*args)

    def get_om2_fnc(self):
        return mya_core.Om2Base._get_om2_nurbs_surface_fnc_(
            self.obj.path
        )
