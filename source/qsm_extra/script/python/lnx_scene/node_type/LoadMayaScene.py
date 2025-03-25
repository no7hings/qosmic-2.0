# coding:utf-8
import sys

import os

import lxgui.core as gui_core

from ..node_graph import model as _ng_model

from ..node_graph import gui as _ng_gui


class Node(_ng_model.ImagingNode):
    NODE_TYPE = os.path.splitext(os.path.basename(__file__))[0]

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)

    @classmethod
    def compute(cls, node, stage):
        scene_path = node.get('input.file')
        if scene_path:
            location = node.get('setting.location')
            stg_node = stage.add_node('MaysScene', location)
            stg_node.add_attr('file').add_string(
                scene_path
            )
            stg_node.add_attr('frame_range').add_integer_array(
                node.get('data.frame_range')
            )
            stg_node.add_attr('fps').add_integer(
                node.get('data.fps')
            )
            stg_node.add_attr('references').add_string_array(
                node.get('data.references')
            )

    @classmethod
    def create(cls, node):
        node._generate_input(port_path='in')
        node._generate_output(port_path='out')

        node.set_image(gui_core.GuiIcon.get('file/ma'))

        # input
        node.parameters.add_group(param_path='input').set_options(
            gui_name='Input', gui_name_chs='输入'
        )
        node.parameters.add_string(param_path='input.file').set_options(
            widget='file', open=True, gui_name='Scene', gui_name_chs='文件', ext_includes=['.ma']
        )

        # setting
        node.parameters.add_group(param_path='setting').set_options(
            gui_name='Setting', gui_name_chs='设置'
        )
        node.parameters.add_string(param_path='setting.location', value='/root/maya/scene').set_options(
            widget='path', gui_name='Location', gui_name_chs='位置'
        )
        node.parameters.add_boolean(param_path='setting.ignore_unloaded', value=True).set_options(
            gui_name='Ignore Unloaded (Reference)', gui_name_chs='忽略未加载（引用）'
        )

        # data
        node.parameters.add_group(param_path='data').set_options(
            gui_name='Data', gui_name_chs='数据'
        )
        node.parameters.add_integer_array(param_path='data.frame_range').set_options(
            widget='integer2', lock=True, gui_name='Frame Range', gui_name_chs='帧范围'
        )
        node.parameters.add_integer(param_path='data.fps').set_options(
            lock=True, gui_name='FPS', gui_name_chs='帧率'
        )
        node.parameters.add_string_array(param_path='data.references').set_options(
            widget='json', lock=True, gui_name='References', gui_name_chs='引用'
        )

        # button
        node.parameters.add_custom(param_path='data.update_data').set_options(
            widget='button',
            script=r'import lnx_scene.node_handle as h; h.LoadMayaScene(node).update_data()',
            gui_name='Update Data', gui_name_chs='更新数据',
        )


class NodeGui(_ng_gui.ImagingNodeGui):
    def __init__(self, *args, **kwargs):
        super(NodeGui, self).__init__(*args, **kwargs)


def register():
    sys.stdout.write('Register node: {}.\n'.format(Node.NODE_TYPE))
    _ng_model.RootNode.register_node_type(
        Node.NODE_TYPE, Node, NodeGui, 'Load MAYA Scene', '加载MAYA文件'
    )
