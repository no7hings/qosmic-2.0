# coding:utf-8
from lxgui.qt.core.wrap import *

import lxbasic.scan as bsc_scan

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._b = qt_widgets.QtInputForContent()
        self.add_widget(self._b)

        self._executor = None

        self._test()

    def _test(self):
        def result_fnc_(path_):
            self._b._append_value_use_signal_(path_)

        def finished_fnc_():
            self._b._append_value_use_signal_('finished')

        self._executor = bsc_scan.ScanGlob.concurrent_glob_file(
            'X:/QSM_TST/Assets/*/*/Rig/Final/scenes/*_Skin.ma', result_fnc_, finished_fnc_
        )


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((480, 480))
    w.show_window_auto()
    #
    sys.exit(app.exec_())

