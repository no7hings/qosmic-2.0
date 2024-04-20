# coding:utf-8
import lxgui.proxy.widgets as utl_prx_widgets

import lxresolver.core as rsv_core


class TestWindow(utl_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self._test_()

    def _test_(self):
        tool_box = utl_prx_widgets.PrxHToolBoxNew()
        self.add_widget(tool_box)
        tool_box.set_expanded(True)

        tool = utl_prx_widgets.PrxIconPressButton()
        tool_box.add_widget(tool)
        tool.set_icon_name('application/python')

        tool = utl_prx_widgets.PrxIconPressButton()
        tool_box.add_widget(tool)
        tool.set_icon_name('application/python')

        tool_box = utl_prx_widgets.PrxVToolBoxNew()
        self.add_widget(tool_box)
        tool_box.set_expanded(True)

        tool = utl_prx_widgets.PrxIconPressButton()
        tool_box.add_widget(tool)
        tool.set_icon_name('application/python')

        tool = utl_prx_widgets.PrxIconPressButton()
        tool_box.add_widget(tool)
        tool.set_icon_name('application/python')


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
