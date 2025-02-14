# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import node as _node


class NodeGraph(object):
    
    @classmethod
    def get_all_source_nodes(cls, path, type_includes=None):
        def _rcs_fnc(path_):
            _paths = cls.get_source_nodes(path_)
            for _i_path in _paths:
                if _i_path not in keys:
                    keys.add(_i_path)
                    _.append(_i_path)
                    _rcs_fnc(_i_path)

        keys = set()
        _ = []
        _rcs_fnc(path)
        if type_includes:
            return [
                x for x in
                _
                if _node.Node.get_type(x) in type_includes
            ]
        return _
    
    @classmethod
    def get_source_nodes(cls, path, type_includes=None):
        _ = cmds.listConnections(path, destination=0, source=1) or []
        if type_includes:
            return [
                x for x in
                _
                if _node.Node.get_type(x) in type_includes]
        return _
