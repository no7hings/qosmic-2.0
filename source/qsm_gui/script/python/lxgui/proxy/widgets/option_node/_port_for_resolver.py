# coding:utf-8
# proxy widgets
import _port_base

import _input_for_resolver


class PrxPortForRsvChoose(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_resolver.PrxInputForRsvEntity

    def __init__(self, *args, **kwargs):
        super(PrxPortForRsvChoose, self).__init__(*args, **kwargs)


#   project choose
class PrxPortForRsvProjectChoose(_port_base.AbsPrxPortForConstant):
    PRX_PORT_INPUT_CLS = _input_for_resolver.PrxInputForRsvProject

    def __init__(self, *args, **kwargs):
        super(PrxPortForRsvProjectChoose, self).__init__(*args, **kwargs)

    def get_histories(self):
        return self.entry_widget.get_histories()