# coding:utf-8
import lxtool.manager.gui.abstracts as mng_gui_abstracts

import lxmaya.dcc.objects as mya_dcc_objects


class PnlManagerForAssetTextureDcc(mng_gui_abstracts.AbsPnlManagerForAssetTextureDcc):
    DCC_SELECTION_CLS = mya_dcc_objects.Selection
    DCC_NAMESPACE = 'maya'

    def __init__(self, *args, **kwargs):
        super(PnlManagerForAssetTextureDcc, self).__init__(*args, **kwargs)

    def _set_dcc_texture_references_update_(self):
        self._dcc_texture_references = mya_dcc_objects.TextureReferences()

    def _set_dcc_objs_update_(self):
        if self._dcc_texture_references is not None:
            self._dcc_objs = self._dcc_texture_references.get_objs()
