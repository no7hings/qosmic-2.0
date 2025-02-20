# coding=utf-8
import functools

import lxbasic.log as bsc_log

import lxbasic.web as bsc_web

import lxbasic.core as bsc_core

from ..core.wrap import *


class AbsQtWebServerForWindowNotice(QtCore.QObject):
    LOG_KEY = 'web socket server'
    NAME = 'Qosmic Window Notice'

    def __init__(self, *args, **kwargs):
        super(AbsQtWebServerForWindowNotice, self).__init__(*args, **kwargs)

        self._name = None
        self._host = None
        self._port = None

        self._web_server = None

        self._verbose = False

        self._window = self.parent()

    def _start_(self, name, host, port):
        self._name = None
        self._host = host
        self._port = port

        if bsc_web.WebSocket.check_is_in_use(host, port) is True:
            raise RuntimeError()

        self._web_server = QtWebSockets.QWebSocketServer(
            name, QtWebSockets.QWebSocketServer.NonSecureMode
        )

        # noinspection PyArgumentList
        if self._web_server.listen(port=self._port):
            bsc_log.Log.trace_method_result(
                self.LOG_KEY, 'start for "{}"'.format(
                    port
                )
            )

        # noinspection PyUnresolvedReferences
        self._web_server.newConnection.connect(self._new_connection_fnc_)
        self._sockets = []

    @qt_slot(str)
    def _process_fnc_(self, text):
        text = bsc_core.ensure_string(text)
        self._window._show_notice_(text)
        for i in self._sockets:
            i.sendTextMessage(text)

        if self._verbose is True:
            bsc_log.Log.trace_method_result(
                self.LOG_KEY, 'received: "{}"'.format(text)
            )

    def _new_connection_fnc_(self):
        skt = self._web_server.nextPendingConnection()
        self._sockets.append(skt)
        skt.textMessageReceived.connect(self._process_fnc_)
        skt.disconnected.connect(functools.partial(self._disconnected_fnc_, skt))
        if self._verbose is True:
            bsc_log.Log.trace_method_result(
                self.LOG_KEY, 'new connection'
            )

    def _disconnected_fnc_(self, skt):
        self._sockets.remove(skt)
        skt.close()
        skt.deleteLater()
        if self._verbose is True:
            bsc_log.Log.trace_method_result(
                self.LOG_KEY, 'disconnected'
            )

    def _do_close_(self):
        if self._web_server is not None:
            for seq, i in enumerate(self._sockets):
                i.close()
                i.deleteLater()
            self._sockets = []
            self._web_server.close()


class QtWebServerForWindowNotice(AbsQtWebServerForWindowNotice):
    LOG_KEY = 'web socket server'

    def __init__(self, *args, **kwargs):
        super(QtWebServerForWindowNotice, self).__init__(*args, **kwargs)

    @qt_slot(str)
    def _process_fnc_(self, text):
        text = bsc_core.ensure_string(text)
        self._window._show_notice_(text)
        for i in self._sockets:
            i.sendTextMessage(text)

        if self._verbose is True:
            bsc_log.Log.trace_method_result(
                self.LOG_KEY, 'received: "{}"'.format(text)
            )


class QtWebServerForDcc(AbsQtWebServerForWindowNotice):
    def __init__(self, *args, **kwargs):
        super(QtWebServerForDcc, self).__init__(*args, **kwargs)

        # self._verbose = True

    @qt_slot(str)
    def _process_fnc_(self, text):
        text = bsc_core.ensure_string(text)

        exec (text)

        for i in self._sockets:
            i.sendTextMessage(text)

        if self._verbose is True:
            bsc_log.Log.trace_method_result(
                self.LOG_KEY, 'received: "{}"'.format(text)
            )
