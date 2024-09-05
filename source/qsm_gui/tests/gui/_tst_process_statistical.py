# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxbasic.storage as bsc_storage


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        data, data_keys = bsc_storage.Statistics.get_data_args()

        self._d = qt_widgets.QtViewForBarChart(self._qt_widget)
        self._d._set_data_(
            data,
            data_keys,
        )
        self._d._set_name_text_('TEST')
        self.add_widget(self._d)


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap

    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((960, 480))
    w.show_window_auto()

    sys.exit(app.exec_())
