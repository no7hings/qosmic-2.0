# coding:utf-8
import lxbasic.storage as bsc_storage

from .... import core as _gui_core
# qt
from ....qt import core as _qt_core
# qt widgets
from ....qt.widgets import base as _qt_wgt_base
# proxy abstracts
from ... import abstracts as _abstracts

from ....qt.widgets import utility as _qt_wgt_utility


# entry
class AbsPrxInput(_abstracts.AbsPrxWidget):
    QT_INPUT_WIDGET_CLS = None

    QT_H = _gui_core.GuiSize.InputHeight

    def __init__(self, *args, **kwargs):
        super(AbsPrxInput, self).__init__(*args, **kwargs)
        if self.QT_H > 0:
            self.widget.setFixedHeight(self.QT_H)

    def _gui_build_fnc(self):
        self._qt_layout = _qt_wgt_base.QtHBoxLayout(self._qt_widget)
        self._qt_layout.setContentsMargins(0, 0, 0, 0)
        self._qt_layout.setSpacing(2)
        #
        if self.QT_INPUT_WIDGET_CLS is None:
            raise RuntimeError(self.__class__.__name__)
        self._qt_input_widget = self.QT_INPUT_WIDGET_CLS()
        self._qt_layout.addWidget(self._qt_input_widget)
        #
        self._use_as_storage = False

    def get_input_widget(self):
        return self._qt_input_widget

    def add_button(self, widget):
        if isinstance(widget, _qt_core.QtCore.QObject):
            self._qt_layout.addWidget(widget)
        else:
            self._qt_layout.addWidget(widget.widget)

    def get(self):
        raise NotImplementedError()

    def set(self, *args, **kwargs):
        raise NotImplementedError()

    def set_options(self, *args, **kwargs):
        pass

    def set_default(self, *args, **kwargs):
        pass

    def get_default(self):
        pass

    def get_is_default(self):
        return False

    def do_clear(self):
        pass

    def connect_input_changed_to(self, fnc):
        pass

    def connect_user_input_changed_to(self, fnc):
        pass

    def connect_tab_pressed_to(self, fnc):
        pass

    def set_focus_in(self):
        pass

    def set_use_as_storage(self, boolean=True):
        if hasattr(self._qt_input_widget, '_set_entry_use_as_storage_'):
            self._qt_input_widget._set_entry_use_as_storage_(boolean)

    def _set_file_show_(self):
        bsc_storage.StgFileOpt(self.get()).show_in_system()

    def get_use_as_storage(self):
        return self._use_as_storage

    def set_locked(self, boolean):
        pass

    def set_history_key(self, key):
        self._qt_input_widget._set_history_key_(key)

    def pull_history(self):
        return self._qt_input_widget._pull_history_()

    def set_tool_tip(self, *args, **kwargs):
        if hasattr(self._qt_input_widget, '_set_tool_tip_'):
            self._qt_input_widget._set_tool_tip_(args[0], **kwargs)

    def set_height(self, h):
        self._qt_widget.setFixedHeight(h)

    def set_history_button_visible(self, boolean):
        pass

    def set_action_enable(self, boolean):
        self._qt_input_widget._set_action_enable_(boolean)


# any
class AbsPrxInputForConstant(AbsPrxInput):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = None

    def __init__(self, *args, **kwargs):
        super(AbsPrxInputForConstant, self).__init__(*args, **kwargs)
        # self._qt_input_widget.setAlignment(_qt_core.QtCore.Qt.AlignLeft | _qt_core.QtCore.Qt.AlignVCenter)
        #
        self.widget.setFocusProxy(self._qt_input_widget)

    def set_value_type(self, value_type):
        self._qt_input_widget._set_value_type_(value_type)

    def set_use_as_frames(self):
        self._qt_input_widget._set_value_validator_use_as_frames_()

    def set_use_as_rgba(self):
        self._qt_input_widget._set_value_validator_use_as_rgba_()

    def get(self):
        return self._qt_input_widget._get_value_()

    def set(self, raw=None, **kwargs):
        self._qt_input_widget._set_value_(raw)

    def set_default(self, raw, **kwargs):
        self._qt_input_widget._set_value_default_(raw)

    def get_default(self):
        return self._qt_input_widget._get_value_default_()

    def get_is_default(self):
        return self._qt_input_widget._get_value_is_default_()

    def connect_input_changed_to(self, fnc):
        self._qt_input_widget._connect_input_entry_value_changed_to_(fnc)

    def set_maximum(self, value):
        self._qt_input_widget._set_value_maximum_(value)

    def get_maximum(self):
        return self._qt_input_widget._get_value_maximum_()

    def set_minimum(self, value):
        self._qt_input_widget._set_value_minimum_(value)

    def get_minimum(self):
        return self._qt_input_widget._get_value_minimum_()

    def set_range(self, maximum, minimum):
        self._qt_input_widget._set_value_range_(maximum, minimum)

    def get_range(self):
        return self._qt_input_widget._get_value_range_()

    def set_locked(self, boolean):
        self._qt_input_widget._set_entry_enable_(not boolean)


# proxy
# noinspection PyMethodMayBeStatic
class AbsPrxInputExtra(_abstracts.AbsPrxWidget):
    PRX_INPUT_CLS = None

    def __init__(self, *args, **kwargs):
        super(AbsPrxInputExtra, self).__init__(*args, **kwargs)

    def _gui_build_fnc(self):
        self._qt_layout = _qt_wgt_base.QtHBoxLayout(self._qt_widget)
        self._qt_layout.setContentsMargins(0, 0, 0, 0)
        self._qt_layout.setSpacing(2)
        #
        self._prx_input = self.PRX_INPUT_CLS()
        self._qt_layout.addWidget(self._prx_input.widget)

    def get(self):
        raise NotImplementedError()

    def set(self, raw=None, **kwargs):
        raise NotImplementedError()

    def get_default(self):
        return None

    def set_default(self, raw=None, **kwargs):
        pass

    def get_is_default(self):
        return False

    def set_tool_tip(self, *args, **kwargs):
        if hasattr(self._prx_input._qt_widget, '_set_tool_tip_'):
            if args[0]:
                self._prx_input._qt_widget._set_tool_tip_(args[0], **kwargs)

    def do_clear(self):
        pass

    def connect_input_changed_to(self, fnc):
        pass

    def set_locked(self, boolean):
        pass

    def set_height(self, h):
        self._qt_widget.setFixedHeight(h)

    def connect_tab_pressed_to(self, fnc):
        pass
