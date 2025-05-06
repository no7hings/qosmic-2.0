# coding:utf-8
import six

import lxbasic.core as bsc_core

from ... import core as _gui_core
# qt
from ...qt import core as gui_qt_core
# qt widgets
from ...qt.widgets import base as gui_qt_wgt_base

from ...qt.widgets import utility as gui_qt_wgt_utility

from ...qt.widgets import head as gui_qt_wgt_head

from ...qt.widgets import scroll as gui_qt_wgt_scroll
# proxy abstracts
from .. import abstracts as gui_prx_abstracts

from . import container_for_box as _container_for_box

from . import utility as _utility


class AbsPrxToolGroup(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtVLine
    QT_HEAD_CLS = None

    QT_HEAD_HEIGHT = 22

    def __init__(self, *args, **kwargs):
        super(AbsPrxToolGroup, self).__init__(*args, **kwargs)

    def _gui_build_fnc(self):
        qt_layout_0 = gui_qt_wgt_base.QtVBoxLayout(self._qt_widget)
        qt_layout_0.setAlignment(gui_qt_core.QtCore.Qt.AlignTop)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        qt_layout_0.setSpacing(2)
        # header
        self._qt_head = self.QT_HEAD_CLS()
        qt_layout_0.addWidget(self._qt_head)
        self._qt_head.setFixedHeight(self.QT_HEAD_HEIGHT)
        self._qt_head.expand_toggled.connect(self.set_expanded)
        self._qt_head._update_action_tip_text_('"LMB-click" to expand "on" / "off"')
        self._qt_head.press_toggled.connect(self._qt_widget._set_pressed_)
        #
        qt_widget_1 = gui_qt_wgt_utility.QtTranslucentWidget()
        qt_layout_0.addWidget(qt_widget_1)
        qt_layout_1 = gui_qt_wgt_base.QtVBoxLayout(qt_widget_1)
        qt_layout_1.setContentsMargins(2, 0, 0, 0)
        qt_layout_1.setSpacing(2)
        #
        self._layout = qt_layout_1
        #
        self._qt_view = qt_widget_1
        #
        self._refresh_expand_fnc()

    def _refresh_expand_fnc(self):
        self._qt_view.setVisible(
            self.get_is_expanded()
        )

    def set_name(self, name):
        self._qt_head._set_name_text_(name)

    def set_icon_by_text(self, name):
        self._qt_head._set_name_icon_text_(name)

    def set_name_icon_enable(self, boolean):
        self._qt_head._set_name_icon_enable_(boolean)

    def set_expand_icon_file(self, icon_file_path_0, icon_file_path_1):
        self._qt_head._set_expand_icon_file_path_(
            icon_file_path_0, icon_file_path_1
        )

    def set_expand_icon_names(self, icon_name_0, icon_name_1):
        self._qt_head._set_expand_icon_names_(
            icon_name_0, icon_name_1
        )

    def set_expand_sub_icon_names(self, icon_name_0, icon_name_1):
        self._qt_head._set_expand_sub_icon_names_(
            icon_name_0, icon_name_1
        )

    def set_name_font_size(self, size):
        self._qt_head._set_name_font_size_(size)

    def set_tool_tip(self, text):
        self._qt_head._update_tool_tip_text_(text)

    def set_expanded(self, boolean):
        self._qt_head._set_expanded_(boolean)
        self._refresh_expand_fnc()

    def set_head_visible(self, boolean):
        self._qt_head.setHidden(not boolean)

    def get_is_expanded(self):
        return self._qt_head._is_expanded_()

    def add_widget(self, widget):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            qt_widget = widget
            self._layout.addWidget(widget)
        else:
            qt_widget = widget.widget
        #
        if qt_widget != self.widget:
            self._layout.addWidget(qt_widget)

    def set_layout_alignment_to_top(self):
        self._layout.setAlignment(
            gui_qt_core.QtCore.Qt.AlignTop
        )

    def set_size_mode(self, mode):
        if mode == 0:
            self._qt_view.setSizePolicy(
                gui_qt_core.QtWidgets.QSizePolicy.Expanding,
                gui_qt_core.QtWidgets.QSizePolicy.Expanding
            )
        elif mode == 1:
            self._qt_view.setSizePolicy(
                gui_qt_core.QtWidgets.QSizePolicy.Expanding,
                gui_qt_core.QtWidgets.QSizePolicy.Minimum
            )

    def set_height_match_to_minimum(self):
        self._qt_view.setSizePolicy(
            gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            gui_qt_core.QtWidgets.QSizePolicy.Minimum
        )

    def set_height_match_to_maximum(self):
        self._qt_view.setSizePolicy(
            gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            gui_qt_core.QtWidgets.QSizePolicy.Maximum
        )

    def connect_expand_changed_to(self, fnc):
        self._qt_head.expand_clicked.connect(fnc)

    def do_clear(self):
        def rcs_fnc_(layout_):
            c = layout_.count()
            for i in range(c):
                i_item = self._layout.takeAt(0)
                if i_item is not None:
                    i_widget = i_item.widget()
                    if i_widget:
                        i_widget.deleteLater()
                    else:
                        _i_layout = i_item.layout()
                        if _i_layout:
                            rcs_fnc_(_i_layout)
                        else:
                            spacer = i_item.spacerItem()
                            if spacer:
                                spacer.deleteLater()

        #
        rcs_fnc_(self._layout)


class PrxHToolGroupA(AbsPrxToolGroup):
    QT_HEAD_CLS = gui_qt_wgt_head.QtHeadStyleA

    QT_HEAD_HEIGHT = 22

    def __init__(self, *args, **kwargs):
        super(PrxHToolGroupA, self).__init__(*args, **kwargs)


class PrxHToolGroupB(AbsPrxToolGroup):
    QT_HEAD_CLS = gui_qt_wgt_head.QtHeadStyleB

    QT_HEAD_HEIGHT = 20

    def __init__(self, *args, **kwargs):
        super(PrxHToolGroupB, self).__init__(*args, **kwargs)


class _Stack(bsc_core.AbsStack):
    def __init__(self):
        super(_Stack, self).__init__()

    def get_key(self, obj):
        return obj.get_path()


class PrxHToolbar(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtWidget
    QT_ORIENTATION = gui_qt_core.QtCore.Qt.Horizontal

    def __init__(self, *args, **kwargs):
        super(PrxHToolbar, self).__init__(*args, **kwargs)

        if self._is_h():
            self.widget.setSizePolicy(
                gui_qt_core.QtWidgets.QSizePolicy.Expanding,
                gui_qt_core.QtWidgets.QSizePolicy.Minimum
            )
        else:
            self.widget.setSizePolicy(
                gui_qt_core.QtWidgets.QSizePolicy.Minimum,
                gui_qt_core.QtWidgets.QSizePolicy.Expanding
            )

        self._language = _gui_core.GuiUtil.get_language()
        self._history_group = ['toolbar']

        self._stack = _Stack()

    def _is_h(self):
        return self.QT_ORIENTATION == gui_qt_core.QtCore.Qt.Horizontal

    def do_gui_refresh(self, fix_bug=False):
        self._qt_view._refresh_widget_all_(fix_bug=fix_bug)

    def _gui_build_fnc(self):
        self._wgt_w, self._wgt_h = 28, 28
        self._wgt_w_min, self._wgt_h_min = 12, 12

        if self._is_h():
            qt_layout_0 = gui_qt_wgt_base.QtHBoxLayout(self._qt_widget)
        else:
            qt_layout_0 = gui_qt_wgt_base.QtVBoxLayout(self._qt_widget)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        qt_layout_0.setSpacing(2)
        # header
        if self._is_h():
            self._qt_head = gui_qt_wgt_head.QtHHeadFrame()
        else:
            self._qt_head = gui_qt_wgt_head.QtVHeadFrame()
        qt_layout_0.addWidget(self._qt_head)
        self._qt_head.expand_toggled.connect(self.set_expanded)
        self._qt_head._set_tool_tip_text_('"LMB-click" to expand "on" / "off"')

        if self._is_h():
            qt_widget_1 = gui_qt_wgt_scroll.QtHScrollBox()
        else:
            qt_widget_1 = gui_qt_wgt_scroll.QtVScrollBox()
        qt_layout_0.addWidget(qt_widget_1)

        self._qt_view = qt_widget_1
        self._qt_layout_0 = qt_widget_1._get_layout_()

        self._refresh_expand_fnc()

        if self._is_h():
            self._qt_view.setSizePolicy(
                gui_qt_core.QtWidgets.QSizePolicy.Expanding,
                gui_qt_core.QtWidgets.QSizePolicy.Minimum
            )
        else:
            self._qt_view.setSizePolicy(
                gui_qt_core.QtWidgets.QSizePolicy.Minimum,
                gui_qt_core.QtWidgets.QSizePolicy.Expanding
            )

    def _refresh_expand_fnc(self):
        if self.get_is_expanded() is True:
            if self._is_h():
                self._qt_head.setMaximumSize(self._wgt_w_min, self._wgt_h)
                self._qt_head.setMinimumSize(self._wgt_w_min, self._wgt_h)

                self.widget.setMaximumHeight(self._wgt_h)
                self.widget.setMinimumHeight(self._wgt_h)
            else:
                self._qt_head.setMaximumSize(self._wgt_w, self._wgt_h_min)
                self._qt_head.setMinimumSize(self._wgt_w, self._wgt_h_min)

                self.widget.setMaximumWidth(self._wgt_w)
                self.widget.setMinimumWidth(self._wgt_w)
        else:
            if self._is_h():
                self._qt_head.setMaximumSize(166667, self._wgt_h_min)
                self._qt_head.setMinimumSize(self._wgt_w_min, self._wgt_h_min)

                self.widget.setMaximumHeight(self._wgt_h_min)
                self.widget.setMinimumHeight(self._wgt_h_min)
            else:
                self._qt_head.setMaximumSize(self._wgt_w_min, 166667)
                self._qt_head.setMinimumSize(self._wgt_w_min, self._wgt_h_min)

                self.widget.setMaximumWidth(self._wgt_w_min)
                self.widget.setMinimumWidth(self._wgt_w_min)

        self._qt_view.setVisible(self.get_is_expanded())
        self._qt_head._refresh_expand_()

    def create_tool_box(self, name, expanded=True, visible=True, size_mode=0, insert_args=None):
        tool_box = _container_for_box.PrxHToolboxOld()
        if isinstance(insert_args, int):
            self.insert_widget_at(insert_args, tool_box)
        else:
            self.add_widget(tool_box)

        tool_box.set_name(name)
        tool_box.set_expanded(expanded)
        tool_box.set_visible(visible)
        tool_box.set_size_mode(size_mode)
        return tool_box

    def set_name(self, name):
        self._qt_head._set_name_text_(
            'tool bar for "{}"'.format(name)
        )

    def set_expanded(self, boolean):
        self._qt_head._set_expanded_(boolean)
        self._refresh_expand_fnc()

    def swap_expanded(self):
        self.set_expanded(not self.get_is_expanded())

    def swap_visible(self):
        self.set_visible(not self.get_is_visible())

    def get_is_expanded(self):
        return self._qt_head._is_expanded_()

    def add_widget(self, widget):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            self._qt_layout_0.addWidget(widget)
        else:
            self._qt_layout_0.addWidget(widget.widget)

    def insert_widget_at(self, index, widget):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            self._qt_layout_0.insertWidget(index, widget)
        else:
            self._qt_layout_0.insertWidget(index, widget.widget)

    def set_width(self, w):
        self._wgt_w = w
        self._refresh_expand_fnc()

    def set_height(self, h):
        self._wgt_h = h
        self._refresh_expand_fnc()

    def get_qt_layout(self):
        return self._qt_layout_0

    def set_top_direction(self):
        self._qt_head._set_expand_direction_(self._qt_head.ExpandDirection.TopToBottom)

    def set_bottom_direction(self):
        self._qt_head._set_expand_direction_(self._qt_head.ExpandDirection.BottomToTop)

    def set_align_center(self):
        self._qt_layout_0.setAlignment(gui_qt_core.QtCore.Qt.AlignHCenter)

    def set_align_left(self):
        self._qt_layout_0.setAlignment(gui_qt_core.QtCore.Qt.AlignLeft)

    def set_align_right(self):
        self._qt_layout_0.setAlignment(gui_qt_core.QtCore.Qt.AlignRight)

    def set_align_top(self):
        self._qt_layout_0.setAlignment(gui_qt_core.QtCore.Qt.AlignTop)

    def set_border_radius(self, radius):
        self._qt_head._set_frame_border_radius_(radius)

    # method for create by configure
    def _create_group_auto(self, path):
        paths = bsc_core.BscPortPath.get_dag_component_paths(path)
        paths.reverse()
        for i_path in paths:
            if self._stack.exists_one(i_path) is False:
                self._create_group(i_path)

        return self._stack.get_one(path)

    def _create_group(self, path):
        if self._is_h():
            gui = _container_for_box.PrxHToolbox()
        else:
            gui = _container_for_box.PrxVToolbox()

        parent_path = bsc_core.BscPortPath.get_dag_parent_path(path)
        if parent_path is None:
            self.add_widget(gui)
        else:
            self._stack.get_one(parent_path).add_widget(gui)

        gui.set_path(path)
        gui.set_name(bsc_core.BscPortPath.to_dag_name(path))
        gui.set_expanded(True)
        self._stack.add_one(gui)

    def _create_group_fnc(self, data):
        if self._is_h():
            gui = _container_for_box.PrxHToolbox()
        else:
            gui = _container_for_box.PrxVToolbox()

        name_ = data.get('name')
        tool_tip_ = data.get('tool_tip')
        if self._language == 'chs':
            if 'gui_name_chs' in data:
                name_ = data['gui_name_chs']

            if 'tool_tip_chs' in data:
                tool_tip_ = data['tool_tip_chs']

        if name_:
            gui.set_name(name_)
        if tool_tip_:
            gui.set_tool_tip(tool_tip_)

        gui.set_expanded(data.get('expand', True))
        gui.set_visible(data.get('visible', True))
        gui.set_size_mode([0, 1][data.get('size_mode', 'fixed') == 'expanding'])
        return gui

    def _create_button_fnc(self, data):
        mode_ = data.get('mode')
        if mode_ == 'toggle':
            gui = _utility.PrxIconToggleButton()
        else:
            gui = _utility.PrxIconPressButton()

        name_ = data.get('name')
        tool_tip_ = data.get('tool_tip')
        if self._language == 'chs':
            if 'gui_name_chs' in data:
                name_ = data['gui_name_chs']

            if 'tool_tip_chs' in data:
                tool_tip_ = data['tool_tip_chs']

        if name_:
            gui.set_name(name_)
        if tool_tip_:
            gui.set_tool_tip(tool_tip_)

        icon_name_ = data.get('icon_name')
        if icon_name_:
            gui.set_icon_name(icon_name_)
        return gui

    def _update_exclusive_set(self, paths):
        tools = []
        for i_path in paths:
            i_path = i_path.replace('/', '.')
            i_tool = self.get_tool(i_path)
            tools.append(i_tool._qt_widget)
            i_tool._qt_widget._set_exclusive_widgets_(tools)

    def build_by_data(self, data):
        for k, v in data.items():
            self._create_by_data(k.replace('/', '.'), v)

    def _create_by_data(self, path, data):
        parent_path = bsc_core.BscPortPath.get_dag_parent_path(path)
        widget_ = data['widget']
        if widget_ == 'group':
            gui = self._create_group_fnc(data)
        elif widget_ == 'button':
            gui = self._create_button_fnc(data)
        else:
            raise RuntimeError()

        gui.set_path(path)
        self._stack.add_one(gui)

        if parent_path is None:
            self.add_widget(gui)
        else:
            parent_gui = self._stack.get_one(parent_path)
            if parent_gui is None:
                parent_gui = self._create_group_auto(parent_path)
            parent_gui.add_widget(gui)

        # run latest
        if 'exclusive_set' in data:
            self._update_exclusive_set(data['exclusive_set'])

    def get_tool(self, path):
        return self._stack.get_one(path)

    def set_history_group(self, arg):
        if arg:
            if isinstance(arg, six.string_types):
                _ = [arg]
            elif isinstance(arg, (tuple, list)):
                _ = list(arg)
            else:
                raise RuntimeError()

            self._history_group = _

    def get_history_group(self):
        return self._history_group


class PrxVToolbar(PrxHToolbar):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtWidget
    QT_ORIENTATION = gui_qt_core.QtCore.Qt.Vertical

    def __init__(self, *args, **kwargs):
        super(PrxVToolbar, self).__init__(*args, **kwargs)
