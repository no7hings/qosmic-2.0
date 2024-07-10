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

        self._qt_widget._thread_worker_maximum = 2

        self._prc_list = []

        btn = gui_qt_widgets.QtPressButton()
        self.add_widget(btn)
        self._main_qt_layout.setAlignment(gui_qt_core.QtCore.Qt.AlignTop)
        btn.press_clicked.connect(self._do_close_)
        for i in range(5):
            wgt = gui_qt_widgets.QtProgressBarForSubprocess()
            self.add_widget(wgt)
            self._prc_list.append(wgt)
            wgt._set_text_('测试-{}'.format(i))

            trd = wgt._generate_thread_(self._qt_widget)

            trd.set_fnc(
                qsm_gnl_core.MayaCacheProcess.generate_command(
                    'method=test-process'
                )
            )
            trd.start()

        self._qt_widget.window_closed.connect(self._do_close_)

    def _do_close_(self):
        # self._prc_list.reverse()
        [x._do_kill_() for x in self._prc_list]
        # self._qt_widget._thread_worker_condition.wakeAll()
        [x._do_quit_() for x in self._prc_list]


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap

    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((480, 480))
    w.show_window_auto()

    sys.exit(app.exec_())
