# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class Connection(object):
    @classmethod
    def create(cls, atr_path_src, atr_path_dst):
        cmds.connectAttr(atr_path_src, atr_path_dst, force=1)


class Connections(object):
    @classmethod
    def get_all_from(cls, path):
        list_ = []
        _ = cmds.listConnections(path, destination=0, source=1, connections=1, plugs=1) or []
        # ["source-atr-path", "target-atr-path", ...]
        for seq, i in enumerate(_):
            if seq % 2:
                source_atr_path = i
                target_atr_path = _[seq - 1]
                #
                list_.append((source_atr_path, target_atr_path))
        return list_
