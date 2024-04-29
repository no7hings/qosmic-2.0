# coding:utf-8
import functools

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core
# gui
from ... import core as gui_core
# qt widgets
from ...qt.widgets import base as gui_qt_wgt_base

from ...qt.widgets import utility as gui_qt_wgt_utility
# proxy widgets
from . import port_base as _port_base

from . import input_for_port as _input_for_port


# port =============================================================================================================== #
class AbsPrxPortBaseDef(object):
    ENTRY_TYPE = 'custom'

    Status = gui_core.GuiProcessStatus
    ProcessStatus = gui_core.GuiProcessStatus
    ShowStatus = gui_core.GuiShowStatus
    ValidationStatus = gui_core.GuiValidationStatus

    def _init_prx_port_def_(self, category, port_path, label=None):
        self._prx_node = None
        self._prx_group = None
        #
        self._category = category
        self._port_path = port_path
        self._name = self._port_path.split('.')[-1]

        self.__is_pseudo_root = False
        #
        if label is not None:
            self._label = label
        else:
            self._label = bsc_core.RawStrUnderlineOpt(self._name).to_prettify(capitalize=False)

    def _set_use_as_pseudo_root(self):
        self.__is_pseudo_root = True

    def _set_node(self, obj):
        self._prx_node = obj

    def get_node(self):
        return self._prx_node

    def set_group(self, obj):
        self._prx_group = obj

    def get_group(self):
        return self._prx_group

    def get_node_path(self):
        return self.get_node().get_path()

    def get_category(self):
        return self._category

    category = property(get_category)

    def get_type(self):
        return self.ENTRY_TYPE

    type = property(get_type)

    def get_name(self):
        return self._name

    name = property(get_name)

    def get_path(self):
        return '{}.{}'.format(
            self.get_node_path(),
            self.get_port_path()
        )

    path = property(get_path)

    def get_port_path(self):
        return self._port_path

    port_path = property(get_port_path)

    def get_group_path(self):
        return bsc_core.PthPortOpt(
            self.get_port_path()
        ).get_parent_path()

    group_path = property(get_group_path)

    def get_label(self):
        return self._label

    label = property(get_label)

    def get_is_top_level(self):
        return bsc_core.PthPortOpt(
            self._port_path
        ).get_is_top_level()

    def get_is_pseudo_root(self):
        return self.__is_pseudo_root is True

    def get_is_node(self):
        return self == self.get_node()

    def get_children(self):
        node = self.get_node()
        port_path = self.get_port_path()
        port_paths = node.get_port_paths()
        if self.get_is_pseudo_root():
            _ = [i for i in port_paths if '.' not in i]
        else:
            _ = bsc_core.PthNodeMtd.find_dag_child_paths(
                port_path, port_paths, pathsep='.'
            )
        return node._get_ports_(_)

    def set_visible(self, *args, **kwargs):
        pass

    def set_visible_condition(self, condition):
        def visible_fnc_():
            _operator = condition.get('operator')
            _value_cdt = condition.get('value')
            _value = p.get()
            if _operator == 'in':
                self.set_visible(_value_cdt in _value)
            elif _operator == 'match_one':
                self.set_visible(_value in _value_cdt)
            elif _operator == 'is':
                self.set_visible(_value_cdt == _value)

        if condition:
            p = self.get_node().get_port(condition.get('port').replace('/', '.'))
            if p is not None:
                p.connect_input_changed_to(visible_fnc_)
                visible_fnc_()
            else:
                bsc_log.Log.trace_method_warning(
                    'visible condition connect',
                    'port="{}" is non-exists'.format(condition.get('port'))
                )

    def connect_input_changed_to(self, fnc):
        pass

    def connect_tab_pressed_to(self, fnc):
        pass

    def set_focus_in(self):
        pass

    def __str__(self):
        return '{}(path="{}")'.format(
            self.get_type(), self.get_path()
        )

    def __repr__(self):
        return self.__str__()


