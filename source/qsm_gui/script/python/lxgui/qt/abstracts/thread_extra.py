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
            # image_path = 'Z:/temeporaries/dongchangbao/playblast_tool/test.export.v004.png'
            if os.path.isfile(image_path):
                ext = os.path.splitext(image_path)[-1]
                if ext in {'.jpg', '.png'}:
                    image = QtGui.QImage(image_path)
                    if image.isNull() is False:
                        s = image.size()
                        size = s.width(), s.height()
                        return [image, size]
        except Exception:
            import traceback
            traceback.print_stack()
            return []

    @classmethod
    def _get_data_from_video_(cls, video_path):
        # noinspection PyBroadException
        try:
            if os.path.isfile(video_path):
                ext = os.path.splitext(video_path)[-1]
                if ext in {'.mp4', '.mov', '.rmvb', '.mkv'}:
                    import lxbasic.media.core as bsc_mda_core
                    opt = bsc_mda_core.VideoCaptureOpt(video_path)
                    if opt.is_valid() is False:
                        return []
                    data = opt.get_data(0)
                    opt.release()
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

        self._image_size = None

        self._image = None
        self._pixmap = None

        self._video_flag = False
        self._video_auto_play_flag = False

        self._video_play_rect = QtCore.QRect()
        self._video_s = 24

        self._video_path = None

        self._svg_flag = False
        self._svg_path = None

    def _set_image_path_(self, file_path):
        self._image_flag = True

        self._image_path = file_path

        self._svg_flag = True
        self._svg_path = _gui_core.GuiIcon.get('placeholder/image')
        self._image_size = 64, 64

        self._load_image_data_use_thread_(self._image_path)

    def _load_image_data_use_thread_(self, image_path):
        def cache_fnc_():
            return self._get_data_from_image_(image_path)

        def build_fnc_(data_):
            if data_:
                self._image, self._image_size = data_
                self._svg_flag = False

            self._widget._refresh_widget_all_()

        t = _qt_core.QtBuildThread(self._widget)
        self._ts.append(t)
        t.set_cache_fnc(cache_fnc_)
        t.cache_value_accepted.connect(build_fnc_)
        t.start()
        # build_fnc_(cache_fnc_())

    def _set_video_path_(self, video_path, thumbnail_path=None):
        self._image_flag = True
        self._video_flag = True

        self._video_path = video_path

        self._svg_flag = True
        self._svg_path = _gui_core.GuiIcon.get('placeholder/video')
        self._image_size = 64, 64

        self._load_image_data_use_thread_(thumbnail_path)
        self._check_auto_play_flag_use_thread_(self._video_path)

    def _set_video_auto_play_flag_(self, boolean):
        self._video_auto_play_flag = boolean

    def _check_auto_play_flag_use_thread_(self, video_path):
        def cache_fnc_():
            import lxbasic.media.core as bsc_mda_core

            opt = bsc_mda_core.VideoCaptureOpt(video_path)
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
            # return self._get_data_from_video_(self._video_path)

        def build_fnc_(data_):
            if data_:
                self._image, self._image_size = data_
                self._svg_flag = False
                # self._video_auto_play_flag = True

            self._widget._refresh_widget_all_()

        # t = _qt_core.QtBuildThread(self._widget)
        # self._ts.append(t)
        # t.set_cache_fnc(cache_fnc_)
        # t.cache_value_accepted.connect(build_fnc_)
        #
        # t.start()
        build_fnc_(cache_fnc_())
