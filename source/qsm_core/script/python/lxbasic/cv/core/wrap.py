# coding:utf-8
import pkgutil as _pkgutil

import lxbasic.log as _log_core

CV2_FLAG = False


_cv2 = _pkgutil.find_loader('cv2')

if _cv2:
    CV2_FLAG = True

    _log_core.Log.trace_method_result(
        'cv2', 'load successful'
    )

    import cv2
