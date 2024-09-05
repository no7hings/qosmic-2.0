# coding:utf-8
import fnmatch

import lxbasic.core as bsc_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_gui.proxy.widgets as qsm_proxy_widgets


class W0(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W0, self).__init__(*args, **kwargs)

        self._widget = qsm_proxy_widgets.PrxInputForAsset()
        self.add_widget(self._widget)


if __name__ == '__main__':
    import sys
    # noinspection PyUnresolvedReferences
    from QtSide import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = W0()
    w.set_definition_window_size((480, 240))
    w.show_window_auto()
    #
    sys.exit(app.exec_())
