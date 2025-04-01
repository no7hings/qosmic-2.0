# coding:utf-8
import lxgui.proxy.widgets as gui_prx_widgets

import lnx_dcc_tool_prc.gui.qt.widgets as lzy_gui_qt_widgets


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        wgt = lzy_gui_qt_widgets.QtAdvCharacterPicker()
        self.add_widget(wgt)

        wgt._set_namespace_('test_Skin')


if __name__ == '__main__':
    import sys
    # noinspection PyUnresolvedReferences
    from QtSide import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((480, 480))
    w.show_window_auto()
    #
    sys.exit(app.exec_())