# port
class _AbsPrxPortBase(AbsPrxPortBaseDef):
    ENTRY_TYPE = 'custom'
    ENABLE_CLS = None
    LABEL_CLS = None
    LABEL_HIDED = False
    KEY_HIDE = False
    PRX_PORT_INPUT_CLS = None

    # noinspection PyUnusedLocal
    def __init__(
        self, port_path, label=None, enable=None, default_value=None, join_to_next=False,
        scheme_key=None,
        node_widget=None
    ):
        self._init_prx_port_def_('value', port_path, label)
        #
        self._key = None
        #
        if isinstance(enable, bool):
            self._use_enable = enable
        else:
            self._use_enable = False
        #
        self._prx_port_enable = self.ENABLE_CLS(node_widget)
        self._prx_port_enable.set_hide()
        # gui
        self._prx_port_label = self.LABEL_CLS(node_widget)
        self._prx_port_label.set_hide()
        self._prx_port_label.set_name(self._label)
        #
        self._prx_port_input = self.PRX_PORT_INPUT_CLS(node_widget)
        #
        if default_value is not None:
            self._prx_port_input.set(default_value)
        #
        self._layout = None
        #
        self._join_to_next_flag = join_to_next
        self._join_layout = None
        self._key_widget = None
        #
        self._custom_widget = None
        #
        self.set_name(self.label)

        self.connect_input_changed_to(
            self.set_changed_update
        )

        self._main_qt_widget = None

    def set_main_widget(self, widget):
        self._main_qt_widget = widget

    def set_node_widget(self, widget):
        self._prx_port_enable.set_parent_widget(
            widget
        )
        self._prx_port_input.set_parent_widget(
            widget
        )
        self._prx_port_input.set_parent_widget(
            widget
        )

    def get_input_widget(self):
        return self._prx_port_input.get_input_widget()

    @property
    def label(self):
        return self._label

    @property
    def label_widget(self):
        return self._prx_port_label

    @property
    def entry_widget(self):
        return self._prx_port_input

    def set_label_visible(self, boolean):
        self._prx_port_label.set_visible(boolean)

    def set_key(self, key):
        self._key = key

    def get_key(self):
        return self._key

    def set_name(self, name):
        self._prx_port_label.set_name(name)
        group = self.get_group()
        if group:
            group.update_children_name_width()

    def set_label(self, text):
        if text:
            self.set_name(text)
            self._label = text

    def _update_sub_name(self):
        if hasattr(self.get_input_widget(), '_set_name_text_'):
            self.get_input_widget()._set_name_text_(self.label)

    def set_enable(self, boolean):
        if boolean is not None:
            if isinstance(boolean, bool):
                self._prx_port_enable.set_show()
                # self._prx_port_enable.set(boolean)
        else:
            self._prx_port_enable.set_hide()

    def set_use_enable(self, boolean):
        self._use_enable = boolean
        if boolean is not None:
            if isinstance(boolean, bool):
                if self._use_enable is True:
                    self._prx_port_enable.set_show()
                # self._prx_port_enable.set(boolean)
        else:
            self._prx_port_enable.set_hide()

    def get_use_enable(self):
        return self._use_enable

    def set_name_width(self, w):
        self.label_widget.set_width(w)

    def set(self, raw=None, **kwargs):
        self._prx_port_input.set(raw, **kwargs)
        #
        self.set_changed_update()

    def set_default(self, raw, **kwargs):
        self._prx_port_input.set_default(raw, **kwargs)
        #
        self.set_changed_update()

    def get_default(self):
        return self._prx_port_input.get_default()

    def set_changed_update(self):
        if self.get_default() is not None:
            if self._prx_port_input.get_is_default() is False:
                self._prx_port_enable.set(True)
            else:
                self._prx_port_enable.set(False)

    def set_value(self, *args, **kwargs):
        self.set(*args, **kwargs)

    def set_choose_values(self, *args, **kwargs):
        self._prx_port_input.set_choose_values(*args, **kwargs)

    def append(self, raw):
        if hasattr(self._prx_port_input, 'append'):
            self._prx_port_input.append(raw)

    def set_clear(self):
        self._prx_port_input.set_clear()

    def set_reset(self):
        default = self.get_default()
        if default is not None:
            self.set(default)

    def set_options(self, values, names=None):
        self._prx_port_input.set_options(values, names)

    def set_tool_tip(self, *args, **kwargs):
        kwargs['name'] = 'entry as "{}"'.format(
            self.ENTRY_TYPE,
        )
        kwargs['name'] = self.get_port_path()
        self._prx_port_input.set_tool_tip(*args, **kwargs)

    def get(self):
        return self._prx_port_input.get()

    def connect_input_changed_to(self, fnc):
        return self._prx_port_input.connect_input_changed_to(fnc)

    def connect_tab_pressed_to(self, fnc):
        return self._prx_port_input.connect_tab_pressed_to(fnc)

    def set_focus_in(self):
        self._prx_port_input.set_focus_in()

    def set_use_as_storage(self, boolean=True):
        self._prx_port_input.set_use_as_storage(boolean)

    def _set_layout_(self, layout):
        self._layout = layout

    def _get_layout_(self):
        return self._layout

    # join to next
    def _set_join_to_next_flag(self, boolean):
        self._join_to_next_flag = boolean

    def _get_join_next_flag(self):
        return self._join_to_next_flag

    def _register_join_layout(self, layout):
        self._join_layout = layout

    def _get_join_layout(self):
        return self._join_layout

    def _set_key_widget_(self, widget):
        self._key_widget = widget

    def set_menu_data(self, raw):
        self._prx_port_input.set_menu_data(raw)

    def to_custom_widget(self, label_width=80):
        if self._custom_widget is not None:
            return self._custom_widget
        else:
            widget = gui_qt_wgt_utility.QtTranslucentWidget()
            layout = gui_qt_wgt_base.QtHBoxLayout(widget)
            label = self.label_widget
            label.set_width(label_width)
            layout.addWidget(label.widget)
            entry = self._prx_port_input
            layout.addWidget(entry.widget)
            self._custom_widget = widget
            return self._custom_widget

    def set_locked(self, *args, **kwargs):
        self._prx_port_input.set_locked(*args, **kwargs)

    def set_history_key(self, key):
        self._prx_port_input.set_history_key(key)

    def pull_history_latest(self):
        return self._prx_port_input.pull_history_latest()

    def update_exclusive_set(self, ps):
        def exclusive_fnc_(p_cur_):
            for _i_p in ps:
                if _i_p == p_cur_:
                    self.get_node().set(_i_p, True)
                else:
                    self.get_node().set(_i_p, False)

        for i_p in ps:
            i_port = self.get_node().get_port(i_p)
            i_qt_widget = i_port._prx_port_input._qt_input_widget
            # use radio icon
            i_qt_widget._set_check_icon_file_paths_(
                gui_core.GuiIcon.get('radio_unchecked'),
                gui_core.GuiIcon.get('radio_checked')
            )
            i_qt_widget.user_check_clicked.connect(
                functools.partial(
                    exclusive_fnc_, i_p
                )
            )

    def set_height(self, h):
        self._prx_port_input.set_height(h)

    def set_visible(self, boolean):
        if self._main_qt_widget is not None:
            self._main_qt_widget.setVisible(boolean)


