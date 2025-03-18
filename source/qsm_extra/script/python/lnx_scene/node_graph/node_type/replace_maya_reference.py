# coding:utf-8
import sys

from ..core import model as _cor_model

from ..core import gui as _core_gui


class Node(_cor_model.StandardNodeModel):
    NODE_TYPE = 'ReplaceMayaReference'

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)

    @classmethod
    def create(cls, root, *args, **kwargs):
        flag, node = root.generate_node(cls.NODE_TYPE, *args, **kwargs)
        if flag is True:
            node.set_add_port_enable(True)
            node.set_input_prefix('i0')
            node.add_input('i0')
            node.add_output('out')
        return flag, node


class NodeGui(_core_gui.QtStandardNode):
    def __init__(self, *args, **kwargs):
        super(NodeGui, self).__init__(*args, **kwargs)


def register():
    sys.stdout.write('Register node: {}.\n'.format(Node.NODE_TYPE))
    _cor_model.RootNodeModel.register_node_type(
        Node.NODE_TYPE, Node, NodeGui, 'Replace Maya Reference', '替换MAYA引用'
    )
