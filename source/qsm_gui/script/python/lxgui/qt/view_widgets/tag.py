# coding=utf-8
import lxbasic.core as bsc_core
# gui
from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core
# qt widgets
from ..widgets import base as _wgt_base

from ..widgets import utility as _wgt_utility

from ..widgets import container as _wgt_container

from ..widgets import button as _wgt_button

from ..widgets import scroll as _wgt_scroll

from ..widgets import input_for_filter as _wgt_input_for_filter

from ..widgets import view_for_histogram_chart as _wgt_view_for_histogram_chart

from ..view_models import tag as _vew_mod_tag

from . import base as _base

from . import item_for_tag as _item_for_tag


class _QtTagViewWidget(
    QtWidgets.QWidget,

    _item_for_tag._AbsTagBase,
):
    SPACING = 2

    MARGIN = 2

    check_paths_change_accepted = qt_signal(list)
    check_paths_changed = qt_signal()

    focus_changed = qt_signal()

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        pass

    def _user_filter_check_cbk_(self):
        self.check_paths_change_accepted.emit(
            self._get_all_checked_node_paths_()
        )
        self.check_paths_changed.emit()

    def __init__(self, *args, **kwargs):
        super(_QtTagViewWidget, self).__init__(*args, **kwargs)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.setMinimumHeight(self.HEIGHT)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        self._init_tag_base_(self)

        self._frame_background_color = _qt_core.QtBackgroundColors.Dim

        self._lot = _wgt_base.QtVBoxLayout(self)
        self._lot.setContentsMargins(self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN)
        self._lot.setAlignment(QtCore.Qt.AlignTop)

        self._sca = _wgt_utility.QtVScrollArea()
        self._lot.addWidget(self._sca)
        self._sca._set_background_color_(self._frame_background_color)
        self._sca._set_empty_draw_flag_(True)
        self._sca._layout.setAlignment(QtCore.Qt.AlignTop)

        self._view_model = _vew_mod_tag.TagViewModel(self)
        self._view_model._data.item.cls = _item_for_tag._QtTagNode
        self._view_model._data.item.group_cls = _item_for_tag._QtTagGroup

        self._item_dict = self._view_model._data.item_dict

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
        return False

    def paintEvent(self, event):
        pass
        # if not self._item_dict:
        #     painter = _qt_core.QtPainter(self)
        #     painter._draw_empty_image_by_rect_(
        #         self.rect(),
        #         self._empty_icon_name
        #     )
        # offset = self._sca.verticalScrollBar().value()
        # h = self._sca._layout.minimumSize().height()
        # x, y = 0, 0
        # print offset, h

    def _create_root_(self, path, *args, **kwargs):
        widget = _item_for_tag._QtTagGroup()
        self._sca._add_widget_(widget)
        widget._set_path_text_(path)
        if 'show_name' in kwargs:
            widget._set_text_(kwargs['show_name'])
        else:
            widget._set_text_('All')

        widget._set_group_root_(self)
        self._item_dict[path] = widget
        widget.user_filter_checked.connect(self._user_filter_check_cbk_)
        self._sca._set_empty_draw_flag_(False)
        return widget

    def _create_group_(self, path, *args, **kwargs):
        if path in self._item_dict:
            return self._item_dict[path]

        if path == self.PATHSEP:
            return self._create_root_(path, *args, **kwargs)

        group_widget = self._item_dict[bsc_core.BscPath.get_dag_parent_path(path)]
        widget = group_widget._create_group_(path, *args, **kwargs)

        widget._set_group_root_(self)
        self._item_dict[path] = widget
        widget.user_filter_checked.connect(self._user_filter_check_cbk_)
        return widget

    def _create_node_(self, path, *args, **kwargs):
        if path in self._item_dict:
            return self._item_dict[path]

        group_widget = self._item_dict[bsc_core.BscPath.get_dag_parent_path(path)]
        widget = group_widget._create_node_(path, *args, **kwargs)

        widget._set_group_root_(self)
        self._item_dict[path] = widget
        widget.user_filter_checked.connect(self._user_filter_check_cbk_)
        return widget

    def _check_exists_(self, path):
        return path in self._item_dict

    def _clear_all_checked_(self):
        [x._set_checked_(False) for x in self._item_dict.values()]

    def _get_one_(self, path):
        return self._item_dict[path]

    def _get_all_checked_node_paths_(self):
        return [x._get_path_text_() for x in self._get_all_checked_nodes_()]

    def _get_all_checked_nodes_(self):
        return [x for x in self._item_dict.values() if x._is_checked_() and isinstance(x, _item_for_tag._QtTagNode)]

    def _apply_intersection_paths_(self, path_set):
        [x._update_path_set_as_intersection_(path_set) for x in self._item_dict.values()]

    def _restore_(self):
        self._item_dict.clear()
        self._sca._layout._clear_all_widgets_()
        self._sca._set_empty_draw_flag_(True)

    def _collapse_all_group_items_(self):
        [x._set_expanded_(False) for x in self._item_dict.values() if isinstance(x, _item_for_tag._QtTagGroup)]

    def _expand_exclusive_for_node_(self, path):
        self._collapse_all_group_items_()
        paths = bsc_core.BscPath.get_dag_component_paths(path)
        for i in paths:
            if i in self._item_dict:
                i_widget = self._item_dict[i]
                if isinstance(i_widget, _item_for_tag._QtTagGroup):
                    i_widget._set_expanded_(True)

    def _expand_all_groups_(self):
        [x._set_expanded_(True) for x in self._item_dict.values() if isinstance(x, _item_for_tag._QtTagGroup)]

    def _expand_for_all_from_(self, path):
        self._collapse_all_group_items_()
        paths = bsc_core.BscPath.get_dag_component_paths(path)
        self._set_expanded_for_(paths, True)
        descendant_paths = bsc_core.BscPath.find_dag_descendant_paths(path, self._item_dict.keys())
        self._set_expanded_for_(descendant_paths, True)

    def _set_expanded_for_(self, paths, boolean):
        for i in paths:
            if i in self._item_dict:
                i_widget = self._item_dict[i]
                if isinstance(i_widget, _item_for_tag._QtTagGroup):
                    i_widget._set_expanded_(boolean)

    def _set_force_hidden_flag_for_group_(self, path, boolean):
        pass

    def _generate_chart_data_(self):
        dict_ = {}
        for i_wgt in self._item_dict.values():
            if isinstance(i_wgt, _item_for_tag._QtTagGroup):
                i_dict = {}
                for j_wgt in i_wgt._node_widgets:
                    j_value = j_wgt._number
                    if j_value:
                        i_dict[j_wgt._text] = j_value
                if i_dict:
                    dict_[i_wgt._text] = i_dict
        return dict_


