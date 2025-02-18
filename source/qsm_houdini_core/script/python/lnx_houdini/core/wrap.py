# coding:utf-8
import os as _os

import sys as _sys

HOUDINI_FLAG = False
HOUDINI_UI_FLAG = False

_ = _os.environ.get('HIP')

if _:
    HOUDINI_FLAG = True
    # noinspection PyUnresolvedReferences
    import hou
    # noinspection PyRedeclaration
    hou = _sys.modules['hou']
