# coding:utf-8
import lxgui.proxy.widgets as prx_widgets

import lxuniverse.objects as unr_objects


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        #
        c = prx_widgets.PrxNGGraph()
        self.add_widget(c)
        u = unr_objects.ObjUniverse()

        o_t = u.generate_obj_type('lynxi', 'shader')

        t = u.generate_type(u.Category.CONSTANT, u.Type.NODE)

        r = u.get_root()

        r.create_input_port(
            t, 'input'
        )
        r.create_output_port(
            t, 'output'
        )

        p_n = None
        for i in range(10):
            i_n = o_t.create_obj(
                '/test_{}'.format(i)
            )
            i_n.create_input_port(
                t, 'input'
            )
            i_n.create_output_port(
                t, 'output'
            )
            if p_n is not None:
                p_n.get_input_port('input').set_source(i_n.get_output_port('output'))
            else:
                i_n.get_output_port('output').set_target(r.get_input_port('input'))
            #
            if not i % 10:
                p_n = i_n
            else:
                i_n.get_output_port('output').set_target(r.get_input_port('input'))

        c.set_universe(u)
        c.set_node_show()

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
