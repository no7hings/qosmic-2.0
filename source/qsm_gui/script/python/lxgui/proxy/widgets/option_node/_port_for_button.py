# coding:utf-8
# gui
from .... import core as _gui_core

import _port_base

from ..input import input_for_button as _input_for_button


class PrxPortForPressButton(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    KEY_HIDE = True
    LABEL_HIDED = True
    PRX_PORT_INPUT_CLS = _input_for_button.PrxInputForPressButton

    def __init__(self, *args, **kwargs):
        super(PrxPortForPressButton, self).__init__(*args, **kwargs)

    def set_name(self, text):
        self.get_input_widget()._set_name_text_(text)

    def set_option_enable(self, boolean):
        self._prx_port_input.set_option_enable(boolean)

    def set_menu_enable(self, boolean):
        self._prx_port_input.set_menu_enable(boolean)

    def set_icon(self, icon_key):
        self._prx_port_input.set_icon_by_file(
            _gui_core.GuiIcon.get(icon_key)
        )

    def set_name_icon_text(self, text):
        self._prx_port_input.set_name_icon_text(text)

    def set_status(self, status):
        self.get_input_widget()._set_status_(status)

    def set_sub_name(self, text):
        self.get_input_widget()._set_sub_name_text_(text)

    def set_locked(self, boolean):
        self.get_input_widget()._set_action_enable_(not boolean)


class PrxPortForCheckButton(PrxPortForPressButton):
    def __init__(self, *args, **kwargs):
        super(PrxPortForCheckButton, self).__init__(*args, **kwargs)
        self.get_input_widget()._set_check_action_enable_(True)

    def set_checked(self, boolean):
        self.get_input_widget()._set_checked_(boolean)

    def get_is_checked(self):
        return self.get_input_widget()._is_checked_()

    def execute(self):
        self.get_input_widget()._execute_()


class PrxPortForSpcButton(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    KEY_HIDE = True
    LABEL_HIDED = True
    PRX_PORT_INPUT_CLS = _input_for_button.PrxInputForSpcButton

    def __init__(self, *args, **kwargs):
        super(PrxPortForSpcButton, self).__init__(*args, **kwargs)
        self.label_widget.widget._set_name_text_('')
        self.get_input_widget()._set_name_text_(
            self.label
        )

        self._is_stopped = False

        self.set_stop_connect_to(
            self.set_stopped
        )

    def set_name(self, text):
        self.get_input_widget()._set_name_text_(text)

    def set_status(self, status):
        widget = self.get_input_widget()
        widget.status_changed.emit(status)

    def set_statuses(self, statuses):
        self.get_input_widget()._set_sub_process_statuses_(statuses)

    def initialization(self, count, status=_gui_core.GuiProcessStatus.Waiting):
        self.get_input_widget()._initialization_sub_process_(count, status)

    def restore_all(self):
        self.get_input_widget()._restore_sub_process_()

    def set_status_at(self, index, status):
        widget = self.get_input_widget()
        widget.rate_status_update_at.emit(index, status)

    def set_finished_at(self, index, status):
        widget = self.get_input_widget()
        widget.rate_finished_at.emit(index, status)

    def connect_finished_to(self, fnc):
        widget = self.get_input_widget()
        widget._connect_sub_process_finished_to_(fnc)

    def set_stop_connect_to(self, fnc):
        self._prx_port_input.set_stop_connect_to(fnc)

    def set_stopped(self, boolean=True):
        self._is_stopped = boolean
        # self.restore_all()

    def get_is_started(self):
        return self.get_input_widget()._get_sub_process_is_started_()

    def get_is_stopped(self):
        return self._is_stopped

    def set_icon(self, icon_key):
        self._prx_port_input.set_icon_by_file(
            _gui_core.GuiIcon.get(icon_key)
        )


class PrxPortForValidateButton(_port_base.AbsPrxPort):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    KEY_HIDE = True
    LABEL_HIDED = True
    PRX_PORT_INPUT_CLS = _input_for_button.PrxInputForValidateButton

    def __init__(self, *args, **kwargs):
        super(PrxPortForValidateButton, self).__init__(*args, **kwargs)
        self.label_widget.widget._set_name_text_('')
        self.get_input_widget()._set_name_text_(
            self.label
        )

    def set_name(self, text):
        self.get_input_widget()._set_name_text_(text)

    def set_status(self, status):
        self.get_input_widget()._set_status_(status)

    def set_statuses(self, statuses):
        self.get_input_widget()._set_validator_statuses_(statuses)

    def restore_all(self):
        self.get_input_widget()._restore_validator_()

    def set_status_at(self, index, status):
        self.get_input_widget()._set_validator_status_at_(index, status)