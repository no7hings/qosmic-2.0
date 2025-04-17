# coding:utf-8
import pkgutil as _pkgutil

CV2_FLAG = False

_module = _pkgutil.find_loader('cv2')

if _module:
    CV2_FLAG = True

    import lxbasic.log as _log_core

    _log_core.Log.trace_method_result(
        'cv2', 'load successful.'
    )

    # noinspection PyUnresolvedReferences
    import cv2
    # noinspection PyUnresolvedReferences
    import numpy
