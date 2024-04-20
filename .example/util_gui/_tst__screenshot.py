# coding:utf-8
from lxgui.qt.widgets import utility

import lxgui.proxy.widgets as prx_widgets


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = prx_widgets.PrxScreenshotFrame()
    w.set_start()
    #
    sys.exit(app.exec_())
