# coding:utf-8
from lxgui.qt.core.wrap import *

import lxgui.qt.core as qt_core

import lxgui.qt.widgets as qt_widgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        menu = qt_widgets.QtMenuNew(self)
        menu.setTitle('test')
        self.menuBar().addMenu(menu)
        menu._set_menu_data_(
            [
                ('test', 'file/file', self._test),
                ('test', 'file/file', self._test),
                ('test', 'file/file', self._test),
                ('test', 'file/file', self._test)
            ]
        )

    def _test(self):
        pass


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    _w = MainWindow()
    _w.resize(640, 480)
    _w.show()
    sys.exit(app.exec_())
