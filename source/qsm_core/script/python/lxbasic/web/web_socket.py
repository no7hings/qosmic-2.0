# coding=utf-8
import uuid

import socket

import base64

import struct

import six

import lxbasic.log as bsc_log

from . import url as _url


class WebSocketBase(object):
    LOCALHOST = 'localhost'


class WebSocket(object):
    KEY = 'web socket'

    TIMEOUT = 10

    VERBOSE_LEVEL = 1

    @staticmethod
    def auto_string(text):
        if isinstance(text, six.text_type):
            return text.encode('utf-8')
        return text

    @classmethod
    def receive_websocket_message(cls, sock):
        response = sock.recv(1024)
        if response:
            bsc_log.Log.trace_method_result(
                cls.KEY, 'received: "{}"'.format(response)
            )

    @classmethod
    def create_handshake_request(cls, host, port, path):
        key = base64.b64encode(str(uuid.uuid1()).upper())
        request = (
            "GET {path} HTTP/1.1\r\n"
            "Host: {host}:{port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            "Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        ).format(
            path=path, host=host, port=port, key=key
        )
        return request

    @classmethod
    def create_fnc(cls, host, port, path='/'):
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.settimeout(cls.TIMEOUT)
        try:
            skt.connect((host, port))
        except socket.error as e:
            bsc_log.Log.trace_method_error(
                cls.KEY, 'Connection failed: {}'.format(e)
            )
            return None

        if cls.VERBOSE_LEVEL < 1:
            bsc_log.Log.trace_method_result(
                cls.KEY, 'Connection successful'
            )

        handshake_request = cls.create_handshake_request(host, port, path)
        skt.sendall(handshake_request)

        response = skt.recv(1024)
        if b"101 Switching Protocols" in response:
            if cls.VERBOSE_LEVEL < 1:
                bsc_log.Log.trace_method_result(
                    cls.KEY, 'Handshake successful'
                )
            return skt
        else:
            if cls.VERBOSE_LEVEL <= 1:
                bsc_log.Log.trace_method_error(
                    cls.KEY, 'Handshake failed'
                )
            skt.close()
            return None

    @classmethod
    def send_fnc(cls, sock, text):
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

    def __init__(self, host, port):
        self._host = host
        self._port = port

        self._skt = None

    def is_valid(self):
        return self.check_is_in_use(self._host, self._port)

    @classmethod
    def check_is_in_use(cls, host, port):
        # noinspection PyBroadException
        try:
            skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return skt.connect_ex((host, port)) == 0
        except Exception:
            return False

    def close(self):
        if self._skt is not None:
            self._skt.close()

    def connect(self):
        if self._skt is not None:
            return True

        self._skt = self.create_fnc(self._host, self._port)
        if self._skt is None:
            return False
        return True

    def connect_to_desktop(self):
        self._skt = self.create_fnc(WebSocketBase.LOCALHOST, self._port)
        if self._skt is None:
            return False
        return True

    def send(self, data):
        if self._skt is None:
            return False

        if isinstance(data, dict):
            text = _url.UrlOptions.to_string(data)
        else:
            text = data

        self.send_fnc(self._skt, text)
        return True

    def get_receive(self):
        response = self._skt.recv(1024)
        if response:
            return response
