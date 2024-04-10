# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core
# maya
from .wrap import *


class Om2Base(object):
    DEFAULT_MAP_NAME = 'map1'

    @classmethod
    def _get_om2_dag_path_(cls, path):
        return om2.MGlobal.getSelectionListByName(path).getDagPath(0)

    @classmethod
    def _get_om2_dag_obj_(cls, path):
        return om2.MFnDagNode(cls._get_om2_dag_path_(path)).object()

    @classmethod
    def _get_om2_transform_(cls, path=None):
        if path:
            return om2.MFnTransform(cls._get_om2_dag_path_(path))
        return om2.MFnTransform()

    @classmethod
    def _get_om2_mesh_fnc_(cls, path):
        return om2.MFnMesh(cls._get_om2_dag_path_(path))

    @classmethod
    def _get_om2_nurbs_curve_fnc_(cls, path):
        return om2.MFnNurbsCurve(cls._get_om2_dag_path_(path))

    @classmethod
    def _get_om2_nurbs_surface_fnc_(cls, path):
        return om2.MFnNurbsSurface(cls._get_om2_dag_path_(path))

    @classmethod
    def _get_om2_dag_node_fnc_(cls, path):
        return om2.MFnDagNode(cls._get_om2_dag_path_(path))

    @classmethod
    def _get_om2_obj_(cls, name):
        return om2.MFnDependencyNode(
            om2.MGlobal.getSelectionListByName(name).getDependNode(0)
        )

    #
    @classmethod
    def _get_om2_point_(cls, point):
        om2_point = om2.MPoint()
        om2_point.x, om2_point.y, om2_point.z = point
        return om2_point

    @classmethod
    def _to_om2_point_array_(cls, point_array):
        if isinstance(point_array, om2.MPointArray):
            return point_array
        om2_point_array = om2.MPointArray()
        for i_point in point_array:
            if isinstance(i_point, om2.MPoint):
                i_om2_point = i_point
            elif isinstance(i_point, tuple):
                i_om2_point = cls._get_om2_point_(i_point)
            else:
                raise RuntimeError()
            om2_point_array.append(i_om2_point)
        return om2_point_array

    #
    @classmethod
    def to_integer_array(cls, om2_int_array):
        return map(int, om2_int_array)

    @classmethod
    def _to_float_array_(cls, om2_float_array):
        """
        :param om2_float_array: instance(OpenMaya.MFloatArray)
        :return:
            list(
                float,
                ...
            )
        """
        return map(float, om2_float_array)

    @classmethod
    def _to_point_(cls, om2_point, round_count=None):
        x, y, z = om2_point.x, om2_point.y, om2_point.z
        if isinstance(round_count, int):
            return round(x, round_count), round(y, round_count), round(z, round_count)
        return x, y, z

    @classmethod
    def to_point_array(cls, om2_point_array, round_count=None):
        return map(lambda x: cls._to_point_(x, round_count=round_count), om2_point_array)

    @classmethod
    def _get_float_vector_(cls, om2_float_vector):
        """
        :param om2_float_vector: instance(OpenMaya.MFloatVector)
        :return:
            tuple(float(x), float(y), float(z))
        """
        return om2_float_vector.x, om2_float_vector.y, om2_float_vector.z

    @classmethod
    def _get_float_vector_array_(cls, om2_float_vector_array):
        """
        :param om2_float_vector_array: instance(OpenMaya.MFloatVectorArray)
        :return:
            list(
                tuple(float(x), float(y), float(z)),
                ...
            )
        """
        return [(i.x, i.y, i.z) for i in om2_float_vector_array]

    @classmethod
    def _get_rgba_array_(cls, om2_color_array):
        """
        :param om2_color_array: instance(OpenMaya.MColorArray)
        :return:
            list(
                tuple(float(r), float(g), float(b), float(a)),
                ...
            )
        """
        return [(i.r, i.g, i.b, i.a) for i in om2_color_array]

    @classmethod
    def _get_om2_vector_(cls, vector):
        return om2.MVector(*vector)

    @classmethod
    def _get_om2_int_array_(cls, int_array):
        return om2.MIntArray(int_array)

    @classmethod
    def _get_om2_matrix_(cls, matrix):
        om2_matrix = om2.MMatrix()
        for seq in range(4):
            for sub_seq in range(4):
                om2_matrix.setElement(seq, sub_seq, matrix[seq*4+sub_seq])
        return om2_matrix

    @classmethod
    def _get_om2_transformation_matrix_(cls, matrix):
        return om2.MTransformationMatrix(cls._get_om2_matrix_(matrix))

    @staticmethod
    def _to_int_array_reduce(array):
        lis = []
        #
        maximum, minimum = max(array), min(array)
        #
        start, end = None, None
        count = len(array)
        index = 0
        #
        array.sort()
        for seq in array:
            if index > 0:
                pre = array[index-1]
            else:
                pre = None
            #
            if index < (count-1):
                nex = array[index+1]
            else:
                nex = None
            #
            if pre is None and nex is not None:
                start = minimum
                if seq-nex != -1:
                    lis.append(start)
            elif pre is not None and nex is None:
                end = maximum
                if seq-pre == 1:
                    lis.append((start, end))
                else:
                    lis.append(end)
            elif pre is not None and nex is not None:
                if seq-pre != 1 and seq-nex != -1:
                    lis.append(seq)
                elif seq-pre == 1 and seq-nex != -1:
                    end = seq
                    lis.append((start, end))
                elif seq-pre != 1 and seq-nex == -1:
                    start = seq
            #
            index += 1
        #
        return lis

    @classmethod
    def _get_mesh_comp_names_(cls, indices, comp_key):
        lis = []
        if indices:
            reduce_ids = cls._to_int_array_reduce(indices)
            if len(reduce_ids) == 1:
                if isinstance(reduce_ids[0], tuple):
                    return ['{}[{}:{}]'.format(comp_key, *reduce_ids[0])]
            for i in reduce_ids:
                if isinstance(i, int):
                    lis.append('{}[{}]'.format(comp_key, i))
                elif isinstance(i, tuple):
                    lis.append('{}[{}:{}]'.format(comp_key, *i))
        #
        return lis

    @classmethod
    def _get_mesh_face_comp_names_(cls, indices):
        return cls._get_mesh_comp_names_(indices, 'f')

    @classmethod
    def _get_mesh_edge_comp_names_(cls, indices):
        return cls._get_mesh_comp_names_(indices, 'e')

    @classmethod
    def _get_mesh_vertex_comp_names_(cls, indices):
        return cls._get_mesh_comp_names_(indices, 'vtx')

    @classmethod
    def _get_curve_knots_(cls, count, degree):
        span = count-3
        M = span
        N = degree
        # c = M+2*N-1
        lis = []
        knot_minimum, knot_maximum = 0.0, float(M)
        #
        [lis.append(knot_minimum) for _ in range(degree)]
        #
        add_count = count-N-1
        for seq in range(add_count):
            lis.append(float(seq+1)*knot_maximum/(add_count+1))
        #
        [lis.append(knot_maximum) for _ in range(degree)]
        return lis

    @classmethod
    def _get_surface_knots_(cls, count, degree):
        lis = []
        knots_min, knots_max = 0.0, 1.0
        #
        c_ip = count-2
        [lis.append(knots_min) for _ in range(degree)]
        #
        for seq in range(c_ip):
            lis.append(float(seq+1)*knots_max/(c_ip+1))
        #
        [lis.append(knots_max) for _ in range(degree)]
        return lis

    @classmethod
    def _set_locator_create_by_points(cls, points):
        for seq, point in enumerate(points):
            cmds.spaceLocator(name='test_{}_loc'.format(seq), position=point)

    @classmethod
    def _get_center_point_(cls, point_0, point_1):
        x, y, z = (point_0.x+point_1.x)/2, (point_0.y+point_1.y)/2, (point_0.z+point_1.z)/2
        return om2.MPoint(x, y, z)

    @staticmethod
    def _set_value_map_(range1, range2, value1):
        min1, max1 = range1
        min2, max2 = range2
        #
        percent = float(value1-min1)/(max1-min1)
        #
        value2 = (max2-min2)*percent+min2
        return value2

    @classmethod
    def _set_om2_curve_create_(cls, points, knots, degree, form, parent):
        om2_curve = om2.MFnNurbsCurve()
        om2_curve.create(
            points,
            knots, degree, form,
            False,
            True,
            parent=parent
        )


