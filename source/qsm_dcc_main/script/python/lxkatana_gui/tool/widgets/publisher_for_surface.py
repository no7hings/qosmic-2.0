# coding:utf-8
import lxtool.publisher.gui.abstracts as pbs_gui_abstracts

import lxkatana.dcc.objects as ktn_dcc_objects


class ValidatorOpt(pbs_gui_abstracts.AbsValidatorOpt):
    DCC_NAMESPACE = 'katana'
    DCC_NODE_CLS = ktn_dcc_objects.Node
    DCC_SELECTION_CLS = ktn_dcc_objects.Selection
    DCC_PATHSEP = '/'

    def __init__(self, *args, **kwargs):
        super(ValidatorOpt, self).__init__(*args, **kwargs)


class PnlPublisherForSurface(pbs_gui_abstracts.AbsPnlPublisherForSurface):
    DCC_VALIDATOR_OPT_CLS = ValidatorOpt

    def __init__(self, session, *args, **kwargs):
        super(PnlPublisherForSurface, self).__init__(session, *args, **kwargs)

    def _get_dcc_scene_file_path_(self):
        return ktn_dcc_objects.Scene.get_current_file_path()
