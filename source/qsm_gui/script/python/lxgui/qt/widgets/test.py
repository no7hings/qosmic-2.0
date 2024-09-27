# coding:utf-8
import lxbasic.core as bsc_core
# qt
from ...qt.core.wrap import *


class QtTestForFit(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(QtTestForFit, self).__init__(*args, **kwargs)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        w, h = self.width(), self.height()
        painter.fillRect(
            QtCore.QRect(
                0, 0, self.width(), self.height()
            ),
            QtGui.QColor(255, 0, 0)
        )

        x_0, y_0, w_0, h_0 = bsc_core.BscSize.fit_to_center(
            (280, 40), (w, h)
        )

        painter.fillRect(
            QtCore.QRect(
                x_0, y_0, w_0, h_0
            ),
            QtGui.QColor(0, 255, 0)
        )


