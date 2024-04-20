# coding:utf-8
import lxgui.proxy.widgets as prx_widgets


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        s_c = prx_widgets.PrxHistogramChart()
        self.add_widget(
            s_c
        )
        s_c.set_chart_data(
            [1000, 2000, 3000, 1000, 2000, 3000, 1000, 2000, 3000]
        )
        s_c.set_labels(
            ('Frame', 'Size')
        )
        # s_c.widget.setDrawData(
        #     [1000, 2000, 3000],
        #     (0, 0),
        #     ('Frame', 'Size')
        # )

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
    w.set_definition_window_size((640, 640))
    w.set_window_show()
    #
    sys.exit(app.exec_())
