# coding=utf-8
import os
# gui
from ... import core as _gui_core
# qt
from ..core.wrap import *

from .. import core as _qt_core

from . import widget as _widget

from . import thread as _thread


class AbsQtMediaBaseDef(
    _thread.AbsQtThreadExtraDef,
    _widget.AbsQtWidgetCloseBaseDef,
):
    @classmethod
    def _get_data_from_image_(cls, image_path):
        # noinspection PyBroadException
        try:
            if os.path.isfile(image_path):
                image = QtGui.QImage(image_path)
                if image.isNull() is False:
                    s = image.size()
                    size = s.width(), s.height()
                    pixmap_new = QtGui.QPixmap.fromImage(image, QtCore.Qt.AutoColor)
                    return [pixmap_new, size]

        except Exception:
            import traceback
            traceback.print_stack()
            return []

    @classmethod
    def _get_data_from_video_(cls, video_path):
        # noinspection PyBroadException
        try:
            if os.path.isfile(video_path):
                import lxbasic.cv.core as bsc_cv_core
                with bsc_cv_core.VideoCaptureOpt(video_path) as opt:
                    if opt.is_valid() is False:
                        return []

                    data = opt.get_data(0)
                    if data:
                        frame, width, height, channel = data
                        bytes_per_line = 3*width
                        image = QtGui.QImage(
                            frame.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888
                        )
                        if image.isNull() is False:
                            s = image.size()
                            size = s.width(), s.height()
                            return [image, size]
        except Exception:
            return []

    def _init_media_base_def_(self, widget):
        self._init_thread_extra_def_(widget)
        self._init_widget_close_base_def_(widget)

        self._image_path = None

        self._image_flag = False
        self._image_draw_flag = False

        self._image_frame_rect = QtCore.QRect()
        self._image_draw_rect = QtCore.QRect()

        self._image_margin = 4

        self._image_size = 64, 64

        self._image = None
        self._image_pixmap = None
        self._image_pixmap_draw = None

        self._video_flag = False
        self._video_auto_play_flag = False

        self._video_play_rect = QtCore.QRect()
        self._video_play_s = 24
        self._video_path = None
        self._video_play_widget = None

        self._image_svg_path = _gui_core.GuiIcon.get('placeholder/image')

    def _set_image_path_(self, image_path):
        self._image_flag = True
        self._widget.update()

        if os.path.exists(image_path) is False:
            return

        self._image_path = image_path

        self._load_image_data_(self._image_path)

    def _load_image_data_(self, image_path):
        def cache_fnc_():
            return self._get_data_from_image_(image_path)

        def build_fnc_(data_):
            if data_:
                self._image_pixmap, self._image_size = data_
                self._image_draw_flag = True

            self._widget._refresh_widget_all_()

        t = _qt_core.QtBuildThread(self._widget)
        self._ts.append(t)
        t.set_cache_fnc(cache_fnc_)
        t.cache_value_accepted.connect(build_fnc_)
        t.start()
        # build_fnc_(cache_fnc_())

    def _set_video_path_(self, video_path):
        self._video_flag = True
        self._image_svg_path = _gui_core.GuiIcon.get('placeholder/video')

        if os.path.exists(video_path) is False:
            return

        self._video_path = video_path

        self._check_auto_play_flag_use_thread_(self._video_path)

    def _set_video_auto_play_flag_(self, boolean):
        self._video_auto_play_flag = boolean

    def _check_auto_play_flag_use_thread_(self, video_path):
        def cache_fnc_():
            import lxbasic.cv.core as bsc_cv_core
            opt = bsc_cv_core.VideoCaptureOpt(video_path)
            is_valid = opt.is_valid()
            opt.release()
            return [is_valid]

        def build_fnc_(data_):
            if data_:
                is_valid = data_[0]
                self._video_auto_play_flag = is_valid

            self._widget._refresh_widget_all_()

        # fixme: use thread maybe crash
        # t = _qt_core.QtBuildThread(self._widget)
        # self._ts.append(t)
        # t.set_cache_fnc(cache_fnc_)
        # t.cache_value_accepted.connect(build_fnc_)
        #
        # t.start()
        build_fnc_(cache_fnc_())

    def _load_video_data_use_thread_(self, thumbnail_path):
        def cache_fnc_():
            if thumbnail_path:
                return self._get_data_from_image_(thumbnail_path)

        def build_fnc_(data_):
            if data_:
                self._image_pixmap, self._image_size = data_
                self._image_draw_flag = True

            self._widget._refresh_widget_all_()

        # t = _qt_core.QtBuildThread(self._widget)
        # self._ts.append(t)
        # t.set_cache_fnc(cache_fnc_)
        # t.cache_value_accepted.connect(build_fnc_)
        #
        # t.start()
        build_fnc_(cache_fnc_())