class Om2CurveCreator(object):
    def __init__(self, path):
        # if cmds.objExists(path) is False:
        #     cmds.createNode('transform', name=path)
        self._obj_path = path
        self._om2_obj_fnc = Om2Base._get_om2_dag_obj_(path)

    @classmethod
    def _to_om2_point_array_(cls, point_array):
        om2_point_array = om2.MPointArray()
        for point in point_array:
            om2_point = Om2Base._get_om2_point_(point)
            om2_point_array.append(om2_point)
        return om2_point_array

    @classmethod
    def _get_knots__(cls, count, degree, span):
        M = span
        N = degree
        # c = M+2*N-1
        lis = []
        knot_minimum, knot_maximum = 0.0, float(M)
        #
        [lis.append(knot_minimum) for _ in range(degree)]
        #
        add_count = count-N-1
        for seq in range(add_count):
            lis.append(float(seq+1)*knot_maximum/(add_count+1))
        #
        [lis.append(knot_maximum) for _ in range(degree)]
        return lis

    @classmethod
    def _set_points_reduce_(cls, points):
        lis = [points[0], cls._get_mid_point_(points[0], points[1])]
        for i in points[1:-1]:
            lis.append(i)
        lis.extend(
            [points[-1]]
        )
        return lis

    @classmethod
    def _get_mid_point_(cls, point_0, point_1):
        x_0, y_0, z_0 = point_0
        x_1, y_1, z_1 = point_1
        return (x_1+x_0)/2, (y_1+y_0)/2, (z_1+z_0)/2

    def set_create_by_points(self, points, degree=3):
        points_ = points
        form = 1
        count = len(points_)
        knots = Om2Base._get_curve_knots_(count, degree)
        om2_curve = om2.MFnNurbsCurve()
        om2_curve.create(
            self._to_om2_point_array_(points_),
            knots, degree, form,
            False,
            True,
            parent=Om2Base._get_om2_dag_obj_('|{}'.format(self._obj_path))
        )

    def set_create_by_raw(self, raw):
        points, knots, degree, form = raw
        om2_curve = om2.MFnNurbsCurve()
        om2_curve.create(
            self._to_om2_point_array_(points),
            knots, degree, form,
            False,
            True,
            parent=Om2Base._get_om2_dag_obj_(self._obj_path)
        )


