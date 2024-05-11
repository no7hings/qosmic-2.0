# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.api.OpenMaya as om2


class MeshBoxGenerate(object):
    @staticmethod
    def to_cube_data(bbox_map):
        _x, _y, _z, x, y, z = bbox_map
        return (
            x-_x,  # w
            y-_y,  # h
            z-_z,  # d
            (x+_x)/2,  # x
            (y+_y)/2,  # y
            (z+_z)/2,  # z
        )

    @classmethod
    def is_point_in_bbox(cls, point, bbox_map):
        px, py, pz = point
        _bx, _by, _bz, bx, by, bz = bbox_map
        if _bx < px < bx and _by < py < by and _bz < pz < bz:
            return True
        return False

    @classmethod
    def is_point_array_in_bbox(cls, point_array, bbox_map):
        list_ = []
        for point in point_array:
            if cls.is_point_in_bbox(point, bbox_map):
                list_.append(point)
        return list_

    @classmethod
    def to_om2_dag_path(cls, path):
        return om2.MGlobal.getSelectionListByName(path).getDagPath(0)

    @classmethod
    def to_om2_mesh_fnc(cls, path):
        return om2.MFnMesh(cls.to_om2_dag_path(path))

    @classmethod
    def to_point_array(cls, om2_point_array):
        return [(i[0], i[1], i[2]) for i in om2_point_array]

    @classmethod
    def get_mesh_point_array(cls, mesh):
        om2_mesh = cls.to_om2_mesh_fnc(mesh)
        om2_point_array = om2_mesh.getPoints()
        return cls.to_point_array(om2_point_array)

    @staticmethod
    def get_oc_branch_data(bbox_map):
        _x, _y, _z, x, y, z = bbox_map
        mx = (x+_x)/2
        my = (y+_y)/2
        mz = (z+_z)/2
        b0 = mx, my, _z, x, y, mz
        b1 = _x, my, _z, mx, y, mz
        b2 = mx, _y, _z, x, my, mz
        b3 = _x, _y, _z, mx, my, mz
        b4 = mx, my, mz, x, y, z
        b5 = _x, my, mz, mx, y, z
        b6 = mx, _y, mz, x, my, z
        b7 = _x, _y, mz, mx, my, z
        return b0, b1, b2, b3, b4, b5, b6, b7

    @classmethod
    def get_mesh_point_array_by_paths(cls, paths, exists_only=True):
        list_ = []
        for i_path in paths:
            point_array = []
            if not exists_only:
                point_array = cls.get_mesh_point_array(i_path)
            if exists_only:
                exists = 0
                if cmds.getAttr(i_path+'.visibility') == 1:
                    exists += 1
                transforms = cmds.listRelatives(i_path, parent=1, fullPath=1)
                if transforms:
                    transform = transforms[0]
                    if cmds.getAttr(transform+'.visibility') == 1:
                        exists += 1
                if exists == 2:
                    point_array = cls.get_mesh_point_array(i_path)
            list_.extend(point_array)
        return list_

    @classmethod
    def to_om2_dag_node(cls, path):
        return om2.MFnDagNode(cls.to_om2_dag_path(path))

    @classmethod
    def get_mesh_paths_by_group(cls, location):
        return cmds.ls(location, dag=1, long=1, type='mesh') or []

    @classmethod
    def get_bbox(cls, path):
        om2_bbox = cls.to_om2_dag_node(path).boundingBox
        return cls.to_point_array([om2_bbox.min, om2_bbox.max])

    @classmethod
    def get_bbox_map(cls, bbox):
        mini, maxi = bbox
        _x, _y, _z = mini
        x, y, z = maxi
        return _x, _y, _z, x, y, z

    # Reduce Bounding Box Map to Cube
    @classmethod
    def reduce_bbox_map(cls, bbox_map):
        _x, _y, _z, x, y, z = bbox_map
        mini = min(_x, _y, _z)
        maxi = max(x, y, z)
        return mini, mini, mini, maxi, maxi, maxi

    @classmethod
    def get_bbox_data_by_group(cls, location, exists_only=True):
        # Sub Method
        def rcs_fnc_(point_array_, bbox_map_, depth_):
            if depth_ > 0:
                _depth = depth_-1
                _point_array_in_bbox = cls.is_point_array_in_bbox(point_array_, bbox_map_)
                if _point_array_in_bbox:
                    list_.remove(bbox_map_)
                    _branches = cls.get_oc_branch_data(bbox_map_)
                    for _i_branch in _branches:
                        if cls.is_point_array_in_bbox(_point_array_in_bbox, _i_branch):
                            list_.append(_i_branch)
                        rcs_fnc_(_point_array_in_bbox, _i_branch, _depth)

        paths = cls.get_mesh_paths_by_group(location)
        point_array = cls.get_mesh_point_array_by_paths(paths, exists_only)
        bbox_max = cls.get_bbox(location)
        bbox_map_max = cls.get_bbox_map(bbox_max)
        bbox_map_max_reduce = cls.reduce_bbox_map(bbox_map_max)
        list_ = [bbox_map_max_reduce]

        depth_max = 4
        rcs_fnc_(point_array, bbox_map_max_reduce, depth_max)
        return list_

    @classmethod
    def generate_by_group(cls, location_src, location_dst=None, exists_only=True):
        bbox_map_array = cls.get_bbox_data_by_group(location_src, exists_only)
        box_paths = []
        for i_seq, i_bbox_map in enumerate(bbox_map_array):
            i_w, i_h, i_d, i_tx, i_ty, i_tz = cls.to_cube_data(i_bbox_map)
            i_box_name = 'box'+'_'+str(i_seq).zfill(4)
            i_box_path, _ = cmds.polyCube(name=i_box_name, w=i_w, h=i_h, d=i_d)
            cmds.delete(i_box_path, constructionHistory=1)
            box_paths.append(i_box_path)
            cmds.setAttr(i_box_path+'.translate', i_tx, i_ty, i_tz)
        #
        if location_dst:
            location_dst_name = location_dst.split('|')[-1]
            cmds.group(empty=1, name=location_dst_name)
            cmds.parent(box_paths, location_dst)

    @classmethod
    def test(cls):
        pass
