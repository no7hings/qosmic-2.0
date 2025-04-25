# coding:utf-8
import six

import lxbasic.core as bsc_core

import lxbasic.pinyin as bsc_pinyin

import lxbasic.storage as bsc_storage

from .... import core as _gui_core
# qt
from ....qt.core.wrap import *

from ....qt import core as _qt_core

from .. import item_base as _item_base


class _ImagePlayThread(QtCore.QThread):
    timeout = qt_signal()

    def __init__(self, parent):
        super(_ImagePlayThread, self).__init__(parent)
        self._interval = 1000.0/24

        self._running_flag = False
        self._close_flag = False

    def set_interval(self, interval):
        self._interval = interval

    def do_start(self):
        if self._close_flag is False:
            self._running_flag = True
            self.start()

    def run(self):
        while self._running_flag:
            # noinspection PyArgumentList
            QtCore.QThread.msleep(self._interval)
            self.timeout.emit()

    def do_stop(self):
        self._running_flag = False

    def do_close(self):
        self._close_flag = True
        self.do_stop()
        self.wait()
        self.deleteLater()


class _AudioPlayThread(QtCore.QThread):
    """
    thread for play, fix timer fps error
    """
    finished = qt_signal()
    progress_percent_changed = qt_signal(float)

    def __init__(self, parent, audio_segment):
        super(_AudioPlayThread, self).__init__(parent)
        self._audio_segment = audio_segment
        self._time_maximum = len(audio_segment)/1000.0

        self._interval = 1000.0/24
        self._start_time = 0
        self._start_percent = 0.0
        self._loop_flag = True

        self._running_flag = False
        self._close_flag = False

        self._progress_percent = 0.0

    def set_interval(self, interval):
        self._interval = interval

    def run(self):
        import pyaudio

        pa = pyaudio.PyAudio()

        stream = None
        while self._running_flag:
            segment_to_play = self._audio_segment[self._start_time:]

            stream = pa.open(
                format=pyaudio.paInt16,
                channels=segment_to_play.channels,
                rate=segment_to_play.frame_rate,
                output=True
            )

            samples = segment_to_play.get_array_of_samples()
            frame_count = len(samples)

            chunk_size = 1024
            for i in range(0, frame_count, chunk_size):
                if not self._running_flag:
                    break

                if six.PY2:
                    chunk = samples[i:i+chunk_size].tostring()
                else:
                    chunk = samples[i:i+chunk_size].tobytes()

                stream.write(chunk)

                if self._close_flag is False:
                    percent = (i+chunk_size)/float(frame_count)*(1-self._start_percent)+self._start_percent
                    percent = round(percent, 4)
                    if percent != self._progress_percent:
                        self._progress_percent = percent
                        self.progress_percent_changed.emit(self._progress_percent)

            # when loop is enable, restart from zero
            if self._loop_flag and self._running_flag:
                self._start_time = 0
                self._start_percent = 0.0
            else:
                break

        if stream is not None:
            stream.stop_stream()
            if not stream.is_stopped():
                stream.close()

        self.finished.emit()

    def do_start_from(self, percent):
        if self._close_flag is False:
            self._start_percent = percent
            self._start_time = int(self._time_maximum*percent*1000)
            self.do_start()

    def do_start(self):
        if self._close_flag is False:
            self._running_flag = True
            self.start()

    def do_stop(self):
        self._running_flag = False
        self._start_time = 0
        self._start_percent = 0.0
        self._progress_percent = 0.0

    def do_close(self):
        self._close_flag = True
        self.do_stop()
        self.wait()
        self.deleteLater()


