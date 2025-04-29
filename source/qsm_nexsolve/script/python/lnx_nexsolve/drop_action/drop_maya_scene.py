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

    def accept_file(self, file_path, index=0):
        name = '{}_MA'.format(os.path.splitext(os.path.basename(file_path))[0])
        flag, node = self._root_model.add_node_on_cursor('LoadMayaScene', name=name, index=index)
        if flag is True:
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            node.set('input.file', file_path, ignore_undo=True)
            node.set('setting.location', '/root/maya/scene/{}'.format(file_name), ignore_undo=True)
            node.execute('data.update_data')


def register():
    sys.stdout.write('Register drop action: {}.\n'.format(DropAction.NAME))
    _ng_model.RootNode.register_drop_action(DropAction.NAME, DropAction)
