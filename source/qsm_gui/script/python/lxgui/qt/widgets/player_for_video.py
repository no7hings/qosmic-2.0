# coding=utf-8
import lxbasic.core as bsc_core
# gui
from ... import core as _gui_core
# qt
from ..core.wrap import *

from .. import core as _qt_core

from .. import abstracts as _qt_abstracts


class QtVideoPlayWidget(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtWidgetCloseBaseDef,
    _qt_abstracts.AbsQtThreadExtraDef,
):
    class PlayModes(object):
        Video = 0x01
        ImageSequence = 0x02

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

            img_size = self._resolution

            _x, _y, img_frm_w, img_frm_h = bsc_core.RawSizeMtd.fit_to(
                (img_size[0], img_size[1]), (w, h)
            )
            img_frm_x, img_frm_y = x+_x, y+_y

            self._image_frame_rect.setRect(
                img_frm_x, img_frm_y, img_frm_w, img_frm_h
            )

            img_x, img_y, img_w, img_h = (
                img_frm_x+img_mrg, img_frm_y+img_mrg, img_frm_w-img_mrg*2, img_frm_h-img_mrg*2
            )

            self._image_draw_rect.setRect(
                img_x, img_y, img_w, img_h
            )

            prg_h = self._progress_h
            self._progress_draw_rect.setRect(
                img_x, img_y+img_h-prg_h, img_w, prg_h
            )

            txt_frm_w, txt_frm_h = self._text_frm_w, self._text_frm_h

            txt_frm_x, txt_frm_y = img_x+(img_w-txt_frm_w)/2, img_y+img_h-prg_h-txt_frm_h-spc
            self._text_draw_rect.setRect(
                txt_frm_x, txt_frm_y, txt_frm_w, txt_frm_h
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

    def _set_item_widget_(self, widget):
        self._item_widget = widget

    def _do_hover_move_(self, event):
        pos = event.pos()
        if self._item_widget is not None:
            if self._item_widget._check_frame_rect.contains(pos):
                self._item_widget._set_check_hovered_(True)
            else:
                self._item_widget._set_check_hovered_(False)

        if self._video_flag is True:
            if 0 <= pos.x() <= self.width():
                frame_index = int((float(pos.x())/self.width())*self._frame_index_maximum)
                frame_index = min(self._frame_index_maximum-1, frame_index)
                self._update_at_(frame_index)
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
        self._resolution = None

        self._image_margin = 4

        self._image_current = None
        self._pixmap_current = None
        self._image_cover = None
        self._pixmap_cover = None
        self._image_frame_rect = QtCore.QRect()
        self._image_draw_rect = QtCore.QRect()

        self._play_mode = self.PlayModes.Video

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

        self._text = '00:00:00:00'
        self._text_draw_rect = QtCore.QRect()
        self._text_frame_draw_rect = QtCore.QRect()
        self._text_frm_h = 20
        self._text_frm_w = 96
        self._text_font = _qt_core.QtFont.generate(size=10)
        self._text_color = _gui_core.GuiRgba.DarkWhite
        self._text_frame_color = _gui_core.GuiRgba.Basic
        self._text_option = QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter

        self._image_cache_dict = {}
        self._pixmap_cache_dict = {}

        self._image_paths = []

        self._item_widget = None

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
                    self._pixmap_current = self._pixmap_cache_dict[self._frame_index]
                else:
                    if self._image_current is not None:
                        pixmap = QtGui.QPixmap.fromImage(self._image_current, QtCore.Qt.AutoColor)
                        self._pixmap_current = pixmap.scaled(
                            self._image_draw_rect.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
                        )
                        self._pixmap_cache_dict[self._frame_index] = self._pixmap_current

                if self._pixmap_current is not None:
                    painter.drawPixmap(
                        self._image_draw_rect,
                        self._pixmap_current
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
                        _gui_core.GuiRgba.LightAzureBlue
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

            if self._item_widget is not None:
                self._item_widget._draw_index_(painter)
                self._item_widget._draw_check_(painter)

    def _do_play_(self):
        if self._video_flag is True:
            self._is_playing = True
            self._wait_play_timer.stop()

            self._play_timer.start(self._frame_interval)

    def _next_frame_(self):
        if self._video_flag is True:
            if self._is_playing and self._frame_index < self._frame_index_maximum:
                self._update_at_(self._frame_index)
                self._frame_index += 1
            else:
                self._frame_index = 0

            self._refresh_widget_draw_()

    def _update_at_(self, frame_index):
        if self._video_flag is True:
            if self._play_mode == self.PlayModes.Video:
                if frame_index in self._image_cache_dict:
                    self._image_current = self._image_cache_dict[frame_index]
                    return

                data = self._video_capture_opt.get_data(frame_index)
                if data:
                    frame, width, height, channel = data
                    bytes_per_line = 3*width
                    img = QtGui.QImage(
                        frame.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888
                    )
                    self._image_cache_dict[frame_index] = img
                    self._image_current = img
            elif self._play_mode == self.PlayModes.ImageSequence:
                if frame_index in self._image_cache_dict:
                    self._image_current = self._image_cache_dict[frame_index]
                    return

                image_path = self._image_paths[frame_index]
                img = QtGui.QImage(image_path)
                self._image_cache_dict[frame_index] = img
                self._image_current = img

    def _setup_by_video_data_(self):
        def cache_fnc_():
            import lxbasic.cv.core as bsc_cv_core

            self._video_capture_opt = bsc_cv_core.VideoCaptureOpt(self._video_path)

            data = self._video_capture_opt.get_data(0)
            if data:
                frame, width, height, channel = data
                self._frame_index_maximum = self._video_capture_opt.get_frame_count()
                self._fps = self._video_capture_opt.get_fps_tag()
                self._frame_interval = int(1000/self._fps)
                return [frame, width, height, channel]

        def build_fnc_(data_):
            if self._close_flag is True:
                return

            if data_:
                frame, width, height, channel = data_
                self._video_flag = True

                self._resolution = width, height
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
        self._play_mode = self.PlayModes.Video
        self._setup_by_video_data_()
        
    def _setup_by_image_data_(self):
        if self._image_paths:
            image_path = self._image_paths[0]

            self._video_flag = True

            self._frame_index_maximum = len(self._image_paths)-1

            self._image_cover = QtGui.QImage(image_path)
            self._resolution = self._image_cover.width(), self._image_cover.height()

    def _set_images_(self, file_paths, fps):
        self._fps = fps
        self._image_paths = file_paths
        self._play_mode = self.PlayModes.ImageSequence
        self._setup_by_image_data_()
