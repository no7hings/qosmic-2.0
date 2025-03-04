# coding:utf-8
# gui
from .... import core as _gui_core
# qt
from ....qt.core.wrap import *

from ....qt import core as _qt_core

from ....qt import abstracts as _qt_abstracts

from ...widgets import utility as _wgt_utility

from . import model as _model


class _QtItemDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, *args, **kwargs):
        QtWidgets.QStyledItemDelegate.__init__(self, *args, **kwargs)

    def paint(self, painter, option, index):
        self.parent()._view_model.draw_item(painter, option, index)


class _QtSpcTaskItem(QtWidgets.QTreeWidgetItem):
    GROUP_FLAG = False

    def __init__(self, *args, **kwargs):
        super(_QtSpcTaskItem, self).__init__(*args)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
        )
        self._item_model = _model._SpcTaskItemModel(self)

    def __str__(self):
        return '{}(path={})'.format(
            self.__class__.__name__,
            self._item_model.get_path()
        )

    def __repr__(self):
        return '\n'+self.__str__()


class _QtSpcTaskGroupItem(QtWidgets.QTreeWidgetItem):
    GROUP_FLAG = True

    def __init__(self, *args, **kwargs):
        super(_QtSpcTaskGroupItem, self).__init__(*args)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
        )
        self._item_model = _model._SpcTaskGroupItemModel(self)

    def __str__(self):
        return '{}(path={})'.format(
            self.__class__.__name__,
            self._item_model.get_path()
        )

    def __repr__(self):
        return '\n'+self.__str__()


# view
class _QtSpcTaskView(
    QtWidgets.QTreeWidget,
    _qt_abstracts.AbsQtThreadWorkerExtraDef,
):
    QT_MENU_CLS = _wgt_utility.QtMenu

    PEN_LINE = QtGui.QPen(QtGui.QColor(*_gui_core.GuiRgba.Dark), _gui_core.GuiDpiScale.get(1))
    PEN_BRANCH = QtGui.QPen(QtGui.QColor(*_gui_core.GuiRgba.Gray), _gui_core.GuiDpiScale.get(1))
    PEN_BRANCH_HIGHLIGHT = QtGui.QPen(QtGui.QColor(*_gui_core.GuiRgba.LightAzureBlue), _gui_core.GuiDpiScale.get(1))

    status_changed = qt_signal()

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

    def __init__(self, *args, **kwargs):
        super(_QtSpcTaskView, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)
        qt_palette = _qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)

        self.setStyleSheet(_qt_core.QtStyle.get('QTreeView_new'))
        self.header().setStyleSheet(_qt_core.QtStyle.get('QHeaderView'))
        self.verticalScrollBar().setStyleSheet(_qt_core.QtStyle.get('QScrollBar'))
        self.horizontalScrollBar().setStyleSheet(_qt_core.QtStyle.get('QScrollBar'))

        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.setIndentation(20)

        self.setSelectionMode(self.NoSelection)
        self.setHorizontalScrollMode(self.ScrollPerItem)
        self.setVerticalScrollMode(self.ScrollPerItem)
        self.setDragEnabled(False)
        self.setExpandsOnDoubleClick(False)

        self.header().setFixedHeight(16)
        self.header().setHighlightSections(True)
        self.header().setSortIndicatorShown(True)
        self.header().setCascadingSectionResizes(True)
        self.header().setPalette(_qt_core.GuiQtDcc.generate_qt_palette())
        self.header().setSortIndicatorShown(True)

        self.setHeaderHidden(True)

        self._view_model = _model._SpcTaskViewModel(self)

        self._view_model.data.item.cls = _QtSpcTaskItem
        self._view_model.data.item.group_cls = _QtSpcTaskGroupItem

        self.setItemDelegate(_QtItemDelegate(self))

        self._update_timer = QtCore.QTimer(self)
        self._update_timer.timeout.connect(self._refresh_on_time_)

        self._update_timer.start(1000/12)

        self._init_thread_worker_extra_def_(self)

        self._thread_worker_maximum = 2

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

    def contextMenuEvent(self, event):
        menu = None

        menu_data = self._view_model.get_menu_data()
        menu_content = self._view_model.get_menu_content()
        menu_data_generate_fnc = self._view_model.get_menu_data_generate_fnc()
        menu_name_dict = self._view_model.get_menu_name_dict()

        if menu_content:
            if menu is None:
                menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
            menu._set_menu_content_(menu_content, append=True)

        if menu_data:
            if menu is None:
                menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
            menu._set_menu_data_(menu_data)

        if menu_data_generate_fnc:
            if menu is None:
                menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
            menu._set_menu_data_(menu_data_generate_fnc())

        # data from item
        item = self.itemAt(event.pos())
        if item:
            item_menu_data = item._item_model.get_menu_data()
            item_menu_content = item._item_model.get_menu_content()
            item_menu_data_generate_fnc = item._item_model.get_menu_data_generate_fnc()
            item_menu_name_dict = item._item_model.get_menu_name_dict()
            menu_name_dict.update(item_menu_name_dict)

            if item_menu_content:
                if menu is None:
                    menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
                menu._set_menu_content_(item_menu_content, append=True)

            if item_menu_data:
                if menu is None:
                    menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
                menu._set_menu_data_(item_menu_data)

            if item_menu_data_generate_fnc:
                if menu is None:
                    menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
                menu._set_menu_data_(item_menu_data_generate_fnc())

            if menu is not None:
                menu._update_menu_name_dict_(item_menu_name_dict)

        if menu is not None:
            menu._popup_start_()

    def _refresh_on_time_(self):
        self.update()


