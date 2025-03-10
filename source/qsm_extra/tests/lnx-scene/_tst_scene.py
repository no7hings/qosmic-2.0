# coding:utf-8
import json

import lxbasic.storage as bsc_storage

import lxbasic.core as bsc_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_scene.gui.graph.main as m

import os


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        self._d = m.QtSceneGraphWidget()

        self.add_widget(self._d)

        output_port_cur = None
        for i in range(3):
            _, i_node = self._d._model.create_node('node')
            if i % 2:
                for j in range(5):
                    _, j_input_port = i_node.add_input_port('input')
            else:
                _, j_input_port = i_node.add_input_port('input')

            _, i_output_port = i_node.add_output_port('output')

            i_node.set_color(bsc_core.BscTextOpt(i_node.get_name()).to_hash_rgb())

            i_node.move_by(64, 64+96*i)

            if output_port_cur is not None:
                output_port_cur.connect(j_input_port)

            output_port_cur = i_output_port

        _, backdrop = self._d._model.create_backdrop()

        backdrop.set_color((0, 255, 0))
        backdrop.set_description('TEST for Scene Graph')

        button = qt_widgets.QtPressButton()
        button._set_name_text_('Add Node')

        print(self._d._model.to_json())


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap

    os.environ['QSM_UI_LANGUAGE'] = 'chs'
    #
    app = wrap.QtWidgets.QApplication(sys.argv)
    #
    w = W()
    w.set_definition_window_size((640, 480))
    w.show_window_auto()
    #
    sys.exit(app.exec_())
