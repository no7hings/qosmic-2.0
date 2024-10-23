# coding:utf-8
# proxy widgets
import _port_base

from ..input import input_for_extra as _input_for_extra


#  boolean
class PrxPortForBoolean(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = True
    PRX_PORT_INPUT_CLS = _input_for_extra.PrxInputForBoolean

    def __init__(self, *args, **kwargs):
        super(PrxPortForBoolean, self).__init__(*args, **kwargs)

    def set_name(self, text):
        self.get_input_widget()._set_name_text_(text)


# rgba
class PrxPortForRgbaChoose(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    PRX_PORT_INPUT_CLS = _input_for_extra.PrxInputForRgbaChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortForRgbaChoose, self).__init__(*args, **kwargs)
        self._prx_port_input.set_use_as_rgba()


# icon choose
class PrxPortForIconChoose(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_extra.PrxInputForIconChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortForIconChoose, self).__init__(*args, **kwargs)