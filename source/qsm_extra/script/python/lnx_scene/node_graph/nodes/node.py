# coding:utf-8
import sys

from ..core import model as _cor_model

from ..core import gui as _core_gui


class Node(_cor_model._NodeModel):
    NODE_TYPE = 'default'

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)

    @classmethod
    def create(cls, root, *args, **kwargs):
        flag, node = root.generate_node(cls.NODE_TYPE, *args, **kwargs)
        if flag is True:
            node.add_input_port('in')
            node.add_output_port('out')
        return flag, node


class NodeGui(_core_gui._QtNode):
    def __init__(self, *args, **kwargs):
        super(NodeGui, self).__init__(*args, **kwargs)


def register():
    sys.stdout.write('Register node: {}.\n'.format(Node.NODE_TYPE))
    _cor_model._RootNodeModel.register_node_type(Node, NodeGui)
