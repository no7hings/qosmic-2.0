# coding:utf-8
from ..abstracts import subpage_for_new_splicing as _subpage_for_adv


class PrxSubpageForNewAdvSplicing(_subpage_for_adv.AbsPrxSubpageForNewSplicing):
    GUI_KEY = 'adv'

    def __init__(self, *args, **kwargs):
        super(PrxSubpageForNewAdvSplicing, self).__init__(*args, **kwargs)
