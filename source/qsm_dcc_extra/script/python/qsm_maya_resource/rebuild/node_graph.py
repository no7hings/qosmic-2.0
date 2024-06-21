# coding:utf-8
import collections

import qsm_maya.core as qsm_mya_core


class _AbsNodeGraph(object):
    def __init__(self, node_type, node_path):
        self._node_type = node_type
        self._node_path = node_path
