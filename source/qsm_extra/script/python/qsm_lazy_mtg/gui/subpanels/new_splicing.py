# coding:utf-8
from ..abstracts import subpanel_for_new_splicing as _subpanel_for_new_splicing

from ..subpages import mocap as _subpage_new_mocap

from ..subpages import adv as _subpage_new_adv


class PrxSubPanelForNewSplicing(_subpanel_for_new_splicing.AbsPrxSubpanelForNewSplicing):
    SUB_PAGE_CLASSES = [
        _subpage_new_adv.PrxSubpageForNewAdvSplicing,
        _subpage_new_mocap.PrxSubpageForNewMocapSplicing,
    ]

    def __init__(self, *args, **kwargs):
        super(PrxSubPanelForNewSplicing, self).__init__(*args, **kwargs)
