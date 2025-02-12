# coding:utf-8
from . import _port_base

from ..input import input_for_stg_array as _input_for_stg_array


# storage array
#   many files open
class PrxPortForFilesOpen(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_stg_array.PrxInputForFilesOpen

    def __init__(self, *args, **kwargs):
        super(PrxPortForFilesOpen, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortForFilesOpen, self).set_name(*args, **kwargs)
        self.get_input_widget()._set_name_text_(args[0])
        self.get_input_widget()._get_entry_widget_()._set_empty_text_(args[0])

    def set_history_button_visible(self, boolean):
        self._prx_port_input.set_history_button_visible(boolean)

    def set_ext_includes(self, *args, **kwargs):
        self._prx_port_input.set_ext_includes(*args, **kwargs)


#   many directories open
class PrxPortForDirectoriesOpen(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_stg_array.PrxInputForDirectoriesOpen

    def __init__(self, *args, **kwargs):
        super(PrxPortForDirectoriesOpen, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortForDirectoriesOpen, self).set_name(*args, **kwargs)
        self.get_input_widget()._set_name_text_(args[0])
        self.get_input_widget()._get_entry_widget_()._set_empty_text_(args[0])

    def set_history_button_visible(self, boolean):
        self._prx_port_input.set_history_button_visible(boolean)


#   many medias open
class PrxPortForMediasOpen(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_stg_array.PrxInputForMediasOpen

    def __init__(self, *args, **kwargs):
        super(PrxPortForMediasOpen, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortForMediasOpen, self).set_name(*args, **kwargs)
        self.get_input_widget()._set_name_text_(args[0])
        self.get_input_widget()._get_entry_widget_()._set_empty_text_(args[0])

    def set_ext_filter(self, ext_filter):
        self._prx_port_input.set_ext_filter(ext_filter)

    def set_ext_includes(self, *args, **kwargs):
        self._prx_port_input.set_ext_includes(*args, **kwargs)
