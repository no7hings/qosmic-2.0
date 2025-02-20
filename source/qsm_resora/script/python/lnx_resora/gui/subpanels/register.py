# coding:utf-8
from .. import abstracts as _abstracts

from ...resource_types.manifest.gui_widgets import register as _manifest_manifest_register

from ...resource_types.motion.gui_widgets import register as _subpage_motion_register

from ...resource_types.video.gui_widgets import register as _subpage_video_register

from ...resource_types.audio.gui_widgets import register as _subpage_audio_register

from ...resource_types.asset.gui_widgets import register as _subpage_asset_register


class PrxSubPanelForRegister(_abstracts.AbsPrxSubPanelForRegister):

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForRegister, self).__init__(window, session, *args, **kwargs)
