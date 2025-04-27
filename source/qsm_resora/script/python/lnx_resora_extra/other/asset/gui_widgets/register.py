# coding:utf-8
from lnx_resora.gui import abstracts as lnx_rsr_gui_abstracts


class GuiResourceRegisterMain(lnx_rsr_gui_abstracts.AbsPrxSubpageForAssetRegister):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(GuiResourceRegisterMain, self).__init__(window, session, subwindow, *args, **kwargs)
