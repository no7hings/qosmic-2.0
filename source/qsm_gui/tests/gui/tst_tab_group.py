# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        wgt = qt_widgets.QtWidget()
        self.add_widget(wgt)
        lot = qt_widgets.QtVBoxLayout(wgt)
        lot._set_align_as_top_()

        c_h = gui_prx_widgets.PrxHTabToolBox()
        lot.addWidget(c_h.widget)

        t_0 = gui_prx_widgets.PrxOptionsNode('TEST-0')
        c_h.add_widget(t_0, name='TEST-0', icon_name_text='A')

        t_1 = gui_prx_widgets.PrxTreeView()
        c_h.add_widget(t_1, name='TEST-1', icon_name_text='B')

        t_2 = gui_prx_widgets.PrxTreeView()
        c_h.add_widget(t_2, name='TEST-2', icon_name_text='C')

        c_v = gui_prx_widgets.PrxVTabToolBox()
        lot.addWidget(c_v.widget)
        c_v.set_tab_direction(c_v.TabDirections.RightToLeft)

        t_0 = gui_prx_widgets.PrxOptionsNode('TEST-0')
        c_v.add_widget(t_0, name='TEST-0', icon_name_text='A')

        t_1 = gui_prx_widgets.PrxTreeView()
        c_v.add_widget(t_1, name='TEST-1', icon_name_text='B')

        t_2 = gui_prx_widgets.PrxTreeView()
        c_v.add_widget(t_2, name='TEST-2', icon_name_text='C')

        t_2 = gui_prx_widgets.PrxTreeView()
        c_v.add_widget(t_2, name='TEST-3', icon_name_text='D')

        t_2 = gui_prx_widgets.PrxTreeView()
        c_v.add_widget(t_2, name='TEST-4', icon_name_text='E')

        t_2 = gui_prx_widgets.PrxTreeView()
        c_v.add_widget(t_2, name='TEST-5', icon_name_text='F')


if __name__ == '__main__':
    import sys
    # noinspection PyUnresolvedReferences
    from QtSide import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((480, 480))
    w.show_window_auto()
    #
    sys.exit(app.exec_())
