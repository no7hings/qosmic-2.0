# coding:utf-8
import os.path
import sys

from ..core import base as _nxs_cor_base

from ..node_graph import model as _ng_model


class DropAction(_nxs_cor_base._ActionBase):
    NAME = 'DropMayaScene'

    INSTANCE = None

    def __init__(self, *args, **kwargs):
        pass

    def filter_file(self, file_path):
        ext = os.path.splitext(file_path)[-1]
        # support ".ma" only now
        if ext in {'.ma'}:
            return True
        return False

    def accept_file(self, file_path):
        flag, node = self._root_model.add_node('LoadMayaScene')
        if flag is True:
            self._root_model.move_node_to_cursor(node)
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            node.set('input.file', file_path)
            node.set('setting.location', '/root/maya/scene/{}'.format(file_name))
            node.execute('data.update_data')
            # print(file_path, 'ABC')


def register():
    sys.stdout.write('Register drop action: {}.\n'.format(DropAction.NAME))
    _ng_model.RootNode.register_drop_action(DropAction.NAME, DropAction)
