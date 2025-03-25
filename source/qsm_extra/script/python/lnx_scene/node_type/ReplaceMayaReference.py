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
        cel_str = node.get('setting.selection')

        stg_nodes = stage.find_nodes(cel_str)
        for i in stg_nodes:
            i.add_attr('reference_replace_map').create_dict(
                node.get('replace.replace_map')
            )

    @classmethod
    def create(cls, node):
        node.set_add_port_enable(True)
        node.set_input_prefix('i0')
        # node._generate_input(port_path='i0')
        node._generate_output(port_path='out')

        # setting
        node.parameters.add_group(param_path='setting').set_options(
            gui_name='Setting', gui_name_chs='设置'
        )
        node.parameters.create_string(
            param_path='setting.selection',
            value='/root/maya/scene//*{attr("type")=="MaysScene"}'
        ).set_options(
            widget='path', gui_name='Selection', gui_name_chs='选择'
        )

        node.parameters.create_string(
            param_path='setting.reference_pattern',
            value='X:/{project}/Assets/{role}/{asset}/Rig/Final/scenes/{asset}_Skin.ma'
        ).set_options(
            widget='path', gui_name='Reference Pattern', gui_name_chs='引用模版'
        )

        # data
        node.parameters.add_group(param_path='data').set_options(
            gui_name='Data', gui_name_chs='数据'
        )
        node.parameters.create_string_array(param_path='data.references').set_options(
            widget='json', lock=True, gui_name='References', gui_name_chs='引用'
        )

        # data button
        node.parameters.add_custom(param_path='data.update_info').set_options(
            widget='button',
            script=r'import lnx_scene.node_handle as h; h.ReplaceMayaReference(node).update_info()',
            gui_name='Update Data', gui_name_chs='更新数据',
        )

        # replace
        node.parameters.add_group(param_path='replace').set_options(
            gui_name='Replace', gui_name_chs='替换'
        )

        node.parameters.add_dict(param_path='replace.replace_map').set_options(
            widget='json',
            gui_name='Replace Map', gui_name_chs='替换对照',
        )

        # replace button
        node.parameters.add_custom(param_path='replace.create_replace').set_options(
            widget='buttons',
            data=[
                dict(
                    script=r'import lnx_scene.node_handle as h; h.ReplaceMayaReference(node).create_replace()',
                    gui_name='Create Replace', gui_name_chs='创建替换'
                ),
                dict(
                    script=r'import lnx_scene.node_handle as h; h.ReplaceMayaReference(node).remove_replace()',
                    gui_name='Remove Replace', gui_name_chs='移除替换',
                )
            ],
        )


class NodeGui(_ng_gui.StandardNodeGui):
    def __init__(self, *args, **kwargs):
        super(NodeGui, self).__init__(*args, **kwargs)


def register():
    sys.stdout.write('Register node: {}.\n'.format(Node.NODE_TYPE))
    _ng_model.RootNode.register_node_type(
        Node.NODE_TYPE, Node, NodeGui, 'Replace Maya Reference', '替换MAYA引用'
    )
