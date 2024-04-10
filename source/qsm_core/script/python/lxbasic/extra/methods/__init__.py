# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core


def get_module(framework_scheme):
    return bsc_core.PyModule(
        'lxbasic.extra.methods.{}'.format(framework_scheme)
    ).get_module()


if bsc_core.EnvExtraMtd.get_scheme() == 'default':
    bsc_log.Log.trace_method_result(
        'extra script',
        'load scheme: "default"'
    )
    from .default import *
elif bsc_core.EnvExtraMtd.get_scheme() == 'new':
    bsc_log.Log.trace_method_result(
        'extra script',
        'load scheme: "new"'
    )
    from .new import *
else:
    bsc_log.Log.trace_method_result(
        'extra script',
        'load scheme: "new"'
    )
    from .default import *

