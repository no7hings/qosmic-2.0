# coding:utf-8
import sys

from lxgui.qt.core.wrap import *


class S(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super(S, self).__init__(*args, **kwargs)
        self._s = QtWidgets.QGraphicsScene()

        self.installEventFilter(self)

        self.setScene(self._s)

        i = QtWidgets.QGraphicsRectItem()
        i.setFlags(
            i.ItemIsMovable | i.ItemIsSelectable
        )
        i.setRect(
            0, 0, 40, 40
        )
        self._s.addItem(
            i
        )

        self._p = QtCore.QPoint()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                pass
            elif event.type() == QtCore.QEvent.Wheel:
                self._set_scale_(event)
        return False

    def _set_translate_start_(self, event):
        pass

    def _set_translate_execute_(self, event):
        pass

    def _set_translate_stop_(self, event):
        pass

    def _set_scale_(self, event):
        pass


app = QtWidgets.QApplication(sys.argv)

w = S()

w.setFixedSize(480, 480)
w.show()

sys.exit(app.exec_())

