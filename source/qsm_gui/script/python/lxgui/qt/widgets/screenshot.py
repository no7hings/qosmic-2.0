# coding=utf-8
import six

import enum

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# qt
from ..core.wrap import *
# gui
from ... import core as _gui_core
# qt
from .. import core as _qt_core
# qt abstracts
from .. import abstracts as _qt_abstracts
# qt widgets
from . import base as _base

from . import utility as _utility

from . import button as _button

from . import entry_frame as _entry_frame


class AbsQtScreenshotBaseDef(_qt_abstracts.AbsQtHelpBaseDef):
    class Mode(enum.IntEnum):
        Started = 0
        New = 1
        Edit = 2
        Stopped = 3

    RectRegion = _gui_core.GuiRectRegion

    CURSOR_MAPPER = {
        RectRegion.Unknown: QtCore.Qt.ArrowCursor,
        RectRegion.Top: QtCore.Qt.SizeVerCursor,
        RectRegion.Bottom: QtCore.Qt.SizeVerCursor,
        RectRegion.Left: QtCore.Qt.SizeHorCursor,
        RectRegion.Right: QtCore.Qt.SizeHorCursor,
        RectRegion.TopLeft: QtCore.Qt.SizeFDiagCursor,
        RectRegion.TopRight: QtCore.Qt.SizeBDiagCursor,
        RectRegion.BottomLeft: QtCore.Qt.SizeBDiagCursor,
        RectRegion.BottomRight: QtCore.Qt.SizeFDiagCursor,
        RectRegion.Inside: QtCore.Qt.SizeAllCursor,
    }

    screenshot_started = qt_signal()
    screenshot_finished = qt_signal()
    screenshot_accepted = qt_signal(list)
    CACHE = 0, 0, 0, 0

    def _init_screenshot_base_def_(self, widget):
        self._widget = widget
        self._init_help_base_def_(widget)

        self._screenshot_mode = self.Mode.Started
        self._screenshot_is_modify = False

        self._screenshot_file_path = None

        self._screenshot_rect = QtCore.QRect()

        self._screenshot_is_activated = False
        #
        self._screenshot_point_start = QtCore.QPoint()
        #
        self._screenshot_rect_point_start = QtCore.QPoint()
        self._screenshot_rect_point_start_offset = [0, 0]
        self._screenshot_rect_point_start_offset_temp = [0, 0]
        self._screenshot_rect_point_end = QtCore.QPoint()
        self._screenshot_rect_point_end_offset = [0, 0]
        self._screenshot_rect_point_end_offset_temp = [0, 0]

        self._screenshot_rect_region_edit = self.RectRegion.Unknown

        self._screenshot_modify_gap = 8

        self._frame_draw_rect = QtCore.QRect()

        self._position_text = '0, 0'
        self._position_text_color = _gui_core.GuiRgba.LightAzureBlue
        self._position_frame_region = self.RectRegion.BottomRight
        self._position_frame_h = 24
        self._position_frame_draw_rect = QtCore.QRect()
        self._position_text_font = _qt_core.QtFont.generate(size=12)

        self._position_h_line = QtCore.QLine()
        self._position_v_line = QtCore.QLine()

        self._geometry_text = '0, 0, 0, 0'
        self._geometry_text_color = _gui_core.GuiRgba.LightAzureBlue
        self._geometry_frame_h = 24
        self._geometry_frame_draw_rect = QtCore.QRect()
        self._geometry_text_font = _qt_core.QtFont.generate(size=12)

        self._record_frame_draw_rect = QtCore.QRect()
        self._record_frame_h = 36
        self._record_frame_w = 240

        self._record_button_frame_rect = QtCore.QRect()
        self._record_button_draw_rect = QtCore.QRect()

        self._record_button_frame_s = 24

        self._record_button_s = 20

        self._record_button_is_hovered = False

        self._record_button_icon_file_path_0 = _gui_core.GuiIcon.get('tool/play-start')
        self._record_button_icon_file_path_1 = _gui_core.GuiIcon.get('tool/play-stop')
        self._record_button_icon_file_path_current = self._record_button_icon_file_path_0

        self._record_is_started = False

        self._record_frame_background_color = list(_gui_core.GuiRgba.LightBlack)[:3]+[127]

        self._record_text = '00:00:00:00'
        self._record_frame_index = 0
        self._record_fps = 24
        self._record_frame_interval = int(1000/self._record_fps)
        self._record_text_draw_rect = QtCore.QRect()
        self._record_text_color = _gui_core.GuiRgba.DarkWhite
        self._record_text_start_color = _gui_core.GuiRgba.LightRed
        self._record_text_font = _qt_core.QtFont.generate(size=12, weight=75)
        
        self._record_timer = QtCore.QTimer(self)
        self._record_timer.timeout.connect(self._record_next_frame_)

    def _do_screenshot_press_(self, event):
        self._screenshot_point_start = event.pos()
        if self._screenshot_mode == self.Mode.Started:
            self._screenshot_mode = self.Mode.New
        
        if self._record_button_is_hovered is True:
            self._swap_record_()

        self._widget.update()
        event.accept()
        
    def _swap_record_(self):
        self._record_is_started = not self._record_is_started
        self._record_button_icon_file_path_current = [
            self._record_button_icon_file_path_0, self._record_button_icon_file_path_1
        ][self._record_is_started]

        if self._record_is_started is True:
            self._start_record_()
        else:
            self._stop_record_()

    def _start_record_(self):
        self._record_timer.start(self._record_frame_interval)

    def _record_next_frame_(self):
        self._record_frame_index += 1

        self._record_text = bsc_core.BscInteger.frame_to_time_prettify(self._record_frame_index, self._record_fps)

        self._widget.update()

    def _stop_record_(self):
        self._record_timer.stop()

    def _do_screenshot_hover_move_(self, event):
        pos = event.pos()
        m_x, m_y = pos.x(), pos.y()

        if self._record_button_frame_rect.contains(pos):
            self._record_button_is_hovered = True
        else:
            self._record_button_is_hovered = False

        if self._screenshot_mode == self.Mode.Started:
            x, y = 0, 0
            w, h = self._widget.width(), self._widget.height()

            self._position_text = '{}, {}'.format(m_x, m_y)

            frm_w, frm_h = (
                QtGui.QFontMetrics(self._position_text_font).width(self._position_text)+24, self._position_frame_h
            )

            self._position_h_line.setLine(
                0, m_y, x+w, m_y
            )
            self._position_v_line.setLine(
                m_x, 0, m_x, y+h
            )

            self._position_frame_draw_rect.setRect(
                m_x, m_y, frm_w, frm_h
            )
        elif self._screenshot_mode == self.Mode.Edit:
            x, y = self._screenshot_rect.x(), self._screenshot_rect.y()
            w, h = self._screenshot_rect.width(), self._screenshot_rect.height()

            self._screenshot_rect_region_edit = self._get_rect_region_(
                m_x, m_y, x, y, w, h, 8
            )
            cursor = self.CURSOR_MAPPER[self._screenshot_rect_region_edit]

            self._widget.setCursor(QtGui.QCursor(cursor))

        self._widget.update()

        event.accept()

    def _do_screenshot_press_move_(self, event):
        p = event.pos()
        shift_mode = event.modifiers() == QtCore.Qt.ShiftModifier
        if self._screenshot_mode == self.Mode.New:
            # position
            s_x, s_y = self._screenshot_point_start.x(), self._screenshot_point_start.y()
            self._screenshot_rect_point_start.setX(s_x)
            self._screenshot_rect_point_start.setY(s_y)
            if shift_mode is True:
                x, y = p.x(), p.y()
                w, h = x-s_x, y-s_y
                s = max(w, h)
                self._screenshot_rect_point_end = QtCore.QPoint(s_x+s, s_y+s)
            else:
                self._screenshot_rect_point_end = event.pos()

        elif self._screenshot_mode == self.Mode.Edit:
            d_p = p-self._screenshot_point_start
            d_p_x, d_p_y = d_p.x(), d_p.y()
            o_s_x, o_s_y = self._screenshot_rect_point_start_offset_temp
            o_e_x, o_e_y = self._screenshot_rect_point_end_offset_temp
            if self._screenshot_rect_region_edit == self.RectRegion.Inside:
                self._screenshot_rect_point_start_offset[0] = o_s_x+d_p_x
                self._screenshot_rect_point_start_offset[1] = o_s_y+d_p_y
                self._screenshot_rect_point_end_offset[0] = o_e_x+d_p_x
                self._screenshot_rect_point_end_offset[1] = o_e_y+d_p_y
            elif self._screenshot_rect_region_edit == self.RectRegion.Top:
                self._screenshot_rect_point_start_offset[1] = o_s_y+d_p_y
            elif self._screenshot_rect_region_edit == self.RectRegion.Bottom:
                self._screenshot_rect_point_end_offset[1] = o_e_y+d_p_y
            elif self._screenshot_rect_region_edit == self.RectRegion.Left:
                self._screenshot_rect_point_start_offset[0] = o_s_x+d_p_x
            elif self._screenshot_rect_region_edit == self.RectRegion.Right:
                self._screenshot_rect_point_end_offset[0] = o_e_x+d_p_x
            elif self._screenshot_rect_region_edit == self.RectRegion.TopLeft:
                self._screenshot_rect_point_start_offset[0] = o_s_x+d_p_x
                self._screenshot_rect_point_start_offset[1] = o_s_y+d_p_y
            elif self._screenshot_rect_region_edit == self.RectRegion.TopRight:
                self._screenshot_rect_point_start_offset[1] = o_s_y+d_p_y
                self._screenshot_rect_point_end_offset[0] = o_e_x+d_p_x
            elif self._screenshot_rect_region_edit == self.RectRegion.BottomLeft:
                self._screenshot_rect_point_start_offset[0] = o_s_x+d_p_x
                self._screenshot_rect_point_end_offset[1] = o_e_y+d_p_y
            elif self._screenshot_rect_region_edit == self.RectRegion.BottomRight:
                self._screenshot_rect_point_end_offset[0] = o_e_x+d_p_x
                self._screenshot_rect_point_end_offset[1] = o_e_y+d_p_y

        self._update_move_geometry_()
        self._update_screenshot_geometry_()

        self._widget.update()
        event.accept()

    # noinspection PyUnusedLocal
    def _do_screenshot_press_release_(self, event):
        if self._screenshot_mode == self.Mode.New:
            if self._screenshot_rect_point_start != self._screenshot_rect_point_end:
                self._screenshot_mode = self.Mode.Edit
        elif self._screenshot_mode == self.Mode.Edit:
            self._screenshot_rect_point_start_offset_temp[0] = self._screenshot_rect_point_start_offset[0]
            self._screenshot_rect_point_start_offset_temp[1] = self._screenshot_rect_point_start_offset[1]
            self._screenshot_rect_point_end_offset_temp[0] = self._screenshot_rect_point_end_offset[0]
            self._screenshot_rect_point_end_offset_temp[1] = self._screenshot_rect_point_end_offset[1]

        self._widget.update()
        event.accept()

    def _update_move_geometry_(self):
        pass

    def _update_screenshot_geometry_(self):
        x, y = 0, 0
        w, h = self._widget.width(), self._widget.height()

        x_0, y_0 = self._screenshot_rect_point_start.x(), self._screenshot_rect_point_start.y()
        x_1, y_1 = self._screenshot_rect_point_end.x(), self._screenshot_rect_point_end.y()

        o_s_x, o_s_y = self._screenshot_rect_point_start_offset
        o_e_x, o_e_y = self._screenshot_rect_point_end_offset

        spc = 16

        x_0 += o_s_x
        y_0 += o_s_y
        x_1 += o_e_x
        y_1 += o_e_y

        scr_x, scr_y = min(x_0, x_1), min(y_0, y_1)
        scr_w, scr_h = abs(x_1-x_0), abs(y_1-y_0)

        self._screenshot_rect.setRect(
            scr_x, scr_y, scr_w, scr_h
        )

        txt_frm_w, txt_frm_h = self._help_text_draw_size

        txt_w, txt_h = txt_frm_w-48, txt_frm_h-48

        if self._screenshot_mode == self.Mode.Started:
            self._help_frame_draw_rect.setRect(
                x+(w-txt_frm_w)/2, y+(h-txt_frm_h)/2, txt_frm_w, txt_frm_h
            )
            self._help_draw_rect.setRect(
                x+(w-txt_w)/2, y+(h-txt_h)/2, txt_w, txt_h
            )
        elif self._screenshot_mode in {self.Mode.New, self.Mode.Edit}:
            # geometry
            self._geometry_text = '{}, {}, {}, {}'.format(scr_x, scr_y, scr_w, scr_h)
            gmt_frm_w, gmt_frm_h = (
                QtGui.QFontMetrics(self._geometry_text_font).width(self._geometry_text)+24, self._geometry_frame_h
            )

            self._geometry_frame_draw_rect.setRect(
                scr_x, scr_y, gmt_frm_w, gmt_frm_h
            )
            # help
            self._help_frame_draw_rect.setRect(
                scr_x+(scr_w-txt_frm_w)/2, scr_y+scr_h+16, txt_frm_w, txt_frm_h
            )
            self._help_draw_rect.setRect(
                scr_x+(scr_w-txt_frm_w)/2+(txt_frm_w-txt_w)/2, scr_y+scr_h+(txt_frm_h-txt_h)/2+spc, txt_w, txt_h
            )
            # record
            rcd_frm_w, rcd_frm_h = self._record_frame_w, self._record_frame_h
            rcd_frm_x, rcd_frm_y = scr_x+(scr_w-rcd_frm_w)/2, scr_y-rcd_frm_h-spc
            self._record_frame_draw_rect.setRect(
                rcd_frm_x, rcd_frm_y, rcd_frm_w, rcd_frm_h
            )

            rcd_btn_frm_s = self._record_button_frame_s
            rcd_btn_frm_x, rcd_btn_frm_y = rcd_frm_x+(rcd_frm_h-rcd_btn_frm_s)/2, rcd_frm_y+(rcd_frm_h-rcd_btn_frm_s)/2
            self._record_button_frame_rect.setRect(
                rcd_btn_frm_x, rcd_btn_frm_y, rcd_btn_frm_s, rcd_btn_frm_s
            )

            rcd_btn_s = self._record_button_frame_s
            rcd_btn_x, rcd_btn_y = rcd_btn_frm_x+(rcd_btn_frm_s-rcd_btn_s)/2, rcd_btn_frm_y+(rcd_btn_frm_s-rcd_btn_s)/2
            self._record_button_draw_rect.setRect(
                rcd_btn_x, rcd_btn_y, rcd_btn_s, rcd_btn_s
            )
            # record text
            rcd_txt_w, rcd_txt_h = rcd_frm_w-rcd_btn_frm_s, rcd_frm_h
            self._record_text_draw_rect.setRect(
                rcd_frm_x+rcd_btn_frm_s, rcd_frm_y, rcd_txt_w, rcd_txt_h
            )

    def _cancel_screenshot_(self):
        self.screenshot_finished.emit()
        self._widget.close()
        self._widget.deleteLater()

    def _accept_screenshot_(self):
        def fnc_():
            x, y, w, h = self._get_screenshot_accept_geometry_args_()
            # hide first
            self._widget.hide()
            # noinspection PyBroadException
            try:
                self.screenshot_accepted.emit([x, y, w, h])
            except Exception:
                pass
            finally:
                # finish later
                self.screenshot_finished.emit()
                # finally close
                self._widget.close()
                self._widget.deleteLater()

        self._screenshot_mode = self.Mode.Stopped
        self._widget.update()

        AbsQtScreenshotBaseDef.CACHE = self._get_screenshot_accept_geometry_args_()

        self._timer = QtCore.QTimer(self._widget)
        self._timer.singleShot(100, fnc_)

    def _start_screenshot_(self):
        self.screenshot_started.emit()
        # full screen
        # noinspection PyArgumentList
        self._widget.setGeometry(
            QtWidgets.QApplication.desktop().rect()
        )
        self._widget.show()
        self._widget.setCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )

    @classmethod
    def _get_rect_region_(cls, m_x, m_y, x, y, w, h, gap):
        # top
        if x+gap < m_x < x+w-gap and y-gap < m_y < y+gap:
            return cls.RectRegion.Top
        # bottom
        elif x+gap < m_x < x+w-gap and y+h-gap < m_y < y+h+gap:
            return cls.RectRegion.Bottom
        # left
        elif x-gap < m_x < x+gap and y+gap < m_y < y+h-gap:
            return cls.RectRegion.Left
        # right
        elif x+w-gap < m_x < x+w+gap and y+gap < m_y < y+h-gap:
            return cls.RectRegion.Right
        # top left
        elif x-gap < m_x < x+gap and y-gap < m_y < y+gap:
            return cls.RectRegion.TopLeft
        # top right
        elif x+w-gap <= m_x <= x+w+gap and y-gap <= m_y <= y+gap:
            return cls.RectRegion.TopRight
        # bottom left
        elif x-gap < m_x < x+gap and y+h-gap < m_y < y+h+gap:
            return cls.RectRegion.BottomLeft
        # bottom right
        elif x+w-gap < m_x < x+w+gap and y+h-gap < m_y < y+h+gap:
            return cls.RectRegion.BottomRight
        # inside
        elif x+gap < m_x < x+w-gap and y+gap < m_y < y+h-gap:
            return cls.RectRegion.Inside
        else:
            return cls.RectRegion.Unknown

    def _get_screenshot_accept_geometry_args_(self):
        x, y = self._widget.x(), self._widget.y()

        rect_0 = self._screenshot_rect
        x_0, y_0, w_0, h_0 = rect_0.x(), rect_0.y(), rect_0.width(), rect_0.height()
        return x+x_0, y+y_0, w_0, h_0

    @classmethod
    def _save_screenshot_to_(cls, geometry, file_path):
        bsc_storage.StgFileOpt(file_path).create_directory()
        rect = QtCore.QRect(*geometry)
        app = QtWidgets.QApplication
        # noinspection PyArgumentList
        if QT_LOAD_INDEX == 0:
            app_ = QtWidgets.QApplication
            # noinspection PyArgumentList
            image = app_.primaryScreen().grabWindow(
                app_.desktop().winId()
            ).copy(rect).toImage()
        else:
            app_ = QtWidgets.QApplication
            # noinspection PyArgumentList
            image = QtGui.QPixmap.grabWindow(
                app_.desktop().winId()
            ).copy(rect).toImage()

        _qt_core.QtUtil.save_qt_image(image, file_path)


