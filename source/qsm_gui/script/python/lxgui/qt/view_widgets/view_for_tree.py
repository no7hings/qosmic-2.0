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

from ..widgets import utility as _wgt_utility

from ..widgets import container as _wgt_container

from ..widgets import button as _wgt_button

from ..widgets import scroll as _wgt_scroll

from ..widgets import chart as _wgt_chart

from ..widgets import input_for_filter as _wgt_input_for_filter

from ..widgets import view_for_histogram_chart as _wgt_view_for_histogram_chart

from ..view_models import base as _vew_mod_base

from ..view_models import view_for_tree as _vew_mod_tree

from . import item_for_tree as _item_for_tree

from . import base as _base


class _QtListItemDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, *args, **kwargs):
        QtWidgets.QStyledItemDelegate.__init__(self, *args, **kwargs)

    def paint(self, painter, option, index):
        # super(_QtListItemDelegate, self).paint(painter, option, index)
        self.parent()._view_model.draw_item(painter, option, index)


class _QtTreeViewWidget(
    QtWidgets.QTreeWidget,
    _vew_mod_base.AbsView,
    _qt_abstracts.AbsQtThreadWorkerExtraDef,
):
    QT_MENU_CLS = _wgt_utility.QtMenu

    PEN_LINE = QtGui.QPen(QtGui.QColor(*_gui_core.GuiRgba.Dark), _gui_core.GuiDpiScale.get(1))
    PEN_BRANCH = QtGui.QPen(QtGui.QColor(*_gui_core.GuiRgba.Gray), _gui_core.GuiDpiScale.get(1))
    PEN_BRANCH_HIGHLIGHT = QtGui.QPen(QtGui.QColor(*_gui_core.GuiRgba.LightAzureBlue), _gui_core.GuiDpiScale.get(1))

    def __init__(self, *args, **kwargs):
        super(_QtTreeViewWidget, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)
        qt_palette = _qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)

        self.setStyleSheet(_qt_core.GuiQtStyle.get('QTreeView_new'))
        self.header().setStyleSheet(_qt_core.GuiQtStyle.get('QHeaderView'))
        self.verticalScrollBar().setStyleSheet(_qt_core.GuiQtStyle.get('QScrollBar'))
        self.horizontalScrollBar().setStyleSheet(_qt_core.GuiQtStyle.get('QScrollBar'))

        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.setIndentation(20)

        self.setSelectionMode(self.ExtendedSelection)
        self.setHorizontalScrollMode(self.ScrollPerItem)
        self.setVerticalScrollMode(self.ScrollPerItem)
        self.setDragEnabled(False)
        self.setExpandsOnDoubleClick(False)

        self.header().setFixedHeight(16)
        self.header().setHighlightSections(True)
        self.header().setSortIndicatorShown(True)
        self.header().setCascadingSectionResizes(True)
        self.header().setPalette(_qt_core.GuiQtDcc.generate_qt_palette())

        self.setHeaderHidden(True)

        self._view_model = _vew_mod_tree.TreeViewModel(self)
        self._view_model.data.item.cls = _item_for_tree.QtTreeItem

        self.setItemDelegate(_QtListItemDelegate(self))

        self._svg_folder_open = _gui_core.GuiIcon.get('tree/folder-open')
        self._svg_folder_close = _gui_core.GuiIcon.get('tree/folder-close')

        # noinspection PyUnresolvedReferences
        self.expanded.connect(self._view_model.on_item_expand_at)
        # noinspection PyUnresolvedReferences
        self.collapsed.connect(self._view_model.on_item_collapse_at)
        # noinspection PyUnresolvedReferences
        self.itemSelectionChanged.connect(self.item_select_changed.emit)

        self._init_thread_worker_extra_def_(self)

        self.setMouseTracking(True)

        self.installEventFilter(self)
        self.viewport().installEventFilter(self)

    def _set_view_header_(self, raw, max_width=0):
        self.setHeaderHidden(False)
        texts, width_ps = zip(*raw)
        count = len(texts)
        #
        self.setColumnCount(count)
        self.setHeaderLabels(texts)
        set_column_enable = count > 1
        w = 0
        if set_column_enable is True:
            max_division = sum(width_ps)
            w = int(max_width/max_division)
        #
        for index in range(0, count):
            if set_column_enable is True:
                self.setColumnWidth(index, w*(width_ps[index]))
            #
            icon = QtGui.QIcon()
            p = QtGui.QPixmap(16, 16)
            p.load(_gui_core.GuiIcon.get('qt-style/line-v'))
            icon.addPixmap(
                p,
                QtGui.QIcon.Normal,
                QtGui.QIcon.On
            )
            #
            self.headerItem().setBackground(index, _qt_core.QtBrushes.Background)
            self.headerItem().setForeground(index, QtGui.QBrush(QtGui.QColor(255, 255, 255, 255)))
            self.headerItem().setFont(index, _qt_core.QtFonts.NameNormal)
            # todo: in katana will make text display error, PyQt?
            # if QT_LOAD_INDEX == 1:
            self.headerItem().setIcon(index, icon)

    def _get_item_has_visible_children_by_index_(self, index):
        row_count = self.model().rowCount(index)
        for i_row in range(row_count):
            i_index = index.child(i_row, index.column())
            if i_index.isValid():
                if self.itemFromIndex(i_index).isHidden() is False:
                    return True
        return False

    def _get_item_below_is_visible_by_index_(self, index):
        def _rcs_fnc(_index):
            _nxt_index = index.sibling(_index.row()+1, _index.column())
            if _nxt_index.isValid():
                if self.itemFromIndex(_nxt_index).isHidden() is True:
                    return _rcs_fnc(_nxt_index)
                return True
            return False

        return _rcs_fnc(index)

    def _send_check_changed_emit_(self, item, column):
        pass

    def _send_check_toggled_emit_(self, item, column, boolean):
        pass

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            pass
        # view port
        elif widget == self.viewport():
            if event.type() == QtCore.QEvent.ToolTip:
                self._view_model.do_item_popup_tool_tip(event)

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

    def drawBranches(self, painter, rect, index):
        # Get the indention level of the row
        level = 0
        index_tmp = index.parent()
        while index_tmp.isValid():
            level += 1
            index_tmp = index_tmp.parent()

        # Is the row highlighted (selected) ?
        highlight = self.selectionModel().isSelected(index)

        # Line width
        line_w = _gui_core.GuiDpiScale.get(1)

        # Cell width
        cell_w = int(rect.width()/(level+1))
        offset = 2

        # Current cell to draw in
        x = rect.x()+cell_w*level+offset
        y = rect.y()
        w = cell_w
        h = rect.height()

        # Center of the cell
        cx = x+int(w/2)-int(line_w/2)
        cy = y+int(h/2)-int(line_w/2)

        # Backup the old pen
        tmp_pen = painter.pen()

        # Draw the branch indicator on the right most
        if self._get_item_has_visible_children_by_index_(index):
            # Branch icon properties
            r_rect = _gui_core.GuiDpiScale.get(4)
            cross_margin = _gui_core.GuiDpiScale.get(1)
            # Is the row expanded ?
            is_expanded = self.isExpanded(index)
            # [+] and [-] are using different color when highlighted
            painter.setPen(self.PEN_BRANCH_HIGHLIGHT if highlight else self.PEN_BRANCH)
            # Draw a rectangle [ ] as the branch indicator
            painter.drawRect(
                cx-r_rect,
                cy-r_rect,
                r_rect*2,
                r_rect*2
            )
            # Draw the '-' into the rectangle. i.e. [-]
            painter.drawLine(
                cx-r_rect+cross_margin+line_w,
                cy,
                cx+r_rect-cross_margin-line_w,
                cy
            )
            # Draw the '|' into the rectangle. i.e. [+]
            if not is_expanded:
                painter.drawLine(
                    cx,
                    cy-r_rect+cross_margin+line_w,
                    cx,
                    cy+r_rect-cross_margin-line_w
                )
            # Other ornaments are not highlighted
            painter.setPen(self.PEN_LINE)
            # Draw the '|' on the bottom. i.e. [-]
            #                                   |
            if is_expanded:
                painter.drawLine(
                    cx,
                    cy+r_rect+cross_margin+line_w,
                    cx,
                    y+h
                )

            # Draw more ornaments when the row is not a top level row
            if level > 0:
                # Draw the '-' on the left. i.e. --[+]
                painter.drawLine(
                    x,
                    cy,
                    cx-r_rect-cross_margin-line_w,
                    cy
                )
        else:
            # Circle is not highlighted
            painter.setPen(self.PEN_LINE)
            # Draw the line and circle. i.e. --o
            if level > 0:
                painter.drawLine(x, cy, cx, cy)
                # Backup the old brush
                brush_old = painter.brush()
                painter.setBrush(self.PEN_BRANCH_HIGHLIGHT.brush() if highlight else self.PEN_BRANCH.brush())
                # A filled circle
                circle_r = _gui_core.GuiDpiScale.get(2)
                # painter.setPen(self.PEN_BRANCH_HIGHLIGHT if highlight else self.PEN_BRANCH)
                painter.drawEllipse(
                    cx-circle_r,
                    cy-circle_r,
                    circle_r*2,
                    circle_r*2
                )
                # Restore the old brush
                painter.setBrush(brush_old)
        # Draw other vertical and horizontal lines on the left of the indicator
        if level > 0:
            # Move cell window to the left
            x -= cell_w
            cx -= cell_w
            _below_is_visible = self._get_item_below_is_visible_by_index_(index)
            if _below_is_visible is True:
                # The row has more siblings. i.e. |
                #                                 |--
                #                                 |
                painter.drawLine(cx, y, cx, y+h)
                painter.drawLine(cx, cy, x+w, cy)
            else:
                # The row is the last row.   i.e. |
                #                                 L--
                painter.drawLine(cx, y, cx, cy)
                painter.drawLine(cx, cy, x+w, cy)
            # More vertical lines on the left. i.e. ||||-
            tmp_index = index.parent()
            for i in range(0, level-1):
                # Move the cell window to the left
                x -= cell_w
                cx -= cell_w
                # Draw vertical line if the row has siblings at this level
                _below_is_visible = self._get_item_below_is_visible_by_index_(tmp_index)
                if _below_is_visible is True:
                    painter.drawLine(cx, y, cx, y+h)
                tmp_index = tmp_index.parent()
        # Restore the old pen
        painter.setPen(tmp_pen)

    def paintEvent(self, event):
        if not self.topLevelItemCount():
            painter = _qt_core.QtPainter(self.viewport())
            painter._draw_empty_image_by_rect_(
                self.rect(), 'placeholder/empty'
            )
        #
        super(_QtTreeViewWidget, self).paintEvent(event)

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

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            return
        event.ignore()
        return

    def dragMoveEvent(self, event):
        QtCore.QMimeData()
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
            return
        event.ignore()
        return

    def dropEvent(self, event):
        self._view_model.do_drop(event)


