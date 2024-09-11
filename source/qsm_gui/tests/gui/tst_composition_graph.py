# coding:utf-8
import random

import lxbasic.model as bsc_model

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.proxy.graphs as gui_prx_graphs


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        self._prx_wgt = gui_prx_graphs.PrxTrackWidget()
        self.add_widget(self._prx_wgt.widget)

        self._prx_wgt.translate_graph_to(0, 0)
        self._prx_wgt.scale_graph_to(0.01, 1)

        self._prx_wgt.create_test()


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap

    app = wrap.QtWidgets.QApplication(sys.argv)

    w = W()
    w.set_definition_window_size((960, 720))
    w.show_window_auto()

    sys.exit(app.exec_())
