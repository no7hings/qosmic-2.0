# coding:utf-8

import lxgui.proxy.widgets as prx_widgets

import lxgui.qt.widgets as qt_widgets

import lxresolver.core as rsv_core


class TestWindow(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self._test_()

    def _test_(self):
        n = prx_widgets.PrxTabView()
        n.set_drag_enable(True)
        self.set_main_style_mode(1)
        self.add_widget(n)
        for i in range(5):
            i_w = qt_widgets.QtTextBubble()
            i_w._set_text_(str(i))
            n.add_widget(
                i_w, name='a - {}'.format((i*2+1)*'0'), icon_name_text=str(i)
            )


if __name__ == '__main__':
    import time
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    w = TestWindow()
    #
    w.set_window_show()
    #
    sys.exit(app.exec_())
