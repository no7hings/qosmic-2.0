# coding=utf-8
import functools

import lxbasic.core as bsc_core

import lxbasic.model as bsc_model

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage
# gui
from ... import core as _gui_core
# qt
from ..core.wrap import *

from .. import core as _qt_core

from .. import abstracts as _qt_abstracts

from . import utility as _utility


class QtChartForSprcTask(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtMenuBaseDef,
):
    H = 20
    started = qt_signal()
    finished = qt_signal()
    completed = qt_signal()
    failed = qt_signal()
    killed = qt_signal()
    
    profile_accepted = qt_signal(dict)

    progress_started = qt_signal(int)
    progress_update = qt_signal(float)

    log_update = qt_signal(str)
    status_update = qt_signal(int)

    Status = _gui_core.GuiProcessStatus
    Rgba = _gui_core.GuiRgba

    QT_MENU_CLS = _utility.QtMenu

    @qt_slot(int)
    def _on_progress_started_(self, maximum):
        self._data_model.append_maximum(maximum)
        self._refresh_widget_all_()

    @qt_slot(float)
    def _on_update_progress_(self, percent):
        result = self._data_model.update()
        self._percent_pre = self._percent
        self._percent = self._data_model.get_percent()
        self._progress_index = 0
        if result is True:
            self._refresh_widget_all_()

    @qt_slot(int)
    def _on_status_update_(self, status):
        if self._finish_flag is True:
            return

        self._status = status
        
        if self._status == self.Status.Started:
            self._start_timestamp = bsc_core.BscSystem.generate_timestamp()
        
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

    def _on_started_(self):
        self._profile.update_timestamp('started')
        if self._trd is not None:
            self._profile.update('tag', self._tag_text)
            self._profile.update('name', self._text)
            self._profile.update('command', self._trd.fnc_string)
        self.started.emit()

    def _on_finished_(self):
        self._profile.update_timestamp('finished')
        if self._trd is not None:
            self._profile.update('status', int(self._trd.status))
            if self._sprc_memory_sizes:
                memory_size = max(self._sprc_memory_sizes)
                self._profile.update('memory_size', memory_size)
                self._profile.update('memory_size_string', bsc_core.BscInteger.to_prettify_as_file_size(memory_size))
            self.profile_accepted.emit(self._profile.data)
        self.finished.emit()

    def _on_completed_(self):
        self.completed.emit()

    @qt_slot(list)
    def _on_failed_(self, results):
        def fnc_(file_path_):
            bsc_storage.StgPath.start_in_system(file_path_)

        if results:
            file_path = bsc_log.LogBase.get_user_debug_file(
                'process', create=True
            )
            bsc_storage.StgFileOpt(
                file_path
            ).set_write(''.join(results))

            self._set_menu_data_(
                [
                    ('Show Error', 'file/file', functools.partial(fnc_, file_path))
                ]
            )

        self.failed.emit()

    def _on_killed_(self):
        self.killed.emit()

    @qt_slot(dict)
    def _on_system_resource_usage_update_(self, data):
        memory_size = data['memory_size']
        self._sprc_memory_sizes.append(memory_size)

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

        p_b_w_a = 20
        p_b_w_b = prc_w-p_b_w_a

        index = min(self._progress_index, 10)
        d = (self._percent-self._percent_pre)/2
        p_d = sum([(1.0/(2**i))*d for i in range(index)])
        if self._status == self.Status.Completed:
            self._percent_text = '100%'
            self._progress_draw_rect.setRect(
                prc_x, prc_y, prc_w, prc_h
            )
        else:
            self._percent_text = '%3d%%' % (int((self._percent_pre+p_d)*100))
            self._progress_draw_rect.setRect(
                prc_x, prc_y, p_b_w_a+int(p_b_w_b*(self._percent_pre+p_d)), prc_h
            )

        percent_txt_w = QtGui.QFontMetrics(self._text_font).width(self._percent_text)+8

        self._main_text = self._generate_main_text_()
        txt_w = QtGui.QFontMetrics(self._text_font).width(self._main_text)+8
        txt_w = min(txt_w, w-percent_txt_w-8)
        self._main_text_draw_rect.setRect(
            x+2, y+3, txt_w, h-6
        )

        self._percent_text_draw_rect.setRect(
            w-percent_txt_w-2, y+3, percent_txt_w, h-6
        )

    def _do_progress_started_(self, maximum):
        self.progress_started.emit(maximum)

    def _do_progress_update_(self, percent):
        self.progress_update.emit(percent)

    def _do_stop_(self):
        self._update_timer.stop()

        self._finish_timestamp = bsc_core.BscSystem.generate_timestamp()
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
        super(QtChartForSprcTask, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(self.H)

        self._init_menu_base_def_(self)

        self._data_model = bsc_model.Progress(self)

        self._start_timestamp = None
        self._finish_timestamp = None
        self._cost_time = None
        
        self._timeout = None

        self._frame_draw_rect = qt_rect()
        self._progress_draw_rect = qt_rect()
        self._main_text_draw_rect = qt_rect()
        self._percent_text_draw_rect = qt_rect()

        self._status = self.Status.Waiting
        (
            self._processing_draw_color, self._processing_draw_color_hover
        ) = _qt_abstracts.AbsQtStatusBaseDef._get_rgba_args_by_status_(
            self.Status.Waiting
        )

        self._update_timer = QtCore.QTimer(self)
        self._update_timer.timeout.connect(self._refresh_on_time_)

        self._tag_text = None
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

        self._sprc_memory_sizes = []

        self.progress_started.connect(self._on_progress_started_)
        self.progress_update.connect(self._on_update_progress_)
        self.status_update.connect(self._on_status_update_)

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.RightButton:
                    self._popup_menu_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        painter._draw_frame_by_rect_(
            rect=self._frame_draw_rect,
            border_color=self._processing_draw_color,
            background_color=_gui_core.GuiRgba.LightBlack,
            border_radius=3
        )

        if self._finish_flag is True:
            painter._draw_frame_by_rect_(
                rect=self._progress_draw_rect,
                border_color=self._processing_draw_color,
                background_color=self._processing_draw_color,
                border_radius=2
            )
        else:
            painter._draw_alternating_colors_by_rect_(
                rect=self._progress_draw_rect,
                colors=(self._processing_draw_color, _gui_core.GuiRgba.Dim),
                running=not self._finish_flag,
                border_radius=2
            )

        painter._set_border_color_(QtGui.QColor(0, 0, 0, 0))
        painter._set_background_color_(QtGui.QColor(15, 15, 15, 127))
        painter.drawRoundedRect(self._main_text_draw_rect, 2, 2, QtCore.Qt.AbsoluteSize)
        painter.drawRoundedRect(self._percent_text_draw_rect, 2, 2, QtCore.Qt.AbsoluteSize)
        # main
        painter._draw_text_by_rect_(
            rect=self._main_text_draw_rect,
            text=self._main_text,
            font=self._text_font,
            text_color=_gui_core.GuiRgba.DarkWhite,
            text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
        )
        # percent
        painter._draw_text_by_rect_(
            rect=self._percent_text_draw_rect,
            text=self._percent_text,
            font=self._percent_font,
            text_color=_qt_core.QtRgba.TextHover,
            text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
        )

    def _generate_thread_(self, widget):
        self._profile = bsc_storage.Profile.generate()

        self._trd = _qt_core.QtThreadForSpcTask.generate(
            widget, self
        )
        # update per 0.1 sec
        self._update_timer.start(100)

        self._trd.started.connect(self._on_started_)
        self._trd.finished.connect(self._on_finished_)
        self._trd.completed.connect(self._on_completed_)
        self._trd.failed.connect(self._on_failed_)
        self._trd.killed.connect(self._on_killed_)

        self._trd.system_resource_usage_update.connect(self._on_system_resource_usage_update_)
        return self._trd
    
    def _set_timeout_(self, value):
        self._timeout = value

    def _compute_cost_time_(self):
        if self._start_timestamp is None:
            return 0
        if self._finish_timestamp is None:
            return bsc_core.BscSystem.generate_timestamp()-self._start_timestamp
        return self._finish_timestamp-self._start_timestamp

    def _refresh_on_time_(self):
        self._progress_index += 1
        self._refresh_widget_all_()

    def _check_is_finished_(self):
        return self._status in {
            self.Status.Completed,
            self.Status.Error,
            self.Status.Failed
        }

    def _is_killed_(self):
        return self._kill_flag

    def _set_tag_text_(self, text):
        self._tag_text = text

    def _set_text_(self, text):
        self._text = text
        self._main_text = self._generate_main_text_()

    def _generate_main_text_(self):
        self._cost_time = self._compute_cost_time_()
        if self._text:
            return '{} | {} | {}'.format(
                bsc_core.ensure_string(self._text),
                bsc_core.BscInteger.second_to_time_prettify(self._cost_time, mode=1),
                _gui_core.GuiProcessStatusMapper.MAPPER[self._status]

            )
        return bsc_core.BscInteger.second_to_time_prettify(self._cost_time, mode=1)
