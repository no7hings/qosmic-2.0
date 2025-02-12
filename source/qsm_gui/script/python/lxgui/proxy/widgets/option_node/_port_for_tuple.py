# coding:utf-8
# proxy widgets
from . import _port_base

from ..input import input_for_tuple as _input_for_tuple


# tuple
class AbsPrxPortForTuple(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    PRX_PORT_INPUT_CLS = None

    def __init__(self, *args, **kwargs):
        super(AbsPrxPortForTuple, self).__init__(*args, **kwargs)

    def set_name(self, text):
        super(AbsPrxPortForTuple, self).set_name(text)
        self.get_input_widget()._set_name_text_(text)

    def set_value_type(self, value_type):
        self._prx_port_input.set_value_type(value_type)

    def set_value_size(self, size):
        self._prx_port_input.set_value_size(size)


# integer2
class PrxPortForIntegerTuple(AbsPrxPortForTuple):
    PRX_PORT_INPUT_CLS = _input_for_tuple.PrxInputForIntegerTuple

    def __init__(self, *args, **kwargs):
        super(PrxPortForIntegerTuple, self).__init__(*args, **kwargs)


# float2
class PrxPortForFloatTuple(AbsPrxPortForTuple):
    PRX_PORT_INPUT_CLS = _input_for_tuple.PrxInputForFloatTuple

    def __init__(self, *args, **kwargs):
        super(PrxPortForFloatTuple, self).__init__(*args, **kwargs)