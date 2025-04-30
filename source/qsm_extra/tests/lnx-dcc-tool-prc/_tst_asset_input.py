# coding:utf-8
import lxgui.proxy.widgets as gui_prx_widgets

import lnx_dcc_tool_prc.gui.proxy.widgets as qsm_proxy_widgets


class W0(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W0, self).__init__(*args, **kwargs)

        grp = gui_prx_widgets.PrxHToolGroupA()
        self.add_widget(grp)
        grp.set_expanded(True)

        grp.add_widget(qsm_proxy_widgets.PrxInputForProject())
        grp.add_widget(qsm_proxy_widgets.PrxInputForAsset())
        grp.add_widget(qsm_proxy_widgets.PrxInputForSequence())
        grp.add_widget(qsm_proxy_widgets.PrxInputForShot())


if __name__ == '__main__':
    import sys
    # noinspection PyUnresolvedReferences
    from QtSide import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = W0()
    w.set_definition_window_size((720, 240))
    w.show_window_auto()
    #
    sys.exit(app.exec_())
