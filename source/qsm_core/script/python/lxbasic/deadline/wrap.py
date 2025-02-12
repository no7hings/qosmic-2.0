# coding:utf-8
import pkgutil as _pkgutil

import lxbasic.log as _log_core

DEADLINE_FLAG = False

_deadline = _pkgutil.find_loader('Deadline')

if _deadline:
    DEADLINE_FLAG = True

    _log_core.Log.trace_method_result(
        'deadline', 'load successful'
    )
    # noinspection PyUnresolvedReferences
    from Deadline import DeadlineConnect
