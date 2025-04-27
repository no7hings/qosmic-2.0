# coding:utf-8
import lnx_resora.gui.abstracts as lnx_rsr_gui_abstracts


class GuiResourceManagerMain(lnx_rsr_gui_abstracts.AbsPrxPageForManager):
    GUI_KEY = 'manager'

    def __init__(self, window, session, *args, **kwargs):
        super(GuiResourceManagerMain, self).__init__(window, session, *args, **kwargs)
