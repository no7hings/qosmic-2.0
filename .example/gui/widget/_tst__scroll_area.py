# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as prx_widgets


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        wgt = qt_widgets.QtWidget()
        self.add_widget(wgt)
        lot = qt_widgets.QtVBoxLayout(wgt)
        lot._set_align_as_top_()

        h_s = qt_widgets.QtHScrollBox()
        lot.addWidget(h_s)
        h_s._set_layout_align_left_or_top_()
        h_s.setFixedHeight(32)

        for i in range(32):
            i_btn = qt_widgets.QtIconPressButton()
            h_s._get_layout_().addWidget(i_btn)
            i_btn._set_icon_name_('application/{}'.format(['maya', 'katana', 'houdini', 'nuke'][i % 4]))

        v_s = qt_widgets.QtVScrollBox()
        lot.addWidget(v_s)
        v_s._set_layout_align_left_or_top_()
        v_s.setFixedWidth(32)

        for i in range(50):
            i_btn = qt_widgets.QtIconPressButton()
            v_s._get_layout_().addWidget(i_btn)
            i_btn._set_icon_name_('application/{}'.format(['maya', 'katana', 'houdini', 'nuke'][i % 4]))


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((480, 480))
    w.set_window_show()
    #
    sys.exit(app.exec_())
