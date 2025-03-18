# coding:utf-8
import sys

from ..core import model as _cor_model

from ..core import gui as _core_gui


class Node(_cor_model.StandardNodeModel):
    NODE_TYPE = 'LoadPremiereXml'

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)

    @classmethod
    def create(cls, root, *args, **kwargs):
        flag, node = root.generate_node(cls.NODE_TYPE, *args, **kwargs)
        if flag is True:
            node.add_output('out')

            node.parameters.add_group(param_path='input').set_options(
                gui_name='Input', gui_name_chs='输入'
            )
            node.parameters.add_string(param_path='input.file').set_options(
                widget='file', open=True, gui_name='Scene', gui_name_chs='文件', ext_includes=['.xml']
            )

            node.parameters.add_group(param_path='info').set_options(
                gui_name='Info', gui_name_chs='信息'
            )
            node.parameters.add_integer_array(param_path='info.frame_range').set_options(
                widget='integer2', lock=True, gui_name='Frame Range', gui_name_chs='帧范围'
            )
            node.parameters.add_integer(param_path='info.fps').set_options(
                lock=True, gui_name='FPS', gui_name_chs='帧率'
            )
            node.parameters.add_string_array(param_path='info.video_json').set_options(
                widget='json', lock=True, gui_name='Videos', gui_name_chs='视频'
            )

            node.parameters.add_string(param_path='analysis_and_build').set_options(
                widget='button',
                script=r'import lnx_scene.node_graph.node_handle as h; h.LoadPremiereXml(node).analysis_and_build()',
                gui_name='Analysis and Build', gui_name_chs='解析并构建',
            )
        return flag, node


class NodeGui(_core_gui.QtStandardNode):
    def __init__(self, *args, **kwargs):
        super(NodeGui, self).__init__(*args, **kwargs)


def register():
    sys.stdout.write('Register node: {}.\n'.format(Node.NODE_TYPE))
    _cor_model.RootNodeModel.register_node_type(
        Node.NODE_TYPE, Node, NodeGui, 'Load Premiere XML', '加载Premiere XML'
    )
