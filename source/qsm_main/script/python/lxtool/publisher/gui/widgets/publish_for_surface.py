# coding:utf-8
import lxgeneral.dcc.objects as gnl_dcc_objects
# publish
from .. import abstracts as pbs_gui_abstracts


class ValidatorOpt(pbs_gui_abstracts.AbsValidatorOpt):
    GUI_NAMESPACE = 'lynxi'
    DCC_NODE_CLS = gnl_dcc_objects.Node
    DCC_COMPONENT_CLS = gnl_dcc_objects.Component
    DCC_SELECTION_CLS = None
    DCC_PATHSEP = '/'

    def __init__(self, *args, **kwargs):
        super(ValidatorOpt, self).__init__(*args, **kwargs)


class PnlPublisherForSurface(pbs_gui_abstracts.AbsPnlPublisherForSurface):
    GUI_NAMESPACE = 'python'
    DCC_VALIDATOR_OPT_CLS = ValidatorOpt

    def __init__(self, session, *args, **kwargs):
        super(PnlPublisherForSurface, self).__init__(session, *args, **kwargs)