class QtTreeWidget(
    _base._BaseViewWidget
):
    FILTER_COMPLETION_MAXIMUM = 50

    def __init__(self, *args, **kwargs):
        super(QtTreeWidget, self).__init__(*args, **kwargs)
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
        self._keyword_filter_tool_box = self._create_top_tool_box_('keyword filter', size_mode=1)
        # check
        self._check_tool_box = self._create_left_tool_box_('check')
        # sort and chart
        self._sort_and_chart_tool_box = self._create_left_tool_box_('sort and chart')

        self._view = _QtTreeViewWidget()
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
        self._build_sort_and_chart_tool_box_()
        self._build_keyword_filter_tool_box_()

        actions = [
            (self._view.selectAll, 'Ctrl+A'),
        ]
        for i_fnc, i_shortcut in actions:
            i_action = QtWidgets.QAction(self)
            # noinspection PyUnresolvedReferences
            i_action.triggered.connect(
                i_fnc
            )
            i_action.setShortcut(
                QtGui.QKeySequence(
                    i_shortcut
                )
            )
            i_action.setShortcutContext(
                QtCore.Qt.WidgetShortcut
            )
            self.addAction(i_action)

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

    def _build_sort_and_chart_tool_box_(self):
        self._item_sort_button = _wgt_button.QtIconPressButton()
        self._item_sort_button._set_name_text_('sort')
        self._item_sort_button._set_icon_file_path_(_gui_core.GuiIcon.get('tool/sort-by-name-ascend'))
        self._sort_and_chart_tool_box._add_widget_(self._item_sort_button)
        self._item_sort_button._set_menu_data_generate_fnc_(
            self._view_model.generate_item_sort_menu_data
        )
        self._item_sort_button.press_clicked.connect(self._on_sort_order_swap_)

        self._chat_button = _wgt_button.QtIconPressButton()
        self._chat_button._set_name_text_('chart')
        self._chat_button._set_icon_file_path_(_gui_core.GuiIcon.get('tool/chart'))
        self._sort_and_chart_tool_box._add_widget_(self._chat_button)
        self._chat_button.press_clicked.connect(self._on_show_chart_)

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
        self._item_sort_button._set_icon_file_path_(
            _gui_core.GuiIcon.get('tool/sort-by-name-{}'.format(order)),
        )

    def _on_show_chart_(self):
        data = self._view_model.generate_chart_data()
        if data:
            chart_view = _wgt_view_for_histogram_chart.QtViewForHistogramChart()
            chart_view._set_data_(data)
            _qt_core.QtApplication.show_tool_dialog(
                widget=chart_view, title='Histogram Chart', size=(640, 480), parent=self
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
