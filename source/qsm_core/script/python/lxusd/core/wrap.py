# coding:utf-8
import platform as _platform

import pkgutil as _pkgutil

import lxbasic.log as _log_core

USD_FLAG = False

__pypxr = _pkgutil.find_loader('pxr')

if __pypxr:
    USD_FLAG = True

    _log_core.Log.trace_method_result(
        'usd', 'load successful.'
    )

    from pxr import Usd, Sdf, Vt, Gf, Kind, UsdShade, UsdGeom, UsdLux
