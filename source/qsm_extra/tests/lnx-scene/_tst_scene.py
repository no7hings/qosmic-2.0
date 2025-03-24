# coding:utf-8
import json

import lxbasic.storage as bsc_storage

import lxbasic.core as bsc_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_scene.main as m

import os


class W(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)

        spc = gui_prx_widgets.PrxHSplitter()
        self.add_widget(spc)

        self._a = m.QtNodeGraphWidget()
        spc.add_widget(self._a)

        self._b = m.QtNodeParamWidget()
        self._b._set_root_node_gui(self._a._root_node_gui)
        spc.add_widget(self._b)

        spc.set_stretches([4, 2])

        flag, node = self._a._model.add_node('LoadPremiereXml')

        node.set('input.file', 'Z:/temporaries/premiere_xml_test/test_scene.xml')
        node.execute('analysis_and_build')


if __name__ == '__main__':
    import sys

    from lxgui.qt.core import wrap

    os.environ['QSM_UI_LANGUAGE'] = 'chs'

    app = wrap.QtWidgets.QApplication(sys.argv)

    window = W()
    window.set_definition_window_size((1280, 720))
    window.show_window_auto()

    sys.exit(app.exec_())
