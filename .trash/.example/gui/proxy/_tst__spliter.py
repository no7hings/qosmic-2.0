# coding:utf-8
import lxgui.proxy.widgets as gui_prx_widgets


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        s = gui_prx_widgets.PrxVScrollArea()
        self.add_widget(s)
        h_s = gui_prx_widgets.PrxHSplitter()
        s.add_widget(h_s)

        v_s_0 = gui_prx_widgets.PrxVSplitter()
        h_s.add_widget(v_s_0)

        t_0 = gui_prx_widgets.PrxTreeView()
        h_s.add_widget(t_0)
        t_1 = gui_prx_widgets.PrxTreeView()
        v_s_0.add_widget(
            t_1
        )
        t_2 = gui_prx_widgets.PrxTreeView()
        v_s_0.add_widget(
            t_2
        )

        v_s_1 = gui_prx_widgets.PrxVSplitter()
        h_s.add_widget(
            v_s_1
        )

        # h_s.set_widget_hide_at(0)

        h_s.set_fixed_size_at(0, 320)
        h_s.set_fixed_size_at(2, 320)

        # h_s.swap_contract_left_or_top_at(0)
        h_s.swap_contract_right_or_bottom_at(2)

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
    w.set_definition_window_size((1280, 960))
    w.show_window_auto()
    #
    sys.exit(app.exec_())
