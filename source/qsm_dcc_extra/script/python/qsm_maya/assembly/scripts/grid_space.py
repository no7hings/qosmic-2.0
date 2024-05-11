# coding:utf-8
import random
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ... import core as _mya_core


class GridSpace(object):
    def __init__(self, paths, grid_size):
        self._paths = paths
        self._grid_size = grid_size

    def generate(self):
        dict_ = {}
        for i_shape_path in self._paths:
            i_transform_path = _mya_core.Shape.get_transform(i_shape_path)
            i_x, i_y, i_z = _mya_core.Transform.get_world_center(i_transform_path)
            i_x_region = int(i_x/self._grid_size)
            i_y_region = int(i_y/self._grid_size)
            i_z_region = int(i_z/self._grid_size)
            dict_.setdefault(
                (i_x_region, i_y_region, i_z_region), []
            ).append(i_shape_path)

        return dict_

    @classmethod
    def create_test_scene(cls, seed=1):
        cmds.setAttr("perspShape.farClipPlane", 100000000)
        cmds.setAttr("perspShape.nearClipPlane", 10.0)

        group = cmds.group(name='box_grp', empty=1)
        random.seed(seed)
        t_range = range(-2500, 2500)
        s_range = range(100, 150)
        for i in range(10000):
            i_tx, i_ty, i_tz = random.choice(t_range), random.choice(t_range), random.choice(t_range)
            i_w, i_h, i_d = random.choice(s_range), random.choice(s_range), random.choice(s_range)
            i_s_w, i_s_h, i_s_d = int(i_w/10.0), int(i_h/10.0), int(i_d/10.0)

            i_box_name = 'box_{}'.format(i)
            i_box_path, _ = cmds.polyCube(name=i_box_name, w=i_w, h=i_w, d=i_w, sx=i_s_w, sy=i_s_w, sz=i_s_w)
            cmds.delete(i_box_path, constructionHistory=1)
            cmds.setAttr(i_box_path+'.translate', i_tx, i_ty, i_tz)
            cmds.parent(i_box_path, group, relative=1)

    @classmethod
    def test(cls):
        paths = cmds.ls('|box_grp', type='mesh', dag=1) or []
        cls(paths, 100).generate()


class PointGridSpace(object):
    def __init__(self, paths, grid_size):
        self._paths = paths
        self._grid_size = grid_size

    def generate(self):
        group = cmds.group(name='box_grp', empty=1)
        points = set()
        for i_shape_path in self._paths:
            i_points = _mya_core.MeshOpt(i_shape_path).get_points()
            for j_x, j_y, j_z in i_points:
                j_x_r, j_y_r, j_z_r = int(j_x/self._grid_size), int(j_y/self._grid_size), int(j_z/self._grid_size)
                points.add((j_x_r*self._grid_size, j_y_r*self._grid_size, j_z_r*self._grid_size))

        for i_seq, i_p in enumerate(points):
            i_box_name = 'box_{}'.format(i_seq)
            i_box_path, _ = cmds.polyCube(
                name=i_box_name, w=self._grid_size, h=self._grid_size, d=self._grid_size, sx=1, sy=1, sz=1
            )
            cmds.setAttr(i_box_path+'.translate', *i_p)
            cmds.parent(i_box_path, group, relative=1)

    @classmethod
    def test(cls):
        cls(
            ['Aset_interior_decoration_S_wk2nbaf_00_LOD0Shape'], 1.0
        ).generate()