# overview
class _QtSpcTaskOverview(QtWidgets.QWidget):
    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        if self._view_model is not None:
            x, y = 0, 0
            w, h = self.width(), self.height()

            overview_data = self._view_model.data.overview
            overview_data.base_rect.setRect(
                x, y, w, h
            )

            text_font = overview_data.text_font
            count = len(overview_data.paths)

            draw_data = []

            x_c = x
            for i_idx, i_key in enumerate(overview_data.keys):
                i_paths = overview_data.path_dict[i_key]
                i_count = len(i_paths)
                i_status, i_status_name = i_key
                i_rect = QtCore.QRect()
                i_text = '{}*{}'.format(i_status_name, i_count)
                i_text_w = QtGui.QFontMetrics(text_font).width(i_text)+16
                i_color, i_color_hover = _qt_core.QtItemDrawBase._gen_rgba_args_by_status(i_status)
                i_rect.setRect(
                    x_c+1, y+1, i_text_w-2, h-2
                )
                x_c += i_text_w
                draw_data.append((i_text, i_rect, i_color, i_color_hover))

            overview_data.draw_data = draw_data

    def __init__(self, *args, **kwargs):
        super(_QtSpcTaskOverview, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed
        )

        self.setFixedHeight(20)

        self._view_model = None

        self.installEventFilter(self)

    def _set_view_model_(self, model):
        self._view_model = model
        self._view_model.set_overview_widget(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
        return False

    def paintEvent(self, event):
        if self._view_model is not None:
            painter = QtGui.QPainter(self)

            painter.setPen(QtGui.QColor(*_gui_core.GuiRgba.Basic))
            painter.setBrush(QtGui.QColor(*_gui_core.GuiRgba.Basic))

            painter.drawRect(
                self._view_model.data.overview.base_rect
            )

            overview_data = self._view_model.data.overview

            font = overview_data.text_font
            text_color = overview_data.text_color
            painter.setFont(font)
            for i in overview_data.draw_data:
                i_text, i_rect, i_color, i_color_hover = i
                _qt_core.QtItemDrawBase._draw_frame(
                    painter, i_rect, i_color, i_color
                )
                _qt_core.QtItemDrawBase._draw_name_text(
                    painter, i_rect, i_text,
                    text_color, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
                )


class QtSpcTaskWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(QtSpcTaskWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        self._mrg = 4

        self._grid_lot = QtWidgets.QGridLayout(self)
        self._grid_lot.setContentsMargins(*[self._mrg]*4)
        self._grid_lot.setSpacing(2)

        self._overview = _QtSpcTaskOverview()
        self._grid_lot.addWidget(self._overview, 0, 0, 1, 1)

        self._view = _QtSpcTaskView()
        self._grid_lot.addWidget(self._view, 1, 0, 1, 1)
        self._view.setFocusProxy(self)
        self._view_model = self._view._view_model

        self._overview._set_view_model_(self._view_model)

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
        painter.setBrush(QtGui.QColor(*_gui_core.GuiRgba.Dim))
        painter.drawRect(f_x, f_y, f_w, f_h)
