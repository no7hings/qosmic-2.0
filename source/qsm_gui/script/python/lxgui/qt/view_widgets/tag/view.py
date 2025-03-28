# coding=utf-8
import lxbasic.core as bsc_core
# gui
from .... import core as _gui_core
# qt
from ....qt.core.wrap import *

from ....qt import core as _qt_core

from ....qt import abstracts as _qt_abstracts
# qt widgets
from ...widgets import base as _wgt_base

from ...widgets import utility as _wgt_utility

from ...widgets import container as _wgt_container

from ...widgets import button as _wgt_button

from ...widgets import scroll as _wgt_scroll

from ...widgets.input import input_for_filter as _wgt_input_for_filter

from ...chart_widgets import histogram as _cht_wgt_for_histogram

from ...view_models.tag import view as _vew_mod_tag

from .. import base as _base

from . import item as _item


class _QtTagViewWidget(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtThreadWorkerExtraDef,
):
    INDENT = 20
    HEIGHT = 18

    PATHSEP = '/'

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

        self._frame_background_color = _qt_core.QtRgba.Dim

        self._lot = _wgt_base.QtVBoxLayout(self)
        self._lot.setContentsMargins(self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN)
        self._lot.setAlignment(QtCore.Qt.AlignTop)

        self._sca = _wgt_utility.QtVScrollArea()
        self._lot.addWidget(self._sca)
        self._sca._set_background_color_(self._frame_background_color)
        self._sca._set_empty_draw_flag_(True)
        self._sca._layout.setAlignment(QtCore.Qt.AlignTop)

        self._view_model = _vew_mod_tag.TagViewModel(self)
        self._view_model._data.item.cls = _item._QtTagNodeItem
        self._view_model._data.item.group_cls = _item._QtTagGroupItem

        self._item_dict = self._view_model._data.item_dict

        self._init_thread_worker_extra_def_(self)

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
        if path in self._item_dict:
            return False, self._item_dict[path]

        widget = _item._QtTagGroupItem()
        self._sca._add_widget_(widget)

        widget._item_model.set_path(path)

        widget._set_view_(self)
        self._item_dict[path] = widget
        widget.user_filter_checked.connect(self._user_filter_check_cbk_)
        self._sca._set_empty_draw_flag_(False)
        return True, widget

    def _create_group_(self, path, *args, **kwargs):
        if path in self._item_dict:
            return False, self._item_dict[path]

        if path == self.PATHSEP:
            return self._create_root_(path, *args, **kwargs)

        group_widget = self._item_dict[bsc_core.BscNodePath.get_dag_parent_path(path)]
        widget = group_widget._create_group_(path, *args, **kwargs)

        widget._set_view_(self)
        self._item_dict[path] = widget
        widget.user_filter_checked.connect(self._user_filter_check_cbk_)
        return True, widget

    def _create_node_(self, path, *args, **kwargs):
        if path in self._item_dict:
            return False, self._item_dict[path]

        group_widget = self._item_dict[bsc_core.BscNodePath.get_dag_parent_path(path)]
        widget = group_widget._create_node_(path, *args, **kwargs)

        # update item properties
        if self._view_model.is_item_color_enable() is True:
            path_opt = bsc_core.BscNodePathOpt(path)
            name = path_opt.get_name()
            widget._item_model.set_color_rgb(bsc_core.BscTextOpt(name).to_hash_rgb(s_p=(35, 50), v_p=(75, 95)))

        widget._set_view_(self)
        self._item_dict[path] = widget
        widget.user_filter_checked.connect(self._user_filter_check_cbk_)
        return True, widget

    def _uncheck_all_items_(self):
        [x._set_checked_(False) for x in self._item_dict.values()]

    def _get_one_(self, path):
        return self._item_dict[path]

    def _get_all_checked_node_paths_(self):
        return [x._item_model.get_path() for x in self._get_all_checked_nodes_()]

    def _get_all_checked_nodes_(self):
        return [x for x in self._item_dict.values() if x._is_checked_() and isinstance(x, _item._QtTagNodeItem)]

    def _apply_intersection_paths_(self, path_set):
        [x._update_path_set_as_intersection_(path_set) for x in self._item_dict.values()]

    def _restore_(self):
        self._item_dict.clear()
        self._sca._layout._clear_all_widgets_()
        self._sca._set_empty_draw_flag_(True)

    def _collapse_all_group_items_(self):
        [x._set_expanded_(False) for x in self._item_dict.values() if isinstance(x, _item._QtTagGroupItem)]

    def _expand_exclusive_for_node_(self, path):
        self._collapse_all_group_items_()
        paths = bsc_core.BscNodePath.get_dag_component_paths(path)
        for i in paths:
            if i in self._item_dict:
                i_widget = self._item_dict[i]
                if isinstance(i_widget, _item._QtTagGroupItem):
                    i_widget._set_expanded_(True)

    def _expand_all_group_items_(self):
        [x._set_expanded_(True) for x in self._item_dict.values() if isinstance(x, _item._QtTagGroupItem)]

    def _expand_for_all_from_(self, path):
        self._collapse_all_group_items_()
        paths = bsc_core.BscNodePath.get_dag_component_paths(path)
        self._set_expanded_for_(paths, True)
        descendant_paths = bsc_core.BscNodePath.find_dag_descendant_paths(path, self._item_dict.keys())
        self._set_expanded_for_(descendant_paths, True)

    def _set_expanded_for_(self, paths, boolean):
        for i in paths:
            if i in self._item_dict:
                i_widget = self._item_dict[i]
                if isinstance(i_widget, _item._QtTagGroupItem):
                    i_widget._set_expanded_(boolean)

    def _set_force_hidden_flag_for_group_(self, path, boolean):
        pass

    def _generate_chart_data_(self):
        dict_ = {}
        for i_wgt in self._item_dict.values():
            if isinstance(i_wgt, _item._QtTagGroupItem):
                i_dict = {}
                for j_wgt in i_wgt._node_widgets:
                    j_value = j_wgt._item_model.get_number()
                    if j_value:
                        i_dict[j_wgt._item_model.get_name()] = j_value
                if i_dict:
                    dict_[i_wgt._item_model.get_name()] = i_dict
        return dict_

    def _get_all_nodes_(self):
        return [x for x in self._item_dict.values() if isinstance(x, _item._QtTagNodeItem)]

    def _get_all_items_(self):
        return self._item_dict.values()


