# coding:utf-8
import sys

from .wrap import *


class ViewPanel:
    @classmethod
    def _set_viewport_shader_display_mode_(cls, name):
        cmds.modelEditor(
            name,
            edit=1,
            useDefaultMaterial=0,
            displayAppearance='smoothShaded',
            displayTextures=0,
            displayLights='default',
            shadows=0
        )

    @classmethod
    def _set_viewport_texture_display_mode_(cls, name):
        cmds.modelEditor(
            name,
            edit=1,
            useDefaultMaterial=0,
            displayAppearance='smoothShaded',
            displayTextures=1,
            displayLights='default',
            shadows=0
        )

    @classmethod
    def _set_viewport_light_display_mode_(cls, name):
        cmds.modelEditor(
            name,
            edit=1,
            useDefaultMaterial=0,
            displayAppearance='smoothShaded',
            displayTextures=1,
            displayLights='all',
            shadows=1
        )

    @classmethod
    def set_render_mode(cls, name, texture_enable=True, light_enable=True, shadow_enable=True):
        cmds.modelEditor(
            name,
            edit=1,
            useDefaultMaterial=0,
            displayAppearance='smoothShaded',
            displayTextures=texture_enable,
            displayLights='all' if light_enable is True else 'default',
            shadows=shadow_enable
        )

    @classmethod
    def set_display_mode(cls, name, display_mode):
        if display_mode == 5:
            cls._set_viewport_shader_display_mode_(name)
        elif display_mode == 6:
            cls._set_viewport_texture_display_mode_(name)
        elif display_mode == 7:
            cls._set_viewport_light_display_mode_(name)


class ViewPanels:
    @classmethod
    def get_all_names(cls):
        return cmds.getPanel(typ='modelPanel')

    @classmethod
    def get_current_name(cls):
        return cmds.paneLayout('viewPanes', q=True, pane1=True)

    @classmethod
    def isolate_select(cls, boolean):
        for i in cls.get_all_names():
            cmds.isolateSelect(i, state=boolean)

    @classmethod
    def isolate_select_for(cls, paths, boolean):
        for i in cls.get_all_names():
            cmds.isolateSelect(i, state=boolean)
            for j in paths:
                cmds.isolateSelect(i, addDagObject=j)


class ViewPanelIsolateSelectOpt(object):
    def __init__(self, panel_name='modelPanel4'):
        self._panel_name = panel_name

    def set_enable(self, boolean):
        cmds.isolateSelect(self._panel_name, state=boolean)

    def is_enable(self):
        return cmds.isolateSelect(self._panel_name, state=1, query=1)

    def add_node(self, path):
        cmds.isolateSelect(self._panel_name, addDagObject=path)

    def add_nodes(self, paths):
        [self.add_node(i) for i in paths]

    def remove_node(self, path):
        cmds.isolateSelect(self._panel_name, removeDagObject=path)

    def remove_nodes(self, paths):
        [self.remove_node(i) for i in paths]


class ViewportProject:
    """
    from chatgpt, compute a point from mouse project in viewport
    """
    @classmethod
    def screen_to_world(cls, mouse_x, mouse_y):
        view = omui.M3dView.active3dView()
        width, height = view.portWidth(), view.portHeight()

        # adjust Y coordinate (special handling for Maya's screen coordinate system)
        mouse_y = height-mouse_y

        # initialize near point
        pos_near = om.MPoint()

        # initialize far point
        pos_far = om.MPoint()

        try:
            # Get the world coordinates of the view's ray
            view.viewToWorld(int(mouse_x), int(mouse_y), pos_near, pos_far)
        except:
            sys.stderr.write('viewToWorld failed.\n')
            return None, None

        # if near and far points are the same, the ray is invalid
        if pos_near.isEquivalent(pos_far):
            sys.stderr.write('near and far points are the same, cannot generate ray.\n')
            return

        return pos_near, pos_far

    @classmethod
    def get_mouse_pos(cls):
        # noinspection PyUnresolvedReferences
        from PySide2 import QtGui, QtWidgets

        # Get the current mouse position
        widget = QtWidgets.QApplication.widgetAt(QtGui.QCursor.pos())
        if not widget:
            sys.stderr.write('Cannot find widget under mouse.\n')
            return

        # Map global mouse position to widget's local coordinates
        local_pos = widget.mapFromGlobal(QtGui.QCursor.pos())
        return local_pos.x(), local_pos.y()

    @classmethod
    def ray_intersect_plane(cls, ray_origin, ray_direction, plane_normal=(0, 1, 0), plane_point=(0, 0, 0)):
        if ray_direction.length() < 1e-6:
            sys.stderr.write('Invalid ray_direction.\n')
            return None

        plane_normal = om.MVector(*plane_normal)
        plane_point = om.MVector(*plane_point)

        # Calculate the denominator for the ray-plane intersection formula
        denominator = plane_normal*ray_direction
        if abs(denominator) < 1e-6:
            return None

        # Calculate the intersection point of the ray and the plane
        t = (plane_point-ray_origin)*plane_normal/denominator
        if t < 0:
            return None

        intersection = ray_origin+ray_direction*t

        # Force the y value to 0 to ensure the Locator is on the horizontal plane
        intersection.y = 0

        return intersection

    @classmethod
    def compute_point_at_mouse(cls):
        mouse_x, mouse_y = cls.get_mouse_pos()

        # get the corresponding world coordinates for the mouse
        pos_args = cls.screen_to_world(mouse_x, mouse_y)
        if not pos_args:
            sys.stderr.write('Failed to get near or far points, exiting.\n')
            return

        # create ray_origin and ray_direction
        pos_near, pos_far = pos_args
        ray_origin = om.MVector(pos_near.x, pos_near.y, pos_near.z)
        ray_direction = om.MVector(pos_far.x-pos_near.x, pos_far.y-pos_near.y, pos_far.z-pos_near.z)

        if ray_direction.length() < 1e-6:
            sys.stderr.write('ray_direction is too small, exiting.\n')
            return

        # normalize the ray direction
        ray_direction.normalize()

        # calculate intersection of the ray with the plane
        intersection = cls.ray_intersect_plane(ray_origin, ray_direction)

        if not intersection:
            sys.stderr.write('ray does not intersect with the plane.\n')
            return

        return intersection.x, intersection.y, intersection.z
