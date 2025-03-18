# coding:utf-8
import sys

from ..core import model as _cor_model

from ..core import gui as _core_gui


class Node(_cor_model.StandardNode):
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

            # setting
            node.parameters.add_group(param_path='setting').set_options(
                gui_name='Setting', gui_name_chs='设置'
            )
            node.parameters.add_string(
                param_path='setting.selection', value='/root/maya/scene//*{{attr("type")=="maya_scene"}}'
            ).set_options(
                widget='path', gui_name='Selection', gui_name_chs='选择'
            )

            # info
            node.parameters.add_group(param_path='info').set_options(
                gui_name='Info', gui_name_chs='信息'
            )
            node.parameters.add_string_array(param_path='info.reference_json').set_options(
                widget='json', lock=True, gui_name='References', gui_name_chs='引用'
            )

            # button
            node.parameters.add_string(param_path='info.update_info').set_options(
                widget='button',
                script=r'import lnx_scene.node_graph.node_handle as h; h.ReplaceMayaReference(node).update_info()',
                gui_name='Update Info', gui_name_chs='更新信息',
            )

        return flag, node


class NodeGui(_core_gui.StandardNodeGui):
    def __init__(self, *args, **kwargs):
        super(NodeGui, self).__init__(*args, **kwargs)


def register():
    sys.stdout.write('Register node: {}.\n'.format(Node.NODE_TYPE))
    _cor_model.RootNode.register_node_type(
        Node.NODE_TYPE, Node, NodeGui, 'Replace Maya Reference', '替换MAYA引用'
    )
