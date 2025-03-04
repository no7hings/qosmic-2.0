# coding:utf-8
import functools

import random

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

        status = [
            gui_core.GuiProcessStatus.Waiting,
            gui_core.GuiProcessStatus.Started,
            gui_core.GuiProcessStatus.Error,
            gui_core.GuiProcessStatus.Completed,
            gui_core.GuiProcessStatus.Failed,
            gui_core.GuiProcessStatus.Killed,
        ]

        percents = [float(x)/10 for x in range(5)]

        random.seed(1)

        self._d._view_model.create_root_item()

        for i in range(20):
            if i % 2:
                i_cmd_script = qsm_gnl_process.MayaCacheSubprocess.generate_cmd_script(
                    'method=test-process&tag=error'
                )
            else:
                i_cmd_script = qsm_gnl_process.MayaCacheSubprocess.generate_cmd_script(
                    'method=test-process'
                )
            self._d._view_model.submit_cmd_script(
                'TEST',
                '测试-{}'.format(i),
                i_cmd_script,
                completed_fnc=functools.partial(
                    self.completed_fnc, i
                ),
                application='maya'
            )
            # _, i_item = self._d._view_model.create_item(
            #     '/test-{}'.format(i)
            # )
            # i_item._item_model._update_percent(random.choice(percents))
            # i_status = random.choice(status)
            # if i_status != gui_core.GuiProcessStatus.Waiting:
            #     i_item._item_model._update_status(i_status)
            # i_item._item_model.set_icon_name('application/python')

        button = qt_widgets.QtPressButton()
        self.add_widget(button)
        button._set_name_text_('Stop')
        button.press_clicked.connect(self._d._view_model.do_quit)

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
