# coding:utf-8
import pkgutil as _pkgutil

import sys as _sys

CLARISSE_FLAG = False

__ix = _pkgutil.find_loader('ix')

if __ix:
    CLARISSE_FLAG = True
    # noinspection PyUnresolvedReferences
    import ix
    # noinspection PyRedeclaration
    ix = _sys.modules['ix']
