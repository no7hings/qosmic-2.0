# coding:utf-8
import lxgui.proxy.widgets as gui_prx_widgets


class W(gui_prx_widgets.PrxFramelessWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

    def test(self):
        pass


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((800, 800))
    w.show_window_auto()
    #
    sys.exit(app.exec_())