class QtTagWidget(
    _base._BaseViewWidget
):
    FILTER_COMPLETION_MAXIMUM = 50

    def __init__(self, *args, **kwargs):
        super(QtTagWidget, self).__init__(*args, **kwargs)
        # refresh
        self._refresh_button = _wgt_button.QtIconPressButton()
        self._grid_lot.addWidget(self._refresh_button, 0, 0, 1, 1)
        self._refresh_button.setFixedSize(self.TOOL_BAR_W, self.TOOL_BAR_W)
        self._refresh_button._set_icon_file_path_(
            _gui_core.GuiIcon.get('refresh')
        )
        self._refresh_button.press_clicked.connect(self.refresh.emit)
        # top
        self._top_scroll_box = _wgt_scroll.QtHScrollBox()
        self._grid_lot.addWidget(self._top_scroll_box, 0, 1, 1, 1)
        self._top_scroll_box._set_layout_align_left_or_top_()
        self._top_scroll_box.setFixedHeight(self.TOOL_BAR_W)
        # left
        self._left_scroll_box = _wgt_scroll.QtVScrollBox()
        self._grid_lot.addWidget(self._left_scroll_box, 1, 0, 1, 1)
        self._left_scroll_box._set_layout_align_left_or_top_()
        self._left_scroll_box.setFixedWidth(self.TOOL_BAR_W)
        # keyword filter
        self._keyword_filter_tool_box = self._add_top_tool_box('keyword filter', size_mode=1)
        # chart
        self._sort_chart_tool_box = self._add_left_tool_box('sort and chart')

        self._view = _QtTagViewWidget()
        self._grid_lot.addWidget(self._view, 1, 1, 1, 1)
        self._view.setFocusProxy(self)
        self._view_model = self._view._view_model

        self._build_chart_tool_box_()
        self._build_keyword_filter_tool_box()

    def _add_top_tool_box(self, name, size_mode=0):
        tool_box = _wgt_container.QtHToolBox()
        self._top_scroll_box.addWidget(tool_box)
        tool_box._set_expanded_(True)
        tool_box._set_name_text_(name)
        tool_box._set_size_mode_(size_mode)
        return tool_box

    def _add_left_tool_box(self, name):
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

    def _build_keyword_filter_tool_box(self):
        self._keyword_filter_completion_cache = None
        self._keyword_filter_input = _wgt_input_for_filter.QtInputForFilter()
        self._keyword_filter_tool_box._add_widget_(self._keyword_filter_input)

    def _on_show_chart_(self):
        data = self._view._generate_chart_data_()
        if data:
            chart_view = _cht_wgt_for_histogram.QtHistogramChartWidget()
            chart_view._set_data_(data)
            _qt_core.QtApplication.show_tool_dialog(
                widget=chart_view, title='Histogram Chart', size=(640, 480), parent=self
            )

    def _hide_all_tool_bar_(self):
        self._toolbar_hide_flag = True
        self._refresh_button.hide()
        self._top_scroll_box.hide()
        self._left_scroll_box.hide()