class QtTagWidget(
    _base._BaseViewWidget
):
    FILTER_COMPLETION_MAXIMUM = 50

    def __init__(self, *args, **kwargs):
        super(QtTagWidget, self).__init__(*args, **kwargs)
        # refresh
        self._refresh_button = _wgt_button.QtIconPressButton()
        self._grid_lot.addWidget(self._refresh_button, 0, 0, 1, 1)
        self._refresh_button.setFixedSize(28, 28)
        self._refresh_button._set_icon_file_path_(
            _gui_core.GuiIcon.get('refresh')
        )
        self._refresh_button.press_clicked.connect(self.refresh.emit)
        # top
        self._top_scroll_box = _wgt_scroll.QtHScrollBox()
        self._grid_lot.addWidget(self._top_scroll_box, 0, 1, 1, 1)
        self._top_scroll_box._set_layout_align_left_or_top_()
        self._top_scroll_box.setFixedHeight(28)
        # left
        self._left_scroll_box = _wgt_scroll.QtVScrollBox()
        self._grid_lot.addWidget(self._left_scroll_box, 1, 0, 1, 1)
        self._left_scroll_box._set_layout_align_left_or_top_()
        self._left_scroll_box.setFixedWidth(28)
        # keyword filter
        self._keyword_filter_tool_box = self._create_top_tool_box_('keyword filter', size_mode=1)
        # chart
        self._sort_chart_tool_box = self._create_left_tool_box_('sort and chart')

        self._view = _QtTagViewWidget()
        self._grid_lot.addWidget(self._view, 1, 1, 1, 1)
        self._view.setFocusProxy(self)
        self._view_model = self._view._view_model

        self._build_chart_tool_box_()
        self._build_keyword_filter_tool_box_()

    def _create_top_tool_box_(self, name, size_mode=0):
        tool_box = _wgt_container.QtHToolBox()
        self._top_scroll_box.addWidget(tool_box)
        tool_box._set_expanded_(True)
        tool_box._set_name_text_(name)
        tool_box._set_size_mode_(size_mode)
        return tool_box

    def _create_left_tool_box_(self, name):
        tool_box = _wgt_container.QtVToolBox()
        self._left_scroll_box.addWidget(tool_box)
        tool_box._set_expanded_(True)
        tool_box._set_name_text_(name)
        return tool_box

    def _build_chart_tool_box_(self):
        self._chat_button = _wgt_button.QtIconPressButton()
        self._chat_button._set_name_text_('chart')
        self._chat_button._set_icon_file_path_(_gui_core.GuiIcon.get('tool/chart'))
        self._sort_chart_tool_box._add_widget_(self._chat_button)
        self._chat_button.press_clicked.connect(self._on_show_chart_)

    def _build_keyword_filter_tool_box_(self):
        self._keyword_filter_completion_cache = None
        self._keyword_filter_input = _wgt_input_for_filter.QtInputAsFilter()
        self._keyword_filter_tool_box._add_widget_(self._keyword_filter_input)

    def _on_show_chart_(self):
        data = self._view._generate_chart_data_()
        if data:
            chart_view = _wgt_view_for_histogram_chart.QtViewForHistogramChart()
            chart_view._set_data_(data)
            _qt_core.QtApplication.show_tool_dialog(
                widget=chart_view, title='Histogram Chart', size=(640, 480), parent=self
            )