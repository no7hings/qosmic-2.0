# coding:utf-8
from . import node_for_dag as _node_for_dag


class XgenDescription(_node_for_dag.Shape):
    def __init__(self, path):
        super(XgenDescription, self).__init__(path)
