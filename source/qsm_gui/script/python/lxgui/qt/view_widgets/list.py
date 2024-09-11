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

from ..widgets import entry_frame as _wgt_entry_frame

from ..widgets import container as _wgt_container

from ..widgets import button as _wgt_button

from ..widgets import chart as _wgt_chart

from ..widgets import input_for_filter as _wgt_input_for_filter

from .. import view_models as _view_models

from . import item_for_list as _item_for_list


class _QtListItemDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, *args, **kwargs):
        QtWidgets.QStyledItemDelegate.__init__(self, *args, **kwargs)

    def paint(self, painter, option, index):
        self.parent()._view_model.draw_item(painter, option, index)


class QtListView(
    QtWidgets.QListWidget,
    _qt_abstracts.AbsQtThreadWorkerExtraDef,
):
    item_check_changed = qt_signal()

    info_text_accepted = qt_signal(str)

    def __init__(self, *args, **kwargs):
        super(QtListView, self).__init__(*args, **kwargs)

        self.setStyleSheet(_qt_core.GuiQtStyle.get('QListView'))
        self.verticalScrollBar().setStyleSheet(_qt_core.GuiQtStyle.get('QScrollBar'))
        self.horizontalScrollBar().setStyleSheet(_qt_core.GuiQtStyle.get('QScrollBar'))

        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setMouseTracking(True)

        self.setResizeMode(self.Adjust)
        self.setViewMode(self.IconMode)
        self.setSelectionMode(self.SingleSelection)
        self.setVerticalScrollMode(self.ScrollPerItem)
        self.setDragEnabled(False)

        self._view_model = _view_models.ViewModelForList(self)
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
                    pass
        return False

    def wheelEvent(self, event):
        if _qt_core.QtUtil.is_ctrl_modifier():
            self._view_model.on_wheel(event)
            event.ignore()
        else:
            super(QtListView, self).wheelEvent(event)


class QtListWidget(
    _wgt_entry_frame.QtEntryFrame
):
    FILTER_COMPLETION_MAXIMUM = 50

    def __init__(self, *args, **kwargs):
        super(QtListWidget, self).__init__(*args, **kwargs)

        lot = _qt_wgt_base.QtVBoxLayout(self)
        lot.setContentsMargins(*[4]*4)
        lot.setSpacing(2)

        self._tool_bar = _wgt_container.QtHToolBar()
        lot.addWidget(self._tool_bar)
        self._tool_bar._set_expanded_(True)
        self._tool_bar._set_align_left_()

        self._check_tool_box = self._tool_bar._create_tool_box_('check')
        self._keyword_filter_tool_box = self._tool_bar._create_tool_box_('keyword filter', size_mode=1)

        self._view = QtListView()
        lot.addWidget(self._view)

        self._info_bar_chart = _wgt_chart.QtChartForInfoBar()
        lot.addWidget(self._info_bar_chart)
        self._info_bar_chart.hide()
        self._view.info_text_accepted.connect(
            self._info_bar_chart._set_text_
        )

        self._build_check_tool_box()
        self._build_filter_tool_box()

    def _build_check_tool_box(self):
        self._check_all_button = _wgt_button.QtIconPressButton()
        self._check_all_button._set_name_text_('check all')
        self._check_all_button._set_icon_file_path_(_gui_core.GuiIcon.get('all_checked'))
        self._check_tool_box._add_widget_(self._check_all_button)
        self._check_all_button.press_clicked.connect(self._on_check_all_)
        self._check_all_button._set_tool_tip_text_(
            '"LMB-click" for checked all visible items'
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

    def _build_filter_tool_box(self):
        self._keyword_filter_completion_cache = None
        self._keyword_filter_input = _wgt_input_for_filter.QtInputAsFilter()
        self._keyword_filter_tool_box._add_widget_(self._keyword_filter_input)

        self._keyword_filter_input._set_input_completion_buffer_fnc_(self._keyword_filter_input_completion_buffer_fnc)
        self._keyword_filter_input.input_value_changed.connect(self._on_keyword_filer)
        self._keyword_filter_input.occurrence_previous_press_clicked.connect(
            self._view._view_model.occurrence_item_previous
        )
        self._keyword_filter_input.occurrence_next_press_clicked.connect(
            self._view._view_model.occurrence_item_next
        )
        self._keyword_filter_input._set_occurrence_buttons_enable_(True)

    def _on_check_all_(self):
        self._view._view_model.set_all_items_checked(True)

    def _on_uncheck_all_(self):
        self._view._view_model.set_all_items_checked(False)

    def _on_keyword_filer(self):
        self._view._view_model.set_keyword_filter_key_src(
            self._keyword_filter_input._get_all_keywords_()
        )
        self._view._view_model.refresh_items_visible_by_any_filter()

    def _keyword_filter_input_completion_buffer_fnc(self, *args, **kwargs):
        keyword = args[0]
        if keyword:
            if self._keyword_filter_completion_cache is None:
                self._keyword_filter_completion_cache = self._view._view_model.get_all_items_keyword_filter_keys()

            _ = bsc_core.BscFnmatch.filter(
                self._keyword_filter_completion_cache, six.u('*{}*').format(keyword)
            )
            return bsc_core.RawTextsMtd.sort_by_initial(_)[:self.FILTER_COMPLETION_MAXIMUM]
        return []
