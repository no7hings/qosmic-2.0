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

        for i in range(3):
            i_path = '/node_{}'.format(i)
            _, i_node = self._d._model.create_node('default', i_path)
            if i % 2:
                for j in range(5):
                    i_node.create_input_port('closure', 'i{}'.format(j))
            else:
                i_node.create_input_port('closure', 'input')

            i_node.create_output_port('closure', 'output')

            i_node.set_color(bsc_core.BscTextOpt(i_path).to_hash_rgb())

            i_node.move_by(0, 96*i)

        _, backdrop = self._d._model.create_backdrop('default', '/backdrop_0')

        backdrop.set_color((0, 255, 0))

        # print(json.dumps({'A': None}))

        # print(self._d._model.get_node('/node_1').to_json())

        f = 'E:/myworkspace/qosmic-2.0/source/qsm_extra/tests/lnx-scene/_tst_node.json'
        with open(f) as j:
            json_str = j.read()

        self._d._model._paste_node_by_json_str(json_str)

        self._d._model.get_node('/node_0').get_output_port('output').connect(
            self._d._model.get_node('/node_1').get_input_port('i0')
        )

        self._d._model.get_node('/node_1').get_output_port('output').connect(
            self._d._model.get_node('/node_2').get_input_port('input')
        )


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

