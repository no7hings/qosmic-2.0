# coding:utf-8
import lxuniverse.objects as unv_objects

import lxbasic.dcc.objects as bsc_dcc_objects
#
from ... import abstracts as usd_abstracts


class Scene(usd_abstracts.AbsUsdObjScene):
    FILE_CLS = bsc_dcc_objects.StgFile
    UNIVERSE_CLS = unv_objects.ObjUniverse

    def __init__(self):
        super(Scene, self).__init__()
