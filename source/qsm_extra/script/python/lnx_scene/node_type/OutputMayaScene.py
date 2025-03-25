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
        # node._generate_input(port_path='i0')

        # setting
        node.parameters.add_group(param_path='setting').set_options(
            gui_name='Setting', gui_name_chs='设置'
        )
        node.parameters.add_string(
            param_path='setting.selection',
            value='/root/maya/scene//*{attr("type")=="MaysScene"}'
        ).set_options(
            widget='path', gui_name='Selection', gui_name_chs='选择'
        )

        # output
        node.parameters.add_group(param_path='output').set_options(
            gui_name='Output', gui_name_chs='输出'
        )
        node.parameters.add_string(param_path='output.directory').set_options(
            widget='directory', save=True, gui_name='Directory', gui_name_chs='目录'
        )
        node.parameters.add_boolean(param_path='output.with_playblast').set_options(
            gui_name='With Playblast', gui_name_chs='包含拍屏'
        )

        node.parameters.add_custom(param_path='output_all').set_options(
            widget='button',
            script=r'import lnx_scene.node_handle as h; h.OutputMayaScene(node).output_all()',
            gui_name='Output All', gui_name_chs='输出所有'
        )


class NodeGui(_ng_gui.StandardNodeGui):
    def __init__(self, *args, **kwargs):
        super(NodeGui, self).__init__(*args, **kwargs)


def register():
    sys.stdout.write('Register node: {}.\n'.format(Node.NODE_TYPE))
    _ng_model.RootNode.register_node_type(
        Node.NODE_TYPE, Node, NodeGui, 'Output MAYA Scene', '输出MAYA文件'
    )
