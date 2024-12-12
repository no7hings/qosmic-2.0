# coding:utf-8
import time

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxbasic.core as bsc_core

import lxgui.qt.core as gui_qt_core

import lxgui.proxy.scripts as prx_scripts

import qsm_general.core as qsm_gnl_core

import qsm_general.process as qsm_gnl_process


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        button = gui_prx_widgets.PrxPressButton()
        self.add_widget(button)
        button.set_name('TEST')
        button.connect_press_clicked_to(self._test)

    def _test(self):
        wgt = gui_prx_widgets.PrxSprcTaskWindow()

        wgt.show_window_auto(exclusive=False)

        for i in range(5):
            wgt.submit(
                'TEST',
                '测试-{}'.format(i),
                qsm_gnl_process.MayaCacheSubprocess.generate_cmd_script(
                    'method=test-process'
                )
            )


if __name__ == '__main__':
    import sys

    import os

    from lxgui.qt.core import wrap

    os.environ['QSM_UI_LANGUAGE'] = 'chs'

    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((480, 480))
    w.show_window_auto()

    sys.exit(app.exec_())
