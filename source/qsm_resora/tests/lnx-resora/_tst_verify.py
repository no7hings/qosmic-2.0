# coding:utf-8
import lxgui.core as gui_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.qt.core as gui_qt_core


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        button = qt_widgets.QtPressButton()
        self.add_widget(button)
        button._set_name_text_('test')
        button.press_clicked.connect(self.test_fnc)

    @gui_core.Verify.execute()
    def test_fnc(self):
        print('ABC')


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap
    #
    app = wrap.QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((480, 480))
    w.show_window_auto()
    #
    sys.exit(app.exec_())