class QtScreenshotFrame(
    QtWidgets.QWidget,
    AbsQtScreenshotBaseDef,

    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForHoverDef,
    _qt_abstracts.AbsQtActionForPressDef,
):
    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        self._frame_draw_rect.setRect(
            x-1, y-1, w+2, h+2
        )

    def __init__(self, *args, **kwargs):
        super(QtScreenshotFrame, self).__init__(*args, **kwargs)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(True)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.Window
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.WindowStaysOnTopHint
        )

        self._init_screenshot_base_def_(self)

        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)

        self._help_text_draw_size = 480, 120
        self._help_text_start = (
            'Screenshot:\n'
            '    "LMB-click" and "LMB-move" to create,\n'
            '    "Escape Key-press" to cancel.'
        )

        self._help_text_edit = (
            'Screenshot:\n'
            '    "LMB-move" to edit,\n'
            '    "LMB-double-click" or "Enter Key-press" to accept,\n'
            '    "Escape Key-press" to cancel.'
        )

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._update_screenshot_geometry_()
                self._refresh_widget_draw_geometry_()
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self._do_screenshot_press_(event)
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                self._accept_screenshot_()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    self._do_screenshot_press_move_(event)
                else:
                    self._do_screenshot_hover_move_(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self._do_screenshot_press_release_(event)
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() in {QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter}:
                    self._accept_screenshot_()
                elif event.key() == QtCore.Qt.Key_Escape:
                    self._cancel_screenshot_()
        return False

    def paintEvent(self, event):
        if self._screenshot_mode != self.Mode.Stopped:
            painter = _qt_core.QtPainter(self)

            # draw start
            if self._screenshot_mode == self.Mode.Started:
                # fixme: must fill color?
                painter._draw_frame_by_rect_(
                    rect=self._frame_draw_rect,
                    border_color=(0, 0, 0, 0),
                    background_color=(0, 0, 0, 1)
                )
                # help
                painter._draw_frame_by_rect_(
                    rect=self._help_frame_draw_rect,
                    border_color=(0, 0, 0, 0),
                    background_color=(31, 31, 31, 127)
                )
                painter._draw_text_by_rect_(
                    rect=self._help_draw_rect,
                    text=self._help_text_start,
                    font=_qt_core.QtFonts.Large,
                    text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                    word_warp=True
                )

                painter._set_border_color_(
                    _gui_core.GuiRgba.DarkWhite
                )
                painter.drawLine(self._position_h_line)
                painter.drawLine(self._position_v_line)
                # position text
                painter._set_text_color_(
                    self._position_text_color
                )
                painter._set_font_(
                    self._position_text_font
                )
                painter.drawText(
                    self._position_frame_draw_rect,
                    QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                    self._position_text
                )
            # draw new or edit
            elif self._screenshot_mode in {self.Mode.New, self.Mode.Edit}:
                painter._set_screenshot_draw_by_rect_(
                    base_rect=self._frame_draw_rect,
                    screenshot_rect=self._screenshot_rect,
                    border_color=_gui_core.GuiRgba.LightAzureBlue,
                    background_color=(0, 0, 0, 127)
                )
                # help
                painter._draw_frame_by_rect_(
                    rect=self._help_frame_draw_rect,
                    border_color=(0, 0, 0, 0),
                    background_color=(31, 31, 31, 127)
                )
                painter._draw_text_by_rect_(
                    rect=self._help_draw_rect,
                    text=self._help_text_edit,
                    font=_qt_core.QtFonts.Large,
                    text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                    word_warp=True
                )
                # geometry text
                painter._set_text_color_(
                    self._geometry_text_color
                )
                painter._set_font_(
                    self._geometry_text_font
                )
                painter.drawText(
                    self._geometry_frame_draw_rect,
                    QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                    self._geometry_text
                )
                if self._screenshot_mode == self.Mode.Edit:
                    # record
                    painter._set_border_color_(
                        0, 0, 0, 0
                    )
                    painter._set_background_color_(
                        self._record_frame_background_color
                    )
                    painter.drawRect(
                        self._record_frame_draw_rect
                    )
                    painter._draw_icon_file_by_rect_(
                        rect=self._record_button_draw_rect,
                        file_path=self._record_button_icon_file_path_current,
                        is_hovered=self._record_button_is_hovered
                    )
                    # record text
                    if self._record_is_started is True:
                        painter._set_text_color_(
                            self._record_text_start_color
                        )
                    else:
                        painter._set_text_color_(
                            self._record_text_color
                        )

                    painter._set_font_(
                        self._record_text_font
                    )
                    painter.drawText(
                        self._record_text_draw_rect,
                        QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                        self._record_text
                    )


class QtEntryAsScreenshot(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtEntryBaseDef,

    _qt_abstracts.AbsQtEntryFrameExtraDef,
):
    def __init__(self, *args, **kwargs):
        super(QtEntryAsScreenshot, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        self._init_entry_base_def_(self)
        self._init_entry_frame_extra_def_(self)

        self.installEventFilter(self)


class QtInputAsScreenshot(
    _entry_frame.QtEntryFrame,
    _qt_abstracts.AbsQtInputBaseDef,
):
    QT_ENTRY_CLS = QtEntryAsScreenshot

    def __init__(self, *args, **kwargs):
        super(QtInputAsScreenshot, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self._init_input_base_def_(self)
        self._build_input_entry_(str)

        self.installEventFilter(self)

    def _build_input_entry_(self, value_type):
        self._entry_frame_widget = self

        self._value_type = value_type

        main_layout = _base.QtVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        entry_widget = _utility.QtTranslucentWidget()
        main_layout.addWidget(entry_widget)
        #
        entry_layout = _base.QtHBoxLayout(entry_widget)
        entry_layout.setContentsMargins(2, 2, 2, 2)
        entry_layout.setSpacing(0)
        #
        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)
        self._entry_widget._set_entry_frame_(self)
        #
        self._input_button_widget = _utility.QtLineWidget()
        self._input_button_widget._set_line_styles_(
            [self._input_button_widget.Style.Null, self._input_button_widget.Style.Null,
             self._input_button_widget.Style.Solid,
             self._input_button_widget.Style.Null]
        )
        entry_layout.addWidget(self._input_button_widget)
        self._input_button_layout = _base.QtVBoxLayout(self._input_button_widget)
        self._input_button_layout._set_align_top_()
        self._input_button_layout.setContentsMargins(2, 0, 0, 0)
        self._input_button_layout.setSpacing(2)

        self._screenshot_button = _button.QtIconPressButton()
        self._input_button_layout.addWidget(self._screenshot_button)
        self._screenshot_button._set_icon_file_path_(_gui_core.GuiIcon.get('camera'))
        self._screenshot_button._set_icon_frame_draw_size_(18, 18)
        self._screenshot_button._set_name_text_('tool/snapshot')
        self._screenshot_button._set_tool_tip_('"LMB-click" to create screenshot')

        self._screenshot_button.press_clicked.connect(self._do_screenshot_)

        self._resize_handle.raise_()

    @staticmethod
    def _generate_screenshot_file_path_():
        d = bsc_core.BscSystem.get_home_directory()
        return six.u('{}/screenshot/untitled-{}.png').format(d, bsc_core.TimeExtraMtd.generate_time_tag_36())

    def _save_screenshot_(self, g):
        f = self._generate_screenshot_file_path_()
        QtScreenshotFrame._save_screenshot_to_(
            g, f
        )
        # self.append(f)
        # self.update_history()

    def _do_screenshot_(self):
        active_window = _qt_core.QtUtil.get_qt_active_window()
        w = QtScreenshotFrame()
        w.screenshot_started.connect(active_window.hide)
        w._start_screenshot_()
        w.screenshot_accepted.connect(self._save_screenshot_)
        w.screenshot_finished.connect(active_window.show)
