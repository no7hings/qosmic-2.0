# coding:utf-8
import _port_base

import _input_for_script


class PrxPortForScript(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_script.PrxInputForScript

    def __init__(self, *args, **kwargs):
        super(PrxPortForScript, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortForScript, self).set_name(*args, **kwargs)
        self.get_input_widget()._get_entry_widget_()._set_empty_text_(args[0])

    def set_external_editor_ext(self, ext):
        self._prx_port_input.set_external_editor_ext(ext)