# constant
class PrxPortAsConstant(_AbsPrxPortBase):
    ENTRY_TYPE = 'constant'
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsConstant

    def __init__(self, *args, **kwargs):
        super(PrxPortAsConstant, self).__init__(*args, **kwargs)

    def set_locked(self, boolean):
        self._prx_port_input.set_locked(boolean)


#   text
class PrxPortAsText(PrxPortAsConstant):
    ENTRY_TYPE = 'text'
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsText

    def __init__(self, *args, **kwargs):
        super(PrxPortAsText, self).__init__(*args, **kwargs)


#   string
class PrxPortAsString(PrxPortAsConstant):
    ENTRY_TYPE = 'string'
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsString

    def __init__(self, *args, **kwargs):
        super(PrxPortAsString, self).__init__(*args, **kwargs)


#   name
class PrxPortAsName(PrxPortAsConstant):
    ENTRY_TYPE = 'name'
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsString

    def __init__(self, *args, **kwargs):
        super(PrxPortAsName, self).__init__(*args, **kwargs)
        self.get_input_widget()._set_value_entry_validator_use_as_name_()


#   frames
class PrxPortAsFrames(PrxPortAsConstant):
    ENTRY_TYPE = 'frames'
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsString

    def __init__(self, *args, **kwargs):
        super(PrxPortAsFrames, self).__init__(*args, **kwargs)
        self._prx_port_input.set_use_as_frames()


#   integer
class PrxPortForInteger(PrxPortAsConstant):
    ENTRY_TYPE = 'integer'
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsInteger

    def __init__(self, *args, **kwargs):
        super(PrxPortForInteger, self).__init__(*args, **kwargs)


