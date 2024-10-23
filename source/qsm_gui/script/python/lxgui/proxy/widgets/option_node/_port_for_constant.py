# coding:utf-8
import _port_base

from ..input import input_for_constant as _input_for_constant


#   text
class PrxPortForText(_port_base.AbsPrxPortForConstant):
    WIDGET_TYPE = 'text'
    PRX_PORT_INPUT_CLS = _input_for_constant.PrxInputForText

    def __init__(self, *args, **kwargs):
        super(PrxPortForText, self).__init__(*args, **kwargs)


#   string
class PrxPortForString(_port_base.AbsPrxPortForConstant):
    WIDGET_TYPE = 'string'
    PRX_PORT_INPUT_CLS = _input_for_constant.PrxInputForString

    def __init__(self, *args, **kwargs):
        super(PrxPortForString, self).__init__(*args, **kwargs)


#   name
class PrxPortForName(_port_base.AbsPrxPortForConstant):
    WIDGET_TYPE = 'name'
    PRX_PORT_INPUT_CLS = _input_for_constant.PrxInputForString

    def __init__(self, *args, **kwargs):
        super(PrxPortForName, self).__init__(*args, **kwargs)
        self.get_input_widget()._set_value_entry_validator_use_as_name_()


#   frames
class PrxPortForFrameString(_port_base.AbsPrxPortForConstant):
    WIDGET_TYPE = 'frames'
    PRX_PORT_INPUT_CLS = _input_for_constant.PrxInputForString

    def __init__(self, *args, **kwargs):
        super(PrxPortForFrameString, self).__init__(*args, **kwargs)
        self._prx_port_input.set_use_as_frames()


#   integer
class PrxPortForInteger(_port_base.AbsPrxPortForConstant):
    WIDGET_TYPE = 'integer'
    PRX_PORT_INPUT_CLS = _input_for_constant.PrxInputForInteger

    def __init__(self, *args, **kwargs):
        super(PrxPortForInteger, self).__init__(*args, **kwargs)


#   float
class PrxPortForFloat(_port_base.AbsPrxPortForConstant):
    WIDGET_TYPE = 'float'
    PRX_PORT_INPUT_CLS = _input_for_constant.PrxInputForFloat

    def __init__(self, *args, **kwargs):
        super(PrxPortForFloat, self).__init__(*args, **kwargs)

