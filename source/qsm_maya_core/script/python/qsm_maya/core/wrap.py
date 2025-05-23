# coding:utf-8
import os as _os

import sys as _sys

MAYA_FLAG = False
MAYA_UI_FLAG = False

_ = _os.environ.get('MAYA_APP_DIR')

if _:
    MAYA_FLAG = True
    # base
    # noinspection PyUnresolvedReferences
    import maya
    # noinspection PyRedeclaration
    maya = _sys.modules['maya']

    cmds = maya.cmds

    mel = maya.mel

    # api
    OpenMayaUI = maya.OpenMayaUI
    omui = OpenMayaUI

    OpenMaya = maya.OpenMaya
    om = OpenMaya
    OpenMaya2 = maya.api.OpenMaya
    om2 = OpenMaya2

    # xgen
    # noinspection PyUnresolvedReferences
    import xgenm
    # noinspection PyRedeclaration
    xg = xgenm

    xgg = xgenm.xgGlobal

    # gui
    shiboken2 = _sys.modules.get('shiboken2')
    PySide2 = _sys.modules.get('PySide2')
    QtWidgets = PySide2.QtWidgets
    QtCore = PySide2.QtCore
    QtGui = PySide2.QtGui
