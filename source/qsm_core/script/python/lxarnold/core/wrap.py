# coding:utf-8
import pkgutil as _pkgutil

import sys as _sys

ARNOLD_FLAG = False

__arnold = _pkgutil.find_loader('arnold')

if __arnold:
    ARNOLD_FLAG = True
    # noinspection PyUnresolvedReferences
    import arnold

    ai = arnold
