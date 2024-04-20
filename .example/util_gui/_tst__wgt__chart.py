# coding:utf-8
import lxgui.core as gui_core

import lxgui.proxy.widgets as prx_widgets


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        #
        a = [('deletion', 41, 10), ('addition', 41, 40), ('name-changed', 41, 0), ('path-changed', 41, 0),
             ('path-exchanged', 41, 0), ('face-vertices-changed', 41, 0), ('points-changed', 41, 0),
             ('geometry-changed', 41, 0)]
        b = [('geometry', 41, 400), ('shell', 41, 41), ('area', 324.800048828125, 324.800048828125),
             ('face', 53489.937469401586, 16456), ('edge', 106979.87493880317, 33328),
             ('vertex', 53768.530893721385, 16842)]
        #
        h_s = prx_widgets.PrxHSplitter()
        self.add_widget(h_s)

        v_s = prx_widgets.PrxVSplitter()
        h_s.add_widget(v_s)

        t = prx_widgets.PrxTreeView()
        h_s.add_widget(t)
        s_c = prx_widgets.PrxSectorChart()
        v_s.add_widget(
            s_c
        )
        #
        s_d = []
        for i in range(10):
            s_d.append(
                ('text-{}'.format(i), 10, i)
            )
        s_c.set_chart_data(
            a, gui_core.GuiSectorChartMode.Error
        )
        #
        r_c = prx_widgets.PrxRadarChart()
        v_s.add_widget(
            r_c
        )
        c_d = []
        for i in range(10):
            if i % 2:
                c_d.append(
                    ('text-{}'.format(i), i, i + 1)
                )
            else:
                c_d.append(
                    ('text-{}'.format(i), i, i - 1)
                )
        r_c.set_chart_data(
            b, gui_core.GuiSectorChartMode.Error
        )

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
    w.set_window_show()
    #
    sys.exit(app.exec_())
