# coding:utf-8
import sys

import lxgui.core as gui_core

from ..core import model as _cor_model

from ..core import gui as _core_gui


class Node(_cor_model.ImagingNode):
    NODE_TYPE = 'LoadMayaScene'

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)

    @classmethod
    def create(cls, root, *args, **kwargs):
        flag, node = root.generate_node(cls.NODE_TYPE, *args, **kwargs)
        if flag is True:
            node.add_input('in')
            node.add_output('out')

            node.set_image(gui_core.GuiIcon.get('file/ma'))

            node.parameters.add_string(param_path='preview').set_options(
                widget='file', open=True, gui_name='Preview', gui_name_chs='预览', ext_includes=['.mov']
            )

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

            # info
            node.parameters.add_group(param_path='info').set_options(
                gui_name='Info', gui_name_chs='信息'
            )
            node.parameters.add_integer_array(param_path='info.frame_range').set_options(
                widget='integer2', lock=True, gui_name='Frame Range', gui_name_chs='帧范围'
            )
            node.parameters.add_integer(param_path='info.fps').set_options(
                lock=True, gui_name='FPS', gui_name_chs='帧率'
            )
            node.parameters.add_string_array(param_path='info.reference_json').set_options(
                widget='json', lock=True, gui_name='References', gui_name_chs='引用'
            )

            # button
            node.parameters.add_string(param_path='analysis_or_update').set_options(
                widget='button',
                script=r'import lnx_scene.node_graph.node_handle as h; h.LoadMayaScene(node).analysis_or_update()',
                gui_name='Analysis/Update', gui_name_chs='解析/更新',
            )
        return flag, node


class NodeGui(_core_gui.ImagingNodeGui):
    def __init__(self, *args, **kwargs):
        super(NodeGui, self).__init__(*args, **kwargs)


def register():
    sys.stdout.write('Register node: {}.\n'.format(Node.NODE_TYPE))
    _cor_model.RootNode.register_node_type(
        Node.NODE_TYPE, Node, NodeGui, 'Load MAYA Scene', '加载MAYA文件'
    )
