# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class Connection(object):
    @classmethod
    def create(cls, atr_path_src, atr_path_tgt):
        return cmds.connectAttr(atr_path_src, atr_path_tgt, force=1)


class NodeConnection(object):
    @classmethod
    def find_all_target_nodes(cls, path, type_name):
        return list(
            set(
                cmds.listConnections(
                    path, destination=1, source=0, type=type_name
                ) or []
            )
        )

    @classmethod
    def find_all_source_nodes(cls, path, type_name):
        return list(
            set(
                cmds.listConnections(
                    path, destination=0, source=1, type=type_name
                ) or []
            )
        )
