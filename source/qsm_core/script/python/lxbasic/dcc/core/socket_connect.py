# coding:utf-8
import socket

import struct


class _AbsSocketConnect(object):
    HOST = None
    PORT = None

    class Status(object):
        Ok = 1
        Error = -1

    class Mode(object):
        Script = 0
        Statement = 1

    def get_status(self):
        return self._status

    status = property(get_status)

    def _init_socket_base_(self):
        self._status = self.Status.Error

    def get_is_valid(self):
        return self.get_status() == self.Status.Ok


class SocketConnectForMaya(_AbsSocketConnect):
    HOST = 'localhost'
    PORT = 13291

    @classmethod
    def create_connection(cls, port):
        # noinspection PyUnresolvedReferences
        import maya.cmds as cmds

        if port is None:
            port = cls.PORT

        if not cmds.commandPort(":{}".format(port), query=True):
            cmds.commandPort(name=":{}".format(port))

    def __init__(self, port=None):
        self.__host = self.HOST
        self.__port = port or self.PORT
        self._init_socket_base_()
        # noinspection PyBroadException
        try:
            self.connect(self.__host, self.__port)
        except Exception:
            import lxgui.core as gui_core

            gui_core.GuiDialog.create(
                label='Connect',
                sub_label='Maya Connect',
                content='Connection to Maya is Failed',
                status=gui_core.GuiDialog.ValidationStatus.Error,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False
            )
            return

    def close(self):
        if self._status == self.Status.Ok:
            self._socket.close()

    def connect(self, host, port):
        self.close()
        self._status = self.Status.Error
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((host, port))
            print("Connected to Maya")
        except Exception:
            raise ValueError('Failed to connect to '+host+':'+str(port))
        self._status = self.Status.Ok

    def run(self, script):
        if self._status != self.Status.Ok:
            print("Not connected to Maya")
        self.__send(script, self.Mode.Script)

    def evaluate(self, statement):
        return self.__send(statement, self.Mode.Statement)

    # noinspection PyUnusedLocal
    def __send(self, command, mode):
        if self._status != self.Status.Ok:
            # http_post(url, data)
            # time.sleep(1)
            # sys.exit()
            return

        mel_command = 'python("{}")'.format(command)
        data_sent = self._socket.sendall(bytes(mel_command))

    def __del__(self):
        self.close()


class SocketConnectForClarisse(_AbsSocketConnect):
    HOST = 'localhost'
    PORT = 55000

    @classmethod
    def create_connection(cls, port=None):
        # noinspection PyUnresolvedReferences
        import ix

        if port is None:
            port = cls.PORT

        if not ix.application.is_command_port_active():
            ix.application.enable_command_port()
        if ix.application.get_command_port() != port:
            ix.application.set_command_port(port)

    def get_status(self):
        return self._status

    status = property(get_status)

    def __init__(self, port=None):
        self.__host = self.HOST
        self.__port = port or self.PORT
        self._init_socket_base_()
        # noinspection PyBroadException
        try:
            self.connect(self.__host, self.__port)
        except Exception:
            import lxgui.core as gui_core

            gui_core.GuiDialog.create(
                label='Connect',
                sub_label='Clarisse Connect',
                content='Connection to Clarisse is Failed',
                status=gui_core.GuiDialog.ValidationStatus.Error,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False
            )
            return

    def connect(self, host, port):
        self.close()
        self._status = self.Status.Error
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((host, port))
        except Exception:
            raise ValueError('Failed to connect to '+host+':'+str(port))
        self._status = self.Status.Ok

    def run(self, script):
        if self._status != self.Status.Ok:
            print("Not connected to Clarisse")
        self.__send(script, self.Mode.Script)

    def evaluate(self, statement):
        return self.__send(statement, self.Mode.Statement)

    def close(self):
        if self._status == self.Status.Ok:
            self._socket.close()

    # noinspection PyUnusedLocal
    def __send(self, command, mode):
        if self._status != self.Status.Ok:
            # http_post(url, data)
            # time.sleep(1)
            # sys.exit()
            return

        command_size = len(command)+1
        command_size = struct.pack("<I", command_size)
        data_sent = self._socket.send(command_size)
        if data_sent == 0:
            print("No Data Sent")
        #
        packet = str(mode)+command
        packet = bytes(packet)
        data_sent = self._socket.send(packet)

        result_size = self._socket.recv(4)
        result_size = struct.unpack("<I", result_size)[0]
        must_recv = True
        result = ''
        remaining = result_size
        while must_recv:
            result += str(self._socket.recv(remaining))
            remaining = result_size-len(result)
            if remaining == 0:
                must_recv = False

        if result[0] == '0':
            print("Send Failed")
        else:
            result = result[1:]
            if result == '':
                return None
            else:
                return result

    def __del__(self):
        self.close()
