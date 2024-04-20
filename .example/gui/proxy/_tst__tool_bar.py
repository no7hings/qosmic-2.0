# coding:utf-8
import lxgui.proxy.widgets as prx_widgets

import lxresolver.core as rsv_core


class TestWindow(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self._test_()

    def _test_(self):
        tool_bar = prx_widgets.PrxHToolBar()
        self.add_widget(tool_bar)
        tool_bar.set_left_alignment()
        tool_bar.set_expanded(True)
        #
        tool_box = prx_widgets.PrxHToolBoxNew()
        tool_bar.add_widget(tool_box)
        tool_box.set_expanded(True)

        for i in range(20):
            i_tool = prx_widgets.PrxIconPressButton()
            tool_box.add_widget(i_tool)
            i_tool.set_icon_name('application/python')


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
