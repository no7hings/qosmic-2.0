# coding:utf-8
import os

import sys

import lxbasic.storage as bsc_storage

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
        file_opt = bsc_storage.StgFileOpt(file_path)
        name_base = file_opt.name_base
        name = '{}_MA'.format(name_base)
        flag, node = self._root_model.add_node_on_cursor('LoadMayaScene', name=name, index=index)
        if flag is True:
            node.set('input.file', file_path, ignore_undo=True)
            node.set('setting.location', '/root/maya/scene/{}'.format(name), ignore_undo=True)
            video_opt = file_opt.replace_ext_to('.mov')
            if video_opt.get_is_file() is True:
                node.set_video(video_opt.get_path())
            node.execute('data.update_data')


def register():
    sys.stdout.write('Register drop action: {}.\n'.format(DropAction.NAME))
    _ng_model.RootNode.register_drop_action(DropAction.NAME, DropAction)
