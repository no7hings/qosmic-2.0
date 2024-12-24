# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class BBox(object):
    @classmethod
    def exact_for_many(cls, paths):
        min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
        max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')
        for i_path in paths:
            i_bbox = cmds.exactWorldBoundingBox(i_path)
            min_x = min(min_x, i_bbox[0])
            min_y = min(min_y, i_bbox[1])
            min_z = min(min_z, i_bbox[2])
            max_x = max(max_x, i_bbox[3])
            max_y = max(max_y, i_bbox[4])
            max_z = max(max_z, i_bbox[5])

        return [min_x, min_y, min_z, max_x, max_y, max_z]

    @classmethod
    def exact_for(cls, path):
        return cmds.exactWorldBoundingBox(path)

    @classmethod
    def create_bbox(cls, locations, cube_box=None):
        cmds.select(locations)
        _x, _y, _z, x, y, z = cls.exact_for_many(locations)
        _y = 0
        w, h, d = x-_x, y-_y, z-_z
        x_c, y_c, z_c = (_x+x)/2, (_y+y)/2, (_z+z)/2
        if cube_box is None:
            cube_box, _ = cmds.polyCube(name='bbox', w=w, h=h, d=d)
            cmds.delete(cube_box, constructionHistory=1)
        else:
            cmds.setAttr(cube_box+'.scale', w, h, d)
        cmds.setAttr(cube_box+'.translate', x_c, y_c, z_c)
        cmds.select(clear=1)
        return cube_box
