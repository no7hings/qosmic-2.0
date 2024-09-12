# coding:utf-8
import six

import os

import lxbasic.core as bsc_core

import lxbasic.pinyin as bsc_pinyin

import lxbasic.storage as bsc_storage

from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from . import base as _base


class _Cache(object):
    def __init__(self):
        pass


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


class ItemModelForList(object):
    WAIT_PLAY_DELAY = 50

    def do_press_click(self, point):
        if self._data.check_rect_f.contains(point):
            self.swap_check()

    def do_press_dbl_click(self, point):
        pass

    def do_hover_move(self, point):
        if self._data.image_sequence.enable is True:
            # rest play
            self._data.image_sequence.play_flag = True
            self._data.image_sequence.auto_play_flag = False

            self._data.image_sequence.point.setX(point.x())
            self._update_sequence_image()

            self._wait_play_timer.start(self.WAIT_PLAY_DELAY)

    def do_close(self):
        self._play_thread.do_close()

    def _start_play(self):
        self._wait_play_timer.stop()
        self._data.image_sequence.auto_play_flag = True
        self._play_thread.do_start()

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
        self._data.image_sequence.auto_play_flag = False
        self._wait_play_timer.stop()
        self._play_thread.do_stop()

    def __init__(self, item):
        if not isinstance(item, QtWidgets.QListWidgetItem):
            raise RuntimeError()

        self._item = item
        self._view = self._item.listWidget()

        self._data = _base._Data(
            size=QtCore.QSize(),
            rect=QtCore.QRect(),
            index=0,
            name=_base._Data(
                text='',
                enable=False,
                rect=QtCore.QRect(),
            ),

            frame_color=QtGui.QColor(*_gui_core.GuiRgba.Dark),
            frame_brush=QtGui.QBrush(QtGui.QColor(*_gui_core.GuiRgba.Dim)),

            select_flag=False,
            select_rect=QtCore.QRect(),
            select_color=QtGui.QColor(*_gui_core.GuiRgba.LightAzureBlue),

            hover_flag=False,
            hover_rect=QtCore.QRect(),
            hover_color=QtGui.QColor(*_gui_core.GuiRgba.LightOrange),

            check_rect_f=QtCore.QRectF(),
            check_svg=_gui_core.GuiIcon.get('tag-filter-unchecked'),
            check_flag=False,

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
            keyword_filter=_base._Data(
                key_set=set()
            ),
            force_hidden_flag=False,
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

            refresh_force_flag=True
        )

        self._pixmap_cache = QtGui.QPixmap()

        self._font = _qt_core.QtFont.generate(size=8)
        self._font_metrics = QtGui.QFontMetrics(self._font)

        self._play_thread = _PlayThread(self._view)
        self._play_thread.timeout.connect(self._play_next)

        self._fps = 24
        self._frame_interval = int(1000/self._fps)
        self._play_thread.set_interval(self._frame_interval)

        self._wait_play_timer = QtCore.QTimer(self._view)
        self._wait_play_timer.timeout.connect(self._start_play)

    @property
    def data(self):
        return self._data

    @property
    def view(self):
        return self._view

    def draw(self, painter, option, rect):
        painter.drawPixmap(
            rect, self.refresh_pixmap_cache(rect)
        )

        select_flag = not not option.state & QtWidgets.QStyle.State_Selected
        hover_flag = not not option.state & QtWidgets.QStyle.State_MouseOver

        if select_flag:
            painter.setPen(self._data.select_color)
            painter.setBrush(QtCore.Qt.transparent)
            painter.drawRect(self._data.select_rect)

        if hover_flag:
            painter.setPen(self._data.hover_color)
            painter.setBrush(QtCore.Qt.transparent)
            painter.drawRect(self._data.hover_rect)

        self._update_play_by_hover(hover_flag)

        self._update_show_auto()

        self._update_image_auto()
        self._update_image_sequence_auto()

        # draw check
        if hover_flag or self._data.check_flag:
            self._draw_svg(painter, self._data.check_rect_f, self._data.check_svg)

        # name
        if self._data.name.enable is True:
            self._draw_name(painter, self._data.name.rect, self._data.name.text)

    def compute_text_width_by(self, text):
        return self._font_metrics.width(text)+16

    def refresh_pixmap_cache(self, rect, force=False):
        self.update(rect)
        # check size change
        refresh_force_flag = self._data.refresh_force_flag
        if rect.size() != self._data.size or force is True or refresh_force_flag is True:
            self._data.size = rect.size()

            self._pixmap_cache = QtGui.QPixmap(self._data.size)
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
                    self._draw_text(painter, time_rect, time_txt)

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

            self._data.refresh_force_flag = False
        return self._pixmap_cache

    def update(self, rect):
        # check rect is change
        if rect != self._data.rect:
            self._data.rect = rect

            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()

            bsc_w = bsc_h = w
            frm_x, frm_y, frm_w, frm_h = x+2, y+2, bsc_w-4, bsc_h-4
            self._data.select_rect.setRect(
                frm_x, frm_y, frm_w, frm_h
            )
            self._data.hover_rect.setRect(
                x+1, y+1, bsc_w-2, bsc_h-2
            )
            self._data.check_rect_f.setRect(
                x+4, y+4, 16, 16
            )
            self._data.name.rect.setRect(
                x, y+h-20, w, 20
            )
            return True
        return False

    def set_tool_tip(self, text):
        if text:
            self._data.tool_tip_css = _qt_core.QtUtil.generate_tool_tip_css(
                self._data.name.text, text
            )

    def set_checked(self, boolean):
        if boolean != self._data.check_flag:
            self._data.check_flag = boolean
            self._update_check()
            self._view.item_check_changed.emit()

    def _set_checked(self, boolean):
        if boolean != self._data.check_flag:
            self._data.check_flag = boolean
            self._update_check()

    def is_checked(self):
        return self._data.check_flag

    def is_visible(self):
        return not self._item.isHidden()

    def swap_check(self):
        self.set_checked(not self._data.check_flag)

    def _update_check(self):
        self._data.check_svg = [
            _gui_core.GuiIcon.get('tag-filter-unchecked'),
            _gui_core.GuiIcon.get('tag-filter-checked')
        ][self._data.check_flag]

        self._view.update()

    @classmethod
    def _draw_text(cls, painter, rect, text):
        painter.setPen(QtGui.QColor(223, 223, 223))
        painter.drawText(rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, text)

    @classmethod
    def _draw_name(cls, painter, rect, text):
        text = painter.fontMetrics().elidedText(
            text,
            QtCore.Qt.ElideMiddle,
            rect.width(),
            QtCore.Qt.TextShowMnemonic
        )
        painter.setPen(QtGui.QColor(223, 223, 223))
        painter.drawText(rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, text)

    @classmethod
    def _draw_svg(cls, painter, rect_f, svg_path):
        svg_render = QtSvg.QSvgRenderer(svg_path)
        svg_render.render(painter, rect_f)

    @classmethod
    def _draw_pixmap(cls, painter, rect, pixmap):
        pxm_scaled = pixmap.scaled(
            rect.size(),
            QtCore.Qt.IgnoreAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        painter.drawPixmap(rect, pxm_scaled)

    def set_name(self, text):
        if text:
            self._data.name.text = text
            self._data.name.enable = True

    def get_name(self):
        return self._data.name.text

    def set_index(self, index):
        self._data.index= index

    def mark_refresh_force_flag(self, boolean):
        self._data.refresh_force_flag = boolean

    def apply_keyword_filter_keys(self, texts):
        keys = []
        keys.extend(texts)
        for i_text in texts:
            i_texts = bsc_pinyin.Text.split_any_to_letters(i_text)
            keys.extend(i_texts)

        self._data.keyword_filter.key_set = set(keys)

    def get_keyword_filter_key_set(self):
        return self._data.keyword_filter.key_set

    def get_force_hidden_flag(self):
        return self._data.force_hidden_flag

    def get_keyword_filter_context(self):
        return '+'.join(self.get_keyword_filter_key_set())

    def generate_keyword_filter_args(self, key_src_set):
        # todo: use match all mode then, maybe use match one mode also
        if key_src_set:
            context = self.get_keyword_filter_context()
            context = context.lower()
            for i_text in key_src_set:
                # fixme: chinese word
                # do not encode, keyword can be use unicode
                i_text = i_text.lower()
                if '*' in i_text:
                    i_filter_key = six.u('*{}*').format(i_text.lstrip('*').rstrip('*'))
                    if not bsc_core.BscFnmatch.filter([context], i_filter_key):
                        return True, True
                else:
                    context = bsc_core.auto_unicode(context)
                    if i_text not in context:
                        return True, True
            return True, False
        return False, False

    def set_image(self, file_path):
        self._data.image.file = file_path
        self._data.image.load_flag = True

    def _do_load_image(self):
        def cache_fnc_():
            _file_path = self._data.image.file
            _ = self._view._view_model.pull_image_cache(_file_path)
            if _:
                return _

            if os.path.isfile(_file_path):
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

                self.mark_refresh_force_flag(True)
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

                self.mark_refresh_force_flag(True)
                self.update_view()

        trd = self._view._generate_thread_(
            cache_fnc_, build_fnc_
        )
        trd.start()

    def _update_sequence_image(self):
        x = self._data.image_sequence.point.x()
        x_offset = self._data.rect.x()
        w = self._data.size.width()
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

            self.mark_refresh_force_flag(True)
            self.update_view()

    def _update_play_by_hover(self, hover_flag):
        if hover_flag != self._data.hover_flag:
            self._data.hover_flag = hover_flag

            if self._data.image_sequence.enable is True:
                self._data.image_sequence.play_flag = hover_flag
                if hover_flag is False:
                    self._stop_play()

            self.mark_refresh_force_flag(True)
            self.update_view()

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
        self.mark_refresh_force_flag(True)
        # self.refresh_pixmap_cache(self._data.rect, True)
        self.update_view()
        
    def set_menu_content(self, content):
        self._data.menu.content = content
    
    def get_menu_content(self):
        return self._data.menu.content

    def set_menu_data(self, data):
        self._data.menu.data = data

    def get_menu_data(self):
        return self._data.menu.data
    
    def set_menu_data_generate_fnc(self, fnc):
        self._data.menu.data_generate_fnc = fnc

    def get_menu_data_generate_fnc(self):
        return self._data.menu.data_generate_fnc

    def set_property_dict(self, dict_):
        self._data.property_dict = dict_

    def get_property(self, key):
        return self._data.property_dict.get(key)

    def update_sort_dict(self, dict_):
        self._data.sort_dict.update(dict_)

    def update_sort(self, key):
        if key == 'index':
            index = self._data.index
            self._item.setText(
                str(index).zfill(4)
            )
            self.set_name(str(index))
        else:
            value = self._data.sort_dict.get(key, '')
            self._item.setText(
                self._data.sort_dict.get(key, '')
            )
            self.set_name(value)
