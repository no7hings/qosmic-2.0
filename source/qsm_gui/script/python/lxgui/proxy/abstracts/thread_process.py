# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# qt
from ...qt import core as gui_qt_core


class AbsQtThreadProcessBase(object):
    KEY = 'command batch'

    def __init__(self, tag, window, button):
        self._tag = tag
        self._window = window
        self._button = button
        self._cmds = []
        self._ts = []

        self._build_warning_texts = []
        self._execute_warning_texts = []

        self._batch_exception_log_file_path = None

    def build_for_data(self):
        raise NotImplementedError()

    def execute_by_data(self, button, cmds):
        def finished_fnc_(index, status, results):
            button.set_finished_at(index, status)
            if status == bsc_core.TrdCommandPool.Status.Failed:
                if self._batch_exception_log_file_path is not None:
                    bsc_storage.StgFileOpt(self._batch_exception_log_file_path).append(
                        '\n'.join(results)
                    )
            else:
                print '\n'.join(results)

        def status_changed_fnc_(index, status):
            button.set_status_at(index, status)

        def run_fnc_():
            self._ts = []
            #
            for _i_index, _i_cmd in enumerate(self._cmds):
                bsc_core.TrdCommandPool.set_wait()
                #
                _i_t = bsc_core.TrdCommandPool.set_start(_i_cmd, _i_index)
                self._ts.append(_i_t)
                _i_t.status_changed.connect_to(status_changed_fnc_)
                _i_t.finished.connect_to(finished_fnc_)

        def quit_fnc_():
            button.set_stopped()
            #
            for _i in self._ts:
                _i.do_kill()
            #
            q_t.do_quit()

        contents = []
        if cmds:
            button.set_stopped(False)

            c = len(cmds)

            button.set_status(bsc_core.TrdCommandPool.Status.Started)
            button.set_initialization(c, bsc_core.TrdCommandPool.Status.Started)

            q_t = gui_qt_core.QtMethodThread(self._window.widget)
            q_t.append_method(
                run_fnc_
            )
            q_t.start()
            self._window.connect_window_close_to(quit_fnc_)
        else:
            button.restore_all()
            contents = self._execute_warning_texts

        if contents:
            self.show_warning(contents)
            return False
        else:
            return True

    def set_build_warning_texts(self, texts):
        self._build_warning_texts = texts

    def set_execute_warning_texts(self, texts):
        self._execute_warning_texts = texts

    def show_warning(self, texts):
        pass

    def restore(self):
        self._cmds = []
        self._ts = []

    def append_cmd(self, cmd):
        bsc_log.Log.trace_method_result(
            self.KEY, 'append command: `{}`'.format(cmd)
        )
        self._cmds.append(cmd)

    def extend_cmds(self, cmds):
        self._cmds.extend(cmds)

    def execute(self):
        self.restore()
        directory_path = bsc_storage.StgUserMtd.get_user_batch_exception_directory(self._tag, create=True)
        self._batch_exception_log_file_path = '{}/{}.log'.format(directory_path, bsc_core.UuidMtd.generate_new())

        self.build_for_data()
        self.execute_by_data(self._button, self._cmds)
