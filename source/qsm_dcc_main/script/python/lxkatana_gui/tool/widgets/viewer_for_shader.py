# coding:utf-8
import lxtool.viewer.gui.abstracts as vwr_gui_abstracts

import lxkatana.dcc.objects as ktn_dcc_objects

import lxkatana.fnc.objects as ktn_fnc_objects


class PnlViewerForShaderDcc(vwr_gui_abstracts.AbsPnlViewerForShaderDcc):
    """
# coding:utf-8
import lxkatana

lxkatana.set_reload()
import lxsession.commands as ssn_commands; ssn_commands.execute_hook("dcc-tools/katana/shader-viewer")
    """
    DCC_SCENE_CLS = ktn_dcc_objects.Scene
    DCC_FNC_LOOK_IMPORTER_CLS = ktn_fnc_objects.FncImporterForLookAssOld
    #
    DCC_MATERIALS_CLS = ktn_dcc_objects.Materials
    DCC_SHADER_CLS = ktn_dcc_objects.AndShader
    #
    DCC_SELECTION_CLS = ktn_dcc_objects.Selection

    def __init__(self, *args, **kwargs):
        super(PnlViewerForShaderDcc, self).__init__(*args, **kwargs)
