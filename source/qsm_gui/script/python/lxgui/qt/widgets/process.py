# coding=utf-8
import sys

import functools

import six

import types

import subprocess

import platform

import threading

import os

import lxbasic.core as bsc_core

import lxbasic.log as bsc_log
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import core as gui_qt_core

from .. import abstracts as gui_qt_abstracts


class _Processing(object):
    # noinspection PyUnusedLocal
    def __init__(self, processing_bar):
        self.__maximum = 1
        self.__value = 0

        self.__is_running = False

        self.__is_killed = False

    def set_maximum(self, value):
        self.__maximum = int(value)

    def get_maximum(self):
        return self.__maximum

    def set_value(self, value):
        self.__value = int(value)

    def get_value(self):
        return self.__value

    def get_percent(self):
        return float(self.__value)/float(self.__maximum)

    def start(self, maximum):
        self.set_maximum(maximum)
        self.__is_running = True

    def stop(self):
        self.__is_running = False

    def kill(self):
        self.__is_killed = True
        self.stop()

    def get_is_killed(self):
        return self.__is_killed

    def get_is_running(self):
        return self.__is_running

    def get_is_finished(self):
        return self.__value == self.__maximum

    def get_status_rgba(self):
        return

    def update(self):
        if self.__is_running is True:
            self.__value += 1
            if self.__value == self.__maximum:
                self.stop()
            return True
        return False


class _SubProcess(object):
    KEY = 'sub process'

    if platform.system() == 'Linux':
        import pty
        M_PTY = pty
    else:
        M_PTY = None

    def __init__(self, thread, command, **kwargs):
        self.__trd = thread
        self.__cmd = command

        self.__is_killed = False

        self.__is_finished = False

        self.__exit_flag = threading.Event()

        self.__master_fd, self.__slave_fd = self.M_PTY.openpty()
        clear_environ = kwargs.get('clear_environ', False)
        if clear_environ == 'auto':
            clear_environ = bsc_core.PrcBaseMtd.check_command_clear_environ(self.__cmd)
        if clear_environ is True:
            self.__proc = subprocess.Popen(
                self.__cmd,
                shell=True,
                universal_newlines=True,
                stdout=self.__slave_fd,
                stderr=self.__slave_fd,
                env=dict()
            )
        else:
            self.__proc = subprocess.Popen(
                self.__cmd,
                shell=True,
                universal_newlines=True,
                stdout=self.__slave_fd,
                stderr=self.__slave_fd,
            )

    def __read_fd(self, process, thread, master_fd):
        while True:
            retcode = process.poll()
            if retcode is not None:
                bsc_log.Log.trace_method_result(
                    self.KEY, 'is killed, return code is {}'.format(retcode)
                )
                self.__exit_flag.set()
                break

            return_line = os.read(master_fd, 4096)

            return_line = return_line.decode('utf-8', 'ignore')
            return_line = return_line.replace(u'\u2018', "'").replace(u'\u2019', "'")
            return_line = return_line.encode('utf-8').rstrip()

            thread.filter_logging(return_line)
            sys.stdout.write(return_line+'\n')
            sys.stdout.flush()

    def run(self):
        t = threading.Thread(
            target=self.__read_fd, args=(self.__proc, self.__trd, self.__master_fd)
        )
        t.setDaemon(True)
        t.start()

        retcode = self.__proc.wait()
        if retcode:
            raise subprocess.CalledProcessError(retcode, self.__cmd)

        bsc_log.Log.trace_method_result(
            self.KEY, 'is finished, return code is {}'.format(retcode)
        )

    def kill(self):
        if self.__is_killed is False:
            if self.__proc.wait() is None:
                self.__is_killed = True
                self.__proc.terminate()
                self.__proc.wait()


