# coding:utf-8
from .. import abstracts as _abstracts


class GuiResourceManagerMain(_abstracts.AbsPrxPageForManager):
    GUI_KEY = 'manager'

    def __init__(self, window, session, *args, **kwargs):
        super(GuiResourceManagerMain, self).__init__(window, session, *args, **kwargs)
