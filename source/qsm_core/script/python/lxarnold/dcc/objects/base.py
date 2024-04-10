# coding:utf-8
import lxuniverse.objects as unv_objects

import lxbasic.dcc.objects as bsc_dcc_objects
# arnold
from ...core.wrap import *

from ... import abstracts as and_abstracts


class Scene(and_abstracts.AbsObjScene):
    if ARNOLD_FLAG is True:
        AR_OBJ_CATEGORY_MASK = [
            ai.AI_NODE_SHAPE,
            ai.AI_NODE_SHADER,
        ]

    FILE_CLS = bsc_dcc_objects.StgFile
    UNIVERSE_CLS = unv_objects.ObjUniverse

    def __init__(self, option=None):
        super(Scene, self).__init__(option=option)
