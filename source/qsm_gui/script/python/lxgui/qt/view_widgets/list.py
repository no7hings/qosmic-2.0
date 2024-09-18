# coding=utf-8
import six

import collections

import lxbasic.core as bsc_core
# gui
from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from ...qt import abstracts as _qt_abstracts

from ..widgets import base as _qt_wgt_base

from ..widgets import utility as _wgt_utility

from ..widgets import entry_frame as _wgt_entry_frame

from ..widgets import scroll as _wgt_scroll

from ..widgets import container as _wgt_container

from ..widgets import button as _wgt_button

from ..widgets import chart as _wgt_chart

from ..widgets import input_for_filter as _wgt_input_for_filter

from ..view_models import base as _vew_mod_base

from ..view_models import list as _vew_mod_list

from . import item_for_list as _item_for_list

from . import base as _base


class _QtListItemDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, *args, **kwargs):
        QtWidgets.QStyledItemDelegate.__init__(self, *args, **kwargs)

    def paint(self, painter, option, index):
        self.parent()._view_model.draw_item(painter, option, index)


class _QtListViewWidget(
    QtWidgets.QListWidget,
    _vew_mod_base.AbsView,
    _qt_abstracts.AbsQtThreadWorkerExtraDef,
):
    QT_MENU_CLS = _wgt_utility.QtMenu

    def __init__(self, *args, **kwargs):
        super(_QtListViewWidget, self).__init__(*args, **kwargs)

        self.setStyleSheet(_qt_core.GuiQtStyle.get('QListView'))
        self.verticalScrollBar().setStyleSheet(_qt_core.GuiQtStyle.get('QScrollBar'))
        self.horizontalScrollBar().setStyleSheet(_qt_core.GuiQtStyle.get('QScrollBar'))

        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setMouseTracking(True)

        self.setResizeMode(self.Adjust)
        self.setViewMode(self.IconMode)

        self.setSelectionMode(self.ExtendedSelection)
        self.setVerticalScrollMode(self.ScrollPerItem)
        self.setDragEnabled(False)
        # noinspection PyUnresolvedReferences
        self.itemSelectionChanged.connect(self.item_select_changed.emit)

        self._view_model = _vew_mod_list.ListViewModel(self)
        self._view_model.data.item.cls = _item_for_list.QtListItem

        self.setItemDelegate(_QtListItemDelegate(self))

        self._item_dict = collections.OrderedDict()

        self._init_thread_worker_extra_def_(self)

        self.installEventFilter(self)
        self.viewport().installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.FocusIn:
                # self._is_focused = True
                parent = self.parent()
                if isinstance(parent, _wgt_entry_frame.QtEntryFrame):
                    parent._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                # self._is_focused = False
                parent = self.parent()
                if isinstance(parent, _wgt_entry_frame.QtEntryFrame):
                    parent._set_focused_(False)
        # view port
        elif widget == self.viewport():
            if event.type() == QtCore.QEvent.ToolTip:
                self._view_model.do_item_tool_tip(event)

            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.buttons() == QtCore.Qt.LeftButton:
                    self._view_model.do_item_press_click(event)
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.buttons() == QtCore.Qt.LeftButton:
                    self._view_model.do_item_press_dbl_click(event)
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.NoButton:
                    self._view_model.do_item_hover_move(event)

            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self.press_released.emit()
        return False

    def paintEvent(self, event):
        if not self.count():
            painter = _qt_core.QtPainter(self.viewport())
            painter._draw_empty_image_by_rect_(
                self.rect(),
                'placeholder/empty'
            )
        else:
            super(_QtListViewWidget, self).paintEvent(event)

    def contextMenuEvent(self, event):
        menu = None

        menu_data = self._view_model.get_menu_data()
        menu_content = self._view_model.get_menu_content()
        menu_data_generate_fnc = self._view_model.get_menu_data_generate_fnc()

        if menu_content:
            if menu is None:
                menu = self.QT_MENU_CLS(self)
            menu._set_menu_content_(menu_content, append=True)

        if menu_data:
            if menu is None:
                menu = self.QT_MENU_CLS(self)
            menu._set_menu_data_(menu_data)

        if menu_data_generate_fnc:
            if menu is None:
                menu = self.QT_MENU_CLS(self)
            menu._set_menu_data_(menu_data_generate_fnc())

        # data from item
        item = self.itemAt(event.pos())
        if item:
            item_menu_data = item._item_model.get_menu_data()
            item_menu_content = item._item_model.get_menu_content()
            item_menu_data_generate_fnc = item._item_model.get_menu_data_generate_fnc()
            if item_menu_content:
                if menu is None:
                    menu = self.QT_MENU_CLS(self)
                menu._set_menu_content_(item_menu_content, append=True)

            if item_menu_data:
                if menu is None:
                    menu = self.QT_MENU_CLS(self)
                menu._set_menu_data_(item_menu_data)

            if item_menu_data_generate_fnc:
                if menu is None:
                    menu = self.QT_MENU_CLS(self)
                menu._set_menu_data_(item_menu_data_generate_fnc())

        if menu is not None:
            menu._popup_start_()

    def wheelEvent(self, event):
        if _qt_core.QtUtil.is_ctrl_modifier():
            self._view_model.on_wheel(event)
            event.ignore()
        else:
            super(_QtListViewWidget, self).wheelEvent(event)


