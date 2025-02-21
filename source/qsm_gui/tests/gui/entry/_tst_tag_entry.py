# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._main_qt_layout._set_align_as_top_()

        self._d_0 = qt_widgets.QtInputForTag()
        self.add_widget(self._d_0)
        self._d_0._set_value_type_(str)

        self._d_0._set_value_options_(
            ['test_{}'.format(x*'A') for x in range(10)]
        )

        self._d_1 = qt_widgets.QtInputForTag()
        self.add_widget(self._d_1)
        self._d_1._set_value_type_(list)

        self._d_1._set_value_options_(
            ['test_{}'.format(x*'B') for x in range(10)]
        )


def test():
    import sys

    from lxgui.qt.core import wrap

    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((320, 320))
    w.show_window_auto()

    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
