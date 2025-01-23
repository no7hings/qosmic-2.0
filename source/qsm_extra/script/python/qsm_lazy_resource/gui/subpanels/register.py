# coding:utf-8
from .. import abstracts as _abstracts

from ...extra.motion.gui_widgets import register as _subpage_motion_register

from ...extra.video.gui_widgets import register as _subpage_video_register

from ...extra.audio.gui_widgets import register as _subpage_audio_register

from ...extra.asset.gui_widgets import register as _subpage_asset_register


class PrxSubPanelForRegister(_abstracts.AbsPrxSubPanelForRegister):
    SUB_PAGE_CLASS_DICT = dict(
        # motion
        motion=_subpage_motion_register.PrxSubpageForMotionRegister,
        # media
        video=_subpage_video_register.PrxSubpageForVideoRegister,
        audio=_subpage_audio_register.PrxSubpageForAudioRegister,
        # asset
        asset=_subpage_asset_register.PrxSubpageForAssetRegister,
    )

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForRegister, self).__init__(window, session, *args, **kwargs)
