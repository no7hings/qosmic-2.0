# coding:utf-8
import sys

import os

from ..node_graph import model as _ng_model

from ..node_graph import gui as _ng_gui


class Node(_ng_model.StandardNode):
    NODE_TYPE = os.path.splitext(os.path.basename(__file__))[0]

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)

    @classmethod
    def compute(cls, node, stage):
        pass

    @classmethod
    def create(cls, node):
        node.set_add_port_enable(True)
        node.set_input_prefix('i0')
        node._generate_input(port_path='i0')

        node.parameters.add_group(param_path='output').set_options(
            gui_name='Output', gui_name_chs='输出'
        )
        node.parameters.create_string(param_path='output.directory').set_options(
            widget='directory', save=True, gui_name='Directory', gui_name_chs='目录'
        )
        node.parameters.add_boolean(param_path='output.with_playblast').set_options(
            gui_name='With Playblast', gui_name_chs='包含拍屏'
        )

        node.parameters.add_custom(param_path='output_all').set_options(
            widget='button', gui_name='Output All', gui_name_chs='输出所有'
        )


class NodeGui(_ng_gui.StandardNodeGui):
    def __init__(self, *args, **kwargs):
        super(NodeGui, self).__init__(*args, **kwargs)


def register():
    sys.stdout.write('Register node: {}.\n'.format(Node.NODE_TYPE))
    _ng_model.RootNode.register_node_type(
        Node.NODE_TYPE, Node, NodeGui, 'Output MAYA Scene', '输出MAYA文件'
    )
