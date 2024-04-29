# coding:utf-8
from lxgui.qt.widgets import utility

import lxgui.proxy.widgets as prx_widgets


if __name__ == '__main__':
    import sys
    #
    from QtSide import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = prx_widgets.PrxScreenshotFrame()
    w.do_start()
    #
    sys.exit(app.exec_())
