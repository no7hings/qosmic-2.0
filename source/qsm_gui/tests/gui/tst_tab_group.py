# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as prx_widgets


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        wgt = qt_widgets.QtWidget()
        self.add_widget(wgt)
        lot = qt_widgets.QtVBoxLayout(wgt)
        lot._set_align_top_()

        c = prx_widgets.PrxHTabBox()
        lot.addWidget(c.widget)

        t_0 = prx_widgets.PrxOptionsNode('TEST-0')
        c.add_widget(t_0, name='TEST-0')

        t_1 = prx_widgets.PrxTreeView()
        c.add_widget(t_1, name='TEST-1')

        t_2 = prx_widgets.PrxTreeView()
        c.add_widget(t_2, name='TEST-2')


if __name__ == '__main__':
    import sys
    # noinspection PyUnresolvedReferences
    from QtSide import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((480, 480))
    w.set_window_show()
    #
    sys.exit(app.exec_())
