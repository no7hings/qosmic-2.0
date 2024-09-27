# coding:utf-8
from .. import abstracts as _abstracts


class PrxSubPageForMotionRegister(_abstracts.AbsPrxSubPageForMotionRegister):
    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(PrxSubPageForMotionRegister, self).__init__(window, session, sub_window, *args, **kwargs)


class PrxSubPageForVideoRegister(_abstracts.AbsPrxSubPageForVideoRegister):
    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(PrxSubPageForVideoRegister, self).__init__(window, session, sub_window, *args, **kwargs)


class PrxSubPageForAudioRegister(_abstracts.AbsPrxSubPageForAudioRegister):
    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(PrxSubPageForAudioRegister, self).__init__(window, session, sub_window, *args, **kwargs)
