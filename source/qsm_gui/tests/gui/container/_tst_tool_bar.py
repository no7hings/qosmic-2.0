# coding:utf-8
import os.path

import lxbasic.storage as bsc_storage

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._main_qt_layout._set_align_as_top_()

        data = bsc_storage.StgFileOpt(
            '{}/data.yml'.format(os.path.dirname(__file__))
        ).set_read()

        self._d_0 = gui_prx_widgets.PrxHToolbar()
        self.add_widget(self._d_0)
        self._d_0.set_align_left()
        self._d_0.set_expanded(True)
        self._d_0.build_by_data(data['build']['top']['toolbar']['tools'])
        self._d_0.set_history_group(data['build']['top']['toolbar']['history_group'])

        self._d_0.get_tool('toolbox0.tool0').connect_press_clicked_to(self._test)

        self._d_1 = gui_prx_widgets.PrxVToolbar()
        self.add_widget(self._d_1)
        self._d_1.set_align_top()
        self._d_1.set_expanded(True)
        self._d_1.build_by_data(data['build']['top']['toolbar']['tools'])

        self._d_1.get_tool('toolbox0.tool0').connect_press_clicked_to(self._test)

    def _test(self):
        print('A')


def test():
    import sys

    from lxgui.qt.core import wrap

    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((720, 560))
    w.show_window_auto()

    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