#   boolean
class PrxPortAsBoolean(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = True
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsBoolean

    def __init__(self, *args, **kwargs):
        super(PrxPortAsBoolean, self).__init__(*args, **kwargs)

    def set_name(self, text):
        self.get_input_widget()._set_name_text_(text)


#   float
class PrxPortAsFloat(PrxPortAsConstant):
    ENTRY_TYPE = 'float'
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsFloat

    def __init__(self, *args, **kwargs):
        super(PrxPortAsFloat, self).__init__(*args, **kwargs)


# storage
class PrxPortAsStorage(PrxPortAsConstant):
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsStorage

    def __init__(self, *args, **kwargs):
        super(PrxPortAsStorage, self).__init__(*args, **kwargs)

    def set_ext_filter(self, ext_filter):
        self._prx_port_input.set_ext_filter(ext_filter)

    def set_ext_includes(self, ext_includes):
        self._prx_port_input.set_ext_includes(ext_includes)

    def set_history_key(self, key):
        self._prx_port_input.set_history_key(key)


#   file open
class PrxPortAsFileOpen(PrxPortAsStorage):
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsFileOpen

    def __init__(self, *args, **kwargs):
        super(PrxPortAsFileOpen, self).__init__(*args, **kwargs)


#   file save
class PrxPortAsFileSave(PrxPortAsStorage):
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsFileSave

    def __init__(self, *args, **kwargs):
        super(PrxPortAsFileSave, self).__init__(*args, **kwargs)


#   directory open
class PrxPortAsDirectoryOpen(PrxPortAsStorage):
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsDirectoryOpen

    def __init__(self, *args, **kwargs):
        super(PrxPortAsDirectoryOpen, self).__init__(*args, **kwargs)


#   directory save
class PrxPortAsDirectorySave(PrxPortAsStorage):
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsDirectorySave

    def __init__(self, *args, **kwargs):
        super(PrxPortAsDirectorySave, self).__init__(*args, **kwargs)


# resolver
#   project choose
class PrxPortAsRsvProjectChoose(PrxPortAsConstant):
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsRsvProject

    def __init__(self, *args, **kwargs):
        super(PrxPortAsRsvProjectChoose, self).__init__(*args, **kwargs)

    def get_histories(self):
        return self.entry_widget.get_histories()


#  scheme choose
class PrxPortAsSchemChoose(PrxPortAsConstant):
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsSchemeWithChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortAsSchemChoose, self).__init__(*args, **kwargs)
        self._prx_port_input.set_scheme_key(kwargs['scheme_key'])


class PrxPortAsConstantChoose(_AbsPrxPortBase):
    ENTRY_TYPE = 'enumerate'
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsConstantWithChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortAsConstantChoose, self).__init__(*args, **kwargs)

    def get_enumerate_strings(self):
        return self._prx_port_input.get_enumerate_strings()

    def set_icon_file_as_value(self, value, file_path):
        self._prx_port_input.set_icon_file_as_value(value, file_path)


