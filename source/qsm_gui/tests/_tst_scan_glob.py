# coding:utf-8
from lxgui.qt.core.wrap import *

import lxbasic.scan as bsc_scan

import lxgui.qt.widgets as qt_widgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self._test()

    def _test(self):
        def fnc_(path_):
            print path_

        bsc_scan.ScanGlob.generate_glob_executor(
            'X:/QSM_TST/Assets/*/*/Rig/Final/scenes/*_Skin.ma', fnc_
        )


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    _w = MainWindow()
    _w.resize(640, 480)
    _w.show()
    sys.exit(app.exec_())
