# coding=utf-8
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *


class QtStatusBar(
    QtWidgets.QWidget
):
    def __init__(self, *args, **kwargs):
        super(QtStatusBar, self).__init__(*args, **kwargs)

        self.setFixedHeight(gui_core.GuiSize.InputHeight)
