# coding:utf-8
from . import _port_base

from ..input import input_for_dcc as _input_for_dcc


class PrxPortForNodeList(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_dcc.PrxInputForNodes

    def __init__(self, *args, **kwargs):
        super(PrxPortForNodeList, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortForNodeList, self).set_name(*args, **kwargs)
        self._prx_port_input._prx_input._qt_widget._set_name_text_(args[0])

    def get_all(self):
        return self._prx_port_input.get_all()

    def update_checked_by_paths(self, paths, extra=False):
        self._prx_port_input.update_checked_by_paths(paths, extra)

    def update_unchecked_by_paths(self, paths, extra=False):
        self._prx_port_input.update_unchecked_by_paths(paths, extra)

    def update_check_by_dict(self, dict_):
        self._prx_port_input.update_check_by_dict(dict_)

    def set_all_items_checked(self, boolean):
        self._prx_port_input.set_all_items_checked(boolean)

    def get_prx_tree(self):
        return self._prx_port_input._prx_input


class PrxPortForNodeTree(PrxPortForNodeList):
    def __init__(self, *args, **kwargs):
        super(PrxPortForNodeTree, self).__init__(*args, **kwargs)

        self._prx_port_input.set_view_mode('tree')
