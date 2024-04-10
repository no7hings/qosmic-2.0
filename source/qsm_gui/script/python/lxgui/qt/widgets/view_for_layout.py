# coding=utf-8
# qt
from ..core.wrap import *

from .. import core as gui_qt_core

from .. import abstracts as gui_qt_abstracts
# qt widgets
from . import utility as gui_qt_wgt_utility


class QtToolGridLayoutWidget(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtFrameBaseDef,
    gui_qt_abstracts.AbsQtPathBaseDef,
    #
    gui_qt_abstracts.AbsQtActionBaseDef,
    gui_qt_abstracts.AbsQtActionForDropDef,

    gui_qt_abstracts.AbsQtMenuBaseDef,
):
    QT_MENU_CLS = gui_qt_wgt_utility.QtMenu

    LAYOUT_MODEL_CLS = gui_qt_core.GuiQtModForGridLayout

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        m_l, m_t, m_r, m_b = self._layout_margins
        v_x, v_y = m_l, m_t
        v_w, v_h = w-m_l-m_r, h-m_t-m_b
        #
        self._layout_model.set_pos(v_x, v_y)
        self._layout_model.set_size(v_w, v_h)
        # print self, self._get_action_flag_()
        # swap when flag is drag child polish or add
        if self._get_action_flag_is_match_(
                self.ActionFlag.DragChildPolish
        ) and self._index_drag_child_polish is not None:
            self._layout_model.set_count(self.__layout_item_stack.get_count())
            self._layout_model.update()
            _index_maximum = self.__layout_item_stack.get_index_maximum()
            for i_index in self.__layout_item_stack.get_indices():
                i_widget = self.__layout_item_stack.get_widget_at(i_index)

                i_index_cur = i_index

                # if self._index_drag_child_polish_start < i_index < self._index_drag_child_polish:
                #     i_index_cur = i_index-1

                if self._index_drag_child_polish_start < i_index <= self._index_drag_child_polish:
                    i_index_cur = i_index-1
                elif self._index_drag_child_polish <= i_index < self._index_drag_child_polish_start:
                    i_index_cur = i_index+1

                # print i_index, i_index_cur, self._index_drag_child_polish_start, self._index_drag_child_polish

                i_x, i_y, i_w, i_h = self._layout_model.get_geometry_at(i_index_cur)

                i_widget.setGeometry(
                    i_x, i_y, i_w, i_h
                )
                i_widget.setFixedSize(i_w, i_h)

                if i_index == self._index_drag_child_polish_start:
                    i_widget.hide()
                else:
                    i_widget.show()
        elif self._get_action_flag_is_match_(
                self.ActionFlag.DragChildRemove
        ):
            self._layout_model.set_count(self.__layout_item_stack.get_count())
            self._layout_model.update()
            for i_index in self.__layout_item_stack.get_indices():
                i_widget = self.__layout_item_stack.get_widget_at(i_index)

                if self._index_drag_child_polish_start < i_index:
                    i_index_cur = i_index-1
                else:
                    i_index_cur = i_index

                i_x, i_y, i_w, i_h = self._layout_model.get_geometry_at(i_index_cur)

                i_widget.setGeometry(
                    i_x, i_y, i_w, i_h
                )
                i_widget.setFixedSize(i_w, i_h)

                if i_index == self._index_drag_child_polish_start:
                    i_widget.hide()
                else:
                    i_widget.show()
        elif self._get_action_flag_is_match_(
                self.ActionFlag.DragChildAdd
        ):
            self._layout_model.set_count(self.__layout_item_stack.get_count()+1)
            self._layout_model.update()
            for i_index in self.__layout_item_stack.get_indices():
                i_item = self.__layout_item_stack.get_item_at(i_index)
                i_widget = i_item.get_widget()

                if self._index_drag_child_add <= i_index:
                    i_index_cur = i_index+1
                else:
                    i_index_cur = i_index

                i_x, i_y, i_w, i_h = self._layout_model.get_geometry_at(i_index_cur)

                i_widget.setGeometry(
                    i_x, i_y, i_w, i_h
                )
                i_widget.setFixedSize(i_w, i_h)
                i_widget.show()
        else:
            self._layout_model.set_count(self.__layout_item_stack.get_count())
            self._layout_model.update()
            for i_index in self.__layout_item_stack.get_indices():
                i_item = self.__layout_item_stack.get_item_at(i_index)
                i_widget = i_item.get_widget()

                i_x, i_y, i_w, i_h = self._layout_model.get_geometry_at(i_index)
                i_widget.setGeometry(
                    i_x, i_y, i_w, i_h
                )
                i_widget.setFixedSize(i_w, i_h)
                i_widget.show()

        vpt_w, vpt_h = self._layout_model.get_abs_size()
        self._viewport_rect.setRect(
            v_x, v_y, vpt_w, vpt_h
        )

        frm_w, frm_h = w, vpt_h+m_t+m_b
        self.setMinimumHeight(frm_h)

        self._rect_frame_draw.setRect(
            x+1, y+1, w-2, frm_h-2
        )

    def _init_layout_base_def_(self, widget):
        self._widget = widget

        self._layout_model = self.LAYOUT_MODEL_CLS()
        self.__layout_item_stack = gui_qt_core.GuiQtModForLayoutItemStack(self)

        self._layout_margins = 4, 4, 4, 4

        self._viewport_rect = QtCore.QRect()

    def __init__(self, *args, **kwargs):
        super(QtToolGridLayoutWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self._init_layout_base_def_(self)

        self._init_frame_base_def_(self)
        self._init_path_base_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_drop_def_(self)

        self._init_menu_base_def_(self)
        self._frame_draw_is_enable = False

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()

            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    pass
                elif event.button() == QtCore.Qt.RightButton:
                    p = event.pos()
                    if not self._viewport_rect.contains(p):
                        self._popup_menu_()
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.DragEnter:
                self._do_drag_enter_(event)
            elif event.type() == QtCore.QEvent.DragMove:
                if self._get_action_flag_is_match_(
                        self.ActionFlag.DragChildPolish
                ):
                    self._do_drag_child_polish_(event)
                elif self._get_action_flag_is_match_(
                        self.ActionFlag.DragChildAdd
                ):
                    self._do_drag_child_add_(event)
            elif event.type() == QtCore.QEvent.DragLeave:
                if self._get_action_flag_is_match_(
                        self.ActionFlag.DragChildPolish
                ):
                    self._do_drag_child_polish_leave_(event)
                elif self._get_action_flag_is_match_(
                        self.ActionFlag.DragChildAdd
                ):
                    self._do_drag_child_add_leave_(event)
            elif event.type() == QtCore.QEvent.Drop:
                if self._get_action_flag_is_match_(
                        self.ActionFlag.DragChildPolish
                ):
                    self._do_drop_child_polish_(event)
                elif self._get_action_flag_is_match_(
                        self.ActionFlag.DragChildAdd
                ):
                    self._do_drop_child_add_(event)
        return False

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)
        if self._frame_draw_is_enable is True:
            painter._draw_frame_by_rect_(
                rect=self._rect_frame_draw,
                border_color=gui_qt_core.QtBorderColors.Basic,
                background_color=gui_qt_core.QtBackgroundColors.Dark,
                border_radius=4
            )

        if self._get_action_flag_is_match_(self.ActionFlag.DragChildPolish):
            painter._draw_frame_by_rect_(
                rect=self._drag_rect_child_polish,
                border_color=gui_qt_core.QtBorderColors.Button,
                background_color=gui_qt_core.QtBackgroundColors.BDragChildPolish,
                border_width=1,
            )
        elif self._get_action_flag_is_match_(self.ActionFlag.DragChildAdd):
            painter._draw_frame_by_rect_(
                rect=self._drag_rect_child_add,
                border_color=gui_qt_core.QtBorderColors.Button,
                background_color=gui_qt_core.QtBackgroundColors.BDragChildAdd,
                border_width=1,
            )

    def _do_drag_enter_(self, event):
        mdt = event.mimeData()
        scheme = mdt.data('lynxi/drag-and-drop-scheme')
        if not scheme:
            event.ignore()
            return False
        if scheme == 'unknown':
            event.ignore()
            return False
        if scheme != self._get_drag_and_drop_scheme_():
            event.ignore()
            return False

        key = mdt.data('lynxi/drag-and-drop-key')
        if key:
            key_cur = str(key)
            item = self.__layout_item_stack.get_item_by(key_cur)
            if item:
                self._drag_and_drop_key = key_cur
                index = self.__layout_item_stack.get_index_by(item)
                self._set_action_flag_(self.ActionFlag.DragChildPolish)
                self._index_drag_child_polish_start = index
                self._refresh_widget_all_()
                event.accept()
                return True

        self._set_action_flag_(self.ActionFlag.DragChildAdd)
        self._index_drag_child_add_start = self.__layout_item_stack.get_index_maximum()+1
        self._layout_model.set_count(self.__layout_item_stack.get_count()+1)
        self._layout_model.update()
        event.accept()
        return True

    def _do_drag_child_polish_(self, event):
        p = event.pos()
        x, y = p.x(), p.y()
        column, row = self._layout_model.get_coord_loc(x, y)
        index_cur = self._layout_model.get_index_between(column, row)
        if index_cur != self._index_drag_child_polish:
            self._index_drag_child_polish = min(index_cur, self.__layout_item_stack.get_index_maximum())
            c_x, c_y, c_w, c_h = self._layout_model.get_geometry_at(self._index_drag_child_polish)
            self._drag_rect_child_polish.setRect(c_x, c_y, c_w-1, c_h-1)
            self._refresh_widget_all_()

    def _do_drag_child_add_(self, event):
        p = event.pos()
        x, y = p.x(), p.y()
        column, row = self._layout_model.get_coord_loc(x, y)
        index_cur = self._layout_model.get_index_between(column, row)
        if index_cur != self._index_drag_child_add:
            self._index_drag_child_add = min(index_cur, self.__layout_item_stack.get_index_maximum()+1)
            c_x, c_y, c_w, c_h = self._layout_model.get_geometry_at(self._index_drag_child_add)
            self._drag_rect_child_add.setRect(c_x, c_y, c_w-1, c_h-1)
            self._refresh_widget_all_()
        # refresh widget first
        # self._refresh_widget_all_()

    def _do_drag_child_polish_leave_(self, event):
        self._set_action_flag_(self.ActionFlag.DragChildRemove)
        self._refresh_widget_all_()
        event.ignore()

    def _do_drag_child_add_leave_(self, event):
        self._set_action_flag_(self.ActionFlag.DragChildAddCancel)
        self._refresh_widget_all_()
        event.ignore()

    def _do_drag_leave_(self, event):
        self._set_action_flag_(self.ActionFlag.DragLeave)
        self._refresh_widget_all_()
        event.ignore()

    def _do_drop_child_polish_(self, event):
        self.__layout_item_stack.insert_item_between(
            self._index_drag_child_polish_start, self._index_drag_child_polish
        )

        self._index_drag_child_polish_start = 0
        self._index_drag_child_polish = 0

        self._clear_all_action_flags_()

        self._refresh_widget_all_()
        event.accept()

    def _do_drop_child_add_(self, event):
        # item = self.__layout_item_stack.fetch_drag_and_drop_cache()
        # self.__layout_item_stack.drop_item_to(item, 0)

        self._index_drag_child_add_start = None
        self._index_drag_child_add = None

        self._clear_all_action_flags_()

        self._refresh_widget_all_()
        event.ignore()

    def _drag_release_cbk_(self):
        self._index_drag_child_polish_start = None
        self._index_drag_child_polish = None

        self._clear_all_action_flags_()
        self._refresh_widget_all_()

    def _set_drop_enable_(self, boolean):
        self.setAcceptDrops(boolean)

    def _set_item_size_(self, w, h):
        self._layout_model.set_item_size(w, h)

    # noinspection PyUnusedLocal
    def _add_widget_(self, widget, *args, **kwargs):
        widget.setParent(self)
        self.__layout_item_stack.create_item(widget)
        self._refresh_widget_all_()

    def _clear_all_widgets_(self):
        self.__layout_item_stack.restore()


