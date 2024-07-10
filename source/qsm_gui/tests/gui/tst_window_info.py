# coding:utf-8
import time

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxbasic.core as bsc_core

import lxgui.qt.core as gui_qt_core

import lxgui.proxy.scripts as prx_scripts

import qsm_general.core as qsm_gnl_core


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        button = gui_prx_widgets.PrxPressButton()
        self.add_widget(button)
        button.set_name('TEST')

        button.connect_press_clicked_to(self._test)

    def _test(self):
        self._qt_widget._popup_bubble_message_('拷贝成功')


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap

    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((480, 480))
    w.show_window_auto()

    sys.exit(app.exec_())
