# coding:utf-8
import functools

import random
import time

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import qsm_general.process as qsm_gnl_process

import os


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._d = qt_widgets.QtSpcTaskWidget()
        self.add_widget(self._d)

        random.seed(1)

        self._d._view_model.create_root_item()

        for i in range(10):
            self._d._view_model.submit_fnc(
                'TEST',
                '测试-{}'.format(i),
                self.fnc, (i, ),
                completed_fnc=functools.partial(
                    self.completed_fnc, i
                )
            )

        button = qt_widgets.QtPressButton()
        self.add_widget(button)
        button._set_name_text_('Stop')
        button.press_clicked.connect(self._d._view_model.do_quit)

    def fnc(self, thread, index):
        time.sleep(5)
        print(thread)

    def completed_fnc(self, index):
        print(index)


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap

    os.environ['QSM_UI_LANGUAGE'] = 'chs'
    #
    app = wrap.QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((480, 480))
    w.show_window_auto()
    #
    sys.exit(app.exec_())
