# coding:utf-8
import pkgutil as _pkgutil

import lxbasic.log as _log_core

CGT_FLAG = False

_module = _pkgutil.find_loader('cgtw2')

if _module:
    CGT_FLAG = True

    _log_core.Log.trace_method_result(
        'cgtw2', 'load successful.'
    )

    # noinspection PyUnresolvedReferences
    import cgtw2