class _QtProcessingThread(QtCore.QThread):
    started = qt_signal()
    finished = qt_signal()
    completed = qt_signal()
    killed = qt_signal()
    failed = qt_signal()

    KEY = 'thread processing'

    Status = gui_core.GuiStatus

    def __init__(self, *args, **kwargs):
        super(_QtProcessingThread, self).__init__(*args, **kwargs)
        self.__parent = self.parent()
        if not isinstance(self.__parent, QtProcessingBar):
            raise RuntimeError()

        self.__fnc = None
        self.__args = ()
        self.__kwargs = ()

        self.__sub_process = None

        self.update_status(self.Status.Waiting)

    def start_processing(self, maximum):
        self.__parent._start_processing_(maximum)

    def get_is_killed(self):
        return self.__parent._get_is_killed_()

    def update_processing(self):
        self.__parent._update_processing_()

    def update_logging(self, text):
        # noinspection PyUnresolvedReferences
        self.__parent.update_logging.emit(text)

    def filter_logging(self, text):
        process_start = bsc_log.Log.filter_process_start(text)
        if process_start:
            _count = process_start[-1]
            self.start_processing(_count)

        process = bsc_log.Log.filter_process(text)
        if process:
            self.update_processing()

        result = bsc_log.Log.filter_result(text)
        if result:
            self.update_logging(text)

    def update_status(self, status):
        # noinspection PyUnresolvedReferences
        self.__parent.update_status.emit(status)

    def set_fnc(self, fnc, *args, **kwargs):
        self.__fnc = fnc
        self.__args = args
        self.__kwargs = kwargs

    def kill(self):
        self.__parent._kill_processing_()

    def kill_sub_process(self):
        if self.__sub_process is not None:
            self.__sub_process.kill()
            self.__sub_process = None

    def run(self):
        self.update_logging(
            bsc_log.Log.get_method_result(
                self.KEY, 'is started'
            )
        )
        self.update_status(self.Status.Started)
        self.started.emit()
        # noinspection PyBroadException
        try:
            if isinstance(self.__fnc, (types.FunctionType, types.MethodType, functools.partial, types.LambdaType)):
                self.__fnc(
                    self,
                    *self.__args,
                    **self.__kwargs
                )
            elif isinstance(self.__fnc, six.string_types):
                self.__sub_process = _SubProcess(self, self.__fnc, clear_environ='auto')
                self.__sub_process.run()
                self.__sub_process = None
            else:
                raise RuntimeError()

            if self.get_is_killed() is True:
                self.update_logging(
                    bsc_log.Log.get_method_result(
                        self.KEY, 'is killed'
                    )
                )
                self.update_status(self.Status.Killed)
                self.killed.emit()
            else:
                self.update_logging(
                    bsc_log.Log.get_method_result(
                        self.KEY, 'is completed'
                    )
                )
                self.update_status(self.Status.Completed)
                self.completed.emit()
        except Exception:
            import traceback

            self.update_logging(
                bsc_log.Log.get_method_error(
                    self.KEY, 'is failed'
                )
            )
            self.update_logging(
                '*'*80
            )
            self.update_logging(traceback.format_exc())
            self.update_logging(
                '*'*80
            )
            self.update_status(self.Status.Failed)
            self.failed.emit()
        finally:
            self.finished.emit()


