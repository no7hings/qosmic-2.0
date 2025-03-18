# coding:utf-8
import json

import lxbasic.storage as bsc_storage

import lxbasic.core as bsc_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_scene.node_graph.core.model as _model

import lnx_scene.node_graph.core.gui as _gui

import lnx_scene.node_graph.main as m

import os


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        spc = gui_prx_widgets.PrxHSplitter()
        self.add_widget(spc)

        self._a = m.QtNodeGraphWidget()
        spc.add_widget(self._a)

        self._b = m.QtParametersWidget()
        self._b._set_root_node_gui(self._a._root_node_gui)
        spc.add_widget(self._b)

        spc.set_stretches([4, 2])

        # _, backdrop = self._a._model.add_node('backdrop')
        #
        # backdrop.set_color((0, 255, 0))
        # backdrop.set_aescription('TEST for Scene Graph')
        # backdrop.set_size((320, 480))

        _, node = self._a._model.add_node('LoadPremiereXml')

        node.set('input.file', 'Z:/temporaries/premiere_xml_test/test_scene.xml')

        x, y = node.get_position()
        w, h = node.get_size()

        _, node_1 = self._a._model.add_node('ReplaceMayaReference')
        x, y = node_1.move_by(64, y+h+240)
        w, h = node_1.get_size()

        for i in range(5):
            _, node_0 = self._a._model.add_node('LoadMayaScene')
            node_0.set_image('E:/myworkspace/qosmic-2.0/source/qsm_resource/resources/icons/file/ma.png')
            node_0.set('preview', 'X:/QSM_TST/A001/A001_001/动画/通过文件/A001_001_001.mov')
            node_0.set('input.file', 'X:/QSM_TST/A001/A001_001/动画/通过文件/A001_001_001.ma')
            node_0.set('info.reference_json', ['X:/QSM_TST/Assets/chr/lily/Rig/Final/scenes/lily_Skin.ma'])
            # node_0.set_video('X:/videos/2024-0925/houdini_20_beach_aemo_+_rnd (1080p).mp4')
            node_0.move_by(240*i, 64)

            node.get_output('out').connect_node(node_0)
            node_0.get_output('out').connect_node(node_1)

        _, node_2 = self._a._model.add_node('OutputMaya')
        x, y = node_2.move_by(64, y+h+32*4)

        node_1.get_output('out').connect_node(node_2)

        # print(node.to_json())

        self._a._model.set_edited_node(node)

        # print(self._a._model.to_json())


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap

    os.environ['QSM_UI_LANGUAGE'] = 'chs'

    app = wrap.QtWidgets.QApplication(sys.argv)

    window = W()
    window.set_definition_window_size((1280, 720))
    window.show_window_auto()

    sys.exit(app.exec_())