# noinspection PyUnusedLocal
class Om2CurveOpt(object):
    def __init__(self, path):
        self._om2_obj_fnc = Om2Base._get_om2_nurbs_curve_fnc_(path)

    @property
    def path(self):
        return self._om2_obj_fnc.fullPathName()

    def get_degree(self):
        return self._om2_obj_fnc.degree

    def get_form(self):
        return self._om2_obj_fnc.form

    def get_knots(self):
        return Om2Base._to_float_array_(self._om2_obj_fnc.knots())

    def set_knots(self, knots):
        self._om2_obj_fnc.setKnots(knots, 0, len(knots)-1)
        self._om2_obj_fnc.updateCurve()

    def get_points(self):
        return Om2Base.to_point_array(self._om2_obj_fnc.cvPositions())

    def get_create_raw(self):
        points = Om2Base.to_point_array(self._om2_obj_fnc.cvPositions())
        knots = Om2Base._to_float_array_(self._om2_obj_fnc.knots())
        degree = self._om2_obj_fnc.degree
        form = self._om2_obj_fnc.form
        return points, knots, degree, form

    def _test_(self):
        print self._om2_obj_fnc.cvs()

    @staticmethod
    def _get_curve_knots_(count, degree, form):
        if form == 1:
            if count == 2:
                return [0.0]*degree+[1.0]
            span = max(count-3, 1)
            M = span
            N = degree
            lis = []
            knot_minimum, knot_maximum = 0.0, float(M)
            #
            [lis.append(knot_minimum) for _ in range(degree)]
            #
            add_count = count-N-1
            for seq in range(add_count):
                lis.append(float(seq+1)*knot_maximum/(add_count+1))
            #
            [lis.append(knot_maximum) for _ in range(degree)]
            return lis
        elif form == 3:
            span = max(count-3, 1)
            M = span
            N = degree
            lis = []
            knot_minimum, knot_maximum = 0.0, float(M)+1
            #
            [lis.append(knot_minimum+i-degree+1) for i in range(degree)]
            #
            add_count = count-N-1
            for seq in range(add_count):
                lis.append(float(seq+1)*knot_maximum/(add_count+1))
            #
            [lis.append(knot_maximum+i) for i in range(degree)]
            return lis

    @classmethod
    def set_create(cls, name, degree, form, points):
        if form == 3:
            if degree > 1:
                points.append(points[1])
        #
        count = len(points)
        knots = cls._get_curve_knots_(count, degree, 1)
        # print knots
        # knots = [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        knots = [0.0, 0.2, 0.4, 0.6, 1.0]
        transform = cmds.createNode('transform', name=name)
        Om2Base._set_om2_curve_create_(
            Om2Base._to_om2_point_array_(points),
            knots, degree, form,
            parent=Om2Base._get_om2_dag_obj_(transform)
        )


