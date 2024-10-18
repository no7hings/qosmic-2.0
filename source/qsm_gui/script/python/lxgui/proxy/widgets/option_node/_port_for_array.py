# coding:utf-8
import _port_base

import _input_for_array


# any array
class PrxPortForArray(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_array.PrxInputForArray

    def __init__(self, *args, **kwargs):
        super(PrxPortForArray, self).__init__(*args, **kwargs)

    def append(self, value):
        self._prx_port_input.append(value)


# any array choose
class PrxPortForArrayChoose(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_array.PrxInputForArrayChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortForArrayChoose, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortForArrayChoose, self).set_name(*args, **kwargs)
        self.get_input_widget()._set_name_text_(args[0])

    def append(self, value):
        self._prx_port_input.append(value)