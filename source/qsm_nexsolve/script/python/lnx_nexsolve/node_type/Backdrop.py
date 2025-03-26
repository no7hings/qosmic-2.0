# coding:utf-8
import sys

import os

from ..node_graph import model as _ng_model

from ..node_graph import gui as _ng_gui


class Node(_ng_model.Backdrop):
    NODE_TYPE = os.path.splitext(os.path.basename(__file__))[0]

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)

    @classmethod
    def create(cls, node):
        pass


class NodeGui(_ng_gui.BackdropGui):
    def __init__(self, *args, **kwargs):
        super(NodeGui, self).__init__(*args, **kwargs)


def register():
    sys.stdout.write('Register node: {}.\n'.format(Node.NODE_TYPE))
    _ng_model.RootNode.register_node_type(
        Node.NODE_TYPE, Node, NodeGui, 'Backdrop', '背板'
    )

