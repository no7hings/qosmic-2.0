# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.api.OpenMaya as om2

import lxbasic.core as bsc_core

from . import node as _node

from . import node_dag as _node_dag

from . import shape as _shape


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

    def __init__(self, shape_path):
        super(MeshOpt, self).__init__(shape_path)
        self._om2_obj_fnc = self.to_om2_mesh_fnc(shape_path)

    def update_path(self):
        if self._uuid:
            _ = cmds.ls(self._uuid, long=1)
            if _:
                self._path = _[0]
            else:
                raise RuntimeError()

    @property
    def shape_path(self):
        return self._shape_path

    @property
    def shape_name(self):
        return self.shape_path.split('|')[-1]

    @property
    def transform_path(self):
        return bsc_core.PthNodeMtd.get_dag_parent_path(
            self._shape_path, _node_dag.NodeDag.PATHSEP
        )

    @property
    def transform_name(self):
        return self.transform_path.split('|')[-1]

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
    
    def get_points(self, round_count=None):
        return self.to_point_array(
            self._om2_obj_fnc.getPoints(),
            round_count
        )
    
    def to_hash(self):
        face_vertices = self.get_face_vertices()
        points = self.get_points()
        return bsc_core.HashMtd.to_hash_key((face_vertices, points), as_unique_id=True)
