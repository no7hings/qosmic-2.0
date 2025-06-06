# coding:utf-8
from ..abstracts import subpanel_for_new_splicing as _subpanel_for_new_splicing

from ..subpages import general as _subpage_new_general


class PrxSubPanelForNewSplicing(_subpanel_for_new_splicing.AbsPrxSubpanelForNewSplicing):
    SUBPAGE_CLASSES = [
        _subpage_new_general.PrxSubpageForNewGeneralSplicing,
    ]

    def __init__(self, *args, **kwargs):
        super(PrxSubPanelForNewSplicing, self).__init__(*args, **kwargs)
