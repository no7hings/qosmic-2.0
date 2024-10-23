# coding:utf-8
import _port_base

from ..input import input_for_choose as _input_for_choose


# constant choose
class PrxPortForConstantChoose(_port_base.AbsPrxPort):
    WIDGET_TYPE = 'enumerate'

    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    PRX_PORT_INPUT_CLS = _input_for_choose.PrxInputForConstantChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortForConstantChoose, self).__init__(*args, **kwargs)

    def get_enumerate_strings(self):
        return self._prx_port_input.get_enumerate_strings()

    def set_options(self, values, *args, **kwargs):
        self._prx_port_input._qt_input_widget._set_choose_values_(values)

    def set_icon_file_as_value(self, value, file_path):
        self._prx_port_input.set_icon_file_as_value(value, file_path)


#  scheme choose
class PrxPortForSchemChoose(_port_base.AbsPrxPortForConstant):
    PRX_PORT_INPUT_CLS = _input_for_choose.PrxInputForSchemeChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortForSchemChoose, self).__init__(*args, **kwargs)
        self._prx_port_input.set_scheme_key(kwargs['scheme_key'])