# noinspection PyUnusedLocal
class Om2MeshOpt(object):
    def __init__(self, path):
        self._om2_obj_fnc = Om2Base._get_om2_mesh_fnc_(path)

    def get_name(self):
        return self._om2_obj_fnc.name()

    name = property(get_name)

    def get_path(self):
        return self._om2_obj_fnc.fullPathName()

    path = property(get_path)

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

    def get_unused_vertices(self):
        lis = []
        om2_vertex_itr = om2.MItMeshVertex(self._om2_obj_fnc.object())
        vertex_count = self._om2_obj_fnc.numVertices
        for i_vertex_index in range(vertex_count):
            om2_vertex_itr.setIndex(i_vertex_index)
            if not om2_vertex_itr.numConnectedFaces():
                lis.append(i_vertex_index)
        return lis

    def set_unused_vertices_delete(self):
        c = self.get_unused_vertices()
        for i in Om2Base._get_mesh_vertex_comp_names_(c):
            p = '{}.{}'.format(self.path, i)
            cmds.delete(p)

    def set_vertex_delete(self, vertex_index):
        om2_fnc = self._om2_obj_fnc
        om2_fnc.deleteVertex(vertex_index)

    def get_face_count(self):
        om2_fnc = self._om2_obj_fnc
        return om2_fnc.numPolygons

    def get_points(self, round_count=None):
        return Om2Base.to_point_array(
            self._om2_obj_fnc.getPoints(),
            round_count
        )

    def get_point_at(self, vertex_index):
        return Om2Base._to_point_(
            self._om2_obj_fnc.getPoint(vertex_index),
        )

    def _get_points_(self):
        return self._om2_obj_fnc.getPoints()

    def get_bounding_box(self):
        om2_world_matrix = self.get_world_matrix()
        om2_bounding_box = self._om2_obj_fnc.boundingBox
        om2_bounding_box.transformUsing(om2_world_matrix)
        return om2_bounding_box

    def get_center_point(self):
        return self.get_bounding_box().center

    def get_width(self):
        return self.get_bounding_box().width

    def get_height(self):
        return self.get_bounding_box().height

    def get_depth(self):
        return self.get_bounding_box().depth

    def get_world_matrix(self):
        plug = om2.MPlug(self._om2_obj_fnc.object(), self._om2_obj_fnc.attribute('worldMatrix'))
        plug = plug.elementByLogicalIndex(0)
        plug_obj = plug.asMObject()
        matrix_data = om2.MFnMatrixData(plug_obj)
        world_matrix = matrix_data.matrix()
        return world_matrix

    @classmethod
    def create_fnc(
        cls, name, face_vertices, points, uv_coords_maps=None, uv_maps=None, normal_maps=None, color_maps=None
    ):
        """
        face_vertex_counts = [4]
        face_vertex_indices = [0, 1, 2, 3]
        points = [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)]
        :param name:
        :param face_vertices:
        :param points:
        :param uv_coords_maps:
        :param uv_maps:
        :param normal_maps:
        :param color_maps:
        :return:
        """
        bsc_log.Log.debug('start create transform')
        transform = cmds.createNode('transform', name=name, skipSelect=1)
        transform_name = bsc_core.PthNodeMtd.get_dag_name(transform, '|')
        bsc_log.Log.debug('start create mesh')
        om2_fnc = om2.MFnMesh()
        face_vertex_counts, face_vertex_indices = face_vertices
        om2_fnc.create(
            Om2Base._to_om2_point_array_(points),
            face_vertex_counts, face_vertex_indices,
            parent=Om2Base._get_om2_dag_obj_(transform)
        )
        bsc_log.Log.debug('start assign uv map')
        if isinstance(uv_coords_maps, dict):
            if uv_coords_maps:
                if 'map1' not in uv_coords_maps:
                    uv_coords_maps['map1'] = uv_coords_maps.values()[0]
                for i_map_name, i_uv_coords in uv_coords_maps.items():
                    if i_map_name != 'map1':
                        om2_fnc.createUVSet(i_map_name)
                    #
                    i_u_coords, i_v_coords = zip(*i_uv_coords)
                    om2_fnc.setUVs(i_u_coords, i_v_coords, i_map_name)
                    om2_fnc.assignUVs(
                        face_vertex_counts, face_vertex_indices,
                        i_map_name
                    )
        #
        if isinstance(uv_maps, dict):
            cls(om2_fnc.fullPathName()).assign_uv_maps(uv_maps)
        #
        cmds.sets(om2_fnc.fullPathName(), forceElement='initialShadingGroup')
        om2_fnc.setName(transform_name+'Shape')
        return om2_fnc.fullPathName()

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
        if Om2Base.DEFAULT_MAP_NAME not in uv_map_names:
            om2_fnc.copyUVSet(uv_map_names[0], Om2Base.DEFAULT_MAP_NAME)
            uv_map_names = self.get_uv_map_names()
        if uv_map_names:
            for uv_map_name in uv_map_names:
                uv_face_vertex_counts, uv_face_vertex_indices = om2_fnc.getAssignedUVs(uv_map_name)
                coords = self.get_uv_map_coords(uv_map_name)
                dict_[uv_map_name] = (
                    Om2Base.to_integer_array(uv_face_vertex_counts),
                    Om2Base.to_integer_array(uv_face_vertex_indices),
                    coords
                )
        return dict_

    def get_uv_map(self, uv_map_name):
        om2_fnc = self._om2_obj_fnc
        if uv_map_name in self.get_uv_map_names():
            uv_face_vertex_counts, uv_face_vertex_indices = om2_fnc.getAssignedUVs(uv_map_name)
            us, vs = om2_fnc.getUVs(uv_map_name)
            coords = zip(us, vs)
            return list(uv_face_vertex_counts), list(uv_face_vertex_indices), coords

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

    def get_uv_map_range(self, uv_map_name):
        us, vs = self._om2_obj_fnc.getUVs(uv_map_name)
        return (min(us), max(us)), (min(vs), max(vs))

    def _set_morph_by_uv_map_0_(self, uv_map_name):
        scale = self.get_height()+self.get_width()+self.get_depth()
        #
        face_vertices = self._om2_obj_fnc.getAssignedUVs(uv_map_name)
        #
        (u_minimum, u_maximum), (v_minimum, v_maximum) = self.get_uv_map_range(uv_map_name)
        uv_coords = self.get_uv_map_coords(uv_map_name)
        points = []
        for i in uv_coords:
            x, z = i
            x, z = (
                Om2Base._set_value_map_((u_minimum, u_maximum), (0, 1), x),
                Om2Base._set_value_map_((v_minimum, v_maximum), (0, 1), z)
            )
            y = 0
            points.append((x*scale, y, -z*scale))
        #
        name = '{}_morph_mesh_0'.format(self.name)
        Om2MeshOpt.create_fnc(
            name, face_vertices, points
        )

    def _set_morph_by_uv_map_1_(self, uv_map_name):
        scale = self.get_height()+self.get_width()+self.get_depth()
        #
        om2_vertex_itr = om2.MItMeshVertex(self._om2_obj_fnc.object())
        face_vertices = self.get_face_vertices()
        #
        (u_minimum, u_maximum), (v_minimum, v_maximum) = self.get_uv_map_range(uv_map_name)
        #
        points = []
        vertex_count = self._om2_obj_fnc.numVertices
        for vertex_index in range(vertex_count):
            om2_vertex_itr.setIndex(vertex_index)
            x, z = om2_vertex_itr.getUV(uv_map_name)
            x, z = (
                Om2Base._set_value_map_((u_minimum, u_maximum), (0, 1), x),
                Om2Base._set_value_map_((v_minimum, v_maximum), (0, 1), z)
            )
            y = 0
            points.append((x*scale, y, -z*scale))
        #
        name = '{}_morph_mesh_0'.format(self.name)
        #
        Om2MeshOpt.create_fnc(
            name, face_vertices, points
        )

    def set_morph_by_uv_map(self, keep_face_vertices, uv_map_name='map1'):
        if keep_face_vertices is True:
            self._set_morph_by_uv_map_1_(uv_map_name)
        else:
            self._set_morph_by_uv_map_0_(uv_map_name)

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
        cmds.polyColorPerVertex(self.path, cdo=1)
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

    def _test_(self):
        vertex_index = 11144
        om2_vertex_itr = om2.MItMeshVertex(self._om2_obj_fnc.object())
        om2_vertex_itr.setIndex(vertex_index)
        print om2_vertex_itr.getConnectedFaces()

    def get_face_shell_ids(self):
        counts, indices = self.get_face_vertices()
        return bsc_core.DccMeshFaceShellOpt(counts, indices).generate()

    def assign_uv_map(self, uv_map_name, uv_map):
        om2_fnc = self._om2_obj_fnc
        #
        if uv_map_name == 'st':
            uv_map_name = 'map1'
        #
        uv_map_names = self.get_uv_map_names()
        #
        if uv_map_name not in uv_map_names:
            om2_fnc.createUVSet(uv_map_name)
        #
        current_uv_map_name = om2_fnc.currentUVSetName()
        om2_fnc.setCurrentUVSetName(current_uv_map_name)
        # noinspection PyBroadException
        try:
            uv_face_vertex_counts, uv_face_vertex_indices, uv_coords = uv_map
            us, vs = zip(*uv_coords)
            #
            om2_fnc.setUVs(us, vs, uv_map_name)
            om2_fnc.assignUVs(uv_face_vertex_counts, uv_face_vertex_indices, uv_map_name)
        except Exception:
            bsc_log.Log.trace_error(
                'assign uv expression: path is "{}", uv map name is "{}"'.format(self.get_path(), uv_map_name)
            )
            bsc_core.ExceptionMtd.set_print()

    def assign_uv_maps(self, maps):
        if 'map1' not in maps:
            maps['map1'] = maps.values()[0]
        #
        for uv_map_name, uv_map in maps.items():
            self.assign_uv_map(uv_map_name, uv_map)

    def duplicate_faces(self, face_indices):
        """
# coding:utf-8
import lxmaya

lxmaya.set_reload()

import lxmaya.core as mya_core

print mya_core.Om2MeshOpt(
    'mesh_001Shape'
).duplicate_faces(
    range(741326, 741829+1)
)

        :param face_indices:
        :return:
        """
        bsc_log.Log.debug('start duplicate faces, count is {}'.format(len(face_indices)))
        om2_fnc = self._om2_obj_fnc
        om2_itr_face = om2.MItMeshPolygon(om2_fnc.object())
        # geometry
        bsc_log.Log.debug('start build geometry data')
        face_vertex_counts = []
        face_vertex_indices_ = []
        points_ = []
        points_opt = bsc_core.RawElementArrayOpt(points_)
        om2_itr_face.reset()
        for i_face_index in face_indices:
            om2_itr_face.setIndex(i_face_index)
            i_count = int(om2_itr_face.polygonVertexCount())
            face_vertex_counts.append(i_count)
            i_points = om2_itr_face.getPoints()
            #
            i_indices = points_opt.extend(Om2Base.to_point_array(i_points))
            face_vertex_indices_.extend(i_indices)
        # uv map
        bsc_log.Log.debug('start build uv map data')
        uv_map_names = self.get_uv_map_names()
        uv_maps = {}
        for i_map_name in uv_map_names:
            i_uv_face_vertex_counts = face_vertex_counts
            i_uv_face_vertex_indices = []
            i_uv_coords = []
            i_uv_coords_opt = bsc_core.RawElementArrayOpt(i_uv_coords)
            om2_itr_face.reset()
            for j_face_index in face_indices:
                om2_itr_face.setIndex(j_face_index)
                j_us, j_vs = om2_itr_face.getUVs()
                j_uv_coords = zip(j_us, j_vs)
                j_uv_indices = i_uv_coords_opt.extend(j_uv_coords)
                i_uv_face_vertex_indices.extend(j_uv_indices)
            #
            uv_maps[i_map_name] = i_uv_face_vertex_counts, i_uv_face_vertex_indices, i_uv_coords
        #
        bsc_log.Log.debug('start create subset')
        return Om2MeshOpt.create_fnc(
            'mesh_subset',
            face_vertices=(face_vertex_counts, face_vertex_indices_),
            points=points_,
            uv_maps=uv_maps
        )

    def duplicate_faces_(self, face_indices):
        bsc_log.Log.debug('start duplicate faces, count is {}'.format(len(face_indices)))
        om2_fnc = self._om2_obj_fnc
        om2_itr_face = om2.MItMeshPolygon(om2_fnc.object())
        # geometry
        bsc_log.Log.debug('start build geometry data')
        face_vertex_counts = []
        face_vertex_indices_old = []
        om2_itr_face.reset()
        for i_face_index in face_indices:
            om2_itr_face.setIndex(i_face_index)
            i_count = int(om2_itr_face.polygonVertexCount())
            face_vertex_counts.append(i_count)
            #
            i_om2_indices = om2_itr_face.getVertices()
            face_vertex_indices_old.extend(list(i_om2_indices))
        #
        face_vertex_indices_new = []
        points_new = om2.MPointArray()
        face_vertex_indices_stack = list(set(face_vertex_indices_old))
        face_vertex_indices_stack_opt = bsc_core.RawStackOpt(face_vertex_indices_stack)
        index_count = len(face_vertex_indices_stack)
        index_old_dict = {}
        for i_index_old in face_vertex_indices_old:
            i_index_new = face_vertex_indices_stack_opt.index(i_index_old)
            face_vertex_indices_new.append(i_index_new)
            index_old_dict[i_index_new] = i_index_old
        #
        for i_index_new in range(index_count):
            points_new.append(om2_fnc.getPoint(index_old_dict[i_index_new]))
        # uv map
        bsc_log.Log.debug('start build uv map data')
        uv_map_names = self.get_uv_map_names()
        uv_maps = {}
        for i_map_name in uv_map_names:
            i_uv_face_vertex_indices = []
            i_uv_coords = []
            i_uv_coords_opt = bsc_core.RawElementArrayOpt(i_uv_coords)
            om2_itr_face.reset()
            for j_face_index in face_indices:
                om2_itr_face.setIndex(j_face_index)
                j_us, j_vs = om2_itr_face.getUVs()
                j_uv_coords = zip(j_us, j_vs)
                j_uv_indices = i_uv_coords_opt.extend(j_uv_coords)
                i_uv_face_vertex_indices.extend(j_uv_indices)
            #
            uv_maps[i_map_name] = face_vertex_counts, i_uv_face_vertex_indices, i_uv_coords
        #
        bsc_log.Log.debug('start create subset')
        return Om2MeshOpt.create_fnc(
            'mesh_subset',
            face_vertices=(face_vertex_counts, face_vertex_indices_new),
            points=points_new,
            uv_maps=uv_maps
        )


