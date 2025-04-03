# coding:utf-8
import platform as _platform

import pkgutil as _pkgutil

import lxbasic.log as _log_core
# qt
from ...qt.core.wrap import *

QT_USD_FLAG = False
QT_USD_VIEWPORT_FLAG = False

__pypxr = _pkgutil.find_loader('pxr')

if __pypxr and QT_LOAD_INDEX == 1:
    QT_USD_FLAG = True

    _log_core.Log.trace_method_result(
        'qt for usd', 'load successful.'
    )

    from pxr import Usd, Sdf, Vt, Gf, Glf, Tf, Kind, UsdShade, UsdGeom, UsdLux

    from pxr import Usdviewq, UsdAppUtils, UsdImagingGL

    if hasattr(Usdviewq, '_usdviewq'):
        QT_USD_VIEWPORT_FLAG = True