# capsule
class PrxPortAsCapsuleString(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsCapsule

    def __init__(self, *args, **kwargs):
        super(PrxPortAsCapsuleString, self).__init__(*args, **kwargs)

        self.get_input_widget()._set_value_type_(str)


class PrxPortAsCapsuleStrings(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsCapsule

    def __init__(self, *args, **kwargs):
        super(PrxPortAsCapsuleStrings, self).__init__(*args, **kwargs)
        self.get_input_widget()._set_value_type_(list)


class PrxPortAsScript(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsScript

    def __init__(self, *args, **kwargs):
        super(PrxPortAsScript, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortAsScript, self).set_name(*args, **kwargs)
        self.get_input_widget()._get_entry_widget_()._set_empty_text_(args[0])

    def set_external_editor_ext(self, ext):
        self._prx_port_input.set_external_editor_ext(ext)


class PrxPortAsTuple(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsTuple

    def __init__(self, *args, **kwargs):
        super(PrxPortAsTuple, self).__init__(*args, **kwargs)

    def set_value_type(self, value_type):
        self._prx_port_input.set_value_type(value_type)

    def set_value_size(self, size):
        self._prx_port_input.set_value_size(size)


class PrxPortForIntegerTuple(PrxPortAsTuple):
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsIntegerTuple

    def __init__(self, *args, **kwargs):
        super(PrxPortForIntegerTuple, self).__init__(*args, **kwargs)


class PrxPortForFloatTuple(PrxPortAsTuple):
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsFloatTuple

    def __init__(self, *args, **kwargs):
        super(PrxPortForFloatTuple, self).__init__(*args, **kwargs)


class PrxPortAsRgbaChoose(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsRgbaChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortAsRgbaChoose, self).__init__(*args, **kwargs)
        self._prx_port_input.set_use_as_rgba()


class PrxPortAsButton(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    KEY_HIDE = True
    LABEL_HIDED = True
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsPressButton

    def __init__(self, *args, **kwargs):
        super(PrxPortAsButton, self).__init__(*args, **kwargs)

    def set_name(self, text):
        self.get_input_widget()._set_name_text_(text)

    def set_option_enable(self, boolean):
        self._prx_port_input.set_option_enable(boolean)

    def set_icon(self, icon_key):
        self._prx_port_input.set_icon_by_file(
            gui_core.GuiIcon.get(icon_key)
        )

    def set_status(self, status):
        self.get_input_widget()._set_status_(status)

    def set_locked(self, boolean):
        self.get_input_widget()._set_action_enable_(not boolean)


class PrxPortAsCheckButton(PrxPortAsButton):
    def __init__(self, *args, **kwargs):
        super(PrxPortAsButton, self).__init__(*args, **kwargs)
        self.get_input_widget()._set_check_action_enable_(True)

    def set_checked(self, boolean):
        self.get_input_widget()._set_checked_(boolean)

    def get_is_checked(self):
        return self.get_input_widget()._get_is_checked_()

    def execute(self):
        self.get_input_widget()._execute_()


class PrxSubProcessPort(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    KEY_HIDE = True
    LABEL_HIDED = True
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsSubProcessButton

    def __init__(self, *args, **kwargs):
        super(PrxSubProcessPort, self).__init__(*args, **kwargs)
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

    def initialization(self, count, status=gui_core.GuiProcessStatus.Started):
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
            gui_core.GuiIcon.get(icon_key)
        )


class PrxValidatorPort(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    KEY_HIDE = True
    LABEL_HIDED = True
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsValidationButton

    def __init__(self, *args, **kwargs):
        super(PrxValidatorPort, self).__init__(*args, **kwargs)
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


class PrxRsvObjChoosePort(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsResolverEntity

    def __init__(self, *args, **kwargs):
        super(PrxRsvObjChoosePort, self).__init__(*args, **kwargs)


# storage array
#   many files open
class PrxPortAsFilesOpen(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsFilesOpen

    def __init__(self, *args, **kwargs):
        super(PrxPortAsFilesOpen, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortAsFilesOpen, self).set_name(*args, **kwargs)
        self.get_input_widget()._set_name_text_(args[0])
        self.get_input_widget()._get_entry_widget_()._set_empty_text_(args[0])

    def set_history_button_visible(self, boolean):
        self._prx_port_input.set_history_button_visible(boolean)

    def set_ext_includes(self, *args, **kwargs):
        self._prx_port_input.set_ext_includes(*args, **kwargs)


#   many directories open
class PrxPortAsDirectoriesOpen(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsDirectoriesOpen

    def __init__(self, *args, **kwargs):
        super(PrxPortAsDirectoriesOpen, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortAsDirectoriesOpen, self).set_name(*args, **kwargs)
        self.get_input_widget()._set_name_text_(args[0])
        self.get_input_widget()._get_entry_widget_()._set_empty_text_(args[0])

    def set_history_button_visible(self, boolean):
        self._prx_port_input.set_history_button_visible(boolean)


#   many medias open
class PrxPortAsMediasOpen(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsMediasOpen

    def __init__(self, *args, **kwargs):
        super(PrxPortAsMediasOpen, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortAsMediasOpen, self).set_name(*args, **kwargs)
        self.get_input_widget()._set_name_text_(args[0])
        self.get_input_widget()._get_entry_widget_()._set_empty_text_(args[0])

    def set_ext_filter(self, ext_filter):
        self._prx_port_input.set_ext_filter(ext_filter)

    def set_ext_includes(self, *args, **kwargs):
        self._prx_port_input.set_ext_includes(*args, **kwargs)


# icon choose
class PrxPortAsIconChoose(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsIconWithChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortAsIconChoose, self).__init__(*args, **kwargs)


# any array
class PrxPortForValueArray(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsArray

    def __init__(self, *args, **kwargs):
        super(PrxPortForValueArray, self).__init__(*args, **kwargs)

    def append(self, value):
        self._prx_port_input.append(value)


# any array choose
class PrxPortForValueArrayAsChoose(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsArrayWithChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortForValueArrayAsChoose, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortForValueArrayAsChoose, self).set_name(*args, **kwargs)
        self.get_input_widget()._set_name_text_(args[0])

    def append(self, value):
        self._prx_port_input.append(value)


# shotgun
class PrxPortAsShotgunEntity(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsShotgunEntityWithChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortAsShotgunEntity, self).__init__(*args, **kwargs)

    def get_stg_entity(self):
        return self._prx_port_input.get_stg_entity()

    def set_name(self, *args, **kwargs):
        super(PrxPortAsShotgunEntity, self).set_name(*args, **kwargs)
        self.get_input_widget()._set_name_text_(args[0])

    def append(self, value):
        self._prx_port_input.append(value)

    def set_shotgun_entity_kwargs(self, *args, **kwargs):
        self._prx_port_input.set_shotgun_entity_kwargs(*args, **kwargs)

    def run_as_thread(self, cache_fnc, build_fnc, post_fnc):
        self._prx_port_input.run_as_thread(
            cache_fnc, build_fnc, post_fnc
        )


class PrxPortAsShotgunEntities(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsShotgunEntitiesWithChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortAsShotgunEntities, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortAsShotgunEntities, self).set_name(*args, **kwargs)
        self.get_input_widget()._set_name_text_(args[0])
        self.get_input_widget()._get_entry_widget_()._set_empty_text_(args[0])

    def append(self, value):
        self._prx_port_input.append(value)

    def set_shotgun_entity_kwargs(self, *args, **kwargs):
        self._prx_port_input.set_shotgun_entity_kwargs(*args, **kwargs)

    def run_as_thread(self, cache_fnc, build_fnc, post_fnc):
        self._prx_port_input.run_as_thread(
            cache_fnc, build_fnc, post_fnc
        )


class PrxNodeListViewPort(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsNodes

    def __init__(self, *args, **kwargs):
        super(PrxNodeListViewPort, self).__init__(*args, **kwargs)

    def get_all(self):
        return self._prx_port_input.get_all()

    def set_checked_by_include_paths(self, paths):
        self._prx_port_input.set_checked_by_include_paths(paths)

    def set_unchecked_by_include_paths(self, paths):
        self._prx_port_input.set_unchecked_by_include_paths(paths)

    def set_all_items_checked(self, boolean):
        self._prx_port_input.set_all_items_checked(boolean)

    def get_prx_tree(self):
        return self._prx_port_input._prx_input


class PrxNodeTreeViewPort(PrxNodeListViewPort):
    def __init__(self, *args, **kwargs):
        super(PrxNodeTreeViewPort, self).__init__(*args, **kwargs)

        self._prx_port_input.set_view_mode('tree')


class PrxPortAsFileList(_AbsPrxPortBase):
    ENABLE_CLS = _port_base.PrxPortStatus
    LABEL_CLS = _port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = _input_for_port.PrxInputAsFiles

    def __init__(self, *args, **kwargs):
        super(PrxPortAsFileList, self).__init__(*args, **kwargs)

    def restore(self):
        self._prx_port_input.restore()

    def get_all(self, *args, **kwargs):
        return self._prx_port_input.get_all(*args, **kwargs)

    def set_root(self, path):
        self._prx_port_input.set_root(path)

    def set_checked_by_include_paths(self, paths):
        self._prx_port_input.set_checked_by_include_paths(paths)

    def set_unchecked_by_include_paths(self, paths):
        self._prx_port_input.set_unchecked_by_include_paths(paths)

    def set_all_items_checked(self, boolean):
        self._prx_port_input.set_all_items_checked(boolean)

    def get_prx_tree(self):
        return self._prx_port_input._prx_input

    def connect_refresh_action_for(self, fnc):
        self._prx_port_input.connect_refresh_action_for(fnc)


# file tree
class PrxPortAsFileTree(PrxPortAsFileList):
    def __init__(self, *args, **kwargs):
        super(PrxPortAsFileTree, self).__init__(*args, **kwargs)
        self._prx_port_input.set_view_mode('tree')