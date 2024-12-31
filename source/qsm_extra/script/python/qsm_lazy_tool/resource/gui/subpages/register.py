# coding:utf-8
from .. import abstracts as _abstracts


class PrxSubpageForMotionRegister(_abstracts.AbsPrxSubpageForMotionRegister):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(PrxSubpageForMotionRegister, self).__init__(window, session, subwindow, *args, **kwargs)


class PrxSubpageForVideoRegister(_abstracts.AbsPrxSubpageForVideoRegister):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(PrxSubpageForVideoRegister, self).__init__(window, session, subwindow, *args, **kwargs)


class PrxSubpageForAudioRegister(_abstracts.AbsPrxSubpageForAudioRegister):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(PrxSubpageForAudioRegister, self).__init__(window, session, subwindow, *args, **kwargs)


class PrxSubpageForAssetRegister(_abstracts.AbsPrxSubpageForAssetRegister):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(PrxSubpageForAssetRegister, self).__init__(window, session, subwindow, *args, **kwargs)
