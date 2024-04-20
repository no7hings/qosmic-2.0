# coding:utf-8
import fnmatch

import lxbasic.core as bsc_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as prx_widgets


class W0(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W0, self).__init__(*args, **kwargs)

        self._sub_label = qt_widgets.QtTextItem()
        self.add_widget(self._sub_label)
        self._sub_label.setFixedHeight(20)
        self._sub_label._set_name_draw_font_(gui_qt_core.QtFonts.SubTitle)
        self._sub_label._set_name_text_option_to_align_center_()

        self._ipt = prx_widgets.PrxInputAsStgTask()
        self.add_widget(self._ipt)

        self._ipt.set_focus_in()

        self.get_widget().key_escape_pressed.connect(
            self.__do_cancel
        )

        self._tip = prx_widgets.PrxTextBrowser()
        self.add_widget(self._tip)
        self._tip.set_focus_enable(False)

        self._ipt.connect_result_to(
            self._do_accept
        )
        self._ipt.connect_tip_trace_to(
            self._do_tip_trace
        )

        self._ipt.setup()

    def set_application(self, application):
        self._sub_label._set_name_text_(application)

    def _do_accept(self, dict_):
        if dict_:
            self.close_window_later()

    def _do_tip_trace(self, text):
        self._tip.set_content(text)

    def __do_cancel(self):
        if self._ipt.has_focus() is False:
            self.close_window_later()


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = W0()
    w.set_definition_window_size((480, 240))
    w.set_window_show()
    w.set_application('maya')
    #
    sys.exit(app.exec_())
