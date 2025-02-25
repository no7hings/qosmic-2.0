# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.log as bsc_log


class Undo(object):
    @staticmethod
    def execute(fnc):
        def sub_fnc_(*args, **kwargs):
            cmds.undoInfo(openChunk=1, undoName=fnc.__name__)
            # noinspection PyBroadException
            try:
                _method = fnc(*args, **kwargs)
                return _method
            except Exception:
                bsc_log.LogException.trace()
            #
            finally:
                cmds.undoInfo(closeChunk=1, undoName=fnc.__name__)
        return sub_fnc_

    @classmethod
    def flush(cls):
        cmds.flushUndo()
