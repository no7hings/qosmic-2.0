# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from . import base as _base


class _PlayThread(QtCore.QThread):
    timeout = qt_signal()

    def __init__(self, parent):
        super(_PlayThread, self).__init__(parent)
        self._interval = 1000.0/24
        self._running = True
        self._close_flag = False

    def set_interval(self, interval):
        self._interval = interval

    def do_start(self):
        self._running = True
        if self._close_flag is False:
            self.start()

    def run(self):
        while self._running:
            # noinspection PyArgumentList
            QtCore.QThread.msleep(self._interval)
            self.timeout.emit()

    def do_stop(self):
        self._running = False

    def do_close(self):
        self._close_flag = True
        self.do_stop()
        self.wait()
        self.deleteLater()


class ListItemModel(_base.AbsItemModel):
    WAIT_PLAY_DELAY = 50
    
    def __init__(self, item):
        super(ListItemModel, self).__init__(
            item,
            _base._Data(
                size=QtCore.QSize(),
                rect=QtCore.QRect(),
                path=_base._Data(
                    text=''
                ),

                frame_color=QtGui.QColor(*_gui_core.GuiRgba.Dark),
                frame_brush=QtGui.QBrush(QtGui.QColor(*_gui_core.GuiRgba.Dim)),

                basic=_base._Data(
                    rect=QtCore.QRect(),
                    size=QtCore.QSize(),
                ),

                tool_tip_css=None,

                image_placeholder_svg=_gui_core.GuiIcon.get('placeholder/image'),
                # image
                image=_base._Data(
                    enable=False,
                    load_flag=False,

                    file=None,
                    pixmap=None,
                    size=None,
                ),
                # image sequence
                image_sequence=_base._Data(
                    enable=False,
                    load_flag=False,

                    play_flag=False,
                    auto_play_flag=False,
                    file=None,
                    files=[],
                    pixmap_dict={},
                    size=None,
                    index=0,
                    index_maximum=1,
                    point=QtCore.QPoint(),
                    fps=24,
                    time_text='00:00:00:00',
                    percent=0.0,
                    progress_color=QtGui.QColor(*_gui_core.GuiRgba.LightNeonGreen),
                    progress_color_auto_play=QtGui.QColor(*_gui_core.GuiRgba.LightAzureBlue),
                ),
                # show
                show=_base._Data(
                    load_flag=False,

                    cache_fnc=None,
                    build_fnc=None,
                ),
                menu=_base._Data(
                    content=None,
                    data=None,
                    data_generate_fnc=None
                ),

                property_dict=dict(),
                sort_dict=dict(),
            )
        )

        if not isinstance(self._item, QtWidgets.QListWidgetItem):
            raise RuntimeError()

        self._view = self._item.listWidget()

        self._pixmap_cache = QtGui.QPixmap()

        self._auto_play_thread = _PlayThread(self._view)
        self._auto_play_thread.timeout.connect(self._play_next)

        self._fps = 24
        self._frame_interval = int(1000/self._fps)
        self._auto_play_thread.set_interval(self._frame_interval)

        self._wait_play_timer = QtCore.QTimer(self._view)
        self._wait_play_timer.timeout.connect(self._start_play)

    def do_press_dbl_click(self, point):
        pass

    def do_hover_move(self, point):
        if self._data.image_sequence.enable is True:
            # rest play
            self._data.image_sequence.auto_play_flag = False
            self._auto_play_thread.do_stop()

            self._data.image_sequence.play_flag = True

            self._data.image_sequence.point.setX(point.x())
            self._update_sequence_image()

            self._wait_play_timer.start(self.WAIT_PLAY_DELAY)

    def do_close(self):
        self._auto_play_thread.do_close()

    def _start_play(self):
        self._wait_play_timer.stop()
        self._data.image_sequence.auto_play_flag = True
        self._auto_play_thread.do_start()

    def _play_next(self):
        if self._data.image_sequence.auto_play_flag is True:
            index = self._data.image_sequence.index
            index += 1
            if index > self._data.image_sequence.index_maximum:
                index = 0

            self._update_sequence_image_at(index)

    def _stop_play(self):
        self._update_sequence_image_at(0)
        self._data.image_sequence.play_flag=False
        self._wait_play_timer.stop()

        self._data.image_sequence.auto_play_flag = False
        self._auto_play_thread.do_stop()

    @property
    def view(self):
        return self._view

    def draw(self, painter, option, index):
        painter.save()

        self.update(option.rect)
        self._update_select(not not option.state & QtWidgets.QStyle.State_Selected)
        self._update_hover(not not option.state & QtWidgets.QStyle.State_MouseOver)

        self._update_show_auto()

        self.draw_background(painter, option, index)

        self._update_image_auto()
        self._update_image_sequence_auto()

        painter.drawPixmap(
            self._data.basic.rect, self.refresh_pixmap_cache()
        )

        self.draw_names(painter, option, index)

        painter.restore()

    def draw_background(self, painter, option, index):
        if self._data.select.flag:
            painter.setPen(self._data.select.color)
            painter.setBrush(self._data.select.color)
            painter.drawRect(self._data.select.rect)

        if self._data.hover.flag:
            painter.setPen(self._data.hover.color)
            painter.setBrush(self._data.hover.color)
            painter.drawRect(self._data.hover.rect)
        # draw check
        if self._data.check.enable is True:
            self._draw_icon(painter, self._data.check.rect, self._data.check.file)
        # draw icon
        if self._data.icon.enable is True:
            self._draw_icon(painter, self._data.icon.rect, self._data.icon.file)

    def draw_names(self, painter, option, index):
        # name
        if self._data.name.enable is True:
            self._draw_name(
                painter, self._data.name.rect, self._data.name.text,
                [self._data.name.color, self._data.name.hover_color][self._data.select.flag or self._data.hover.flag]
            )

    def refresh_pixmap_cache(self):
        rect = self._data.basic.rect
        # check size change
        if rect.size() != self._data.basic.size or self._data.force_refresh_flag is True:

            self._data.basic.size = rect.size()

            self._pixmap_cache = QtGui.QPixmap(self._data.basic.size)
            self._pixmap_cache.fill(QtGui.QColor(*_gui_core.GuiRgba.Dim))

            painter = QtGui.QPainter(self._pixmap_cache)
            rect = QtCore.QRect(0, 0, rect.width(), rect.height())

            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()

            bsc_w = bsc_h = w

            painter.setPen(self._data.frame_color)
            painter.setBrush(self._data.frame_brush)
            frm_x, frm_y, frm_w, frm_h = x+2, y+2, bsc_w-4, bsc_h-4
            frame_rect = QtCore.QRect(frm_x, frm_y, frm_w, frm_h)
            painter.drawRect(frame_rect)
            frame_rect_f = QtCore.QRectF(frm_x, frm_y, frm_w, frm_h)
            # image sequence for play, draw image sequence first
            if self._data.image_sequence.enable is True:
                img_w, img_h = self._data.image_sequence.size.width(), self._data.image_sequence.size.height()
                img_x_, img_y_, img_w_, img_h_ = bsc_core.RawSizeMtd.fit_to(
                    (img_w, img_h), (frm_w, frm_h)
                )
                img_rect = QtCore.QRect(frm_x+img_x_, frm_y+img_y_, img_w_, img_h_)
                self._draw_pixmap(painter, img_rect, self._data.image_sequence.pixmap)
                if self._data.image_sequence.play_flag is True:
                    time_txt = self._data.image_sequence.time_text
                    time_txt_w = self.compute_text_width_by(time_txt)
                    time_rect = QtCore.QRect(
                        frm_x+(frm_w-time_txt_w)/2, frm_y+frm_h-16, time_txt_w, 16
                    )
                    self._draw_time_text(painter, time_rect, time_txt)

                    progress_w = int(frm_w*self._data.image_sequence.percent)
                    progress_rect = QtCore.QRect(
                        frm_x, frm_y+frm_h-2, progress_w, 2
                    )
                    if self._data.image_sequence.auto_play_flag is True:
                        painter.setPen(self._data.image_sequence.progress_color_auto_play)
                        painter.setBrush(QtGui.QColor(self._data.image_sequence.progress_color_auto_play))
                    else:
                        painter.setPen(self._data.image_sequence.progress_color)
                        painter.setBrush(QtGui.QColor(self._data.image_sequence.progress_color))
                    painter.drawRect(progress_rect)
            # image
            elif self._data.image.enable is True:
                img_w, img_h = self._data.image.size.width(), self._data.image.size.height()
                img_x_, img_y_, img_w_, img_h_ = bsc_core.RawSizeMtd.fit_to(
                    (img_w, img_h), (frm_w, frm_h)
                )
                img_rect = QtCore.QRect(frm_x+img_x_, frm_y+img_y_, img_w_, img_h_)
                self._draw_pixmap(painter, img_rect, self._data.image.pixmap)
            else:
                self._draw_svg(painter, frame_rect_f, self._data.image_placeholder_svg)

            painter.end()

            self._data.force_refresh_flag = False
        return self._pixmap_cache

    def update(self, rect):
        # check rect is change
        if rect != self._data.rect:
            # need re instance
            self._data.rect = QtCore.QRect(rect)

            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()

            bsc_w = bsc_h = w

            self._data.basic.rect.setRect(
                x+2, y+2, bsc_w-3, bsc_h-3
            )

            self._data.select.rect.setRect(
                x+1, y+1, w-2, h-2
            )
            self._data.hover.rect.setRect(
                x+1, y+1, w-2, h-2
            )
            # check icon
            item_h = 20
            icn_w = 16
            cck_w = 0
            if self._data.check.enable is True:
                cck_w = 20
                self._data.check.rect.setRect(
                    x+(cck_w-icn_w)/2+1, y+h-item_h+(cck_w-icn_w)/2, icn_w, icn_w
                )
            # icon
            icn_w = 0
            if self._data.icon.enable is True:
                icn_w = 20
                self._data.icon.rect.setRect(
                    x+cck_w+(icn_w-icn_w)/2+1, y+h-item_h+(icn_w-icn_w)/2, icn_w, icn_w
                )
            # name
            self._data.name.rect.setRect(
                x+cck_w+icn_w+1, y+h-item_h, w-(cck_w+icn_w)-2, item_h
            )
            return True
        return False

    @classmethod
    def _draw_time_text(cls, painter, rect, text):
        painter.setPen(QtGui.QColor(223, 223, 223))
        painter.drawText(rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, text)

    @classmethod
    def _draw_name(cls, painter, rect, text, color):
        text = painter.fontMetrics().elidedText(
            text,
            QtCore.Qt.ElideMiddle,
            rect.width(),
            QtCore.Qt.TextShowMnemonic
        )
        painter.setPen(color)
        painter.drawText(rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, text)

    @classmethod
    def _draw_pixmap(cls, painter, rect, pixmap):
        pxm_scaled = pixmap.scaled(
            rect.size(),
            QtCore.Qt.IgnoreAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        painter.drawPixmap(rect, pxm_scaled)

    def set_image(self, file_path):
        self._data.image.file = file_path
        self._data.image.load_flag = True

    def _do_load_image(self):
        def cache_fnc_():
            _file_path = self._data.image.file
            _ = self._view._view_model.pull_image_cache(_file_path)
            if _:
                return _
            # fixme: when check is file cost lost of time
            # if os.path.isfile(_file_path):
            _image = QtGui.QImage()
            _image.load(_file_path)
            if _image.isNull() is False:
                _pixmap = QtGui.QPixmap.fromImage(_image, QtCore.Qt.AutoColor)
                _data = [[_file_path], _pixmap, _pixmap.size()]
                self._view._view_model.push_image_cache(_file_path, _data)
                return _data
            return []

        def build_fnc_(data_):
            if data_:
                _file_paths, _pixmap, _image_size = data_
                self._data.image.enable = True
                self._data.image.pixmap = _pixmap
                self._data.image.size = _image_size

                self.mark_force_refresh(True)
                self.update_view()

        trd = self._view._generate_thread_(
            cache_fnc_, build_fnc_
        )
        trd.start()

    def _update_image_auto(self):
        if self._data.image.load_flag is True:
            self._data.image.load_flag = False
            self._do_load_image()

    def set_image_sequence(self, file_path):
        self._data.image_sequence.file = file_path
        self._data.image_sequence.load_flag = True

    def _update_image_sequence_auto(self):
        if self._data.image_sequence.load_flag is True:
            self._data.image_sequence.load_flag = False
            self._do_load_image_sequence()

    def _do_load_image_sequence(self):
        def cache_fnc_():
            _file_path = self._data.image_sequence.file
            _ = self._view._view_model.pull_image_cache(_file_path)
            if _:
                return _

            _file_paths = bsc_storage.StgFileTiles.get_tiles(_file_path)
            if _file_paths:
                _image = QtGui.QImage()
                _image.load(_file_paths[0])
                if _image.isNull() is False:
                    _pixmap = QtGui.QPixmap.fromImage(_image, QtCore.Qt.AutoColor)
                    _data = [_file_paths, _pixmap, _pixmap.size()]
                    self._view._view_model.push_image_cache(_file_path, _data)
                    return _data
            return []

        def build_fnc_(data_):
            if data_:
                _file_paths, _pixmap, _image_size = data_
                self._data.image_sequence.enable = True
                self._data.image_sequence.pixmap = _pixmap
                self._data.image_sequence.size = _image_size
                self._data.image_sequence.files = _file_paths
                self._data.image_sequence.index_maximum = len(_file_paths)-1

                self.mark_force_refresh(True)
                self.update_view()

        trd = self._view._generate_thread_(
            cache_fnc_, build_fnc_
        )
        trd.start()

    def _update_sequence_image(self):
        x = self._data.image_sequence.point.x()
        x_offset = self._data.rect.x()
        w = self._data.basic.size.width()
        percent = float(x-x_offset)/float(w)
        index = int(self._data.image_sequence.index_maximum*percent)
        if index != self._data.image_sequence.index:
            self._update_sequence_image_at(index)

    def set_video(self, file_path):
        pass

    def update_view(self):
        # todo: use update() error in maya 2017?
        # noinspection PyBroadException
        try:
            self._view.update()
        except Exception:
            pass

    def _update_sequence_image_at(self, index):
        index = max(min(index, self._data.image_sequence.index_maximum), 0)
        percent = float(index)/float(self._data.image_sequence.index_maximum)
        self._data.image_sequence.index = index
        self._data.image_sequence.percent = percent
        self._data.image_sequence.time_text = bsc_core.BscInteger.frame_to_time_prettify(
            index,
            self._data.image_sequence.fps
        )
        if index in self._data.image_sequence.pixmap_dict:
            self._data.image_sequence.pixmap = self._data.image_sequence.pixmap_dict[index]
        else:
            file_path = self._data.image_sequence.files[index]
            image = QtGui.QImage()
            image.load(file_path)
            self._data.image_sequence.pixmap = QtGui.QPixmap.fromImage(image, QtCore.Qt.AutoColor)

            self.mark_force_refresh(True)
            self.update_view()

    def _update_hover(self, flag):
        if flag != self._data.hover.flag:
            self._data.hover.flag = flag
            if self._data.image_sequence.enable is True:
                self._data.image_sequence.play_flag = flag
                if flag is False:
                    self._stop_play()
                self.mark_force_refresh(True)

    def _update_show_auto(self):
        if self._data.show.load_flag is True:
            self._data.show.load_flag = False
            self._do_load_show_fnc()

    def _do_load_show_fnc(self):
        trd = self._view._generate_thread_(
            self._data.show.cache_fnc, self._data.show.build_fnc, post_fnc=self.refresh_force
        )
        trd.start()

    def set_show_fnc(self, cache_fnc, build_fnc):
        if cache_fnc is not None and build_fnc is not None:
            if self._data.show.cache_fnc is None and self._data.show.build_fnc is None:
                self._data.show.load_flag = True

                self._data.show.cache_fnc = cache_fnc
                self._data.show.build_fnc = build_fnc

    def refresh_force(self):
        self.mark_force_refresh(True)
        self.update_view()

    def set_property_dict(self, dict_):
        self._data.property_dict = dict_

    def get_property(self, key):
        return self._data.property_dict.get(key)
