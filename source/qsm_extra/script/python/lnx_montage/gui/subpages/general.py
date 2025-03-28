# coding:utf-8
from ..abstracts import subpage_for_new_splicing as _subpage_for_adv


class PrxSubpageForNewGeneralSplicing(_subpage_for_adv.AbsPrxSubpageForNewSplicing):
    GUI_KEY = 'general'

    def __init__(self, *args, **kwargs):
        super(PrxSubpageForNewGeneralSplicing, self).__init__(*args, **kwargs)
