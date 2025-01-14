# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.qt.chart_widgets as qt_cht_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import random


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._d = qt_cht_widgets.QtHistogramChartWidget(self._qt_widget)
        self._d._set_data_(
            self.generate_data()
        )

        self.add_widget(self._d)

    @staticmethod
    def generate_data():
        random.seed(0)

        values = range(100)
        leaf_counts = range(5, 20)
        dict_ = {}
        for i in range(10):
            i_dict = {}
            for j in range(random.choice(leaf_counts)):
                i_dict['leaf_{}'.format(j)] = random.choice(values)
            dict_['branch_{}'.format(i*'A')] = i_dict

        return dict_


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap

    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((960, 480))
    w.show_window_auto()

    sys.exit(app.exec_())
