# coding:utf-8
from .. import abstracts as _abstracts

from ..subpages import register as _subpage_register


class PrxSubPanelForRegister(_abstracts.AbsPrxSubPanelForRegister):
    SUB_PAGE_CLASS_DICT = dict(
        # motion
        motion=_subpage_register.PrxSubpageForMotionRegister,
        # media
        video=_subpage_register.PrxSubpageForVideoRegister,
        audio=_subpage_register.PrxSubpageForAudioRegister,
        # asset
        asset=_subpage_register.PrxSubpageForAssetRegister,
    )

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForRegister, self).__init__(window, session, *args, **kwargs)
