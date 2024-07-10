# coding:utf-8
import time

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxbasic.core as bsc_core

import lxgui.qt.core as gui_qt_core

import lxgui.proxy.scripts as prx_scripts


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self.test()

    def test(self):
        for i in range(10):
            i_thread = gui_qt_core.QtThreadWorkerForBuild.generate(self._qt_widget)
            i_thread.set_cache_fnc(lambda: (time.sleep(5), []))
            i_thread.set_entity(i)
            i_thread.start()


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap
    #
    app = wrap.QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((480, 480))
    w.show_window_auto()
    #
    sys.exit(app.exec_())
