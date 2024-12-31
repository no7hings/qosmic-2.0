# coding:utf-8
from ..abstracts import subpage_for_new_splicing as _subpage_for_new_splicing


class PrxSubpageForNewMocapSplicing(_subpage_for_new_splicing.AbsPrxSubpageForNewSplicing):
    GUI_KEY = 'mocap'

    def __init__(self, *args, **kwargs):
        super(PrxSubpageForNewMocapSplicing, self).__init__(*args, **kwargs)