class ListItemModel(_item_base.AbsItemModel):
    WAIT_PLAY_DELAY = 100

    def __init__(self, item):
        super(ListItemModel, self).__init__(
            item,
            _gui_core.DictOpt(
                # group
                group_enable=False,
                # image
                thumbnail_placeholder_svg=_gui_core.GuiIcon.get('placeholder/image'),
                image_enable=False,
                image=None,
                # image sequence, default use none
                image_sequence_enable=False,
                image_sequence=None,
                # video
                video_enable=False,
                video=None,
                # audio
                audio_enable=False,
                audio=None,
                # play
                play_enable=False,
                autoplay_enable=False,
            )
        )

        if not isinstance(self._item, QtWidgets.QListWidgetItem):
            raise RuntimeError()

        self._view = self._item.listWidget()

        self._pixmap_cache = QtGui.QPixmap()

    def _init_play(self):
        self._data.play_enable = True
        self._data.play = _gui_core.DictOpt(
            flag=False,

            point=QtCore.QPoint(),
            fps=24,
            # only image sequence show frame
            time_index_text='00:00:00:00',
            time_maximum_text='00:00:00:00',
            # progress
            progress_enable=False,
            progress_percent=0.0,
            progress_color=QtGui.QColor(*_gui_core.GuiRgba.LightOrange),
            progress_color_auto_play=QtGui.QColor(*_gui_core.GuiRgba.LightAzureBlue),

            file=_gui_core.GuiIcon.get('play-watermark'),
        )

    def _init_autoplay(self, fps):
        self._data.autoplay_enable = True

        play_thread = _ImagePlayThread(self._view)
        play_thread.timeout.connect(self._on_autoplaying)
        frame_interval = int(1000/fps)
        play_thread.set_interval(frame_interval)

        wait_timer = QtCore.QTimer(self._view)
        wait_timer.timeout.connect(self._start_autoplay)

        self._data.autoplay = _gui_core.DictOpt(
            flag=False,
            play_thread=play_thread,
            wait_timer=wait_timer,

            frame_interval=frame_interval,
        )

    def do_press_click(self, point):
        super(ListItemModel, self).do_press_click(point)

        if self._data.basic.rect.contains(point):
            if _qt_core.QtApplication.is_ctrl_modifier():
                if self._data.audio_enable is True:
                    if self._data.audio.autoplay_flag is True:
                        percent = self._data.play.progress_percent
                        # close pre and create new thread to play from percent
                        self._data.audio.play_thread.do_close()
                        self._data.audio.play_thread = _AudioPlayThread(
                            self._view, self._data.audio.play_thread._audio_segment
                        )
                        self._data.audio.play_thread.progress_percent_changed.connect(
                            self._update_audio_play_progress_percent
                        )
                        self._data.audio.play_thread.do_start_from(percent)

    def do_hover_move(self, point):
        # hover play
        if self._data.basic.rect.contains(point):
            if self._data.play_enable is True:
                self._data.play.flag = True

                self._data.play.point.setX(point.x())
                # update video or image sequence frame
                if self._data.video_enable is True:
                    self._update_video_by_hover_move()
                elif self._data.image_sequence_enable is True:
                    self._update_sequence_image_by_hover_move()
                elif self._data.audio_enable is True:
                    self._update_audio_by_hover_move()

                if self._data.autoplay_enable is True:
                    # rest autoplay
                    self._data.autoplay.flag = False
                    # stop first
                    self._data.autoplay.play_thread.do_stop()
                    # wait to autoplay when ctrl modifier is disabled
                    if _qt_core.QtApplication.is_ctrl_modifier() is False:
                        self._data.autoplay.wait_timer.start(self.WAIT_PLAY_DELAY)
            # audio
            if self._data.audio_enable is True:
                self._start_audio_autoplay()
        else:
            self._stop_any_play()

    def do_close(self):
        self._close_flag = True

        if self._data.autoplay_enable is True:
            self._data.autoplay.play_thread.do_close()

        if self._data.audio_enable is True:
            self._data.audio.play_thread.do_close()

    # play
    def _start_autoplay(self):
        if self._data.autoplay_enable is True:
            # stop wait
            self._data.autoplay.wait_timer.stop()
            self._data.autoplay.flag = True
            # autoplay
            self._data.autoplay.play_thread.do_start()

    def _start_audio_autoplay(self):
        if self._data.audio.autoplay_flag is False:
            self._data.audio.autoplay_flag = True

            self._update_audio_play_progress_percent(0.0)
            self._data.audio.play_thread.do_start()

    def _on_autoplaying(self):
        if self._data.play_enable is True:
            if self._data.autoplay_enable is True:
                if self._data.autoplay.flag is True:
                    if self._data.video_enable is True:
                        # make frame cycle
                        index = self._data.video.index
                        index += 1
                        if index > self._data.video.index_maximum:
                            index = 0

                        self._update_video_image_at(index)
                    elif self._data.image_sequence_enable is True:
                        # make frame cycle
                        index = self._data.image_sequence.index
                        index += 1
                        if index > self._data.image_sequence.index_maximum:
                            index = 0
                        self._update_sequence_image_frame_at(index)

    def _stop_any_play(self):
        if self._data.play_enable is True:
            # reset image to first frame
            if self._data.video_enable is True:
                self._update_video_image_at(
                    self._data.video.index_default
                )
            elif self._data.image_sequence_enable is True:
                self._update_sequence_image_frame_at(
                    self._data.image_sequence.index_default
                )
            # hover play
            self._data.play.flag = False
            # auto play
            if self._data.autoplay_enable is True:
                self._data.autoplay.wait_timer.stop()
                self._data.autoplay.flag = False
                self._data.autoplay.play_thread.do_stop()
        # audio
        if self._data.audio_enable is True:
            self._data.audio.autoplay_flag = False
            self._update_audio_play_progress_percent(0.0)
            self._data.audio.play_thread.do_stop()

    @property
    def view(self):
        return self._view

    def draw(self, painter, option, index):
        # save painter first
        painter.save()

        self.update(option.rect)

        self._update_select(not not option.state & QtWidgets.QStyle.State_Selected)
        self._update_hover(not not option.state & QtWidgets.QStyle.State_MouseOver)

        self._update_show_auto()

        self.draw_base(painter, option, index)

        self._load_image_auto()
        self._load_image_sequence_auto()
        self._load_video_auto()
        self._load_audio_auto()

        painter.drawPixmap(
            self._data.basic.rect, self.refresh_pixmap_cache()
        )

        self.draw_texts(painter, option, index)

        self.draw_status(painter, option, index)
        self.draw_lock(painter, option, index)

        painter.restore()

    def draw_base(self, painter, option, index):
        condition = (self._data.hover.flag, self._data.select.flag)
        # hover
        if condition == (True, False):
            painter.setPen(self._data.hover.color)
            painter.setBrush(self._data.hover.color)
            painter.drawRect(self._data.hover.rect)
        # select
        elif condition == (False, True):
            painter.setPen(self._data.select.color)
            painter.setBrush(self._data.select.color)
            painter.drawRect(self._data.select.rect)
        elif condition == (True, True):
            rect = self._data.select.rect
            color = QtGui.QLinearGradient(
                rect.topLeft(), rect.topRight()
            )
            color.setColorAt(
                0, self._data.hover.color
            )
            color.setColorAt(
                1, self._data.select.color
            )
            painter.setPen(QtGui.QPen(QtGui.QBrush(color), 1))
            painter.setBrush(color)
            painter.drawRect(rect)

        # draw check
        if self._data.check_enable is True:
            _qt_core.QtItemDrawBase._draw_icon_by_file(
                painter, self._data.check.rect, self._data.check.file
            )

        # draw icon
        if self._data.icon_enable is True:

            # file icon
            if self._data.icon.file_flag is True:
                _qt_core.QtItemDrawBase._draw_icon_by_file(
                    painter, self._data.icon.rect, self._data.icon.file
                )

            # text icon
            elif self._data.icon.text_flag is True:
                _qt_core.QtItemDrawBase._draw_icon_by_text(
                    painter, self._data.icon.rect, self._data.icon.text
                )

            # image
            elif self._data.icon.image_flag is True:
                _qt_core.QtItemDrawBase._draw_image(
                    painter, self._data.icon.rect, self._data.icon.image
                )

    def draw_lock(self, painter, option, index):
        if self._data.lock_enable is True:
            if self._data.lock.flag is True:
                self._draw_icon_by_file(painter, self._data.lock.rect, self._data.lock.file)

    def draw_status(self, painter, option, index):
        if self._data.status_enable is True:
            status_color = self._get_status_color()
            if status_color is not None:
                rect = self._data.basic.rect
                self._draw_status_frame(painter, rect, status_color)

    def draw_texts(self, painter, option, index):
        # name
        if self._data.name_enable is True:
            status_color = self._get_status_color()
            if status_color is not None:
                text_color = status_color
            else:
                text_color = [
                    self._data.text.color, self._data.text.action_color
                ][self._data.select.flag or self._data.hover.flag]

            _qt_core.QtItemDrawBase._draw_name_text(
                painter, self._data.name.rect, self._data.name.text,
                text_color, self._data.name.text_option, self._data.text.font
            )

        # subname
        if self._data.subname_enable is True:
            text_color = [
                self._data.text.color, self._data.text.action_color
            ][self._data.select.flag or self._data.hover.flag]
            _qt_core.QtItemDrawBase._draw_name_text(
                painter, self._data.subname.rect, self._data.subname.text,
                text_color, self._data.subname.text_option, self._data.text.font
            )

        # mtime
        if self._data.mtime_enable is True:
            _qt_core.QtItemDrawBase._draw_name_text(
                painter, self._data.mtime.rect, self._data.mtime.text,
                self._data.mtime.text_color, self._data.mtime.text_option, self._data.text.font
            )

        # user
        if self._data.user_enable is True:
            _qt_core.QtItemDrawBase._draw_name_text(
                painter, self._data.user.rect, self._data.user.text,
                self._data.user.text_color, self._data.user.text_option, self._data.text.font
            )

    def refresh_pixmap_cache(self):
        """
        refresh pixmap cache for painter, when size is changing or "force_refresh_flag" is True
        """
        rect = self._data.basic.rect
        # check size change
        if rect.size() != self._data.basic.size or self._data.force_refresh_flag is True:
            self._data.basic.size = rect.size()

            self._pixmap_cache = QtGui.QPixmap(self._data.basic.size)
            self._pixmap_cache.fill(QtGui.QColor(*_gui_core.GuiRgba.Dim))

            painter = QtGui.QPainter(self._pixmap_cache)
            rect = qt_rect(0, 0, rect.width(), rect.height())

            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
            bsc_w, bsc_h = w, h

            frm_x, frm_y, frm_w, frm_h = x+2, y+2, bsc_w-4, bsc_h-4
            frame_rect = qt_rect(frm_x, frm_y, frm_w, frm_h)
            # basic frame
            painter.setPen(QtGui.QColor(0, 0, 0, 0))
            painter.setBrush(self._data.frame.brush)
            painter.drawRect(frame_rect)
            # video for play
            if self._data.video_enable is True:
                img_w, img_h = self._data.video.size.width(), self._data.video.size.height()
                img_x_, img_y_, img_w_, img_h_ = bsc_core.BscSize.fit_to_center(
                    (img_w, img_h), (frm_w, frm_h)
                )
                # draw base frame
                self._draw_rect(painter, frame_rect, QtGui.QColor(0, 0, 0))
                # draw video image
                video_rect = qt_rect(frm_x+img_x_, frm_y+img_y_, img_w_, img_h_)
                image_data = self._data.video.image_data
                if image_data:
                    image = self._data.video.capture_opt.to_qt_image(QtGui.QImage, image_data)
                    pixmap = QtGui.QPixmap.fromImage(image, QtCore.Qt.AutoColor)
                    self._draw_pixmap(painter, video_rect, pixmap)
            # audio
            elif self._data.audio_enable is True:
                # fill to frame rect
                img_rect = qt_rect(frm_x, frm_y, frm_w, frm_h)
                self._draw_pixmap(painter, img_rect, self._data.audio.pixmap)
                # draw frame
                painter.setPen(self._data.frame.color)
                painter.setBrush(QtGui.QColor(0, 0, 0, 0))
                painter.drawRect(img_rect)
                # draw progress and handle
                if self._data.audio.autoplay_flag is True:
                    progress_w = frm_w*self._data.audio.progress_percent
                    self._data.audio.progress_rect.setRect(
                        frm_x, frm_y, progress_w, frm_h
                    )
                    painter.setPen(self._data.audio.progress_color)
                    painter.setBrush(self._data.audio.progress_color)
                    painter.drawRect(self._data.audio.progress_rect)
                # dra handle
                if self._data.play_enable is True:
                    if self._data.play.flag is True:
                        percent = self._data.play.progress_percent
                        hdl_x = frm_x+int(frm_w*percent)
                        self._data.audio.handle_line.setLine(
                            hdl_x, frm_y, hdl_x, frm_y+frm_h
                        )
                        painter.setPen(self._data.audio.handle_color)
                        painter.drawLine(self._data.audio.handle_line)
            # image sequence for play
            elif self._data.image_sequence_enable is True:
                img_w, img_h = self._data.image_sequence.size.width(), self._data.image_sequence.size.height()
                img_x_, img_y_, img_w_, img_h_ = bsc_core.BscSize.fit_to_center(
                    (img_w, img_h), (frm_w, frm_h)
                )
                # draw base frame
                self._draw_rect_0(painter, frame_rect, QtGui.QColor(0, 0, 0))
                # draw image
                img_rect = qt_rect(frm_x+img_x_, frm_y+img_y_, img_w_, img_h_)
                self._draw_pixmap(painter, img_rect, self._data.image_sequence.pixmap)
            # image
            elif self._data.image_enable is True:
                source_type = self._data.image.source_type
                if source_type == 'audio':
                    img_rect = qt_rect(frm_x, frm_y, frm_w, frm_h)
                    self._draw_pixmap(painter, img_rect, self._data.image.pixmap)
                    # draw frame
                    painter.setPen(self._data.frame.color)
                    painter.setBrush(QtGui.QColor(0, 0, 0, 0))
                    painter.drawRect(img_rect)
                else:
                    img_w, img_h = self._data.image.size.width(), self._data.image.size.height()
                    img_x_, img_y_, img_w_, img_h_ = bsc_core.BscSize.fit_to_center(
                        (img_w, img_h), (frm_w, frm_h)
                    )
                    img_rect = qt_rect(frm_x+img_x_, frm_y+img_y_, img_w_, img_h_)
                    self._draw_pixmap(painter, img_rect, self._data.image.pixmap)
            # placeholder
            else:
                img_w = img_h = min(frm_w, frm_h)
                img_x_, img_y_, img_w_, img_h_ = bsc_core.BscSize.fit_to_center(
                    (img_w, img_h), (frm_w, frm_h)
                )
                img_rect = QtCore.QRectF(frm_x+img_x_, frm_y+img_y_, img_w_, img_h_)
                # draw empty
                self._draw_svg(painter, img_rect, self._data.thumbnail_placeholder_svg)
            # about play
            if self._data.play_enable is True:
                # time and progress
                if (
                    self._data.video_enable is True
                    or self._data.audio_enable is True
                    or self._data.image_sequence_enable is True
                ):
                    if self._data.play.flag is True:
                        # time from index
                        time_txt = self._data.play.time_index_text
                        if self._data.play.progress_enable is True:
                            progress_w = int(frm_w*self._data.play.progress_percent)
                            progress_rect = qt_rect(
                                frm_x, frm_y+frm_h-2, progress_w, 2
                            )
                            if self._data.autoplay.flag is True:
                                painter.setPen(self._data.play.progress_color_auto_play)
                                painter.setBrush(QtGui.QColor(self._data.play.progress_color_auto_play))
                            else:
                                painter.setPen(self._data.play.progress_color)
                                painter.setBrush(QtGui.QColor(self._data.play.progress_color))
                            painter.drawRect(progress_rect)
                    else:
                        time_txt = self._data.play.time_maximum_text

                        play_s = min([40, frm_w/2, frm_h/2])
                        play_rect = qt_rect(
                            frm_x+(frm_w-play_s)/2, frm_y+(frm_h-play_s)/2, play_s, play_s
                        )
                        self._draw_icon_by_file(painter, play_rect, self._data.play.file)

                    mrg = 2

                    time_txt_w = self.compute_text_width_by(time_txt)
                    time_rect = qt_rect(
                        frm_x+frm_w-time_txt_w-mrg, frm_y+frm_h-16-mrg, time_txt_w, 16
                    )

                    painter.setPen(
                        QtGui.QColor(0, 0, 0, 0)
                    )
                    painter.setBrush(
                        QtGui.QBrush(QtGui.QColor(15, 15, 15, 127))
                    )
                    painter.drawRect(time_rect)

                    self._draw_time_text(painter, time_rect, time_txt)

            painter.end()

            self._data.force_refresh_flag = False
        return self._pixmap_cache

    def update(self, rect):
        # check rect is change
        if rect != self._data.rect:
            # need rebuild instance
            self._data.rect = qt_rect(rect)

            txt_h = self._data.text.height

            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()

            bsc_w_0, bsc_h_0 = w, h-txt_h

            bsc_x, bsc_y, bsc_w, bsc_h = x+2, y+2, bsc_w_0-3, bsc_h_0-3

            self._data.basic.rect.setRect(
                bsc_x, bsc_y, bsc_w, bsc_h
            )

            self._data.select.rect.setRect(
                x+1, y+1, w-2, h-2
            )
            self._data.hover.rect.setRect(
                x+1, y+1, w-2, h-2
            )
            # icon
            item_h = 20
            item_icon_w = 16

            txt_x, txt_y = x, y+bsc_h_0
            # lock
            if self._data.lock_enable is True:
                lck_w = lck_h = int(min(bsc_w, bsc_h)*.75)
                self._data.lock.rect.setRect(
                    bsc_x+(bsc_w-lck_w)/2, bsc_y+(bsc_h-lck_h)/2, lck_w, lck_h
                )
            cck_w = 0
            # check
            if self._data.check_enable is True:
                cck_w = 20
                self._data.check.rect.setRect(
                    txt_x+(cck_w-item_icon_w)/2+1, txt_y+(cck_w-item_icon_w)/2, item_icon_w, item_icon_w
                )
            # icon
            icn_w = 0
            if self._data.icon_enable is True:
                icn_w = 20
                self._data.icon.rect.setRect(
                    txt_x+cck_w+(icn_w-item_icon_w)/2+1, txt_y+(icn_w-item_icon_w)/2, item_icon_w, item_icon_w
                )
            # name
            txt_w_sub = cck_w+icn_w
            if txt_w_sub == 0:
                txt_offset = 2
            else:
                txt_offset = txt_w_sub+2

            self._data.name.rect.setRect(
                txt_x+txt_offset+1, txt_y, w-txt_w_sub-4, item_h
            )
            # mtime
            if self._data.mtime_enable is True:
                self._data.mtime.rect.setRect(
                    txt_x+txt_offset, txt_y+20, w-txt_w_sub-4, item_h
                )
            if self._data.user_enable is True:
                self._data.user.rect.setRect(
                    txt_x+txt_offset, txt_y+40, w-txt_w_sub-4, item_h
                )
            # status
            self._update_status_rect(rect)
            return True
        return False

    def _update_hover_play_percent(self):
        x = self._data.play.point.x()
        x_offset = self._data.rect.x()
        w = self._data.basic.size.width()
        percent = round(float(x-x_offset)/float(w), 2)
        if percent != self._data.play.progress_percent:
            self._data.play.progress_percent = percent
            return True, percent
        return False, percent

    # image
    def set_image(self, file_path, source_type=None, reload_cache=False):
        if file_path is not None:
            self._data.image = _gui_core.DictOpt(
                load_flag=False,
                reload_flag=reload_cache,

                file=None,
                pixmap=None,
                size=None,

                source_type=source_type
            )

            self._data.image_enable = False
            self._data.image.file = file_path
            self._data.image.load_flag = True

    def _load_image_auto(self):
        if self._data.image is not None:
            if self._data.image.load_flag is True:
                self._data.image.load_flag = False
                self._load_image()

    @_item_base.ItemThreadPoolFactor.push
    def _load_image(self):
        def cache_fnc_():
            _file_path = self._data.image.file

            if self._data.image.reload_flag is True:
                self._view._view_model.remove_image_cache(_file_path)

            _ = self._view._view_model.pull_image_cache(_file_path)
            if _:
                return _
            # fixme: when check is file cost lost of time
            # if os.path.isfile(_file_path):
            reader = QtGui.QImageReader(_file_path)
            _image = reader.read()
            if _image.isNull() is False:
                _pixmap = QtGui.QPixmap.fromImage(_image, QtCore.Qt.AutoColor)
                _cache = [_pixmap]
                self._view._view_model.push_image_cache(_file_path, _cache)
                return _cache
            return []

        def build_fnc_(data_):
            if self._view._view_model._close_flag is True:
                return

            if data_:
                _pixmap = data_[0]
                self._data.image_enable = True
                self._data.image.pixmap = _pixmap
                self._data.image.size = _pixmap.size()

                self.mark_force_refresh(True)
                self.update_view()

        return cache_fnc_, build_fnc_

    # image sequence
    def set_image_sequence(self, file_path, fps=24):
        if file_path is not None:
            self._data.image_sequence = _gui_core.DictOpt(
                load_flag=False,
                file=None,
                files=[],
                size=None,

                index=0,
                # in play is disable show image at default index
                index_default=0,
                index_maximum=1,

                fps=fps,

                pixmap_cache_dict={},
            )
            self._data.image_sequence.file = file_path
            self._data.image_sequence.load_flag = True

    def _load_image_sequence_auto(self):
        if self._data.image_sequence is not None:
            if self._data.image_sequence.load_flag is True:
                # mark to false for load once
                self._data.image_sequence.load_flag = False
                self._load_image_sequence()

    @_item_base.ItemThreadPoolFactor.push
    def _load_image_sequence(self):
        def cache_fnc_():
            _file_path = self._data.image_sequence.file
            _ = self._view._view_model.pull_image_sequence_cache(_file_path)
            if _:
                return _

            _file_paths = bsc_storage.StgFileTiles.get_tiles(_file_path)
            if _file_paths:
                _image = QtGui.QImage()
                _index = int(len(_file_paths)/2)
                _image.load(_file_paths[_index])
                if _image.isNull() is False:
                    _pixmap = QtGui.QPixmap.fromImage(_image, QtCore.Qt.AutoColor)
                    _cache = [_file_paths, _pixmap]
                    self._view._view_model.push_image_sequence_cache(_file_path, _cache)
                    return _cache
            return []

        def build_fnc_(data_):
            if self._view._view_model._close_flag is True:
                return

            if data_:
                _file_paths, _pixmap = data_
                self._data.image_sequence_enable = True
                self._data.image_sequence.pixmap = _pixmap
                self._data.image_sequence.size = _pixmap.size()
                self._data.image_sequence.files = _file_paths

                _frame_count = len(_file_paths)
                _fps = self._data.image_sequence.fps
                self._data.image_sequence.index_default = int(_frame_count/2)
                self._data.image_sequence.index_maximum = _frame_count-1

                self._init_play()
                self._init_autoplay(self._data.image_sequence.fps)

                self._data.play.progress_enable = True

                self._data.play.time_maximum_text = bsc_core.BscInteger.frame_to_time_prettify(
                    len(_file_paths),
                    _fps
                )

                self.mark_force_refresh(True)
                self.update_view()

        return cache_fnc_, build_fnc_

    def _update_sequence_image_by_hover_move(self):
        flag, percent = self._update_hover_play_percent()
        if flag is True:
            index = int(self._data.image_sequence.index_maximum*percent)
            if index != self._data.image_sequence.index:
                self._update_sequence_image_frame_at(index)
                self._data.image_sequence.index = index

    def _update_sequence_image_frame_at(self, index):
        index = max(min(index, self._data.image_sequence.index_maximum), 0)
        self._data.image_sequence.index = index
        # update percent by index changing
        percent = float(index)/float(self._data.image_sequence.index_maximum)
        self._data.play.progress_percent = percent

        self._data.play.time_index_text = bsc_core.BscInteger.frame_to_time_prettify(
            index+1,
            self._data.image_sequence.fps
        )
        # cache pixmap
        if index in self._data.image_sequence.pixmap_cache_dict:
            self._data.image_sequence.pixmap = self._data.image_sequence.pixmap_cache_dict[index]
        else:
            file_path = self._data.image_sequence.files[index]
            image = QtGui.QImage()
            image.load(file_path)
            pixmap = QtGui.QPixmap.fromImage(image, QtCore.Qt.AutoColor)
            self._data.image_sequence.pixmap = pixmap
            self._data.image_sequence.pixmap_cache_dict[index] = pixmap

        self.mark_force_refresh(True)
        self.update_view()

    # video
    def set_video(self, file_path):
        if file_path is not None:
            self._data.video = _gui_core.DictOpt(
                load_flag=False,
                file=None,
                capture_opt=None,
                size=None,
                index=0,
                # in play is disable show image at default index
                index_default=0,
                index_maximum=1,
                fps=24,

                image_data_dict={},
                image_data=None,
                pixmap_cache_dict={},
                pixmap=None,
            )
            self._data.video.file = file_path
            self._data.video.load_flag = True

    def _load_video_auto(self):
        if self._data.video is not None:
            if self._data.video.load_flag is True:
                # mark to false for load once
                self._data.video.load_flag = False
                self._load_video()

    @_item_base.ItemThreadPoolFactor.push
    def _load_video(self):
        def cache_fnc_():
            _file_path = self._data.video.file
            _ = self._view._view_model.pull_video_cache(_file_path)
            if _:
                return _

            import lxbasic.cv.core as bsc_cv_core

            _capture_opt = bsc_cv_core.VideoCaptureOpt(_file_path)
            # catch first frame
            if _capture_opt.is_valid():
                _index_default = _capture_opt.get_middle_frame_index()
                _image_data = _capture_opt.get_data(_index_default)
                if _image_data:
                    _frame_count = _capture_opt.get_frame_count()
                    _fps = _capture_opt.get_frame_rate()
                    _size = _capture_opt.get_size()
                    _cache = [_capture_opt, _image_data, _frame_count, _fps, _size, _index_default]
                    self._view._view_model.push_video_cache(_file_path, _cache)
                    return _cache
            return []

        def build_fnc_(data_):
            if self._view._view_model._close_flag is True:
                return

            if data_:
                _capture_opt, _image_data, _frame_count, _fps, _size, _index_default = data_
                self._data.video_enable = True
                self._data.video.capture_opt = _capture_opt
                self._data.video.image_data = _image_data
                self._data.video.size = QtCore.QSize(*_size)
                self._data.video.index_default = _index_default
                self._data.video.index_maximum = _frame_count-1
                self._data.video.fps = _fps

                # ignore play when frame count is 1
                if _frame_count > 1:
                    self._init_play()
                    self._init_autoplay(_fps)

                    self._data.play.progress_enable = True

                    self._data.play.time_maximum_text = bsc_core.BscInteger.frame_to_time_prettify(
                        _frame_count,
                        _fps
                    )

                self.mark_force_refresh(True)
                self.update_view()

        return cache_fnc_, build_fnc_

    def _update_video_by_hover_move(self):
        flag, percent = self._update_hover_play_percent()
        if flag is True:
            index = int(self._data.video.index_maximum*percent)
            if index != self._data.video.index:
                self._update_video_image_at(index)
                self._data.video.index = index

    def _update_video_image_at(self, index, cache_flag=True):
        index = max(min(index, self._data.video.index_maximum), 0)
        self._data.video.index = index
        # update percent by index changing
        percent = float(index)/float(self._data.video.index_maximum)
        self._data.play.progress_percent = percent

        self._data.play.time_index_text = bsc_core.BscInteger.frame_to_time_prettify(
            index+1,
            self._data.video.fps
        )

        # cache pixmap
        if index in self._data.video.image_data_dict:
            self._data.video.image_data = self._data.video.image_data_dict[index]
        else:
            # do not create QImage here use image_data
            capture_opt = self._data.video.capture_opt
            image_data = capture_opt.get_data(index)
            if image_data:
                self._data.video.image_data = image_data

        self.mark_force_refresh(True)
        self.update_view()

    # audio
    def set_audio(self, file_path, thumbnail_path=None):
        if file_path is not None:
            self._data.audio = _gui_core.DictOpt(
                load_flag=False,
                file=None,
                thumbnail=thumbnail_path,
                capture_opt=None,
                size=None,

                time_microsecond=1,

                pixmap_cache_dict={},

                play_thread=None,

                progress_percent=0.0,
                progress_rect=qt_rect(),
                progress_color=QtGui.QColor(255, 255, 255, 31),

                handle_line=QtCore.QLine(),
                handle_color=QtGui.QColor(*_gui_core.GuiRgba.LightTorchRed),

                autoplay_flag=False,
            )
            self._data.audio.file = file_path
            self._data.audio.load_flag = True

    def _load_audio_auto(self):
        if self._data.audio is not None:
            if self._data.audio.load_flag is True:
                # mark to false for load once
                self._data.audio.load_flag = False
                self._load_audio()

    @_item_base.ItemThreadPoolFactor.push
    def _load_audio(self):
        def cache_fnc_():
            _file_path = self._data.audio.file
            _ = self._view._view_model.pull_audio_cache(_file_path)
            if _:
                return _

            import lxbasic.cv.core as bsc_cv_core

            _capture_opt = bsc_cv_core.AudioCaptureOpt(_file_path)
            # catch first frame
            if _capture_opt.is_valid():
                if self._data.audio.thumbnail is not None:
                    _image = QtGui.QImage()
                    _image.load(self._data.audio.thumbnail)
                else:
                    _image = _capture_opt.generate_at_image_from_cache(QtGui.QImage)
                _microsecond = _capture_opt.get_frame_count()
                _pixmap = QtGui.QPixmap.fromImage(_image, QtCore.Qt.AutoColor)
                _cache = [_capture_opt, _pixmap, _microsecond]
                self._view._view_model.push_audio_cache(_file_path, _cache)
                return _cache
            return []

        def build_fnc_(data_):
            if self._view._view_model._close_flag is True:
                return

            if data_:
                _capture_opt, _pixmap, _microsecond = data_
                self._data.audio_enable = True
                self._data.audio.capture_opt = _capture_opt
                self._data.audio.pixmap = _pixmap
                self._data.audio.size = _pixmap.size()
                self._data.audio.time_microsecond = _microsecond

                self._data.audio.play_thread = _AudioPlayThread(self._view, _capture_opt._audio_segment)
                self._data.audio.play_thread.progress_percent_changed.connect(
                    self._update_audio_play_progress_percent
                )

                self._init_play()

                self._data.play.time_maximum_text = bsc_core.BscInteger.millisecond_to_time_prettify(
                    _microsecond
                )

                self.mark_force_refresh(True)
                self.update_view()

        return cache_fnc_, build_fnc_

    def _update_audio_by_hover_move(self):
        flag, percent = self._update_hover_play_percent()

    def _update_audio_play_progress_percent(self, percent):
        self._data.audio.progress_percent = percent

        self._data.play.time_index_text = bsc_core.BscInteger.millisecond_to_time_prettify(
            int(percent*self._data.audio.time_microsecond),
        )

        self.mark_force_refresh(True)
        self.update_view()

    def update_view(self):
        # todo: use update() error in maya 2017?
        # noinspection PyBroadException
        try:
            self._view.update()
        except Exception:
            pass

    def _update_hover(self, flag):
        if flag != self._data.hover.flag:
            self._data.hover.flag = flag
            if (
                self._data.video_enable is True
                or self._data.audio_enable is True
                or self._data.image_sequence_enable is True
            ):
                # stop when mouse leave
                if flag is False:
                    self._stop_any_play()

                # refresh draw force final
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

    # name
    def _update_name(self, text):
        self._item.setText(text)

    # status
    def _update_status_rect(self, rect):
        if self._data.status_enable is True:
            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
            self._data.status.rect.setRect(
                x+2, y+2, 20, 20
            )

    # sort
    def _generate_current_sort_name_text(self):
        name_text = super(ListItemModel, self)._generate_current_sort_name_text()

        if self._data.group_enable is True:
            group_text = self._generate_group_name_for(self._data.group.key)
        else:
            group_text = ''

        if group_text:
            return '{}:{}'.format(group_text, name_text)
        return name_text

    # group
    def set_group_enable(self, boolean):
        self._data.group_enable = boolean
        if boolean is True:
            self._data.group = _gui_core.DictOpt(
                dict=dict(),
                key=None,
            )

    def set_group_dict(self, dict_):
        if self.data.group_enable is True:
            self._data.group.dict = dict_

    def _generate_current_group_name(self):
        if self._data.group_enable is True:
            return self._generate_group_name_for(self._data.group.key)

    def _generate_group_name_for(self, group_key):
        if group_key == self.GroupKey.Category:
            return self.get_category()
        if group_key == self.GroupKey.Type:
            return self.get_type()
        elif group_key == self.GroupKey.Name:
            return bsc_core.BscChrGroup().get_group(
                bsc_pinyin.Text.find_first_chr(self._data.name.text)
            )
        return self._data.group.dict.get(group_key)

    def apply_group_key(self, key):
        if self._data.group_enable is True:
            self._data.group.key = key
            self._item.setText(self._generate_current_sort_name_text())

    # select
    def focus_select(self):
        widget = self._item.listWidget()
        widget.scrollToItem(self._item, widget.PositionAtTop)
        widget.setCurrentItem(self._item)

    def do_delete(self):
        widget = self._item.listWidget()
        widget._view_model._remove_item(self.get_path())


