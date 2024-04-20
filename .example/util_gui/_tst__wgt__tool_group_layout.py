# coding:utf-8

import lxgui.proxy.widgets as prx_widgets

import lxgui.qt.widgets as qt_widgets

import lxresolver.core as rsv_core


class TestWindow(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self._test_()

    def _test_(self):
        scheme = 'test-tool'
        s = prx_widgets.PrxVScrollArea()
        self.add_widget(s)

        ss = ['python', 'maya', 'katana', 'houdini']*5

        lot = qt_widgets.QtToolGroupVLayoutWidget()
        s.add_widget(lot)
        lot._set_drop_enable_(True)

        for i in range(5):
            i_n = qt_widgets.QtHToolGroupStyleB()
            lot._add_widget_(i_n)
            i_n._set_name_text_('tool group {}'.format(i))
            i_n._set_expanded_(True)
            i_n._set_drag_enable_(True)

            i_w = prx_widgets.PrxToolGridLayoutWidget()
            i_n._add_widget_(i_w._qt_widget)
            i_w.set_drop_enable(True)
            i_w.set_item_size(48, 96)
            i_w.set_drag_and_drop_scheme(scheme)
            for j in range(7):
                j_b = prx_widgets.PrxIconPressButton()
                i_w.add_widget(j_b)
                j_b.set_drag_enable(True)
                j_b.set_icon_name('application/{}'.format(ss[j]))
                j_b.set_name('tool {}'.format(j))
                j_b.set_drag_and_drop_scheme('test-tool')


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
