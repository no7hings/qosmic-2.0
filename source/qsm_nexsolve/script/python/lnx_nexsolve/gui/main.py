# coding:utf-8
import os

import pkgutil

import importlib
# gui
import lxgui.core as gui_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

from .. import node_type as _node_type

from .. import drop_action as _drop_action

from . import widgets as _widgets


def register_fnc(module):
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

    GUI_KEY = 'nexsolve'

    def __init__(self, *args, **kwargs):
        super(PrxNexsolveTool, self).__init__(*args, **kwargs)

    def _gui_build_scene_tool_box(self):
        self._scene_new_qt_button = gui_qt_widgets.QtIconPressButton()
        self._scene_prx_tool_box.add_widget(self._scene_new_qt_button)
        self._scene_new_qt_button._set_icon_name_('file/file')
        self._scene_new_qt_button.press_clicked.connect(self._node_graph._model._on_new_file_action)
        self._scene_new_qt_button._set_name_text_('New Scene')
        self._scene_new_qt_button._set_tool_tip_('"LMB-click" to new scene')
        self._scene_new_qt_button._update_action_tip_text_('Ctrl+N')

        self._scene_open_qt_button = gui_qt_widgets.QtIconPressButton()
        self._scene_prx_tool_box.add_widget(self._scene_open_qt_button)
        self._scene_open_qt_button._set_icon_name_('file/open-folder')
        self._scene_open_qt_button.press_clicked.connect(self._node_graph._model._on_open_file_action)
        self._scene_open_qt_button._set_name_text_('Open Scene')
        self._scene_open_qt_button._set_tool_tip_('"LMB-click" to open scene')
        self._scene_open_qt_button._update_action_tip_text_('Ctrl+O')

        self._scene_save_qt_button = gui_qt_widgets.QtIconPressButton()
        self._scene_prx_tool_box.add_widget(self._scene_save_qt_button)
        self._scene_save_qt_button._set_icon_name_('tool/save')
        self._scene_save_qt_button.press_clicked.connect(self._node_graph._model._on_save_file_action)
        self._scene_save_qt_button._set_name_text_('Save Scene')
        self._scene_save_qt_button._set_tool_tip_('"LMB-click" to save scene')
        self._scene_save_qt_button._update_action_tip_text_('Ctrl+S')

        self._scene_save_as_qt_button = gui_qt_widgets.QtIconPressButton()
        self._scene_prx_tool_box.add_widget(self._scene_save_as_qt_button)
        self._scene_save_as_qt_button._set_icon_name_('tool/save-as')
        self._scene_save_as_qt_button.press_clicked.connect(self._node_graph._model._on_save_file_as_action)
        self._scene_save_as_qt_button._set_name_text_('Save Scene As')
        self._scene_save_as_qt_button._set_tool_tip_('"LMB-click" to save scene as')
        self._scene_save_as_qt_button._update_action_tip_text_('Ctrl+Shift+S')

    def _update_scene_path(self, path):
        self._scene_qt_info._set_text_(path)

    def gui_setup_fnc(self):
        wgt = gui_qt_widgets.QtWidget()
        self.add_widget(wgt)

        lot = gui_qt_widgets.QtVBoxLayout(wgt)
        lot.setContentsMargins(*[0]*4)
        lot.setSpacing(2)

        self._top_prx_tool_bar = gui_prx_widgets.PrxHToolbar()
        lot.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_align_left()
        self._top_prx_tool_bar.set_expanded(True)

        h_s = gui_prx_widgets.PrxHSplitter()
        lot.addWidget(h_s.widget)

        self._node_graph = _widgets.QtNodeGraphWidget()
        h_s.add_widget(self._node_graph)

        self._node_param = _widgets.QtNodeParamWidget()
        self._node_param._set_root_node_gui(self._node_graph._root_node_gui)
        h_s.add_widget(self._node_param)

        h_s.set_stretches([4, 2])
        
        # file tool box
        self._scene_prx_tool_box = self._top_prx_tool_bar.create_tool_box('scene')
        self._gui_build_scene_tool_box()
        
        # file info tool box
        self._scene_info_prx_tool_box = self._top_prx_tool_bar.create_tool_box('scene info', size_mode=1)

        self._scene_button = gui_qt_widgets.QtIconPressButton()
        self._scene_info_prx_tool_box.add_widget(self._scene_button)
        self._scene_button._set_icon_name_('file/jsz')

        self._scene_qt_info = gui_qt_widgets.QtInfoBubble()
        self._scene_info_prx_tool_box.add_widget(self._scene_qt_info)
        self._scene_qt_info._set_text_(self._node_graph._scene_file.get_current())

        self._node_graph._root_node_gui.scene_path_accepted.connect(self._update_scene_path)

        register_fnc(_node_type)
        register_fnc(_drop_action)

        # self._node_graph._scene_file.open('C:/Users/nothings/QSM/scenes/untitled_2.nxs_prj')

    def gui_close_fnc(self):
        self._node_graph._scene_file.close_with_dialog()
