# coding:utf-8
import lxgui.proxy.widgets as gui_prx_widgets

import lxresolver.core as rsv_core


class TestWindow(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self._test_()

    def _test_(self):
        button = gui_prx_widgets.PrxPressButton()
        self.add_widget(button)
        button.set_name('test')
        # button.set_status(button.ProcessStatus.Started)
        button.initialization(100, button.ProcessStatus.Started)
        button.set_status_at(0, button.ProcessStatus.Running)
        button.set_status_at(5, button.ProcessStatus.Running)

        # for i in range(100):
        #     button.set_status_at(i, button.ProcessStatus.Running)
        #     button.set_finished_at(i, button.ProcessStatus.Completed)


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
    #
    sys.exit(app.exec_())
