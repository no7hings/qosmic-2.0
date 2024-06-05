# coding:utf-8
import lxgeneral.dcc.objects as gnl_dcc_objects
# comparer
from .. import abstracts as cpr_gui_abstracts


class ComparerOpt(cpr_gui_abstracts.AbsDccComparerOpt):
    GUI_NAMESPACE = 'lynxi'
    DCC_NODE_CLS = gnl_dcc_objects.Node
    DCC_COMPONENT_CLS = gnl_dcc_objects.Component
    DCC_SELECTION_CLS = None
    DCC_PATHSEP = '/'

    def __init__(self, *args, **kwargs):
        super(ComparerOpt, self).__init__(*args, **kwargs)


class PnlComparerForAssetGeometry(cpr_gui_abstracts.AbsPnlComparerForAssetGeometry):
    DCC_COMPARER_OPT_CLS = ComparerOpt

    def __init__(self, session, *args, **kwargs):
        super(PnlComparerForAssetGeometry, self).__init__(session, *args, **kwargs)

