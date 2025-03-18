# coding:utf-8
import sys

from ..core import model as _cor_model

from ..core import gui as _core_gui


class Node(_cor_model.BackdropModel):
    NODE_TYPE = 'backdrop'

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)

    @classmethod
    def create(cls, root, *args, **kwargs):
        flag, node = root.generate_node(cls.NODE_TYPE, *args, **kwargs)
        return flag, node


class NodeGui(_core_gui.QtBackdrop):
    def __init__(self, *args, **kwargs):
        super(NodeGui, self).__init__(*args, **kwargs)


def register():
    sys.stdout.write('Register node: {}.\n'.format(Node.NODE_TYPE))
    _cor_model.RootNodeModel.register_node_type(
        Node.NODE_TYPE, Node, NodeGui, 'Backdrop', '背板'
    )