class QtToolGroupVLayoutWidget(
    QtWidgets.QWidget,

    gui_qt_abstracts.AbsQtActionBaseDef,
    gui_qt_abstracts.AbsQtActionForDropDef,
):
    LAYOUT_MODEL_CLS = gui_qt_core.GuiQtModForVLayout

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    # noinspection PyUnusedLocal
    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        m_l, m_t, m_r, m_b = self._layout_margins
        v_x, v_y = m_l, m_t
        v_w, v_h = w-m_l-m_r, h-m_t-m_b

        heights = []
        if self._get_action_flag_is_match_(
                self.ActionFlag.DragChildPolish, self.ActionFlag.DragChildRemove
        ):
            self._layout_model.set_pos(v_x, v_y)
            self._layout_model.set_size(v_w, v_h)
            for i_index in self.__layout_item_stack.get_indices():
                i_widget = self.__layout_item_stack.get_widget_at(i_index)

                i_index_cur = i_index

                if self._index_drag_child_polish_start < i_index <= self._index_drag_child_polish:
                    i_index_cur = i_index-1
                elif self._index_drag_child_polish <= i_index < self._index_drag_child_polish_start:
                    i_index_cur = i_index+1

                i_x, i_y, i_w, i_h = self._layout_model.get_geometry_at(i_index_cur)

                i_widget.setGeometry(i_x, i_y, i_w, i_h)
                i_widget.setFixedSize(i_w, i_h)

                if i_index == self._index_drag_child_polish_start:
                    i_widget.hide()
                else:
                    i_widget.show()

                heights.append(i_h)
        else:
            c_v_y = v_y
            for i_widget in self.__layout_item_stack.get_all_widgets():
                i_widget.show()
                # i_widget.setFixedWidth(v_w)
                i_size = i_widget._get_layout_minimum_size_()
                i_x, i_y = v_x, c_v_y
                i_w, i_h = v_w, i_size.height()
                i_widget.setGeometry(i_x, i_y, i_w, i_h)
                i_widget.setFixedSize(i_w, i_h)
                c_v_y += i_h
                heights.append(i_h)

        vpt_w, vpt_h = v_w, sum(heights)
        self._viewport_rect.setRect(
            v_x, v_y, vpt_w, vpt_h
        )

        frm_w, frm_h = w, vpt_h+m_t+m_b
        self.setMinimumHeight(frm_h)

    def __init__(self, *args, **kwargs):
        super(QtToolGroupVLayoutWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding
        )
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self._init_action_base_def_(self)
        self._init_action_for_drop_def_(self)

        self._layout_model = self.LAYOUT_MODEL_CLS()
        self.__layout_item_stack = gui_qt_core.GuiQtModForLayoutItemStack(self)

        self._layout_margins = 0, 0, 0, 0

        self._drag_h = 22

        self._layout_model.set_item_h(self._drag_h)

        self._viewport_rect = QtCore.QRect()

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.DragEnter:
                self._do_drag_enter_(event)
            elif event.type() == QtCore.QEvent.DragMove:
                if self._get_action_flag_is_match_(
                        self.ActionFlag.DragChildPolish
                ):
                    self._do_drag_child_polish_(event)
            elif event.type() == QtCore.QEvent.DragLeave:
                if self._get_action_flag_is_match_(
                        self.ActionFlag.DragChildPolish
                ):
                    self._do_drag_child_polish_leave_(event)
            elif event.type() == QtCore.QEvent.Drop:
                if self._get_action_flag_is_match_(
                        self.ActionFlag.DragChildPolish
                ):
                    self._do_drop_child_polish_(event)
        elif widget in self.__layout_item_stack.get_all_widgets():
            if event.type() == QtCore.QEvent.LayoutRequest:
                self._refresh_widget_all_()
        return False

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)

        if self._get_action_flag_is_match_(self.ActionFlag.DragChildPolish):
            painter._draw_frame_by_rect_(
                rect=self._drag_rect_child_polish,
                border_color=gui_qt_core.QtBorderColors.Button,
                background_color=gui_qt_core.QtBackgroundColors.BDragChildPolish,
                border_width=1,
            )

    def _do_drag_enter_(self, event):
        mdt = event.mimeData()
        key = mdt.data('lynxi/drag-and-drop-key')
        if key:
            key_cur = str(key)
            item = self.__layout_item_stack.get_item_by(key_cur)
            if item:
                index = self.__layout_item_stack.get_index_by(item)
                self._index_drag_child_polish_start = index
                self._set_action_flag_(self.ActionFlag.DragChildPolish)
                for i_widget in self.__layout_item_stack.get_all_widgets():
                    i_widget._start_drag_mode_()
                self._refresh_widget_all_()
                event.accept()

    def _do_drag_child_polish_(self, event):
        p = event.pos()
        x, y = p.x(), p.y()
        index_cur = self._layout_model.get_index_loc(x, y)
        if index_cur != self._index_drag_child_polish:
            self._index_drag_child_polish = min(index_cur, self.__layout_item_stack.get_index_maximum())
            c_x, c_y, c_w, c_h = self._layout_model.get_geometry_at(self._index_drag_child_polish)
            self._drag_rect_child_polish.setRect(c_x, c_y, c_w-1, c_h-1)
            self._refresh_widget_all_()

    def _do_drag_child_polish_leave_(self, event):
        self._set_action_flag_(self.ActionFlag.DragChildRemove)
        self._refresh_widget_all_()
        event.ignore()

    def _do_drop_child_polish_(self, event):
        self.__layout_item_stack.insert_item_between(
            self._index_drag_child_polish_start, self._index_drag_child_polish
        )

        self._index_drag_child_polish_start = None
        self._index_drag_child_polish = None

        self._clear_all_action_flags_()

        self._refresh_widget_all_()
        event.accept()

    def _drag_release_cbk_(self):
        for i_widget in self.__layout_item_stack.get_all_widgets():
            i_widget._end_drag_mode_()

        self._index_drag_child_polish_start = None
        self._index_drag_child_polish = None

        self._clear_all_action_flags_()
        self._refresh_widget_all_()

    # noinspection PyUnusedLocal
    def _add_widget_(self, widget, *args, **kwargs):
        widget.setParent(self)
        widget.installEventFilter(self)
        self.__layout_item_stack.create_item(widget)
        self._refresh_widget_all_()

    def _set_drop_enable_(self, boolean):
        self.setAcceptDrops(boolean)

    def _clear_all_widgets_(self):
        self.__layout_item_stack.restore()
        
    def _get_all_widgets_(self):
        return self.__layout_item_stack.get_all_widgets()

    def _get_all_widget_name_texts_(self):
        return self.__layout_item_stack.get_all_widget_names()

    def _sort_widgets_by_name_texts_(self, texts):
        self.__layout_item_stack.sort_widgets_by_names(texts)
