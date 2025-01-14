# coding:utf-8
import lxgui.qt.chart_widgets as qt_cht_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import random


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        keys = ['triangle', 'memory']
        self._d = qt_cht_widgets.QtLineChartWidget(self._qt_widget)
        self._d._set_data_(
            self.generate_data(keys), keys, data_type_dict=dict(memory='file_size')
        )

        self.add_widget(self._d)

    @staticmethod
    def generate_data(keys):
        random.seed(0)

        values_dict = dict(
            triangle=range(10000, 100000),
            memory=range(1000000, 10000000)
        )

        dict_ = {}
        for i in range(10):
            i_dict = {}
            for j_key in keys:
                i_dict[j_key] = random.choice(values_dict[j_key])
            dict_['branch_{}'.format(i)] = i_dict

        return dict_


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap

    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((960, 480))
    w.show_window_auto()

    sys.exit(app.exec_())
