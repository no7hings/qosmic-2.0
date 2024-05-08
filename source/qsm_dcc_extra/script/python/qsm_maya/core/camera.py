# coding:utf-8
import math
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.OpenMaya as om
# noinspection PyUnresolvedReferences
import maya.OpenMayaUI as om_ui

from . import node as _nod

from . import transform as _tsf

from . import shape as _shp

from . import render as _rdr

from . import attribute as _atr


class Camera(object):
    @classmethod
    def to_om_dag_path(cls, path):
        slt = om.MSelectionList()
        dag_path = om.MDagPath()
        slt.add(path)
        slt.getDagPath(0, dag_path)
        return dag_path

    @classmethod
    def generate_mask_nodes(cls, path):
        list_ = []
        tvl = om_ui.MDrawTraversal()
        om_path = cls.to_om_dag_path(path)
        w, h = _rdr.RenderSettings.get_resolution()
        tvl.setFrustum(om_path, w, h)

        tvl.traverse()

        for i in range(tvl.numberOfItems()):
            i_shape_dag_path = om.MDagPath()
            tvl.itemPath(i, i_shape_dag_path)
            i_shape_path = i_shape_dag_path.fullPathName()
            if _nod.Node.is_exists(i_shape_path) is True:
                list_.append(i_shape_path)
        return list_

    @classmethod
    def get_active(cls):
        view = om_ui.M3dView.active3dView()
        camera_dag_path = om.MDagPath()
        view.getCamera(camera_dag_path)
        return camera_dag_path.fullPathName()

    @classmethod
    def get_angle_of_view(cls, path):
        return cmds.camera(path, query=1, horizontalFieldOfView=1)

    @classmethod
    def get_focal_length(cls, path):
        return _atr.Attribute.get_value(
            path, 'focalLength'
        )

    @classmethod
    def f_to_aov(cls, path):
        f = 35.0
        fbw = cmds.getAttr(path+'.horizontalFilmAperture')*25.4
        return math.degrees(2*math.atan(fbw/(2*f)))

    @classmethod
    def get_frustum_size(cls, path, distance):
        aov = cls.get_angle_of_view(path)
        w, h = _rdr.RenderSettings.get_resolution()
        w_ = math.tan(math.radians(aov/2))*distance*2
        h_ = w_*float(w)/float(h)
        return w_, h_


class Cameras(object):
    @classmethod
    def get_all(cls):
        return cmds.ls(type='camera', long=1) or []