class Om2MeshChecker(object):
    def __init__(self, path):
        self._om2_mesh_opt = Om2MeshOpt(path)

    def get_unused_vertex_comp_names(self):
        list_ = []
        om2_obj_fnc = self._om2_mesh_opt._om2_obj_fnc
        om2_vertex_itr = om2.MItMeshVertex(om2_obj_fnc.object())
        for i_vertex_index in range(om2_obj_fnc.numVertices):
            om2_vertex_itr.setIndex(i_vertex_index)
            if not om2_vertex_itr.numConnectedFaces():
                list_.append(i_vertex_index)
        return Om2Base._get_mesh_vertex_comp_names_(list_)

    def set_unused_vertices_delete(self):
        cs = self.get_unused_vertex_comp_names()
        for i_c in Om2Base._get_mesh_vertex_comp_names_(cs):
            p = '{}.{}'.format(self._om2_mesh_opt.path, i_c)
            cmds.delete(p)


class MeshToSurfaceConverter(object):
    def __init__(self, mesh_om2_fnc):
        self._mesh_om2_obj_fnc = mesh_om2_fnc
        #
        self._corner_index = 0
        self._rotation = 1

    @classmethod
    def _get_center_point_(cls, point_0, point_1):
        x, y, z = (point_0.x+point_1.x)/2, (point_0.y+point_1.y)/2, (point_0.z+point_1.z)/2
        return om2.MPoint(x, y, z)

    @classmethod
    def _get_next_comp_index_(cls, comp_index, comp_indices, rotation, step):
        def move_fnc_(i_):
            if rotation > 0:
                if i_ == maximum_index:
                    _n_i = 0
                else:
                    _n_i = i_+1
            else:
                if i_ == 0:
                    _n_i = maximum_index
                else:
                    _n_i = i_-1
            return _n_i

        #
        comp_indices = list(comp_indices)
        maximum_index = len(comp_indices)-1
        i = comp_indices.index(comp_index)
        for _ in range(step):
            i = move_fnc_(i)
        return comp_indices[i]

    @classmethod
    def _get_next_edge_vertex_index_(cls, edge_vertex_index, om2_edge_itr):
        edge_vertex_indices = [om2_edge_itr.vertexId(i) for i in range(2)]
        edge_vertex_indices.remove(edge_vertex_index)
        return edge_vertex_indices[0]

    @classmethod
    def _get_border_next_vertex_index_(cls, vertex_index, edge_index, om2_vertex_itr, om2_edge_itr, rotation, step):
        om2_vertex_itr.setIndex(vertex_index)
        om2_edge_itr.setIndex(edge_index)
        #
        next_vertex_index = cls._get_next_edge_vertex_index_(vertex_index, om2_edge_itr)
        #
        om2_vertex_itr.setIndex(next_vertex_index)
        next_edge_indices = om2_vertex_itr.getConnectedEdges()
        next_edge_index = cls._get_next_comp_index_(
            edge_index, next_edge_indices, rotation, step
        )
        return next_vertex_index, next_edge_index

    def _get_corner_vertex_indices_at_(self, vertex_index, include_vertex_indices, rotation):
        self._mesh_om2_vertex_itr.setIndex(vertex_index)
        #
        start_edge_indices = self._mesh_om2_vertex_itr.getConnectedEdges()
        if rotation == -1:
            start_edge_index = start_edge_indices[1]
        else:
            start_edge_index = start_edge_indices[0]
        self._mesh_om2_edge_itr.setIndex(start_edge_index)
        #
        return self._get_vertex_indices_at_(
            vertex_index, start_edge_index, include_vertex_indices, rotation, step=1
        )

    def _get_border_vertex_indices_at_(self, vertex_index, include_vertex_indices, rotation):
        self._mesh_om2_vertex_itr.setIndex(vertex_index)
        start_edge_indices = self._mesh_om2_vertex_itr.getConnectedEdges()
        # temp
        start_edge_index = start_edge_indices[1]
        self._mesh_om2_edge_itr.setIndex(start_edge_index)
        #
        return self._get_vertex_indices_at_(
            vertex_index, start_edge_index, include_vertex_indices, rotation, step=2
        )

    def _get_vertex_indices_at_(self, start_vertex_index, start_edge_index, include_vertex_indices, rotation, step):
        lis = [start_vertex_index]
        #
        depth = 0
        maximum_depth = 1000
        #
        current_vertex_index = start_vertex_index
        current_edge_index = start_edge_index
        #
        is_end = False
        while is_end is False:
            current_vertex_index, current_edge_index = self._get_border_next_vertex_index_(
                current_vertex_index, current_edge_index,
                self._mesh_om2_vertex_itr, self._mesh_om2_edge_itr,
                rotation, step
            )
            #
            lis.append(current_vertex_index)
            #
            if current_vertex_index in include_vertex_indices:
                is_end = True
            #
            if depth == maximum_depth:
                is_end = True
            #
            depth += 1
        return lis

    def _set_mesh_data_update_(self):
        self._mesh_om2_vertex_itr = om2.MItMeshVertex(self._mesh_om2_obj_fnc.object())
        self._mesh_om2_edge_itr = om2.MItMeshEdge(self._mesh_om2_obj_fnc.object())
        #
        self._mesh_points = self._mesh_om2_obj_fnc.getPoints(space=4)
        #
        self._set_border_vertex_indices_update_()

    def _set_border_vertex_indices_update_(self):
        self._corner_vertex_indices, self._border_vertex_indices = [], []
        om2_vertex_itr = om2.MItMeshVertex(self._mesh_om2_obj_fnc.object())
        vertex_indices = range(om2_vertex_itr.count())
        for vertex_index in vertex_indices:
            om2_vertex_itr.setIndex(vertex_index)
            if om2_vertex_itr.onBoundary() is True:
                if len(om2_vertex_itr.getConnectedFaces()) == 1:
                    self._corner_vertex_indices.append(vertex_index)
                else:
                    self._border_vertex_indices.append(vertex_index)

    def _set_surface_data_update_(self):
        self._set_surface_vertex_indices_update_()
        self._set_surface_points_update_()

    def _set_surface_vertex_indices_update_(self):
        self._surface_grid_vertex_indices_0 = []
        #
        vertex_index = self._corner_vertex_indices[self._corner_index]
        border_start_u_vertex_indices = self._get_corner_vertex_indices_at_(
            vertex_index, self._corner_vertex_indices,
            self._rotation
        )
        border_v_vertex_indices = self._get_corner_vertex_indices_at_(
            vertex_index, self._corner_vertex_indices,
            -self._rotation
        )
        border_end_u_vertex_indices = self._get_corner_vertex_indices_at_(
            border_v_vertex_indices[-1], self._corner_vertex_indices,
            -self._rotation
        )
        self._surface_u_count, self._surface_v_count = len(border_start_u_vertex_indices), len(border_v_vertex_indices)
        #
        for seq, border_v_index in enumerate(border_v_vertex_indices):
            if seq == 0:
                u_vertex_indices = border_start_u_vertex_indices
            elif seq == self._surface_v_count-1:
                u_vertex_indices = border_end_u_vertex_indices
            else:
                u_vertex_indices = self._get_border_vertex_indices_at_(
                    border_v_index, self._border_vertex_indices,
                    self._rotation
                )
            self._surface_grid_vertex_indices_0.append(u_vertex_indices)

        self._surface_grid_vertex_indices_1 = zip(*self._surface_grid_vertex_indices_0)

    def _set_surface_points_update_(self):
        self._surface_points = []
        v_count = len(self._surface_grid_vertex_indices_1)
        for v_index, u_vertex_indices in enumerate(self._surface_grid_vertex_indices_1):
            u_points = self._get_center_u_points_at_(v_index)
            if v_index == 0:
                center_u_points = self._get_center_u_points_between_(
                    v_index, v_index+1
                )
                self._surface_points.extend(u_points+center_u_points)
            elif v_index == v_count-1:
                center_u_points = self._get_center_u_points_between_(
                    v_index-1, v_index
                )
                self._surface_points.extend(center_u_points+u_points)
            else:
                self._surface_points.extend(u_points)

    def _get_center_u_points_at_(self, v_index):
        u_vertex_indices = self._surface_grid_vertex_indices_1[v_index]
        u_count = len(u_vertex_indices)
        u_points = []
        for u_index in range(u_count):
            u_vertex_index = u_vertex_indices[u_index]
            u_point = self._mesh_points[u_vertex_index]
            if u_index == 0:
                next_u_point = self._mesh_points[u_vertex_indices[u_index+1]]
                center_u_point = self._get_center_point_(u_point, next_u_point)
                u_points.extend([u_point, center_u_point])
            elif u_index == u_count-1:
                pre_u_point = self._mesh_points[u_vertex_indices[u_index-1]]
                center_u_point = self._get_center_point_(pre_u_point, u_point)
                u_points.extend([center_u_point, u_point])
            else:
                u_points.append(u_point)
        return u_points

    #
    def _get_center_u_points_between_(self, v_index_0, v_index_1):
        u_vertex_indices_0 = self._surface_grid_vertex_indices_1[v_index_0]
        u_vertex_indices_1 = self._surface_grid_vertex_indices_1[v_index_1]
        u_count = len(u_vertex_indices_0)
        u_points = []
        for u_index, u_vertex_index_0 in enumerate(u_vertex_indices_0):
            u_vertex_index_1 = u_vertex_indices_1[u_index]
            #
            u_point_0 = self._mesh_points[u_vertex_index_0]
            u_point_1 = self._mesh_points[u_vertex_index_1]
            u_point = self._get_center_point_(u_point_0, u_point_1)
            if u_index == 0:
                next_u_point_0 = self._mesh_points[u_vertex_indices_0[u_index+1]]
                next_u_point_1 = self._mesh_points[u_vertex_indices_1[u_index+1]]
                center_u_point_0 = self._get_center_point_(u_point_0, next_u_point_0)
                center_u_point_1 = self._get_center_point_(u_point_1, next_u_point_1)
                center_u_point = self._get_center_point_(center_u_point_0, center_u_point_1)
                u_points.extend([u_point, center_u_point])
            elif u_index == u_count-1:
                pre_u_point_0 = self._mesh_points[u_vertex_indices_0[u_index-1]]
                pre_u_point_1 = self._mesh_points[u_vertex_indices_1[u_index-1]]
                center_u_point_0 = self._get_center_point_(pre_u_point_0, u_point_0)
                center_u_point_1 = self._get_center_point_(pre_u_point_1, u_point_1)
                center_u_point = self._get_center_point_(center_u_point_0, center_u_point_1)
                u_points.extend([center_u_point, u_point])
            else:
                u_points.append(u_point)
        return u_points

    def set_run(self):
        self._set_mesh_data_update_()
        self._set_surface_data_update_()
        Om2SurfaceOpt.set_create(
            'test', self._surface_u_count, self._surface_v_count, self._surface_points
        )


