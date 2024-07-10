# coding=utf-8
import lxbasic.core as bsc_core

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage
# gui
from ... import core as _gui_core
# qt
from ..core.wrap import *

from .. import core as _qt_core

from .. import abstracts as _qt_abstracts
# qt widgets
from ..widgets import button as _button


class _Progress(object):
    # noinspection PyUnusedLocal
    def __init__(self, processing_bar):
        self._maximum = None
        self._value = 0

        self._is_running = False

    def set_maximum(self, value):
        self._maximum = int(value)

    def get_maximum(self):
        return self._maximum

    def set_value(self, value):
        self._value = int(value)

    def get_value(self):
        return self._value

    def get_percent(self):
        return float(self._value)/float(self._maximum)

    def append_maximum(self, maximum):
        if self._maximum is None:
            self._maximum = int(maximum)
            self._is_running = True
        else:
            self._maximum += int(maximum)

    def stop(self):
        self._is_running = False

    def get_is_running(self):
        return self._is_running

    def get_is_finished(self):
        return self._value == self._maximum

    def get_status_rgba(self):
        return

    def update(self):
        if self._is_running is True:
            self._value += 1
            if self._value == self._maximum:
                pass
                # self.stop()
            return True
        return False


class QtProgressBarForSubprocess(QtWidgets.QWidget):
    H = 20
    started = qt_signal()
    completed = qt_signal()
    failed = qt_signal()
    finished = qt_signal()

    progress_started = qt_signal(int)
    progress_update = qt_signal(float)

    log_update = qt_signal(str)
    status_update = qt_signal(int)

    Status = _gui_core.GuiProcessStatus
    Rgba = _gui_core.GuiRgba

    @qt_slot(int)
    def _on_progress_started_(self, maximum):
        self._model.append_maximum(maximum)
        self._refresh_widget_all_()

    @qt_slot(float)
    def _on_progress_update_(self, percent):
        result = self._model.update()
        self._percent_pre = self._percent
        self._percent = self._model.get_percent()
        self._progress_index = 0
        if result is True:
            self._refresh_widget_all_()

    @qt_slot(int)
    def _on_status_update_(self, status):
        if self._finish_flag is True:
            return

        self._status = status
        
        if self._status == self.Status.Started:
            self._start_timestamp = bsc_core.BscSystem.get_timestamp()
        
        (
            self._processing_draw_color, self._processing_draw_color_hover
        ) = _qt_abstracts.AbsQtStatusBaseDef._get_rgba_args_by_status_(
            status
        )

        self._finish_flag = self._check_is_finished_()

        if self._finish_flag is True:
            self._do_stop_()
        else:
            self._refresh_widget_draw_()

    def _on_completed_(self):
        self.completed.emit()

    def _on_failed_(self, results):
        if results:
            file_path = bsc_log.LogBase.get_user_debug_file(
                'process', create=True
            )
            bsc_storage.StgFileOpt(
                file_path
            ).set_write(''.join(results))

        self.failed.emit()

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()

        btn_w, btn_h = 0, self.H

        self._frame_draw_rect.setRect(
            x+1, y+1, w-2-btn_w, h-2
        )
        prc_x, prc_y = x+2, y+2
        prc_w, prc_h = w-4-btn_w, h-4

        p_b_w_a = 10
        p_b_w_b = prc_w-p_b_w_a

        index = min(self._progress_index, 10)
        d = (self._percent-self._percent_pre)/2
        p_d = sum([(1.0/(2**i))*d for i in range(index)])
        if self._status == self.Status.Completed:
            self._percent_text = '100%'
            self._processing_draw_rect.setRect(
                prc_x, prc_y, prc_w, prc_h
            )
        else:
            self._percent_text = '%3d%%'%(int((self._percent_pre+p_d)*100))
            self._processing_draw_rect.setRect(
                prc_x, prc_y, p_b_w_a+int(p_b_w_b*(self._percent_pre+p_d)), prc_h
            )

        self._text_draw_rect.setRect(
            x+2, y+2, w-4-btn_w, h-4
        )

    def _do_progress_started_(self, maximum):
        self.progress_started.emit(maximum)

    def _do_progress_update_(self, percent):
        self.progress_update.emit(percent)

    def _do_stop_(self):
        self._update_timer.stop()
        self._finish_timestamp = bsc_core.BscSystem.get_timestamp()
        self._refresh_widget_all_()

    def _do_kill_(self):
        if self._kill_flag is False:
            self._kill_flag = True

            self._trd.do_kill()

    def _do_quit_(self):
        if self._finish_flag is False:
            self._finish_flag = True

            self._do_stop_()
            self.status_update.emit(self.Status.Killed)
            if self._trd is not None:
                self._trd.do_quit()

    def _do_close_(self):
        self._do_kill_()
        self._do_quit_()

    def __init__(self, *args, **kwargs):
        super(QtProgressBarForSubprocess, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(self.H)

        self._model = _Progress(self)

        self._start_timestamp = None
        self._finish_timestamp = None

        self._frame_draw_rect = QtCore.QRect()
        self._processing_draw_rect = QtCore.QRect()
        self._text_draw_rect = QtCore.QRect()

        self._status = self.Status.Waiting
        (
            self._processing_draw_color, self._processing_draw_color_hover
        ) = _qt_abstracts.AbsQtStatusBaseDef._get_rgba_args_by_status_(
            self.Status.Waiting
        )

        self._update_timer = QtCore.QTimer(self)
        self._update_timer.timeout.connect(self._refresh_processing_)
        
        self._text = None
        self._text_font = _qt_core.QtFont.generate(size=8)
        
        self._percent_pre = 0
        self._percent = 0
        self._percent_text = '0%'
        self._main_text = '00:00:00'

        self._percent_font = _qt_core.QtFont.generate(size=8)

        self._progress_index = 0

        self._kill_flag = False
        self._finish_flag = False

        self._trd = None

        self.progress_started.connect(self._on_progress_started_)
        self.progress_update.connect(self._on_progress_update_)
        self.status_update.connect(self._on_status_update_)

        self.installEventFilter(self)

    def _generate_thread_(self, widget):
        self._trd = _qt_core.QtThreadWorkerForSubprocess.generate(
            widget, self
        )
        self._update_timer.start(100)
        self._trd.failed.connect(self._on_failed_)
        self._trd.completed.connect(self._on_completed_)
        return self._trd

    def _get_cost_timestamp_(self):
        if self._start_timestamp is None:
            return 0
        if self._finish_timestamp is None:
            return bsc_core.BscSystem.get_timestamp()-self._start_timestamp
        return self._finish_timestamp-self._start_timestamp

    def _refresh_processing_(self):
        self._progress_index += 1
        self._refresh_widget_all_()

    def _check_is_finished_(self):
        return self._status in {
            self.Status.Completed,
            self.Status.Error,
            self.Status.Failed
        }

    def _get_is_killed_(self):
        return self._kill_flag

    def _set_text_(self, text):
        self._text = text
        self._main_text = self._generate_draw_text_()

    def _generate_draw_text_(self):
        if self._text:
            return '{} | {} | {}'.format(
                bsc_core.auto_string(self._text),
                bsc_core.RawIntegerMtd.second_to_time_prettify(self._get_cost_timestamp_(), mode=1),
                _gui_core.GuiProcessStatusMapper.MAPPER[self._status]

            )
        else:
            return bsc_core.RawIntegerMtd.second_to_time_prettify(self._get_cost_timestamp_(), mode=1)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        painter._draw_frame_by_rect_(
            rect=self._frame_draw_rect,
            border_color=self._processing_draw_color,
            background_color=_qt_core.QtBackgroundColors.Dim,
            border_radius=3
        )

        painter._draw_alternating_colors_by_rect_(
            rect=self._processing_draw_rect,
            colors=(self._processing_draw_color, (127, 127, 127, 255)),
            running=not self._finish_flag,
            border_radius=2
        )
        # percent
        painter._draw_text_by_rect_(
            rect=self._text_draw_rect,
            text=self._percent_text,
            font=self._percent_font,
            text_color=_qt_core.QtFontColors.Light,
            text_option=QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter,
        )

        # time
        self._main_text = self._generate_draw_text_()
        painter._draw_text_by_rect_(
            rect=self._text_draw_rect,
            text=self._main_text,
            font=self._text_font,
            text_color=_qt_core.QtFontColors.Light,
            text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
        )


if __name__ == '__main__':
    pass
