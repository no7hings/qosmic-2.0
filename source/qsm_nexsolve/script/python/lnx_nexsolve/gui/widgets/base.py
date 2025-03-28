# coding:utf-8
# gui
import lxgui.core as gui_core

from lxgui.qt.core.wrap import *

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.qt.view_widgets.base as gui_qt_vew_wgt_base

from ...node_graph.core import event as _cor_event

from ...node_graph import gui as _ng_cor_gui


class QtNodeGraphWidget(gui_qt_vew_wgt_base._BaseViewWidget):
    def __init__(self, *args, **kwargs):
        super(QtNodeGraphWidget, self).__init__(*args, **kwargs)
        # refresh
        self._refresh_button = gui_qt_widgets.QtIconPressButton()
        self._grid_lot.addWidget(self._refresh_button, 0, 0, 1, 1)
        self._refresh_button.setFixedSize(self.TOOL_BAR_W, self.TOOL_BAR_W)
        self._refresh_button._set_icon_file_path_(
            gui_core.GuiIcon.get('refresh')
        )
        # self._refresh_button.press_clicked.connect(self.refresh.emit)

        # top toolbar
        self._top_scroll_box = gui_qt_widgets.QtHScrollBox()
        self._grid_lot.addWidget(self._top_scroll_box, 0, 1, 1, 1)
        self._top_scroll_box._set_layout_align_left_or_top_()
        self._top_scroll_box.setFixedHeight(self.TOOL_BAR_W)

        # left toolbar
        self._left_scroll_box = gui_qt_widgets.QtVScrollBox()
        self._grid_lot.addWidget(self._left_scroll_box, 1, 0, 1, 1)
        self._left_scroll_box._set_layout_align_left_or_top_()
        self._left_scroll_box.setFixedWidth(self.TOOL_BAR_W)

        # undo
        self._undo_tool_box = self._add_top_tool_box('undo and redo')

        # keyword filter
        self._keyword_filter_tool_box = self._add_top_tool_box('keyword filter', size_mode=1)

        self._root_node_gui = _ng_cor_gui.RootNodeGui()
        self._grid_lot.addWidget(self._root_node_gui, 1, 1, 1, 1)
        self._root_node_gui.setFocusProxy(self)
        self._model = self._root_node_gui._model

        self._scene_file = self._model._scene_file

        self._qt_scene = _ng_cor_gui.SceneGui()
        self._root_node_gui.setScene(self._qt_scene)
        self._qt_scene._set_model(self._model)
        self._qt_scene.setSceneRect(-5000, -5000, 10000, 10000)

        self._info_bar_chart = gui_qt_widgets.QtInfoChartBar()
        self._grid_lot.addWidget(self._info_bar_chart, 2, 1, 1, 1)
        self._info_bar_chart.hide()

        self._build_undo_tool_box()
        self._build_keyword_filter_tool_box()

    def _add_top_tool_box(self, name, size_mode=0):
        tool_box = gui_qt_widgets.QtHToolBox()
        self._top_scroll_box.addWidget(tool_box)
        tool_box._set_expanded_(True)
        tool_box._set_name_text_(name)
        tool_box._set_size_mode_(size_mode)
        return tool_box

    def _build_undo_tool_box(self):
        self._undo_button = gui_qt_widgets.QtIconPressButton()
        self._undo_button._set_name_text_('undo')
        self._undo_button._set_icon_name_('montage/undo')
        self._undo_button._set_action_enable_(False)
        self._undo_button._set_tool_tip_('"LMB-click" to undo')
        self._undo_button._update_action_tip_text_('Ctrl+Z')
        self._undo_tool_box._add_widget_(self._undo_button)
        self._root_node_gui._set_undo_button_(self._undo_button)

        self._redo_button = gui_qt_widgets.QtIconPressButton()
        self._redo_button._set_name_text_('redo')
        self._redo_button._set_icon_name_('montage/redo')
        self._redo_button._set_action_enable_(False)
        self._redo_button._set_tool_tip_('"LMB-click" to redo')
        self._redo_button._update_action_tip_text_('Ctrl+Shift+Z')
        self._undo_tool_box._add_widget_(self._redo_button)
        self._root_node_gui._set_redo_button_(self._redo_button)

    def _build_keyword_filter_tool_box(self):
        self._keyword_filter_input = gui_qt_widgets.QtInputForFilter()
        self._keyword_filter_tool_box._add_widget_(self._keyword_filter_input)
        self._keyword_filter_input._set_occurrence_buttons_visible_(False)

        self._keyword_filter_input.input_value_changed.connect(
            self._on_keyword_filer
        )

    def _on_keyword_filer(self):
        self._model.on_keyword_filter(
            self._keyword_filter_input._get_all_keywords_()
        )


class QtNodeParamWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(QtNodeParamWidget, self).__init__(*args, **kwargs)

        self._mrg = 4

        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setAlignment(QtCore.Qt.AlignTop)
        self._layout.setContentsMargins(*[self._mrg]*4)
        self._layout.setSpacing(2)

        self._param_root_stack_gui = _ng_cor_gui.ParamRootStackGui()
        self._layout.addWidget(self._param_root_stack_gui)

        self._root_node_gui = None
        self._model = None

    def _set_root_node_gui(self, root_node):
        self._root_node_gui = root_node
        self._model = self._root_node_gui._model

        self._model._set_param_root_stack_gui(self._param_root_stack_gui)
        self._root_node_gui.node_edited_changed.connect(self._load_node_path)
        self._root_node_gui.event_sent.connect(self._event_filter)

    def _load_node_path(self, path):
        self._load_node(self._model.get_node(path))

    def _event_filter(self, event_type, event_id, data):
        if event_type == _cor_event.EventTypes.ParamSetValue:
            node_path = data['node']
            param_root_gui = self._param_root_stack_gui._get_one(node_path)
            if param_root_gui:
                param_path = data['param']
                param_root_gui._get_parameter(param_path)._refresh()

    def _load_node(self, node):
        self._param_root_stack_gui._load_node(node)


class QtStageWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(QtStageWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setPalette(gui_qt_core.GuiQtDcc.generate_qt_palette())

        self._mrg = 4

        self._grid_lot = QtWidgets.QGridLayout(self)
        self._grid_lot.setContentsMargins(*[self._mrg]*4)
        self._grid_lot.setSpacing(2)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        mrg = self._mrg
        x, y, w, h = 0, 0, self.width(), self.height()

        f_x, f_y, f_w, f_h = x+1, y+1, w-2, h-2
        is_focus = self.hasFocus()

        pen = QtGui.QPen(QtGui.QColor(*[(71, 71, 71, 255), (95, 95, 95, 255)][is_focus]))
        pen_width = [1, 2][is_focus]

        pen.setWidth(pen_width)
        painter.setPen(pen)
        painter.setBrush(QtGui.QColor(*gui_core.GuiRgba.Dim))
        painter.drawRect(f_x, f_y, f_w, f_h)


