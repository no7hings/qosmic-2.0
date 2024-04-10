# coding:utf-8
from .. import abstracts as grh_gui_abstracts


class PnlAssetLineup(grh_gui_abstracts.AbsPnlAssetLineup):

    def __init__(self, session, *args, **kwargs):
        super(PnlAssetLineup, self).__init__(session, *args, **kwargs)