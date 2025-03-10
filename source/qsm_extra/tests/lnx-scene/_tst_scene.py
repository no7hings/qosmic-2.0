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

        self._d = m.QtSceneGraphWidget()

        self.add_widget(self._d)

        # _, backdrop = self._d._model.add_node('backdrop')
        #
        # backdrop.set_color((0, 255, 0))
        # backdrop.set_description('TEST for Scene Graph')
        # backdrop.set_size((320, 480))

        _, load_maya_scene = self._d._model.add_node('load_maya_scene')
        load_maya_scene.set_image('E:/myworkspace/qosmic-2.0/source/qsm_resource/resources/icons/file/ma.png')
        # load_maya_scene.set_video('X:/videos/2024-0925/houdini_20_beach_demo_+_rnd (1080p).mp4')
        x, y = load_maya_scene.move_by(64, 64)
        w, h = load_maya_scene.get_size()

        _, replace_maya_scene_reference = self._d._model.add_node('replace_maya_scene_reference')
        x, y = replace_maya_scene_reference.move_by(64, y+h+32*4)
        w, h = replace_maya_scene_reference.get_size()

        _, output_maya_scene = self._d._model.add_node('output_maya_scene')
        x, y = output_maya_scene.move_by(64, y+h+32*4)

        # print(self._d._model.to_json())


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap

    app = wrap.QtWidgets.QApplication(sys.argv)

    window = W()
    window.set_definition_window_size((640, 480))
    window.show_window_auto()

    sys.exit(app.exec_())