class QtProcessingBar(QtWidgets.QWidget):
    H = 20
    started = qt_signal()
    start_processing = qt_signal(int)
    update_processing = qt_signal()
    update_logging = qt_signal(str)
    update_status = qt_signal(int)

    Status = gui_core.GuiStatus
    Rgba = gui_core.GuiRgba

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()

        self.__rect_frame_draw.setRect(
            x, y, w-1, h-1
        )
        p_b_x, p_b_y = x+1, y+1
        p_b_w, p_b_h = w-2, h-2

        p_b_w_a = 10
        p_b_w_b = p_b_w-p_b_w_a

        if self.__is_finished is True:
            self.__processing_draw_rect.setRect(
                p_b_x, p_b_y, p_b_w, p_b_h
            )
            self.__draw_percent_text = '100%'
        else:
            index = min(self.__draw_step_index, 10)
            d = (self.__draw_percent-self.__draw_percent_pre)/2
            p_d = sum([(1.0/(2**i))*d for i in range(index)])
            self.__draw_percent_text = '%3d%%'%(int((self.__draw_percent_pre+p_d)*100))
            self.__processing_draw_rect.setRect(
                p_b_x, p_b_y, p_b_w_a+int(p_b_w_b*(self.__draw_percent_pre+p_d)), p_b_h
            )

        self.__text_draw_rect.setRect(
            x+2, y+2, w-4, h-4
        )

    def __init__(self, *args, **kwargs):
        super(QtProcessingBar, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.installEventFilter(self)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )

        self.__model = _Processing(self)

        self.__start_timestamp = None
        self.__finish_timestamp = None

        self.__rect_frame_draw = QtCore.QRect()
        self.__processing_draw_rect = QtCore.QRect()
        self.__text_draw_rect = QtCore.QRect()

        self.__status = self.Status.Waiting
        (
            self.__processing_draw_color, self.__processing_draw_color_hover
        ) = gui_qt_abstracts.AbsQtStatusBaseDef._get_rgba_args_by_status_(
            self.Status.Waiting
        )

        self.__process_timer = QtCore.QTimer(self)
        self.__process_timer.timeout.connect(self._refresh_processing_)

        self.__draw_percent_pre = 0
        self.__draw_percent = 0
        self.__draw_percent_text = '0%'
        self.__draw_time_text = '00:00:00'
        self.__draw_step_index = 0

        self.__is_finished = False

        self.__trd = None

        self.setFixedHeight(self.H)

        self.start_processing.connect(self._start_processing_fnc_)
        self.update_processing.connect(self._update_processing_fnc_)
        self.update_status.connect(self._update_status_fnc_)

    def _generate_thread_(self):
        self.__trd = _QtProcessingThread(self)
        self.__start_timestamp = bsc_core.SysBaseMtd.get_timestamp()
        self.__process_timer.start(100)
        return self.__trd

    def _get_cost_timestamp_(self):
        if self.__finish_timestamp is None:
            return bsc_core.SysBaseMtd.get_timestamp()-self.__start_timestamp
        return self.__finish_timestamp-self.__start_timestamp

    def _start_(self):
        pass

    def _start_processing_(self, maximum):
        self.start_processing.emit(maximum)

    def _start_processing_fnc_(self, maximum):
        self.__model.start(maximum)
        self._refresh_widget_all_()

    def _refresh_processing_(self):
        self.__draw_step_index += 1
        self._refresh_widget_all_()

    def _update_processing_(self):
        self.update_processing.emit()

    def _update_processing_fnc_(self):
        result = self.__model.update()
        self.__draw_percent_pre = self.__draw_percent
        self.__draw_percent = self.__model.get_percent()
        self.__draw_step_index = 0
        if result is True:
            self._refresh_widget_all_()

    def _kill_processing_(self):
        self.__process_timer.stop()

        self.update_status.emit(self.Status.Killed)

        if self.__trd is not None:
            self.__trd.kill_sub_process()
            self.__trd.wait()
            self.__trd.quit()
            self.__trd.deleteLater()
            self.__trd = None

    def _get_is_finished_(self):
        return self.__status in {
            self.Status.Completed, self.Status.Error, self.Status.Killed
        }

    def _update_status_fnc_(self, status):
        self.__status = status
        (
            self.__processing_draw_color, self.__processing_draw_color_hover
        ) = gui_qt_abstracts.AbsQtStatusBaseDef._get_rgba_args_by_status_(
            status
        )

        self.__is_finished = self._get_is_finished_()

        if self.__is_finished is True:
            self.__finish_timestamp = bsc_core.SysBaseMtd.get_timestamp()

        self._refresh_widget_draw_()

    def _get_is_killed_(self):
        return self.__status == self.Status.Killed

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
        return False

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)
        painter._draw_frame_by_rect_(
            rect=self.__rect_frame_draw,
            border_color=self.__processing_draw_color_hover,
            background_color=gui_qt_core.QtBackgroundColors.Dim,
        )

        painter._draw_alternating_colors_by_rect_(
            rect=self.__processing_draw_rect,
            colors=(self.__processing_draw_color, (127, 127, 127, 255)),
            running=not self.__is_finished
        )

        painter._draw_text_by_rect_(
            rect=self.__text_draw_rect,
            text=self.__draw_percent_text,
            font=gui_qt_core.GuiQtFont.generate(size=10, italic=True),
            font_color=gui_qt_core.QtFontColors.Light,
            text_option=QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter,
        )

        self.__draw_time_text = bsc_core.RawIntegerMtd.second_to_time_prettify(self._get_cost_timestamp_(), mode=1)

        painter._draw_text_by_rect_(
            rect=self.__text_draw_rect,
            text=self.__draw_time_text,
            font=gui_qt_core.GuiQtFont.generate(size=10, italic=True),
            font_color=gui_qt_core.QtFontColors.Light,
            text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
        )


if __name__ == '__main__':
    pass
