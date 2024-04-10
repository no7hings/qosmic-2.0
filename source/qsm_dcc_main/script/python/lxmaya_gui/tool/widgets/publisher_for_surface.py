# coding:utf-8
import lxtool.publisher.gui.abstracts as pbs_gui_abstracts

import lxmaya.dcc.objects as mya_dcc_objects


class ValidatorOpt(pbs_gui_abstracts.AbsValidatorOpt):
    DCC_NAMESPACE = 'maya'
    DCC_NODE_CLS = mya_dcc_objects.Node
    DCC_COMPONENT_CLS = mya_dcc_objects.Component
    DCC_SELECTION_CLS = mya_dcc_objects.Selection
    DCC_PATHSEP = '|'

    def __init__(self, *args, **kwargs):
        super(ValidatorOpt, self).__init__(*args, **kwargs)


class PnlPublisherForSurface(pbs_gui_abstracts.AbsPnlPublisherForSurface):
    DCC_VALIDATOR_OPT_CLS = ValidatorOpt

    def __init__(self, session, *args, **kwargs):
        super(PnlPublisherForSurface, self).__init__(session, *args, **kwargs)

    def _get_dcc_scene_file_path_(self):
        return mya_dcc_objects.Scene.get_current_file_path()
