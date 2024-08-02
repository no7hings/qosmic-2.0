# coding:utf-8
import lxgui.proxy.widgets as gui_prx_widgets

import lxgeneral.dcc.objects as gnl_dcc_objects

import lxuniverse.objects as unr_objects


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        #
        c = gui_prx_widgets.PrxNGImageGraph()
        self.add_widget(c)
        u = unr_objects.ObjUniverse()

        o_t = u.create_obj_type('lynxi', 'shader')

        t = u.create_type(u.Category.CONSTANT, u.Type.STRING)

        r = u.get_root()

        r.create_input(
            t, 'input'
        )
        r.create_output(
            t, 'output'
        )
        d = gnl_dcc_objects.StgDirectory('Z:/temporaries/node_graph_test')

        for i in d.get_all_file_paths():
            i_f = gnl_dcc_objects.StgFile(i)
            i_n = o_t.create_obj(
                '/{}'.format(i_f.name_base)
            )
            i_p = i_n.create_parameter(
                t, 'image'
            )
            i_p.set(i)

        c.set_graph_universe(u)
        c.set_node_show()

    def test(self):
        pass


if __name__ == '__main__':
    import sys
    #
    from QtSide import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((800, 800))
    w.show_window_auto()
    #
    sys.exit(app.exec_())
