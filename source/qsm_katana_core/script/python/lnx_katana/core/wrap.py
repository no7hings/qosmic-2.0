# coding:utf-8
import os as _os

import sys as _sys

KATANA_FLAG = False
KATANA_UI_FLAG = False

_ = _os.environ.get('KATANA_ROOT')

if _:
    KATANA_FLAG = True

    Katana = _sys.modules['Katana']

    NodegraphAPI = Katana.NodegraphAPI
    Nodes3DAPI = Katana.Nodes3DAPI
    KatanaFile = Katana.KatanaFile
    ResolutionTable = Katana.ResolutionTable
    FnGeolib = Katana.FnGeolib
    ScenegraphManager = Katana.ScenegraphManager
    Utils = Katana.Utils
    Callbacks = Katana.Callbacks
    Configuration = Katana.Configuration
    CacheManager = Katana.CacheManager
    RenderManager = Katana.RenderManager

    if Configuration.get('KATANA_UI_MODE') == '1':
        KATANA_UI_FLAG = True

        UI4 = _sys.modules['UI4']
        App = UI4.App

        Widgets = UI4.Widgets
        Manifest = UI4.Manifest
        UserNodes = Katana.UserNodes
