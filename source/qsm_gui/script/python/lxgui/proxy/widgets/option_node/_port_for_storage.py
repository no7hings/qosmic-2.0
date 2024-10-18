# coding:utf-8
import _port_base

import _input_for_storage


# storage
class AbsPrxPortForStorage(_port_base.AbsPrxPortForConstant):
    PRX_PORT_INPUT_CLS = None

    def __init__(self, *args, **kwargs):
        super(AbsPrxPortForStorage, self).__init__(*args, **kwargs)

    def set_ext_filter(self, ext_filter):
        self._prx_port_input.set_ext_filter(ext_filter)

    def set_ext_includes(self, ext_includes):
        self._prx_port_input.set_ext_includes(ext_includes)

    def set_history_key(self, key):
        self._prx_port_input.set_history_key(key)


# file open
class PrxPortForFileOpen(AbsPrxPortForStorage):
    PRX_PORT_INPUT_CLS = _input_for_storage.PrxInputForFileOpen

    def __init__(self, *args, **kwargs):
        super(PrxPortForFileOpen, self).__init__(*args, **kwargs)


# file save
class PrxPortForFileSave(AbsPrxPortForStorage):
    PRX_PORT_INPUT_CLS = _input_for_storage.PrxInputForFileSave

    def __init__(self, *args, **kwargs):
        super(PrxPortForFileSave, self).__init__(*args, **kwargs)


# directory open
class PrxPortForDirectoryOpen(AbsPrxPortForStorage):
    PRX_PORT_INPUT_CLS = _input_for_storage.PrxInputForDirectoryOpen

    def __init__(self, *args, **kwargs):
        super(PrxPortForDirectoryOpen, self).__init__(*args, **kwargs)


# directory save
class PrxPortForDirectorySave(AbsPrxPortForStorage):
    PRX_PORT_INPUT_CLS = _input_for_storage.PrxInputForDirectorySave

    def __init__(self, *args, **kwargs):
        super(PrxPortForDirectorySave, self).__init__(*args, **kwargs)