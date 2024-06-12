# coding=utf-8
# qt
from ..core.wrap import *

from ...qt import core as _qt_core

from ...qt import abstracts as _qt_abstracts

from . import resize as _resize


# base entry frame
class QtEntryFrame(
    QtWidgets.QWidget,

    _qt_abstracts.AbsQtNameBaseDef,
    _qt_abstracts.AbsQtFrameBaseDef,
    _qt_abstracts.AbsQtStatusBaseDef,

    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtThreadBaseDef,
):
    geometry_changed = qt_signal(int, int, int, int)
    entry_focus_in = qt_signal()
    entry_focus_out = qt_signal()
    entry_focus_changed = qt_signal()

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        # int left， int top， int right， int bottom
        m_l, m_t, m_r, m_b = self._frame_draw_margins
        #
        c = self._entry_count
        #
        frm_x, frm_y = x+m_l+1, y+m_t+1
        frm_w, frm_h = w-m_l-m_r-2, h-m_t-m_b-2
        #
        self._rect_frame_draw.setRect(
            frm_x, frm_y, frm_w, frm_h
        )
        if c > 1:
            for i in range(c):
                i_widget = self._value_entries[i]
                i_p = i_widget.pos()
                i_r = i_widget.rect()
                i_x, i_y = i_p.x(), i_p.y()
                i_w, i_h = i_r.width(), i_r.height()
                self._frame_draw_rects[i].setRect(
                    i_x, frm_y, i_w, frm_h
                )
        else:
            self._frame_draw_rects[0].setRect(
                frm_x, frm_y, frm_w, frm_h
            )
        #
        if self._tip_draw_enable is True:
            self._tip_draw_rect.setRect(
                x, y, w, h
            )
        #
        if self._resize_handle is not None:
            frm_w, frm_h = 24, 24
            r_x, r_y = x+(w-frm_w), y+(h-frm_h)
            self._resize_handle.setGeometry(
                r_x, r_y, frm_w, frm_h
            )

    def __init__(self, *args, **kwargs):
        super(QtEntryFrame, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._is_hovered = False
        self._is_focused = False
        self._entry_count = 1
        #
        self._entry_widget = None
        self._value_entries = []
        #
        self._init_name_base_def_(self)
        self._init_frame_base_def_(self)
        self._init_status_base_def_(self)
        self._init_action_base_def_(self)
        self._init_thread_base_def_(self)
        #
        self._frame_border_color = _qt_core.QtBorderColors.Light
        self._hovered_frame_border_color = _qt_core.QtBorderColors.Hovered
        self._selected_frame_border_color = _qt_core.QtBorderColors.Selected
        self._frame_background_color = _qt_core.QtBackgroundColors.Dim

        self._resize_handle = _resize.QtVResizeHandle(self)
        self._resize_handle.hide()

        self._tip_draw_enable = False
        self._tip_text = None
        self._tip_draw_rect = QtCore.QRect()
        # self._resize_handle._set_resize_target_(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
                self.geometry_changed.emit(
                    self.x(), self.y(), self.width(), self.height()
                )
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)

        is_selected = self._is_focused

        color_bkg = self._frame_background_color
        color_bdr = [_qt_core.QtBorderColors.Basic, _qt_core.QtBorderColors.HighLight][is_selected]
        w_bdr = [self._frame_border_width, self._frame_border_width+1][is_selected]
        painter._set_border_color_(
            _qt_core.QtColors.Transparent
        )
        painter._set_background_color_(
            color_bkg
        )
        for i_rect in self._frame_draw_rects:
            painter.drawRect(i_rect)

        if self._tip_draw_enable is True:
            if self._tip_text is not None:
                painter._draw_text_by_rect_(
                    rect=self._tip_draw_rect,
                    text=self._tip_text,
                    text_color=_qt_core.QtColors.TextDisable,
                    font=_qt_core.QtFonts.DefaultItalic,
                    text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                )

        if self._thread_draw_flag is True:
            for i_rect in self._frame_draw_rects:
                painter._draw_alternating_colors_by_rect_(
                    rect=i_rect,
                    colors=((0, 0, 0, 63), (0, 0, 0, 0)),
                    running=True
                )

        painter._set_border_color_(
            color_bdr
        )
        painter._set_background_color_(
            _qt_core.QtColors.Transparent
        )
        painter._set_border_width_(w_bdr)
        for i_rect in self._frame_draw_rects:
            painter.drawRect(i_rect)
        #
        if self._is_status_enable is True:
            for i_rect in self._frame_draw_rects:
                painter._set_background_color_(
                    self._status_color
                )
                painter.drawRect(i_rect)

    # resize
    def _get_resize_handle_(self):
        return self._resize_handle

    def _set_resize_enable_(self, boolean):
        self._resize_handle.setVisible(boolean)

    def _set_resize_minimum_(self, value):
        self._resize_handle._set_resize_minimum_(value)

    def _set_resize_target_(self, widget):
        self._resize_handle._set_resize_target_(widget)

    def _update_background_color_by_locked_(self, boolean):
        self._frame_background_color = [
            _qt_core.QtBackgroundColors.Dark, _qt_core.QtBackgroundColors.Dim
        ][boolean]

    def _set_focused_(self, boolean):
        self._is_focused = boolean
        self._refresh_widget_draw_()
        self.entry_focus_changed.emit()

    def _set_focus_in_(self):
        self._set_focused_(True)
        self.entry_focus_in.emit()

    def _set_focus_out_(self):
        self._set_focused_(False)
        self.entry_focus_out.emit()

    def _set_entry_count_(self, size):
        self._entry_count = size
        self._frame_draw_rects = [QtCore.QRect() for _ in range(size)]

    def _set_size_policy_height_fixed_mode_(self):
        self._entry_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )

    def _set_tip_text_(self, text):
        self._tip_text = text

    def _set_tip_draw_enable_(self, boolean):
        self._tip_draw_enable = boolean

    def _set_visible_(self, boolean):
        self.setVisible(boolean)