class QtListWidget(
    _base._BaseViewWidget
):
    FILTER_COMPLETION_MAXIMUM = 50

    def __init__(self, *args, **kwargs):
        super(QtListWidget, self).__init__(*args, **kwargs)
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

        self._check_tool_box = self._create_left_tool_box_('check')
        self._sort_and_group_tool_box = self._create_left_tool_box_('sort and group')
        self._keyword_filter_tool_box = self._create_top_tool_box_('keyword filter', size_mode=1)

        self._view = _QtListViewWidget()
        self._grid_lot.addWidget(self._view, 1, 1, 1, 1)
        self._view.setFocusProxy(self)
        self._view_model = self._view._view_model

        self._info_bar_chart = _wgt_chart.QtChartForInfoBar()
        self._grid_lot.addWidget(self._info_bar_chart, 2, 1, 1, 1)
        self._info_bar_chart.hide()
        self._view.info_text_accepted.connect(
            self._info_bar_chart._set_text_
        )

        self._build_check_tool_box_()
        self._build_sort_and_group_tool_box_()
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

    def _build_check_tool_box_(self):
        self._check_all_button = _wgt_button.QtIconPressButton()
        self._check_all_button._set_name_text_('check all')
        self._check_all_button._set_icon_file_path_(_gui_core.GuiIcon.get('all_checked'))
        self._check_tool_box._add_widget_(self._check_all_button)
        self._check_all_button.press_clicked.connect(self._on_check_all_)
        self._check_all_button._set_tool_tip_text_(
            '"LMB-click" for checked all visible items'
        )
        self._check_all_button._set_menu_data_(
            [
                ('check visible', 'tool/show', self._on_check_visible_)
            ]
        )
        #
        self._uncheck_all_button = _wgt_button.QtIconPressButton()
        self._uncheck_all_button._set_icon_file_path_(_gui_core.GuiIcon.get('all_unchecked'))
        self._uncheck_all_button._set_name_text_('uncheck all')
        self._check_tool_box._add_widget_(self._uncheck_all_button)
        self._uncheck_all_button.press_clicked.connect(self._on_uncheck_all_)
        self._uncheck_all_button._set_tool_tip_text_(
            '"LMB-click" for unchecked all visible items'
        )
        self._uncheck_all_button._set_menu_data_(
            [
                ('uncheck visible', 'tool/show', self._on_uncheck_visible_)
            ]
        )

    def _build_sort_and_group_tool_box_(self):
        self._sort_button = _wgt_button.QtIconPressButton()
        self._sort_button._set_name_text_('sort')
        self._sort_button._set_icon_file_path_(_gui_core.GuiIcon.get('tool/sort-by-name-ascend'))
        self._sort_and_group_tool_box._add_widget_(self._sort_button)

        self._sort_button._set_menu_data_generate_fnc_(
            self._view_model.generate_item_sort_menu_data
        )
        self._sort_button.press_clicked.connect(self._on_sort_order_swap_)

    def _build_keyword_filter_tool_box_(self):
        self._keyword_filter_input = _wgt_input_for_filter.QtInputAsFilter()
        self._keyword_filter_tool_box._add_widget_(self._keyword_filter_input)

        self._keyword_filter_input._set_input_completion_buffer_fnc_(self._keyword_filter_input_completion_buffer_fnc)
        self._keyword_filter_input.input_value_changed.connect(self._on_keyword_filer)
        self._keyword_filter_input.occurrence_previous_press_clicked.connect(
            self._view_model.occurrence_item_previous
        )
        self._keyword_filter_input.occurrence_next_press_clicked.connect(
            self._view_model.occurrence_item_next
        )
        self._keyword_filter_input._set_occurrence_buttons_enable_(True)

    def _on_check_all_(self):
        self._view_model.set_all_items_checked(True)

    def _on_check_visible_(self):
        self._view_model.set_visible_items_checked(True)

    def _on_uncheck_all_(self):
        self._view_model.set_all_items_checked(False)

    def _on_uncheck_visible_(self):
        self._view_model.set_visible_items_checked(False)

    def _on_sort_order_swap_(self):
        self._view_model.swap_item_sort_order()
        order = ['ascend', 'descend'][self._view_model.get_item_sort_order()]
        self._sort_button._set_icon_file_path_(
            _gui_core.GuiIcon.get('tool/sort-by-name-{}'.format(order)),
        )

    def _on_keyword_filer(self):
        self._view_model.set_keyword_filter_key_src(
            self._keyword_filter_input._get_all_keywords_()
        )
        self._view_model.refresh_items_visible_by_any_filter()

    def _keyword_filter_input_completion_buffer_fnc(self, *args, **kwargs):
        keyword = args[0]
        if keyword:
            _ = bsc_core.BscFnmatch.filter(
                self._view_model.generate_keyword_filter_completion_cache(), six.u('*{}*').format(keyword)
            )
            return bsc_core.RawTextsMtd.sort_by_initial(_)[:self.FILTER_COMPLETION_MAXIMUM]
        return []
