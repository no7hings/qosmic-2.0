# coding=utf-8
import socket

import base64

import struct

import lxbasic.log as bsc_log
# qt
import six

from ..core.wrap import *


class WebSocketBase(object):
    NAME = 'Qosmic Web Server'
    HOST = 'localhost'
    PORT = 12306


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
        
        self._name = WebSocketBase.NAME
        self._host = WebSocketBase.HOST
        self._port = WebSocketBase.PORT

        self._verbose = False

        self._window = self.parent()

        self._web_server = QtWebSockets.QWebSocketServer(
            self._name, QtWebSockets.QWebSocketServer.NonSecureMode
        )

        # noinspection PyArgumentList
        if self._web_server.listen(port=WebSocketBase.PORT):
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
        self._window._show_message_(text)
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


class WebSocketConnection(object):
    KEY = 'web socket connection'

    class Status(object):
        Ok = 1
        Error = -1

    class Mode(object):
        Script = 0
        Statement = 1

    @staticmethod
    def auto_string(text):
        if isinstance(text, six.text_type):
            return text.encode('utf-8')
        return text

    def __init__(self):
        self._host = WebSocketBase.HOST
        self._port = WebSocketBase.PORT

        self._status = self.Status.Error

        self.connect(self._host, self._port)

    def close(self):
        if self._status == self.Status.Ok:
            self._skt.close()

    def connect(self, host, port):
        self.close()
        self._status = self.Status.Error
        try:
            self._skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._skt.connect((host, port))
        except Exception:
            raise RuntimeError('Failed to connect to '+host+':'+str(port))
        self._status = self.Status.Ok

    @classmethod
    def check_is_exists(cls):
        # noinspection PyBroadException
        try:
            skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            skt.connect((WebSocketBase.HOST, WebSocketBase.PORT))
            return True
        except Exception:
            return False

    def get_status(self):
        return self._status

    status = property(get_status)

    def send(self, text):
        if self._status != self.Status.Ok:
            return False

        handshake_request = self.create_handshake_request(
            self._host, self._port, path='/'
        )
        self._skt.sendall(handshake_request)

        response = self._skt.recv(1024)
        if b"101 Switching Protocols" in response:
            self._send(self._skt, text)
        else:
            bsc_log.Log.trace_method_error(
                self.KEY, 'handshake failed'
            )
        return True

    @classmethod
    def create_handshake_request(cls, host, port, path):
        key = base64.b64encode("some_random_key")
        request = (
            "GET {} HTTP/1.1\r\n"
            "Host: {}:{}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            "Sec-WebSocket-Key: {}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        ).format(path, host, port, key)
        return request

    @classmethod
    def _send(cls, sock, text):
        text = cls.auto_string(text)
        message_length = len(text)

        frame_header = bytearray()
        frame_header.append(129)  # 10000001: FIN, Text Frame

        if message_length <= 125:
            frame_header.append(message_length)
        elif message_length <= 65535:
            frame_header.append(126)
            frame_header.extend(struct.pack('>H', message_length))  # 2 bytes
        else:
            frame_header.append(127)
            frame_header.extend(struct.pack('>Q', message_length))  # 8 bytes

        sock.sendall(bytes(frame_header)+text)

    def get_receive(self):
        response = self._skt.recv(1024)
        if response:
            return response

    @classmethod
    def receive_websocket_message(cls, sock):
        response = sock.recv(1024)
        if response:
            bsc_log.Log.trace_method_result(
                cls.KEY, 'received: "{}"'.format(response)
            )
