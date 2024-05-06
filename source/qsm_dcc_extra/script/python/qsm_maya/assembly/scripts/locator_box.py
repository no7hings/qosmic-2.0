# coding=utf-8
import collections
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class LocatorBoxGenerate(object):

    @staticmethod
    # Get Target Object's Box Data
    def compute_box(path):
        if cmds.objExists(path):
            _x, _y, _z, x, y, z = cmds.xform(path, boundingBox=1, worldSpace=1, query=1)
            x_ = x-_x
            y_ = y-_y
            z_ = z-_z
            x_p = x+_x
            y_p = y+_y
            z_p = z+_z
            return x_/2, y_/2, z_/2, x_p/2, y_p/2, z_p/2

    @classmethod
    # Dic For Create Box
    def compute_box_data(cls, path):
        x, y, z, x_, y_, z_ = [.5, .5, .5, 0, 0, 0]
        if cmds.objExists(path):
            x, y, z, x_, y_, z_ = cls.compute_box(path)
        dic = collections.OrderedDict()
        dic['x'] = dict(
            yz=[('.localPosition', x_, y_+y, z_+z), ('.localScale', x, 0, 0)],
            _yz=[('.localPosition', x_, y_-y, z_+z), ('.localScale', x, 0, 0)],
            _y_z=[('.localPosition', x_, y_-y, z_-z), ('.localScale', x, 0, 0)],
            y_z=[('.localPosition', x_, y_+y, z_-z), ('.localScale', x, 0, 0)]
        )
        dic['y'] = dict(
            xz=[('.localPosition', x_+x, y_, z_+z), ('.localScale', 0, y, 0)],
            _xz=[('.localPosition', x_+x, y_, z_-z), ('.localScale', 0, y, 0)],
            _x_z=[('.localPosition', x_-x, y_, z_-z), ('.localScale', 0, y, 0)],
            x_z=[('.localPosition', x_-x, y_, z_+z), ('.localScale', 0, y, 0)]
        )
        dic['z'] = dict(
            xy=[('.localPosition', x_+x, y_+y, z_), ('.localScale', 0, 0, z)],
            _xy=[('.localPosition', x_-x, y_+y, z_), ('.localScale', 0, 0, z)],
            _x_y=[('.localPosition', x_-x, y_-y, z_), ('.localScale', 0, 0, z)],
            x_y=[('.localPosition', x_+x, y_-y, z_), ('.localScale', 0, 0, z)]
        )
        return dic

    @classmethod
    # Create Boxs
    def generate_by_paths(cls, paths=None):
        if not paths:
            paths = cmds.ls(selection=True)
        #
        for i_path in paths:
            cls.generate_by_path(i_path)
        cmds.select(clear=1)

    @classmethod
    # Create Box
    def generate_by_path(cls, path):
        data = cls.compute_box_data(path)

        box_path = path+'_box'
        box_name = box_path.split('|')[-1]
        if cmds.objExists(box_path):
            cmds.delete(box_path)

        cmds.createNode('transform', name=box_name, skipSelect=1)
        for k, v in data.items():
            for j_k, j_v in v.items():
                j_border = box_path+j_k
                cmds.createNode('locator', name=j_border, parent=box_path, skipSelect=1)
                cmds.setAttr(j_border+j_v[0][0], j_v[0][1], j_v[0][2], j_v[0][3])
                cmds.setAttr(j_border+j_v[1][0], j_v[1][1], j_v[1][2], j_v[1][3])
        cmds.select(clear=1)
