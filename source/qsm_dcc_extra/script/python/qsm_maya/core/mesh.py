# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.api.OpenMaya as om2

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxmaya.core as mya_core

from . import shape as _shape

from . import transform as _transform

from . import attribute as _attribute


class Mesh(_shape.Shape):
    @classmethod
    def get_shell_number(cls, path):
        return cmds.polyEvaluate(path, shell=1)

    @classmethod
    def get_face_number(cls, path):
        return cmds.polyEvaluate(path, face=1) or 0

    @classmethod
    def is_deformed(cls, path):
        return _attribute.NodeAttribute.has_source(
            path, 'inMesh'
        )


class MeshOpt(_shape.ShapeOpt):
    @classmethod
    def to_om2_dag_path(cls, path):
        return om2.MGlobal.getSelectionListByName(path).getDagPath(0)

    @classmethod
    def to_om2_mesh_fnc(cls, path):
        return om2.MFnMesh(cls.to_om2_dag_path(path))
    
    @classmethod
    def to_point(cls, om2_point, round_count=None):
        x, y, z = om2_point.x, om2_point.y, om2_point.z
        if isinstance(round_count, int):
            return round(x, round_count), round(y, round_count), round(z, round_count)
        return x, y, z
    
    @classmethod
    def to_point_array(cls, om2_point_array, round_count=None):
        return map(lambda x: cls.to_point(x, round_count=round_count), om2_point_array)

    def __init__(self, path):
        super(MeshOpt, self).__init__(path)
        self._om2_obj_fnc = self.to_om2_mesh_fnc(self._path)

    def get_face_vertices(self):
        face_vertex_counts = []
        face_vertex_indices = []
        om2_fnc = self._om2_obj_fnc
        for i_face_index in xrange(om2_fnc.numPolygons):
            i_count = om2_fnc.polygonVertexCount(i_face_index)
            face_vertex_counts.append(i_count)
            om2_indices = om2_fnc.getPolygonVertices(i_face_index)
            indices = list(om2_indices)
            face_vertex_indices.extend(indices)
        return face_vertex_counts, face_vertex_indices

    def get_face_vertices_as_uuid(self):
        return bsc_core.BscHash.to_hash_key(
            self.get_face_vertices()
        )
    
    def get_points(self, round_count=None):
        return self.to_point_array(
            self._om2_obj_fnc.getPoints(),
            round_count
        )

    def get_uv_map_names(self):
        """
        :return:
            list(
                str(uv_map_name),
                ...
            )
        """
        return self._om2_obj_fnc.getUVSetNames()

    def get_uv_maps(self):
        dict_ = {}
        om2_fnc = self._om2_obj_fnc
        uv_map_names = self.get_uv_map_names()
        # check first map name is default
        if mya_core.Om2Base.DEFAULT_MAP_NAME not in uv_map_names:
            om2_fnc.copyUVSet(uv_map_names[0], mya_core.Om2Base.DEFAULT_MAP_NAME)
            uv_map_names = self.get_uv_map_names()
        if uv_map_names:
            for uv_map_name in uv_map_names:
                uv_face_vertex_counts, uv_face_vertex_indices = om2_fnc.getAssignedUVs(uv_map_name)
                coords = self.get_uv_map_coords(uv_map_name)
                dict_[uv_map_name] = (
                    mya_core.Om2Base.to_integer_array(uv_face_vertex_counts),
                    mya_core.Om2Base.to_integer_array(uv_face_vertex_indices),
                    coords
                )
        return dict_

    def get_uv_map_coords(self, uv_map_name):
        """
        :param uv_map_name: str(uv_map_name)
        :return:
            list(
                tuple(float(u), float(v)),
                ...
            )
        """
        us, vs = self._om2_obj_fnc.getUVs(uv_map_name)
        coords = zip(us, vs)
        return coords

    def to_hash(self):
        face_vertices = self.get_face_vertices()
        points = self.get_points()
        return bsc_core.BscHash.to_hash_key_for_large_data(
            (face_vertices, points), as_unique_id=True
        )

    def save_as_json(self, file_path):
        data = dict(
            face_vertices=self.get_face_vertices(),
            points=self.get_points(),
            uv_maps=self.get_uv_maps()
        )
        bsc_storage.StgFileOpt(file_path).set_write(
            data
        )

    def fill_face_vertex_color(self, rgb, alpha=1):
        color_map_name = 'test'
        color_map_names = self.get_color_map_names()
        if color_map_name not in color_map_names:
            self._om2_obj_fnc.createColorSet(
                color_map_name, True
            )
        self._om2_obj_fnc.setCurrentColorSetName(
            color_map_name
        )
        cmds.polyColorPerVertex(self._path, cdo=1)
        idx = 0
        colors = om2.MColorArray()
        face_indices = []
        for i_face_index in xrange(self._om2_obj_fnc.numPolygons):
            face_indices.append(i_face_index)
            i_count = self._om2_obj_fnc.polygonVertexCount(i_face_index)
            j_om2_color = om2.MColor()
            for j in range(i_count):
                j_om2_color = om2.MColor()
                j_r, j_g, j_b = rgb
                j_om2_color.r, j_om2_color.g, j_om2_color.b, j_om2_color.a = (j_r, j_g, j_b, alpha)
                idx += 3
            colors.append(j_om2_color)

        self._om2_obj_fnc.setFaceColors(
            colors, face_indices
        )
        self._om2_obj_fnc.updateSurface()

    def get_color_map_names(self):
        return self._om2_obj_fnc.getColorSetNames()

    def get_color_map(self, color_map_name):
        return self._om2_obj_fnc.getFaceVertexColors(color_map_name)

    def set_face_vertex_color(self, rgbs, alpha=1):
        color_map_name = 'test'
        color_map_names = self.get_color_map_names()
        if color_map_name not in color_map_names:
            self._om2_obj_fnc.createColorSet(
                color_map_name, True
            )
        self._om2_obj_fnc.setCurrentColorSetName(
            color_map_name
        )
        cmds.polyColorPerVertex(self._path, cdo=1)
        idx = 0
        colors = om2.MColorArray()
        face_indices = []
        for i_face_index in xrange(self._om2_obj_fnc.numPolygons):
            face_indices.append(i_face_index)
            i_count = self._om2_obj_fnc.polygonVertexCount(i_face_index)
            j_om2_color = om2.MColor()
            for j in range(i_count):
                j_om2_color = om2.MColor()
                j_r, j_g, j_b = rgbs[idx], rgbs[idx+1], rgbs[idx+2]
                j_om2_color.r, j_om2_color.g, j_om2_color.b, j_om2_color.a = (j_r, j_g, j_b, alpha)
                idx += 3
            colors.append(j_om2_color)

        self._om2_obj_fnc.setFaceColors(
            colors, face_indices
        )
        self._om2_obj_fnc.updateSurface()

    def get_face_number(self):
        return self._om2_obj_fnc.numPolygons

    def get_world_extent(self):
        return _transform.Transform.get_world_extent(
            _shape.Shape.get_transform(self.shape_path)
        )

    def get_dimension(self):
        (_x, _y, _z), (x, y, z) = self.get_world_extent()
        return x-_x, y-_y, z-_z

    def get_material_paths(self):
        return cmds.listConnections(
            self.shape_path, destination=1, source=0, type=mya_core.MyaNodeTypes.Material
        ) or []

    def get_material_assign_map(self):
        dict_ = {}
        transform_path = self.transform_path
        shape_path = self.shape_path
        material_paths = self.get_material_paths()
        if material_paths:
            for i_material_path in material_paths:
                i_results = cmds.sets(i_material_path, query=1)
                if i_results:
                    i_element_paths = cmds.ls(i_results, leaf=1, noIntermediate=1, long=1) or []
                    for j_element_path in i_element_paths:
                        j_show_type = cmds.ls(j_element_path, showType=1)[1]
                        j_value = i_material_path
                        j_key = None
                        if j_show_type in [mya_core.MyaNodeTypes.Mesh]:
                            if j_element_path == shape_path:
                                j_key = 'all'
                        elif j_show_type == 'float3':
                            if j_element_path.startswith(transform_path):
                                comp_name = j_element_path.split('.')[-1]
                                j_key = comp_name
                        #
                        if j_key is not None:
                            dict_[j_key] = j_value
        return dict_

    def get_material_assign_as_hash_key(self):
        return bsc_core.BscHash.to_hash_key(
            self.get_material_assign_map(), as_unique_id=True
        )