class ListGroupItemModel(_item_base.AbsItemModel):

    def __init__(self, item):
        super(ListGroupItemModel, self).__init__(
            item,
            _gui_core.DictOpt(
                line=_gui_core.DictOpt(
                    color=_qt_core.QtRgba.Basic
                ),
                expand_enable=True,
                expand=_gui_core.DictOpt(
                    rect=qt_rect(),
                    file=_gui_core.GuiIcon.get('expand-open')
                )
            )
        )

    def update(self, rect):
        # check rect is change
        if rect != self._data.rect:
            # need rebuild instance
            self._data.rect = qt_rect(rect)

            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()

            bsc_x, bsc_y, bsc_w, bsc_h = x+2, y+2, w-3, h-3

            self._data.basic.rect.setRect(
                bsc_x, bsc_y, bsc_w, bsc_h
            )
            # icon
            item_h = 20
            item_icon_w = 16

            # expand
            epd_w = 0
            if self._data.expand_enable is True:
                epd_w = 20
                epd_icn_w = 12
                self._data.expand.rect.setRect(
                    x+(epd_w-epd_icn_w)/2+1, y+(epd_w-epd_icn_w)/2, epd_icn_w, epd_icn_w
                )
            # check
            cck_w = 0
            if self._data.check_enable is True:
                cck_w = 20
                self._data.check.rect.setRect(
                    x+(cck_w-item_icon_w)/2+1, y+(cck_w-item_icon_w)/2, item_icon_w, item_icon_w
                )

            # name
            txt_w_sub = epd_w+cck_w
            if txt_w_sub == 0:
                txt_offset = 2
            else:
                txt_offset = txt_w_sub

            name_w = self._font_metrics.width(self._data.name.text)+16
            self._data.name.rect.setRect(
                x+txt_offset+1, y, name_w, item_h
            )

    def draw(self, painter, option, index):
        self.update(option.rect)

        self.draw_base(painter, option, index)

        self.draw_texts(painter, option, index)

    def _update_name(self, text):
        self._item.setText(text)

    def draw_texts(self, painter, option, index):
        # name
        if self._data.name_enable is True:
            text_color = [
                self._data.text.color, self._data.text.action_color
            ][self._data.select.flag or self._data.hover.flag]
            self._draw_text(
                painter, self._data.name.rect, self._data.name.text,
                text_color
            )

    def draw_base(self, painter, option, index):
        line = QtCore.QLine(
            self._data.basic.rect.bottomLeft(), self._data.basic.rect.bottomRight()
        )
        painter.setPen(self._data.line.color)
        painter.drawLine(line)

        # draw expand
        if self._data.expand_enable is True:
            self._draw_icon_by_file(painter, self._data.expand.rect, self._data.expand.file)

    # sort
    def apply_sort_order(self, sort_order):
        if sort_order == self.SortOrder.Ascending:
            self._update_name(
                u'{}:'.format(
                    bsc_core.ensure_unicode(self._data.name.text)
                )
            )
        else:
            self._update_name(
                u'{}|'.format(
                    bsc_core.ensure_unicode(self._data.name.text)
                )
            )

    def do_delete(self):
        widget = self._item.listWidget()
        widget._view_model._remove_item(self.get_path())