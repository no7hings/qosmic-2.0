# coding=utf-8
import six

import lxbasic.log as bsc_log

from lxgui.qt.core.wrap import *


class QtWebServerForTask(QtCore.QObject):
    LOG_KEY = 'task web server'

    text_message_accepted = qt_signal(str)

    @staticmethod
    def ensure_string(s):
        if isinstance(s, six.text_type):
            if six.PY2:
                return s.encode('utf-8')
        elif isinstance(s, six.binary_type):
            if six.PY3:
                return s.decode('utf-8')
        return s

    def __init__(self, *args, **kwargs):
        super(QtWebServerForTask, self).__init__(*args, **kwargs)

        self._verbose = False

        self._name = 'Qosmic Task Web Server'

    def _start_(self, host, port):
        self._host = host
        self._port = port

        self._web_server = QtWebSockets.QWebSocketServer(
            self._name, QtWebSockets.QWebSocketServer.NonSecureMode
        )

        # noinspection PyArgumentList
        if self._web_server.listen(port=self._port):
            bsc_log.Log.trace_method_result(
                self.LOG_KEY, 'start for "{}"'.format(
                    self._port
                )
            )

        # noinspection PyUnresolvedReferences
        self._web_server.newConnection.connect(self._new_connection_fnc_)
        self._sockets = []

    @qt_slot(str)
    def _process_fnc_(self, text):
        text = self.ensure_string(text)
        self.text_message_accepted.emit(text)
        for i in self._sockets:
            i.sendTextMessage(text)

        if self._verbose is True:
            bsc_log.Log.trace_method_result(
                self.LOG_KEY, 'received: "{}"'.format(text)
            )

    def _new_connection_fnc_(self):
        skt = self._web_server.nextPendingConnection()
        skt.textMessageReceived.connect(self._process_fnc_)
        skt.disconnected.connect(self._disconnected_fnc_)
        self._sockets.append(skt)
        if self._verbose is True:
            bsc_log.Log.trace_method_result(
                self.LOG_KEY, 'new connection'
            )

    def _disconnected_fnc_(self):
        skt = self.sender()
        self._sockets.remove(skt)
        skt.deleteLater()
        if self._verbose is True:
            bsc_log.Log.trace_method_result(
                self.LOG_KEY, 'disconnected'
            )
