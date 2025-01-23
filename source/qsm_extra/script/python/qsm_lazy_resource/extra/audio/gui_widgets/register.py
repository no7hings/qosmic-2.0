# coding:utf-8
from ....gui import abstracts as _abstracts


class PrxSubpageForAudioRegister(_abstracts.AbsPrxSubpageForAudioRegister):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(PrxSubpageForAudioRegister, self).__init__(window, session, subwindow, *args, **kwargs)
