# coding:utf-8
import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets


class AbsPrxPageForTaskOverview(gui_prx_widgets.PrxBasePage):
    GUI_KEY = 'task_overview'

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForTaskOverview, self).__init__(window, session, *args, **kwargs)
