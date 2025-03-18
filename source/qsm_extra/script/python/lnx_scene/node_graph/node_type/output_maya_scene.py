# coding:utf-8
import sys

from ..core import model as _cor_model

from ..core import gui as _core_gui


class Node(_cor_model.StandardNodeModel):
    NODE_TYPE = 'OutputMaya'

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)

    @classmethod
    def create(cls, root, *args, **kwargs):
        flag, node = root.generate_node(cls.NODE_TYPE, *args, **kwargs)
        if flag is True:
            node.set_add_port_enable(True)
            node.set_input_prefix('i0')
            node.add_input('i0')

            node.parameters.add_group(param_path='output').set_options(
                gui_name='Output', gui_name_chs='输出'
            )
            node.parameters.add_string(param_path='output.directory').set_options(
                widget='directory', save=True, gui_name='Directory', gui_name_chs='目录'
            )
            node.parameters.add_boolean(param_path='output.with_playblast').set_options(
                gui_name='With Playblast', gui_name_chs='包含拍屏'
            )

            node.parameters.add_string(param_path='output_all').set_options(
                widget='button', gui_name='Output All', gui_name_chs='输出所有'
            )
        return flag, node


class NodeGui(_core_gui.QtStandardNode):
    def __init__(self, *args, **kwargs):
        super(NodeGui, self).__init__(*args, **kwargs)


def register():
    sys.stdout.write('Register node: {}.\n'.format(Node.NODE_TYPE))
    _cor_model.RootNodeModel.register_node_type(
        Node.NODE_TYPE, Node, NodeGui, 'Output MAYA Scene', '输出MAYA文件'
    )
