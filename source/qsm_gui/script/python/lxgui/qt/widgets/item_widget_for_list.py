# coding=utf-8
import lxbasic.core as bsc_core
# gui
from ... import core as _gui_core
# qt
from ..core.wrap import *

from .. import core as _qt_core

from .. import abstracts as _qt_abstracts
# qt widgets
from . import base as _base


class QtVideoPlayWidget(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtWidgetCloseBaseDef,
    _qt_abstracts.AbsQtThreadExtraDef,
):
    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        if self._video_flag is True:
            self._pixmap_cache_dict = {}

            x, y = 0, 0
            w, h = self.width(), self.height()

            img_mrg = self._image_margin

            spc = 2

            vdo_w, vdo_h = self._video_size

            frm_x, frm_y, frm_w, frm_h = (
                x+img_mrg, y+img_mrg, w-img_mrg*2, h-img_mrg*2
            )

            img_x, img_y, img_w, img_h = bsc_core.RawSizeMtd.fit_to(
                (vdo_w, vdo_h), (frm_w, frm_h)
            )

            self._image_draw_rect.setRect(
                frm_x+img_x, frm_y+img_y, img_w, img_h
            )

            prg_h = self._progress_h
            self._progress_draw_rect.setRect(
                frm_x+img_x, frm_y+img_y+img_h-prg_h, frm_w, prg_h
            )

            txt_frm_w, txt_frm_h = self._text_frm_w, self._text_frm_h

            txt_frm_x, txt_frm_y = frm_x+(frm_w-txt_frm_w)/2, frm_y+img_y+img_h-prg_h-txt_frm_h-spc
            self._text_draw_rect.setRect(
                frm_x+img_x, txt_frm_y, frm_w, txt_frm_h
            )
            self._text_frame_draw_rect.setRect(
                txt_frm_x, txt_frm_y, txt_frm_w, txt_frm_h
            )

            if self._image_cover is not None:
                pixmap = QtGui.QPixmap.fromImage(self._image_cover, QtCore.Qt.AutoColor)
                self._pixmap_cover = pixmap.scaled(
                    self._image_draw_rect.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
                )

    def _do_enter_(self):
        if self._video_flag is True:
            self._video_play_flag = True

            self._wait_play_timer.start(1000)

            self._refresh_widget_draw_()

    def _do_leave_(self):
        if self._video_flag is True:
            self._video_play_flag = False

            self._is_playing = False
            self._wait_play_timer.stop()
            self._play_timer.stop()

            self._refresh_widget_draw_()

    def _do_hover_move_(self, event):
        if self._video_flag is True:
            pos = event.pos()
            if 0 <= pos.x() <= self.width():
                frame_index = int((float(pos.x())/self.width())*self._frame_index_maximum)
                frame_index = min(self._frame_index_maximum-1, frame_index)
                self._update_frame_(frame_index)
                self._frame_index = frame_index
                if self._is_playing:
                    self._is_playing = False
                    self._play_timer.stop()

            self._wait_play_timer.start(1000)

            self._refresh_widget_draw_()

    def _do_close_(self):
        super(QtVideoPlayWidget, self)._do_close_()
        self._do_thread_quit_()
        if self._video_capture_opt is not None:
            self._video_capture_opt.release()

    def __init__(self, *args, **kwargs):
        super(QtVideoPlayWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self._init_widget_close_base_def_(self)
        self._init_thread_extra_def_(self)

        self._frame_rect = QtCore.QRect()

        self._video_path = None
        self._video_flag = False
        self._video_capture_opt = None
        self._video_size = None

        self._image_margin = 4

        self._image_frame = None
        self._pixmap_frame = None
        self._image_cover = None
        self._pixmap_cover = None
        self._image_draw_rect = QtCore.QRect()

        self._progress_h = 4
        self._progress_draw_rect = QtCore.QRect()

        self._video_play_flag = False

        self._wait_play_timer = QtCore.QTimer(self)
        self._wait_play_timer.timeout.connect(self._do_play_)
        self._play_timer = QtCore.QTimer(self)
        self._play_timer.timeout.connect(self._next_frame_)
        self._is_playing = False
        self._frame_index = 0

        self._frame_index_maximum = 0
        self._fps = 24
        self._frame_interval = int(1000/self._fps)

        self._text = '00:00:00'
        self._text_draw_rect = QtCore.QRect()
        self._text_frame_draw_rect = QtCore.QRect()
        self._text_frm_h = 20
        self._text_frm_w = 72
        self._text_font = _qt_core.QtFont.generate(size=10)
        self._text_color = _gui_core.GuiRgba.DarkWhite
        self._text_frame_color = _gui_core.GuiRgba.Basic
        self._text_option = QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter

        self._image_cache_dict = {}
        self._pixmap_cache_dict = {}

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Close:
                self._do_close_()

            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()

            elif event.type() == QtCore.QEvent.Enter:
                self._do_enter_()
            elif event.type() == QtCore.QEvent.Leave:
                self._do_leave_()

            elif event.type() == QtCore.QEvent.MouseMove:
                self._do_hover_move_(event)

        return False

    def paintEvent(self, event):
        if self._video_flag is True:
            painter = _qt_core.QtPainter(self)
            if self._video_play_flag is False:
                if self._pixmap_cover is not None:
                    painter.drawPixmap(
                        self._image_draw_rect,
                        self._pixmap_cover
                    )
                    painter.device()
            else:
                # update frame
                if self._frame_index in self._pixmap_cache_dict:
                    self._pixmap_frame = self._pixmap_cache_dict[self._frame_index]
                else:
                    if self._image_frame is not None:
                        pixmap = QtGui.QPixmap.fromImage(self._image_frame, QtCore.Qt.AutoColor)
                        self._pixmap_frame = pixmap.scaled(
                            self._image_draw_rect.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation
                        )
                        self._pixmap_cache_dict[self._frame_index] = self._pixmap_frame
                
                if self._pixmap_frame is not None:
                    painter.drawPixmap(
                        self._image_draw_rect,
                        self._pixmap_frame
                    )
                    painter.device()

                rect = self._progress_draw_rect
                value = self._frame_index
                maximum = self._frame_index_maximum
                percent = float(value)/float(maximum)

                x, y = rect.x(), rect.y()
                w, h = rect.width(), rect.height()
                rect_new = QtCore.QRect(
                    x, y, w*percent, h
                )
                painter._set_border_color_(
                    _gui_core.GuiRgba.Transparent
                )
                if self._is_playing:
                    painter._set_background_color_(
                        _gui_core.GuiRgba.LightBlue
                    )
                else:
                    painter._set_background_color_(
                        _gui_core.GuiRgba.LightOrange
                    )
                painter.drawRect(
                    rect_new
                )
                # text frame
                painter._set_border_color_(
                    _gui_core.GuiRgba.Transparent
                )

                painter._set_background_color_(
                    *list(self._text_frame_color)[:3]+[127]
                )
                painter.drawRect(
                    self._text_frame_draw_rect
                )
                self._text = bsc_core.RawIntegerMtd.frame_to_time_prettify(self._frame_index, self._fps)
                # text
                painter._draw_text_by_rect_(
                    rect=self._text_draw_rect,
                    text=self._text,
                    font=self._text_font,
                    text_color=self._text_color,
                    text_option=self._text_option,
                )

    def _do_play_(self):
        if self._video_flag is True:
            self._is_playing = True
            self._wait_play_timer.stop()

            self._play_timer.start(self._frame_interval)

    def _next_frame_(self):
        if self._video_flag is True:
            if self._is_playing and self._frame_index < self._frame_index_maximum:
                self._update_frame_(self._frame_index)
                self._frame_index += 1
            else:
                self._frame_index = 0
                # self._play_timer.stop()

            self._refresh_widget_draw_()

    def _update_frame_(self, frame_index):
        if self._video_flag is True:
            if frame_index in self._image_cache_dict:
                self._image_frame = self._image_cache_dict[frame_index]
                return

            data = self._video_capture_opt.get_data(frame_index)
            if data:
                frame, width, height, channel = data
                bytes_per_line = 3*width
                img = QtGui.QImage(
                    frame.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888
                )
                self._image_cache_dict[frame_index] = img
                self._image_frame = img

    def _load_video_data_use_thread_(self):
        def cache_fnc_():
            import lxbasic.media.core as bsc_mda_core

            self._video_capture_opt = bsc_mda_core.VideoCaptureOpt(self._video_path)

            data = self._video_capture_opt.get_data(0)
            if data:
                frame, width, height, channel = data
                self._frame_index_maximum = self._video_capture_opt.get_frame_count()
                self._fps = self._video_capture_opt.get_fps()
                self._frame_interval = int(1000/self._fps)
                return [frame, width, height, channel]

        def build_fnc_(data_):
            if self._close_flag is True:
                return

            if data_:
                frame, width, height, channel = data_
                self._video_flag = True

                self._video_size = width, height
                bytes_per_line = width*3

                self._image_cover = QtGui.QImage(
                    frame.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888
                )

                self._do_enter_()

                self._refresh_widget_all_()

        # fixme: use thread maybe crash
        # t = _qt_core.QtBuildThread(self._widget)
        # self._ts.append(t)
        # t.set_cache_fnc(cache_fnc_)
        # t.cache_value_accepted.connect(build_fnc_)
        # t.start()
        build_fnc_(cache_fnc_())

    def _set_video_path_(self, file_path):
        self._video_path = file_path

        self._load_video_data_use_thread_()


class QtItemWidgetForList(
    QtWidgets.QWidget,

    _qt_abstracts.AbsQtVirtualItemWidgetBaseDef,

    _qt_abstracts.AbsQtMediaBaseDef,
    _qt_abstracts.AbsQtItemNameBaseDef,

    _qt_abstracts.AbsQtPathBaseDef,
    _qt_abstracts.AbsQtIndexBaseDef,

    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForHoverDef,
    _qt_abstracts.AbsQtActionForCheckDef,
    _qt_abstracts.AbsQtActionForSelectDef,
):
    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        if self._view is not None:
            x, y = 0, 0
            w, h = self.width(), self.height()

            grd_size = self._view.gridSize()
            grd_w, grd_h = grd_size.width(), grd_size.height()
            # frame
            frm_mrg = self._frame_margin
            rdu = self._shadow_radius

            frm_x_0, frm_y_0, frm_w_0, frm_h_0 = x+frm_mrg, y+frm_mrg, w-frm_mrg*2-rdu, h-frm_mrg*2-rdu

            self._frame_state_draw_rect.setRect(
                x+1, y+1, w-rdu-2, h-rdu-2
            )
            self._shadow_draw_rect.setRect(
                x+(w-frm_w_0), y+(h-frm_h_0), frm_w_0, frm_h_0
            )
            self._frame_draw_rect.setRect(
                frm_x_0, frm_y_0, frm_w_0, frm_h_0
            )

            frm_x, frm_y, frm_w, frm_h = (
                x+frm_mrg, y+frm_mrg, grd_w-frm_mrg*2-rdu, grd_h-frm_mrg*2-rdu
            )
            self._frame_main_rect.setRect(
                frm_x, frm_y, frm_w, frm_h
            )

            self._lot.setContentsMargins(
                frm_x, frm_y, w-frm_w, h-frm_h
            )
            # image
            img_mrg = self._image_margin
            img_frm_x, img_frm_y, img_frm_w, img_frm_h = (
                frm_x+img_mrg, frm_y+img_mrg, frm_w-img_mrg*2, frm_h-img_mrg*2
            )

            if self._image_flag is True:
                img_size = self._image_size
                if img_size is not None:
                    self._image_draw_flag = True
                    img_x, img_y, img_w, img_h = bsc_core.RawSizeMtd.fit_to(
                        (img_size[0], img_size[1]), (img_frm_w, img_frm_h)
                    )
                    self._image_draw_rect.setRect(
                        img_frm_x+img_x, img_frm_y+img_y, img_w, img_h
                    )
                    if self._svg_flag is False:
                        pixmap = QtGui.QPixmap.fromImage(self._image, QtCore.Qt.AutoColor)
                        self._pixmap = pixmap.scaled(
                            self._image_draw_rect.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
                        )
                else:
                    self._image_draw_flag = False

            if self._video_auto_play_flag is True:
                vdo_w = vdo_h = self._video_s
                self._video_play_rect.setRect(
                    frm_x+(frm_w-vdo_w)/2, frm_y+(frm_h-vdo_h)/2, vdo_w, vdo_h
                )
            # name
            if self._name_flag is True:
                nme_mrg = self._name_margin
                nme_frm_x, nme_frm_y, nme_frm_w, nme_frm_h = (
                    frm_x+nme_mrg, frm_y+nme_mrg, frm_w-nme_mrg*2, frm_h-nme_mrg*2
                )
                if self._name_text:
                    self._name_text_draw_flag = True
                    self._name_draw_rect.setRect(
                        nme_frm_x, nme_frm_y, nme_frm_w, nme_frm_h
                    )
                else:
                    self._name_text_draw_flag = False

                self._name_dict_draw_flag = False
            # index
            if self._index_flag is True:
                idx_mrg = self._index_margin
                idx_frm_x, idx_frm_y, idx_frm_w, idx_frm_h = (
                    frm_x+idx_mrg, frm_y+idx_mrg, frm_w-idx_mrg*2, frm_h-idx_mrg*2
                )
                if self._index_text:
                    idx_w, idx_h = QtGui.QFontMetrics(self._index_font).width(self._index_text), self._index_h
                    self._index_draw_rect.setRect(
                        idx_frm_x, idx_frm_y, idx_w, idx_h
                    )
                    self._index_draw_flag = True
                else:
                    self._index_draw_flag = False
            #
            if self._view._get_is_grid_mode_():
                self._do_update_widget_frame_geometries_for_grid_mode_()
            else:
                self._do_update_widget_frame_geometries_for_list_mode_()

    def _do_update_widget_frame_geometries_for_grid_mode_(self):
        pass

    def _do_update_widget_frame_geometries_for_list_mode_(self):
        if self._name_flag:
            p = self._frame_main_rect.topRight()
            x, y = p.x(), p.y()
            w, h = self.width()-self._frame_main_rect.width(), self._frame_main_rect.height()
            spc = self._frame_spacing
            if self._name_dict:
                self._name_dict_draw_flag = True

                key_widths = []
                c_x, c_y = x+spc, y
                txt_h = self._name_h
                for i_data in self._name_dict_draw_data:
                    i_key, i_value, i_rect = i_data
                    i_key_width = QtGui.QFontMetrics(self._name_font).width(i_key)+16
                    key_widths.append(i_key_width)
                    i_rect.setRect(
                        c_x, c_y, w, txt_h
                    )
                    c_y += txt_h

                self._name_key_width = max(key_widths)
            else:
                self._name_dict_draw_flag = False

    def _do_enter_(self):
        self._is_hovered = True

        self._refresh_widget_draw_()

    def _do_leave_(self):
        self._set_hovered_(False)

    def __init__(self, *args, **kwargs):
        super(QtItemWidgetForList, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self._init_virtual_item_widget_base_def_(self)

        self._init_media_base_def_(self)
        self._init_item_name_base_dict_(self)

        self._init_path_base_def_(self)
        self._init_index_base_def_(self)

        self._index_font = _qt_core.QtFont.generate(size=6)
        self._index_text_option = QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        self._index_color = _gui_core.GuiRgba.LightGray

        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_check_def_(self)
        self._init_action_for_select_def_(self)

        self._frame_margin = 2
        self._shadow_radius = 2
        self._frame_border_radius = 0
        self._frame_spacing = 2

        self._frame_main_rect = QtCore.QRect()

        self._frame_state_draw_rect = QtCore.QRect()
        self._frame_draw_rect = QtCore.QRect()
        self._shadow_draw_rect = QtCore.QRect()

        self._frame_background_color = _gui_core.GuiRgba.Basic

        self._video_player_show_timer = QtCore.QTimer()

        self._video_player_show_flag = False

        self._lot = _base.QtVBoxLayout(self)
        # m_l, m_t, m_r, m_b

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Close:
                self._do_thread_quit_()

            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()

            elif event.type() == QtCore.QEvent.Enter:
                self._do_enter_()
            elif event.type() == QtCore.QEvent.Leave:
                self._do_leave_()

        return False

    def paintEvent(self, event):
        if self._view is not None:
            painter = _qt_core.QtPainter(self)

            offset = self._get_action_offset_()
            # shadow
            painter._draw_frame_by_rect_(
                rect=self._shadow_draw_rect,
                border_color=_qt_core.QtBorderColors.Transparent,
                background_color=_qt_core.QtBackgroundColors.Shadow,
            )
            # frame base
            bck_color = painter._generate_item_background_color_by_rect_(
                self._frame_state_draw_rect,
                is_hovered=self._is_hovered,
                is_selected=self._is_selected,
                is_actioned=self._get_is_actioned_(),
                background_color=_gui_core.GuiRgba.Transparent,
                background_color_hovered=_gui_core.GuiRgba.LightOrange,
                background_color_selected=_gui_core.GuiRgba.LightBlue,
                background_color_actioned=_gui_core.GuiRgba.LightPurple
            )
            painter._draw_frame_by_rect_(
                rect=self._frame_state_draw_rect,
                border_color=_qt_core.QtBorderColors.Transparent,
                background_color=bck_color,
                border_radius=self._frame_border_radius,
                offset=0
            )
            # frame
            painter._draw_frame_by_rect_(
                self._frame_draw_rect,
                border_color=_qt_core.QtBorderColors.Transparent,
                background_color=self._frame_background_color,
                border_radius=self._frame_border_radius,
                offset=offset
            )
            # image
            if self._image_draw_flag is True:
                if self._svg_flag is True:
                    painter._draw_svg_by_rect_(
                        self._image_draw_rect,
                        self._svg_path
                    )
                else:
                    painter.drawPixmap(
                        self._image_draw_rect,
                        self._pixmap
                    )
                    painter.device()
                
                if self._video_auto_play_flag is True:
                    painter._draw_video_play_button_by_rect_(
                        self._video_play_rect,
                        offset=offset,
                    )
            # name
            self._draw_name_(painter)
            # index
            self._draw_index_(painter)

    def _draw_name_(self, painter):
        # name text
        if self._name_text_draw_flag is True:
            painter._set_text_color_(
                self._name_color
            )
            painter._set_font_(
                self._name_font
            )
            text_option = QtGui.QTextOption(
                self._name_text_option
            )
            text_option.setWrapMode(
                text_option.WrapAtWordBoundaryOrAnywhere
            )
            rect_f = QtCore.QRectF(
                self._name_draw_rect.x(), self._name_draw_rect.y(),
                self._name_draw_rect.width(), self._name_draw_rect.height()
            )
            painter.drawText(
                rect_f,
                self._name_text,
                text_option,
            )
        # name dict
        if self._name_dict_draw_flag is True:
            for i_key, i_value, i_rect in self._name_dict_draw_data:
                painter._set_text_draw_by_rect_use_key_value_(
                    rect=i_rect,
                    key_text=i_key,
                    value_text=i_value,
                    key_text_width=self._name_key_width,
                )

    def _draw_index_(self, painter):
        if self._index_draw_flag is True:
            painter._set_text_color_(
                self._index_color
            )
            painter._set_font_(
                self._index_font
            )
            painter.drawText(
                self._index_draw_rect,
                self._index_text_option,
                self._index_text,
            )

    def _set_selected_(self, boolean):
        self._is_selected = boolean
        self._refresh_widget_draw_()

    def _set_hovered_(self, boolean):
        self._is_hovered = boolean
        if self._video_auto_play_flag is True:
            self._update_video_play_(boolean)
        self._widget.update()

    def _show_video_auto_play_(self):
        if self._video_player_show_flag is True:
            self._lot._clear_all_widgets_()
            self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, False)
            wgt = QtVideoPlayWidget()
            self._lot.addWidget(wgt)
            wgt._set_video_path_(
                self._video_path
            )

    def _close_video_auto_play_(self):
        self._video_player_show_flag = False
        self._lot._clear_all_widgets_()
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)

    def _update_video_play_(self, boolean):
        if boolean is True:
            self._video_player_show_flag = True
            self._video_player_show_timer.singleShot(500, self._show_video_auto_play_)
        else:
            self._close_video_auto_play_()

    # fixme: for size change
    def _set_frame_size_(self, *args, **kwargs):
        pass