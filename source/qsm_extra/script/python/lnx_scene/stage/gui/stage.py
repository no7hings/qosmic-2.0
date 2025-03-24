# coding:utf-8
# gui
import lxgui.core as gui_core

from lxgui.qt.core.wrap import *

import lxgui.qt.core as gui_qt_core

import lxgui.qt.abstracts as gui_qt_abstracts

import lxgui.qt.widgets as gui_qt_widgets


class _QtItemDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, *args, **kwargs):
        QtWidgets.QStyledItemDelegate.__init__(self, *args, **kwargs)

    def paint(self, painter, option, index):
        super(_QtItemDelegate, self).paint(painter, option, index)
        # self.parent()._model.draw(painter, option, index)


class StageNodeGui(QtWidgets.QTreeWidgetItem):
    def __init__(self, *args, **kwargs):
        super(StageNodeGui, self).__init__(*args)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled
        )

    def _do_delete_(self):
        if self.parent():
            index = self.parent().indexOfChild(self)
            self.parent().takeChild(index)
        else:
            tree_widget = self.treeWidget()
            if isinstance(tree_widget, QtWidgets.QTreeWidget):
                if tree_widget:
                    index = tree_widget.indexOfTopLevelItem(self)
                    tree_widget.takeTopLevelItem(index)

    def __str__(self):
        return '{}(path={})'.format(
            self.__class__.__name__,
            self._item_model.get_path()
        )

    def __repr__(self):
        return '\n'+self.__str__()


class StageRootGui(
    QtWidgets.QTreeWidget,
    gui_qt_abstracts.AbsQtThreadWorkerExtraDef,
):
    QT_MENU_CLS = gui_qt_widgets.QtMenu

    PEN_LINE = QtGui.QPen(QtGui.QColor(*gui_core.GuiRgba.Dark), gui_core.GuiDpiScale.get(1))
    PEN_BRANCH = QtGui.QPen(QtGui.QColor(*gui_core.GuiRgba.Gray), gui_core.GuiDpiScale.get(1))
    PEN_BRANCH_HIGHLIGHT = QtGui.QPen(QtGui.QColor(*gui_core.GuiRgba.LightAzureBlue), gui_core.GuiDpiScale.get(1))

    def __init__(self, *args, **kwargs):
        super(StageRootGui, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)
        qt_palette = gui_qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)

        self.setStyleSheet(gui_qt_core.QtStyle.get('QTreeView_new'))
        self.header().setStyleSheet(gui_qt_core.QtStyle.get('QHeaderView'))
        self.verticalScrollBar().setStyleSheet(gui_qt_core.QtStyle.get('QScrollBar'))
        self.horizontalScrollBar().setStyleSheet(gui_qt_core.QtStyle.get('QScrollBar'))

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
        self.header().setPalette(gui_qt_core.GuiQtDcc.generate_qt_palette())
        self.header().setSortIndicatorShown(True)

        self.setHeaderHidden(True)

        self.setItemDelegate(_QtItemDelegate(self))

        # noinspection PyUnresolvedReferences
        self.expanded.connect(self._view_model.on_item_expand_at)
        # noinspection PyUnresolvedReferences
        self.collapsed.connect(self._view_model.on_item_collapse_at)
        # noinspection PyUnresolvedReferences
        self.itemSelectionChanged.connect(self.item_select_changed.emit)

        self._init_thread_worker_extra_def_(self)

        self.setMouseTracking(True)

        self.current_edit = None

        self.installEventFilter(self)
        self.viewport().installEventFilter(self)

    def _get_item_has_visible_children_by_index(self, index):
        row_count = self.model().rowCount(index)
        for i_row in range(row_count):
            i_index = index.child(i_row, index.column())
            if i_index.isValid():
                if self.itemFromIndex(i_index).isHidden() is False:
                    return True
        return False

    def _get_item_below_is_visible_by_index(self, index):
        def _rcs_fnc(_index):
            _nxt_index = index.sibling(_index.row()+1, _index.column())
            if _nxt_index.isValid():
                if self.itemFromIndex(_nxt_index).isHidden() is True:
                    return _rcs_fnc(_nxt_index)
                return True
            return False

        return _rcs_fnc(index)

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
        line_w = gui_core.GuiDpiScale.get(1)

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
        if self._get_item_has_visible_children_by_index(index):
            # Branch icon properties
            r_rect = gui_core.GuiDpiScale.get(4)
            cross_margin = gui_core.GuiDpiScale.get(1)
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
                circle_r = gui_core.GuiDpiScale.get(2)
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
            _below_is_visible = self._get_item_below_is_visible_by_index(index)
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
                _below_is_visible = self._get_item_below_is_visible_by_index(tmp_index)
                if _below_is_visible is True:
                    painter.drawLine(cx, y, cx, y+h)
                tmp_index = tmp_index.parent()
        # Restore the old pen
        painter.setPen(tmp_pen)

    def paintEvent(self, event):
        if not self.topLevelItemCount():
            painter = gui_qt_core.QtPainter(self.viewport())
            painter._draw_empty_image_by_rect_(
                self.rect(), 'placeholder/empty'
            )
        #
        super(StageRootGui, self).paintEvent(event)

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