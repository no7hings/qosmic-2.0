# coding:utf-8
from . import _port_base

from ..input import input_for_tag as _input_for_tag


# capsule string
class PrxPortForTagString(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_tag.PrxInputForTag

    def __init__(self, *args, **kwargs):
        super(PrxPortForTagString, self).__init__(*args, **kwargs)

        self.get_input_widget()._set_value_type_(str)


# capsule strings
class PrxPortForTagStrings(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_tag.PrxInputForTag

    def __init__(self, *args, **kwargs):
        super(PrxPortForTagStrings, self).__init__(*args, **kwargs)
        self.get_input_widget()._set_value_type_(list)
