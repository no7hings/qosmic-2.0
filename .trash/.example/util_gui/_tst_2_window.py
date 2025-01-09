# coding:utf-8

import lxgui.proxy.widgets as gui_prx_widgets


class TestWindow(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)

    def _test_(self):
        pass


if __name__ == '__main__':
    import time
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    w = TestWindow()
    #
    w.show_window_auto()
    w._test_()
    #
    sys.exit(app.exec_())
