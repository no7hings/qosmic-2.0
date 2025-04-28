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
    omui = maya.OpenMayaUI

    om = maya.OpenMaya
    om2 = maya.api.OpenMaya
    # xgen
    # noinspection PyUnresolvedReferences
    import xgenm
    # noinspection PyRedeclaration
    xg = xgenm

    xgg = xgenm.xgGlobal
