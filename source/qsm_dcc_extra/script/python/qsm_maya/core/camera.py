# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class Cameras(object):
    @classmethod
    def get_all(cls):
        return cmds.ls(type='camera', long=1) or []

    @classmethod
    def get_active_camera(cls):
        # noinspection PyUnresolvedReferences
        from maya import OpenMaya, OpenMayaUI
        view = OpenMayaUI.M3dView.active3dView()
        camera_dag_path = OpenMaya.MDagPath()
        view.getCamera(camera_dag_path)
        return camera_dag_path.fullPathName()
