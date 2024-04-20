# coding:utf-8
import os

import lxbasic.storage as bsc_storage

import lxgui.qt.widgets as qt_widgets


import lxgui.proxy.widgets as prx_widgets

y_f = '{}.yml'.format(os.path.splitext(__file__)[0])

c = bsc_storage.StgFileOpt(y_f).set_read()


class TestWindow(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self.set_definition_window_size([480, 480])
        self._test_()

    def _test_(self):
        s = prx_widgets.PrxVScrollArea()
        self.add_widget(s)

        w_3 = qt_widgets.QtLayer()
        s.add_widget(w_3)
        w_4 = prx_widgets.PrxTreeView()
        w_3._add_widget_(w_4._qt_widget)

        btn_3 = qt_widgets.QtPressButton()
        s.add_widget(btn_3)
        btn_3._set_name_text_('Show')
        btn_3.press_clicked.connect(
            w_3._show_delay_
        )

        btn_4 = qt_widgets.QtPressButton()
        s.add_widget(btn_4)
        btn_4._set_name_text_('Hide')
        btn_4.press_clicked.connect(
            w_3._hide_delay_
        )


if __name__ == '__main__':
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
