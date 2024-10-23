# coding:utf-8
import _port_base

from ..input import input_for_file as _input_for_file


class PrxPortForFileList(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_file.PrxInputForFiles

    def __init__(self, *args, **kwargs):
        super(PrxPortForFileList, self).__init__(*args, **kwargs)

    def restore(self):
        self._prx_port_input.restore()

    def get_all(self, *args, **kwargs):
        return self._prx_port_input.get_all(*args, **kwargs)

    def set_root(self, path):
        self._prx_port_input.set_root(path)

    def set_checked_by_include_paths(self, paths):
        self._prx_port_input.set_checked_by_include_paths(paths)

    def set_unchecked_by_include_paths(self, paths):
        self._prx_port_input.set_unchecked_by_include_paths(paths)

    def set_all_items_checked(self, boolean):
        self._prx_port_input.set_all_items_checked(boolean)

    def get_prx_tree(self):
        return self._prx_port_input._prx_input

    def connect_refresh_action_for(self, fnc):
        self._prx_port_input.connect_refresh_action_for(fnc)


# file tree
class PrxPortForFileTree(PrxPortForFileList):
    def __init__(self, *args, **kwargs):
        super(PrxPortForFileTree, self).__init__(*args, **kwargs)
        self._prx_port_input.set_view_mode('tree')
