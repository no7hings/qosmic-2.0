# coding:utf-8
import os

import pkgutil

import importlib
# gui
import lxgui.core as gui_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

from .. import node_type as _node_type

from . import widgets as _widgets


def register_node_types_from(module):
    dir_path = os.path.dirname(module.__file__)

    all_names = os.listdir(dir_path)

    for i in all_names:
        if i.startswith('__init__'):
            continue
        if i.endswith('.pyc'):
            continue

        i_module_name = '{}.{}'.format(module.__name__, os.path.splitext(i)[0])
        if pkgutil.find_loader(i_module_name):
            i_module = importlib.import_module(i_module_name)
            if 'register' in i_module.__dict__:
                i_module.__dict__['register']()


class PrxNexsolveTool(gui_prx_widgets.PrxBasePanel):
    CONFIGURE_KEY = 'nexsolve/gui/main'

    def __init__(self, *args, **kwargs):
        super(PrxNexsolveTool, self).__init__(*args, **kwargs)

    def gui_setup_fnc(self):
        wgt = gui_qt_widgets.QtWidget()
        self.add_widget(wgt)

        lot = gui_qt_widgets.QtVBoxLayout(wgt)
        lot.setContentsMargins(*[0]*4)
        lot.setSpacing(2)

        self._top_tool_bar = gui_prx_widgets.PrxHToolBar()
        lot.addWidget(self._top_tool_bar.widget)
        self._top_tool_bar.set_expanded(True)

        h_s = gui_prx_widgets.PrxHSplitter()
        lot.addWidget(h_s.widget)

        self._node_graph = _widgets.QtNodeGraphWidget()
        h_s.add_widget(self._node_graph)

        self._node_param = _widgets.QtNodeParamWidget()
        self._node_param._set_root_node_gui(self._node_graph._root_node_gui)
        h_s.add_widget(self._node_param)

        h_s.set_stretches([4, 2])

        register_node_types_from(_node_type)
