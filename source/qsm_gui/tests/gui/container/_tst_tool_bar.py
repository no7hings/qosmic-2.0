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

        self._d = gui_prx_widgets.PrxHToolBar()
        self.add_widget(self._d)
        self._d.set_align_left()
        self._d.set_expanded(True)
        self._d.build_by_data(data['build']['top']['toolbar']['tools'])

        self._d.get_tool('toolbox.tool0').connect_press_clicked_to(self._test)

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
