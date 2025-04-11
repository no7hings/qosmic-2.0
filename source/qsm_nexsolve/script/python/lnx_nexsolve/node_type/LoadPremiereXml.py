# coding:utf-8
import sys

import os

import lxgui.core as gui_core

from ..node_graph import model as _ng_model

from ..node_graph import gui as _ng_gui


class Node(_ng_model.ImagingNode):
    NODE_TYPE = os.path.splitext(os.path.basename(__file__))[0]
    NODE_VERSION = '0.0.0'

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)

    @classmethod
    def compute(cls, node, stage):
        location = node.get('setting.location')
        stg_node = stage.add_node('PremiereXml', location)
        stg_node.add_attr('videos').add_string_array(
            node.get('data.videos')
        )

    @classmethod
    def create(cls, node):
        node._generate_output(port_path='out')

        node.set_image(gui_core.GuiIcon.get('file/prproj'))

        # input
        node.parameters.add_group(param_path='input').set_options(
            gui_name='Input', gui_name_chs='输入'
        )
        node.parameters.add_string(param_path='input.file').set_options(
            widget='file', open=True, gui_name='Scene', gui_name_chs='文件', ext_includes=['.xml']
        )

        # setting
        node.parameters.add_group(param_path='setting').set_options(
            gui_name='Setting', gui_name_chs='设置'
        )
        node.parameters.add_string(param_path='setting.location', value='/root/premiere/xml/main').set_options(
            widget='path', gui_name='Location', gui_name_chs='位置'
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
        node.parameters.add_string_array(param_path='data.videos').set_options(
            widget='json', lock=True, gui_name='Videos', gui_name_chs='视频'
        )

        # button
        node.parameters.add_custom(param_path='analysis_and_build').set_options(
            widget='button',
            script=r'import lnx_nexsolve.node_handle as h; h.LoadPremiereXml(node).analysis_and_build()',
            gui_name='Analysis and Build', gui_name_chs='解析并构建',
        )


class NodeGui(_ng_gui.StandardNodeGui):
    def __init__(self, *args, **kwargs):
        super(NodeGui, self).__init__(*args, **kwargs)


def register():
    sys.stdout.write('Register node: {}.\n'.format(Node.NODE_TYPE))
    _ng_model.RootNode.register_node_type(
        Node.NODE_TYPE, Node, NodeGui, Node.NODE_VERSION,
        'Load Premiere XML', '加载Premiere XML'
    )
