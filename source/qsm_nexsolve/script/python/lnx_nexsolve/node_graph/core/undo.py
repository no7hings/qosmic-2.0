# coding:utf-8
import sys

import enum

from lxgui.qt.core.wrap import *


class UndoActions(enum.IntEnum):
    PortConnect = 0x00
    PortDisconnect = 0x01
    PortReconnect = 0x02

    Delete = 0x10

    Copy = 0x11
    Cut = 0x12
    Paste = 0x13
    PasteCut = 0x14

    NodeAdd = 0x20
    NodeMove = 0x21
    NodeResize = 0x22

    NodeAddInput = 0x22
    NodeInputConnectAuto = 0x23
    NodeInputReconnectAuto = 0x24

    NodeBypass = 0x25

    ParamSetValue = 0x30


class GuiUndoCmd(QtWidgets.QUndoCommand):
    @classmethod
    def trace(cls, flag, action, result):
        return sys.stdout.write(
            '{}, {}: {}\n'.format(flag, str(action).split('.')[-1], result)
        )

    def __init__(self, action, redo_fnc, undo_fnc):
        super(GuiUndoCmd, self).__init__()
        self._action = action
        self._redo_fnc = redo_fnc
        self._undo_fnc = undo_fnc
        self._result = None

    def redo(self):
        self._result = self._redo_fnc() or ''
        self.trace('Execute', self._action, '...')

    def undo(self):
        self._result = self._undo_fnc() or ''
        self.trace('Undo', self._action, '...')


class GuiUndoFactory:
    @staticmethod
    def push(action):
        def decorator(fnc):
            def wrapper(*args, **kwargs):
                args = fnc(*args, **kwargs)
                if args:
                    undo_stack, redo_fnc, undo_fnc = args
                    undo_cmd = GuiUndoCmd(action, redo_fnc, undo_fnc)
                    undo_stack.push(undo_cmd)
                    return undo_cmd._result
                return None
            return wrapper
        return decorator
