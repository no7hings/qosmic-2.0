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

        for i in qt_widgets.QtInputAsStorage.StorageScheme.All:
            i_wgt = qt_widgets.QtInputAsStorage()
            lot.addWidget(i_wgt)
            i_wgt._set_storage_scheme_(i)
            i_wgt._set_history_key_('gui.input-storage-test-{}'.format(i))
            i_wgt._pull_history_latest_()


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
