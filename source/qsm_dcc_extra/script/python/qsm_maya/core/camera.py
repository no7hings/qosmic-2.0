# coding:utf-8
import math
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.OpenMaya as om
# noinspection PyUnresolvedReferences
import maya.OpenMayaUI as om_ui

from . import node as _node

from . import shape as _node_for_shape

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
    def generate_mask_nodes(cls, path, type_includes=None):
        def filter_fnc_(path_):
            if type_includes is None:
                return True
            if cmds.nodeType(path_) in type_includes:
                return True
            return False

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
            if _node.Node.is_exists(i_shape_path) is True:
                if filter_fnc_(i_shape_path) is True:
                    list_.append(i_shape_path)

        return list_

    @classmethod
    def get_active(cls):
        view = om_ui.M3dView.active3dView()
        camera_dag_path = om.MDagPath()
        view.getCamera(camera_dag_path)
        return camera_dag_path.fullPathName()

    @classmethod
    def get_non_default_with_dialog(cls):
        import lxgui.core as gui_core

        cameras = Cameras.get_all()

        path_map = {}
        non_default_names = []
        for i_camera in cameras:
            i_transform = _node_for_shape.Shape.get_transform(i_camera)
            i_name = _node_for_shape.Shape.to_name(i_transform)
            path_map[i_name] = i_camera
            if i_name not in Cameras.DEFAULT_NAMES:
                non_default_names.append(i_name)

        if non_default_names:
            if len(non_default_names) > 1:
                options = non_default_names
                result = gui_core.GuiApplication.exec_input_dialog(
                    type='choose',
                    info='Choose a camera...',
                    options=options,
                    value=options[0],
                    title='Camera'
                )
                if result:
                    return path_map[result]
            return path_map[non_default_names[0]]
        return Camera.get_active()

    @classmethod
    def get_angle_of_view(cls, path):
        return cmds.camera(path, query=1, horizontalFieldOfView=1)

    @classmethod
    def get_focal_length(cls, path):
        return _atr.NodeAttribute.get_value(
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

    @classmethod
    def generate_camera_preview(cls):
        pass


class Cameras(object):
    DEFAULT_NAMES = [
        'persp',
        'top',
        'front',
        'side'
    ]

    @classmethod
    def get_all(cls):
        return cmds.ls(type='camera', long=1) or []
