# coding:utf-8
from .. import abstracts as lnc_gui_abstracts


class PnlLauncherForApplication(lnc_gui_abstracts.AbsPnlLauncherForApplication):
    def __init__(self, session, *args, **kwargs):
        super(PnlLauncherForApplication, self).__init__(session, *args, **kwargs)
