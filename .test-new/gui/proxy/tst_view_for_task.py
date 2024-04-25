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

        c = prx_widgets.PrxViewForTask()
        lot.addWidget(c.widget)

        c.set_title('QSM_TST.sam.mod.modeling')

        c.set_root('Z:/projects/QSM_TST/assets/chr/sam/work/user.nothings/mod.modeling')
        # c.set_root('X:/QSM_TST/Assets')


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
