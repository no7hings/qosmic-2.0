# coding:utf-8
import lxgui.proxy.widgets as prx_widgets


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        s_c = prx_widgets.PrxPieChart()
        self.add_widget(
            s_c
        )
        s_c.set_chart_data(
            [('at startup bytes', 273985536, 273985536), ('plugins bytes', 7159808, 7159808), ('AOV samples bytes', 16094400, 16094400), ('output buffers bytes', 3097248, 3097248), ('framebuffers bytes', 264241152, 264241152), ('node overhead bytes', 261569, 261569), ('instance overhead bytes', 0, 0), ('message passing bytes', 24672, 24672), ('memory pools bytes', 16826752, 16826752), ('geometry bytes', 43255401, 43255401), ('polymesh bytes', 3348, 3348), ('subdivs bytes', 43252053, 43252053), ('nurbs bytes', 0, 0), ('points bytes', 0, 0), ('curves bytes', 0, 0), ('accel structs bytes', 35378424, 35378424), ('skydome importance map bytes', 8176896, 8176896), ('quad importance map bytes', 0, 0), ('mesh importance map bytes', 0, 0), ('strings bytes', 25427968, 25427968), ('texture cache bytes', 249178416, 249178416), ('profiler bytes', 6674272, 6674272), ('externally allocated bytes', 0, 0), ('unaccounted bytes', 101009422, 101009422)]
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
    w.set_definition_window_size((640, 640))
    w.set_window_show()
    #
    sys.exit(app.exec_())
