# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import lxgui.qt.core as gui_qt_core


class GuiProcessOpt(object):
    def __init__(self, window, unit):
        self._window = window
        self._page = unit

        self._ts = []

    def execute(self, button, cmds):
        def finished_fnc_(index, status, result):
            button.set_finished_at(index, status)

        def failed_fnc_(index, results):
            file_path = bsc_log.LogBase.get_user_debug_file(
                'process', create=True
            )
            if isinstance(results, (tuple, list)):
                raw = '\n'.join(results)
            else:
                raw = results

            raw = raw.decode('utf-8')
            raw = raw.encode('gbk')

            bsc_storage.StgFileOpt(
                file_path
            ).set_write(raw)

        def status_changed_fnc_(index, status):
            button.set_status_at(index, status)

        def run_fnc_():
            self._ts = []

            for _i_index, _i_cmd in enumerate(cmds):
                _i_t = bsc_core.TrdCommandPool.generate(_i_cmd, _i_index)
                _i_t.status_changed.connect_to(status_changed_fnc_)
                _i_t.finished.connect_to(finished_fnc_)
                _i_t.failed.connect_to(failed_fnc_)
                self._ts.append(_i_t)

            [x.do_wait_for_start() for x in self._ts]

        def quit_fnc_():
            button.set_stopped()

            for _i in self._ts:
                _i.do_kill()

            q_t.do_quit()

        contents = []
        if cmds:
            button.set_stopped(False)

            c = len(cmds)

            button.set_status(bsc_core.TrdCommandPool.Status.Started)
            button.initialization(c, bsc_core.TrdCommandPool.Status.Started)

            q_t = gui_qt_core.QtMethodThread(self._window.widget)
            q_t.append_method(
                run_fnc_
            )
            q_t.start()
            self._window.connect_window_close_to(quit_fnc_)
        else:
            button.restore_all()