# noinspection PyUnusedLocal
class Om2SurfaceOpt(object):
    def __init__(self, path):
        self._om2_obj_fnc = Om2Base._get_om2_nurbs_surface_fnc_(path)

    @property
    def path(self):
        return self._om2_obj_fnc.fullPathName()

    def get_points(self, round_count=None):
        return Om2Base.to_point_array(
            self._om2_obj_fnc.cvPositions(),
            round_count
        )

    def get_count(self):
        return self._om2_obj_fnc.numCVsInU, self._om2_obj_fnc.numCVsInV

    def get_knots(self):
        return self._om2_obj_fnc.knotsInU(), self._om2_obj_fnc.knotsInV()

    def get_degree(self):
        return self._om2_obj_fnc.degreeInU, self._om2_obj_fnc.degreeInV

    def get_form(self):
        return self._om2_obj_fnc.formInU, self._om2_obj_fnc.formInV

    def get_points_(self, u_division, v_division):
        lis = []
        u_p_max, u_p_min = self._om2_obj_fnc.knotDomainInU
        v_p_max, v_p_min = self._om2_obj_fnc.knotDomainInV
        for u_index in range(u_division):
            u_percent = float(u_index)/float(u_division-1)
            u_p = Om2Base._set_value_map_(
                (0, 1), (u_p_max, u_p_min), u_percent
            )
            for v_index in range(v_division):
                v_percent = float(v_index)/float(v_division-1)
                v_p = Om2Base._set_value_map_(
                    (0, 1), (v_p_max, v_p_min), v_percent
                )
                lis.append(
                    Om2Base._to_point_(
                        self._om2_obj_fnc.getPointAtParam(u_p, v_p, 4)
                    )
                )
        return lis

    def get_v_points(self, sample):
        pass

    def set_convert_to_mesh(self):
        def set_face_vertices_update_fnc_():
            _v_face_count = mesh_v_face_count-2
            _u_face_count = mesh_u_face_count-2
            #
            _l = [0, 1, 2+_u_face_count, 1+_u_face_count]
            for _v_face_index in range(_v_face_count):
                for _u_face_index in range(_u_face_count):
                    mesh_face_vertex_counts.append(4)
                    if _u_face_index == 0:
                        __l = [(i+_v_face_index*(_u_face_count+1)) for i in _l]
                    else:
                        __l = [(i+_v_face_index*(_u_face_count+1)+_u_face_index) for i in _l]
                    #
                    mesh_face_vertex_indices.extend(__l)

        #
        def set_points_update_fnc_():
            # u = 5, v = 4
            # [0, 4, 8, 12, 16, 1, 5, 9, 13, 17, 2, 6, 10, 14, 18, 3, 7, 11, 15, 19]
            _v_point_count = surface_v_count
            _u_point_count = surface_u_count
            #
            _exclude_v_point_indices = [1, _v_point_count-2]
            _exclude_u_point_indices = [1, _u_point_count-2]
            for _v_point_index in range(_v_point_count):
                if _v_point_index in _exclude_v_point_indices:
                    continue
                #
                _map_v_coord = float(_v_point_index)/float(_v_point_count-3)
                for _u_point_index in range(_u_point_count):
                    if _u_point_index in _exclude_u_point_indices:
                        continue
                    _index = _u_point_index*_v_point_count+_v_point_index
                    #
                    mesh_points.append(surface_points[_index])
                    #
                    _map_u_coord = float(_u_point_index)/float(_u_point_count-3)
                    mesh_uv_coords.append(
                        (_map_u_coord, _map_v_coord)
                    )

        #
        surface_v_count = self._om2_obj_fnc.numCVsInV
        surface_u_count = self._om2_obj_fnc.numCVsInU
        surface_points = self.get_points()
        #
        mesh_v_face_count = surface_v_count-1
        mesh_u_face_count = surface_u_count-1
        #
        mesh_face_vertex_counts, mesh_face_vertex_indices = [], []
        mesh_points = []
        mesh_uv_coords = []
        #
        set_face_vertices_update_fnc_()
        set_points_update_fnc_()
        #
        Om2MeshOpt.create_fnc(
            'test',
            (mesh_face_vertex_counts, mesh_face_vertex_indices),
            mesh_points,
            uv_coords_maps={'map1': mesh_uv_coords}
        )

    def set_convert_to_mesh_(self, u_division, v_division):
        def set_face_vertices_update_fnc_():
            _v_face_count = mesh_v_face_count
            _u_face_count = mesh_u_face_count
            #
            _l = [0, 1, 2+_u_face_count, 1+_u_face_count]
            for _v_face_index in range(_v_face_count):
                for _u_face_index in range(_u_face_count):
                    mesh_face_vertex_counts.append(4)
                    if _u_face_index == 0:
                        __l = [(i+_v_face_index*(_u_face_count+1)) for i in _l]
                    else:
                        __l = [(i+_v_face_index*(_u_face_count+1)+_u_face_index) for i in _l]
                    #
                    mesh_face_vertex_indices.extend(__l)

        #
        def set_points_update_fnc_():
            # u = 5, v = 4
            # [0, 4, 8, 12, 16, 1, 5, 9, 13, 17, 2, 6, 10, 14, 18, 3, 7, 11, 15, 19]
            _v_point_count = surface_v_count
            _u_point_count = surface_u_count
            #
            _exclude_v_point_indices = [1, _v_point_count-2]
            _exclude_u_point_indices = [1, _u_point_count-2]
            for _v_point_index in range(_v_point_count):
                _map_v_coord = float(_v_point_index)/float(_v_point_count-1)
                for _u_point_index in range(_u_point_count):
                    _index = _u_point_index*_v_point_count+_v_point_index
                    #
                    mesh_points.append(
                        surface_points[_index]
                    )
                    _map_u_coord = float(_u_point_index)/float(_u_point_count-1)
                    mesh_uv_coords.append(
                        (_map_u_coord, _map_v_coord)
                    )

        #
        surface_v_count = u_division
        surface_u_count = v_division
        surface_points = self.get_points_(
            surface_u_count,
            surface_v_count
        )
        #
        mesh_v_face_count = surface_v_count-1
        mesh_u_face_count = surface_u_count-1
        #
        mesh_face_vertex_counts, mesh_face_vertex_indices = [], []
        mesh_points = []
        mesh_uv_coords = []
        #
        set_face_vertices_update_fnc_()
        set_points_update_fnc_()
        #
        Om2MeshOpt.create_fnc(
            'test',
            (mesh_face_vertex_counts, mesh_face_vertex_indices),
            mesh_points,
            uv_coords_maps={'map1': mesh_uv_coords}
        )

    @staticmethod
    def _get_surface_knots_(count, degree, form):
        if form == 1:
            lis = []
            span = max(count-3, 1)
            M = span
            N = degree
            knot_minimum, knot_maximum = 0.0, 1.0
            #
            add_count = count-N-1
            [lis.append(knot_minimum) for _ in range(degree)]
            #
            for seq in range(add_count):
                lis.append(float(seq+1)*knot_maximum/(add_count+1))
            #
            [lis.append(knot_maximum) for _ in range(degree)]
            return lis
        elif form == 3:
            span = max(count-3, 1)
            M = span
            N = degree
            lis = []
            knot_minimum, knot_maximum = 0.0, float(M)+1
            #
            [lis.append(knot_minimum+i-degree+1) for i in range(degree)]
            #
            add_count = count-N-1
            for seq in range(add_count):
                lis.append(float(seq+1)*knot_maximum/(add_count+1))
            #
            [lis.append(knot_maximum+i) for i in range(degree)]
            return lis

    @classmethod
    def set_create(cls, name, u_count, v_count, points, u_form=1, v_form=3):
        u_degree, v_degree = 3, 2
        u_form, v_form = u_form, v_form

        u_knots, v_knots = (
            cls._get_surface_knots_(u_count, u_degree, u_form),
            cls._get_surface_knots_(v_count, v_degree, v_form)
        )
        transform = cmds.createNode('transform', name=name)
        om2_fnc = om2.MFnNurbsSurface()
        om2_fnc.create(
            points,
            u_knots, v_knots,
            u_degree, v_degree,
            u_form, v_form,
            True,
            parent=Om2Base._get_om2_dag_obj_(transform)
        )
