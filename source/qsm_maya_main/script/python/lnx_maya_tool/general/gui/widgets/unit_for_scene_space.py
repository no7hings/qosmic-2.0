# coding:utf-8
import lnx_dcc_tool.generate.gui.abstracts as _gnl_gui_abstracts

import qsm_maya.core as qsm_maya_core


class PrxUnitForSceneSpace(_gnl_gui_abstracts.AbsPrxUnitForSceneSpace):
    def __init__(self, *args, **kwargs):
        super(PrxUnitForSceneSpace, self).__init__(*args, **kwargs)

        self.set_scene_gain_fnc(
            qsm_maya_core.SceneFile.get_current
        )
