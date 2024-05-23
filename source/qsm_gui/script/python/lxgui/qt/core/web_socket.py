# coding=utf-8
import six

import lxbasic.log as bsc_log

import lxbasic.web as bsc_web

from ..core.wrap import *


class QtWebSocketServer(QtCore.QObject):
    KEY = 'web socket server'

    @staticmethod
    def auto_string(text):
        if isinstance(text, six.text_type):
            return text.encode('utf-8')
        return text

    @classmethod
    def auto_unicode(cls, text):
        pass

    def __init__(self, *args, **kwargs):
        super(QtWebSocketServer, self).__init__(*args, **kwargs)
        
        self._name = bsc_web.WebSocketBase.NAME
        self._host = bsc_web.WebSocketBase.HOST
        self._port = bsc_web.WebSocketBase.PORT

        self._verbose = False

        self._window = self.parent()

        self._web_server = QtWebSockets.QWebSocketServer(
            self._name, QtWebSockets.QWebSocketServer.NonSecureMode
        )

        # noinspection PyArgumentList
        if self._web_server.listen(port=self._port):
            bsc_log.Log.trace_method_result(
                self.KEY, 'start for "{}"'.format(
                    self._port
                )
            )

        # noinspection PyUnresolvedReferences
        self._web_server.newConnection.connect(self._do_new_connection_)
        self._sockets = []

    @qt_slot(str)
    def _do_trace_(self, text):
        text = self.auto_string(text)
        self._window._show_notice_(text)
        for i in self._sockets:
            i.sendTextMessage(text)

        if self._verbose is True:
            bsc_log.Log.trace_method_result(
                self.KEY, 'received: "{}"'.format(text)
            )

    @qt_slot()
    def _do_new_connection_(self):
        skt = self._web_server.nextPendingConnection()
        skt.textMessageReceived.connect(self._do_trace_)
        skt.disconnected.connect(self._do_disconnected_)
        self._sockets.append(skt)
        if self._verbose is True:
            bsc_log.Log.trace_method_result(
                self.KEY, 'new connection'
            )

    @qt_slot()
    def _do_disconnected_(self):
        skt = self.sender()
        self._sockets.remove(skt)
        skt.deleteLater()
        if self._verbose is True:
            bsc_log.Log.trace_method_result(
                self.KEY, 'disconnected'
            )
