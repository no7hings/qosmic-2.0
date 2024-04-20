# coding:utf-8
import functools

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxuniverse.abstracts as unr_abstracts
# gui
from ... import core as gui_core
# qt
from ...qt import core as gui_qt_core
# qt widgets
from ...qt.widgets import base as gui_qt_wgt_base

from ...qt.widgets import utility as gui_qt_wgt_utility

from ...qt.widgets import split as gui_qt_wgt_split
# proxy abstracts
from .. import abstracts as gui_prx_abstracts
# proxy widgets
from . import port_base as gui_prx_wgt_port_base

from . import input_for_port as gui_prx_wgt_input_for_port

from . import container as gui_prx_wgt_container


# port =============================================================================================================== #
class AbsPrxPortBaseDef(object):
    ENTRY_TYPE = 'custom'

    Status = gui_core.GuiStatus
    ProcessStatus = gui_core.GuiStatus
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

    def set_option(self, value):
        self._prx_port_input.set_option(value)

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

    #
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
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsConstant

    def __init__(self, *args, **kwargs):
        super(PrxPortAsConstant, self).__init__(*args, **kwargs)

    def set_locked(self, boolean):
        self._prx_port_input.set_locked(boolean)


#   text
class PrxPortAsText(PrxPortAsConstant):
    ENTRY_TYPE = 'text'
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsText

    def __init__(self, *args, **kwargs):
        super(PrxPortAsText, self).__init__(*args, **kwargs)


#   string
class PrxPortAsString(PrxPortAsConstant):
    ENTRY_TYPE = 'string'
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsString

    def __init__(self, *args, **kwargs):
        super(PrxPortAsString, self).__init__(*args, **kwargs)


#   name
class PrxPortAsName(PrxPortAsConstant):
    ENTRY_TYPE = 'name'
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsString

    def __init__(self, *args, **kwargs):
        super(PrxPortAsName, self).__init__(*args, **kwargs)
        self.get_input_widget()._set_value_entry_validator_use_as_name_()


#   frames
class PrxPortAsFrames(PrxPortAsConstant):
    ENTRY_TYPE = 'frames'
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsString

    def __init__(self, *args, **kwargs):
        super(PrxPortAsFrames, self).__init__(*args, **kwargs)
        self._prx_port_input.set_use_as_frames()


#   integer
class PrxPortForInteger(PrxPortAsConstant):
    ENTRY_TYPE = 'integer'
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsInteger

    def __init__(self, *args, **kwargs):
        super(PrxPortForInteger, self).__init__(*args, **kwargs)


#   boolean
class PrxPortAsBoolean(_AbsPrxPortBase):
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = True
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsBoolean

    def __init__(self, *args, **kwargs):
        super(PrxPortAsBoolean, self).__init__(*args, **kwargs)

    def set_name(self, text):
        self.get_input_widget()._set_name_text_(text)


#   float
class PrxPortAsFloat(PrxPortAsConstant):
    ENTRY_TYPE = 'float'
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsFloat

    def __init__(self, *args, **kwargs):
        super(PrxPortAsFloat, self).__init__(*args, **kwargs)


# storage
class PrxPortAsStorage(PrxPortAsConstant):
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsStorage

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
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsFileOpen

    def __init__(self, *args, **kwargs):
        super(PrxPortAsFileOpen, self).__init__(*args, **kwargs)


#   file save
class PrxPortAsFileSave(PrxPortAsStorage):
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsFileSave

    def __init__(self, *args, **kwargs):
        super(PrxPortAsFileSave, self).__init__(*args, **kwargs)


#   directory open
class PrxPortAsDirectoryOpen(PrxPortAsStorage):
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsDirectoryOpen

    def __init__(self, *args, **kwargs):
        super(PrxPortAsDirectoryOpen, self).__init__(*args, **kwargs)


#   directory save
class PrxPortAsDirectorySave(PrxPortAsStorage):
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsDirectorySave

    def __init__(self, *args, **kwargs):
        super(PrxPortAsDirectorySave, self).__init__(*args, **kwargs)


# resolver
#   project choose
class PrxPortAsRsvProjectChoose(PrxPortAsConstant):
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsRsvProject

    def __init__(self, *args, **kwargs):
        super(PrxPortAsRsvProjectChoose, self).__init__(*args, **kwargs)

    def get_histories(self):
        return self.entry_widget.get_histories()


#  scheme choose
class PrxPortAsSchemChoose(PrxPortAsConstant):
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsSchemeWithChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortAsSchemChoose, self).__init__(*args, **kwargs)
        self._prx_port_input.set_scheme_key(kwargs['scheme_key'])


class PrxPortAsConstantChoose(_AbsPrxPortBase):
    ENTRY_TYPE = 'enumerate'
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsConstantWithChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortAsConstantChoose, self).__init__(*args, **kwargs)

    def get_enumerate_strings(self):
        return self._prx_port_input.get_enumerate_strings()

    def set_icon_file_as_value(self, value, file_path):
        self._prx_port_input.set_icon_file_as_value(value, file_path)


# capsule
class PrxPortAsCapsuleString(_AbsPrxPortBase):
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsCapsule

    def __init__(self, *args, **kwargs):
        super(PrxPortAsCapsuleString, self).__init__(*args, **kwargs)

        self.get_input_widget()._set_value_type_(str)


class PrxPortAsCapsuleStrings(_AbsPrxPortBase):
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsCapsule

    def __init__(self, *args, **kwargs):
        super(PrxPortAsCapsuleStrings, self).__init__(*args, **kwargs)
        self.get_input_widget()._set_value_type_(list)


class PrxPortAsScript(_AbsPrxPortBase):
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsScript

    def __init__(self, *args, **kwargs):
        super(PrxPortAsScript, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortAsScript, self).set_name(*args, **kwargs)
        self.get_input_widget()._get_entry_widget_()._set_empty_text_(args[0])

    def set_external_editor_ext(self, ext):
        self._prx_port_input.set_external_editor_ext(ext)


class PrxPortAsTuple(_AbsPrxPortBase):
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsTuple

    def __init__(self, *args, **kwargs):
        super(PrxPortAsTuple, self).__init__(*args, **kwargs)

    def set_value_type(self, value_type):
        self._prx_port_input.set_value_type(value_type)

    def set_value_size(self, size):
        self._prx_port_input.set_value_size(size)


class PrxPortForIntegerTuple(PrxPortAsTuple):
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsIntegerTuple

    def __init__(self, *args, **kwargs):
        super(PrxPortForIntegerTuple, self).__init__(*args, **kwargs)


class PrxPortForFloatTuple(PrxPortAsTuple):
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsFloatTuple

    def __init__(self, *args, **kwargs):
        super(PrxPortForFloatTuple, self).__init__(*args, **kwargs)


class PrxPortAsRgbaChoose(_AbsPrxPortBase):
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsRgbaChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortAsRgbaChoose, self).__init__(*args, **kwargs)
        self._prx_port_input.set_use_as_rgba()


class PrxPortAsButton(_AbsPrxPortBase):
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    KEY_HIDE = True
    LABEL_HIDED = True
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsPressButton

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
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    KEY_HIDE = True
    LABEL_HIDED = True
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsSubProcessButton

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

    def set_initialization(self, count, status=gui_core.GuiStatus.Started):
        self.get_input_widget()._initialization_sub_process_(count, status)

    def restore_all(self):
        self.get_input_widget()._restore_sub_process_()

    def set_status_at(self, index, status):
        widget = self.get_input_widget()
        widget.rate_status_update_at.emit(index, status)

    def set_finished_at(self, index, status):
        widget = self.get_input_widget()
        widget.rate_finished_at.emit(index, status)

    def set_finished_connect_to(self, fnc):
        widget = self.get_input_widget()
        widget._connect_sub_process_finished_to_(fnc)

    def set_stop_connect_to(self, fnc):
        self._prx_port_input.set_stop_connect_to(fnc)

    def set_stopped(self, boolean=True):
        self._is_stopped = boolean
        # self.restore_all()

    def get_is_stopped(self):
        return self._is_stopped


class PrxValidatorPort(_AbsPrxPortBase):
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    KEY_HIDE = True
    LABEL_HIDED = True
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsValidationButton

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
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsResolverEntity

    def __init__(self, *args, **kwargs):
        super(PrxRsvObjChoosePort, self).__init__(*args, **kwargs)


# storage array
#   many files open
class PrxPortAsFilesOpen(_AbsPrxPortBase):
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsFilesOpen

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
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsDirectoriesOpen

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
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsMediasOpen

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
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsIconWithChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortAsIconChoose, self).__init__(*args, **kwargs)


# any array
class PrxPortForValueArray(_AbsPrxPortBase):
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsArray

    def __init__(self, *args, **kwargs):
        super(PrxPortForValueArray, self).__init__(*args, **kwargs)

    def append(self, value):
        self._prx_port_input.append(value)


# any array choose
class PrxPortForValueArrayAsChoose(_AbsPrxPortBase):
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsArrayWithChoose

    def __init__(self, *args, **kwargs):
        super(PrxPortForValueArrayAsChoose, self).__init__(*args, **kwargs)

    def set_name(self, *args, **kwargs):
        super(PrxPortForValueArrayAsChoose, self).set_name(*args, **kwargs)
        self.get_input_widget()._set_name_text_(args[0])

    def append(self, value):
        self._prx_port_input.append(value)


# shotgun
class PrxPortAsShotgunEntity(_AbsPrxPortBase):
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsShotgunEntityWithChoose

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
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsShotgunEntitiesWithChoose

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
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsNodes

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
    ENABLE_CLS = gui_prx_wgt_port_base.PrxPortStatus
    LABEL_CLS = gui_prx_wgt_port_base.PrxPortLabel
    LABEL_HIDED = False
    PRX_PORT_INPUT_CLS = gui_prx_wgt_input_for_port.PrxInputAsFiles

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


# node
class PrxPortStack(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(PrxPortStack, self).__init__()

    def get_key(self, obj):
        return obj.name


class PrxNodeOld(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    PORT_STACK_CLS = PrxPortStack
    LABEL_WIDTH = 160
    PORT_CLS_DICT = dict(
        string=PrxPortAsString,
        interge=PrxPortForInteger,
        float=PrxPortAsFloat,
        button=PrxPortAsButton,
        enumerate=PrxPortAsConstantChoose
    )

    @classmethod
    def get_port_cls(cls, type_name):
        return cls.PORT_CLS_DICT[type_name]

    def __init__(self, *args, **kwargs):
        super(PrxNodeOld, self).__init__(*args, **kwargs)
        qt_layout_0 = gui_qt_wgt_base.QtHBoxLayout(self.widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        #
        qt_splitter_0 = gui_qt_wgt_split.QtHSplitterOld()
        qt_layout_0.addWidget(qt_splitter_0)
        #
        self._qt_label_widget = gui_qt_wgt_utility.QtTranslucentWidget()
        # self._qt_label_widget.setMaximumWidth(self.LABEL_WIDTH)
        self._name_width = 160
        self._qt_label_widget.setFixedWidth(self._name_width)
        qt_splitter_0.addWidget(self._qt_label_widget)
        self._qt_label_layout = gui_qt_wgt_base.QtVBoxLayout(self._qt_label_widget)
        self._qt_label_layout.setAlignment(gui_qt_core.QtCore.Qt.AlignTop)
        self._qt_label_layout.setContentsMargins(2, 0, 2, 0)
        #
        qt_entry_widget = gui_qt_wgt_utility.QtTranslucentWidget()
        qt_splitter_0.addWidget(qt_entry_widget)
        self._qt_entry_layout = gui_qt_wgt_base.QtVBoxLayout(qt_entry_widget)
        self._qt_entry_layout.setAlignment(gui_qt_core.QtCore.Qt.AlignTop)
        self._qt_entry_layout.setContentsMargins(2, 0, 2, 0)

        self._port_stack = self.PORT_STACK_CLS()

    def set_folder_add(self, label):
        pass

    def _get_pre_args(self):
        ports = self._port_stack.get_objects()
        if ports:
            port_pre = ports[-1]
            return port_pre._get_join_next_flag(), port_pre
        return False, None

    def add_port(self, port):
        if isinstance(port, _AbsPrxPortBase):
            port_cur = port
            join_next_pre, port_pre = self._get_pre_args()
            join_next_cur = port_cur._get_join_next_flag()
            #
            port_cur.set_node_widget(self.widget)
            #
            condition = join_next_pre, join_next_cur
            if condition == (False, False):
                self._qt_label_layout.addWidget(
                    port_cur.label_widget.widget
                )
                self._qt_entry_layout.addWidget(
                    port_cur._prx_port_input.widget
                )
                if port_cur.LABEL_HIDED is False:
                    port_cur._prx_port_label.set_show()
            # pre is not join and current join to next
            elif condition == (False, True):
                self._qt_label_layout.addWidget(
                    port_cur.label_widget.widget
                )
                #
                enter_widget_cur = gui_qt_wgt_utility.QtTranslucentWidget()
                self._qt_entry_layout.addWidget(
                    enter_widget_cur
                )
                enter_layout_cur = gui_qt_wgt_base.QtHBoxLayout(enter_widget_cur)
                enter_layout_cur.setContentsMargins(0, 0, 0, 0)
                enter_layout_cur.setSpacing(2)
                enter_layout_cur.addWidget(
                    port_cur._prx_port_input.widget
                )
                port_cur._register_join_layout(enter_layout_cur)
            # pre is join and current also
            elif condition == (True, True):
                enter_layout_pre = port_pre._get_join_layout()
                enter_layout_pre.addWidget(
                    port_cur._prx_port_input.widget
                )
                port_cur._register_join_layout(enter_layout_pre)
            # pre is join but current is not
            elif condition == (True, False):
                enter_layout = port_pre._get_join_layout()
                enter_layout.addWidget(
                    port_cur._prx_port_input.widget
                )
            #
            self._port_stack.set_object_add(port_cur)
            return port
        elif isinstance(port, dict):
            pass

    def get_port(self, port_name):
        return self._port_stack.get_object(port_name)

    def to_dict(self):
        dic = {}
        ports = self._port_stack.get_objects()
        for port in ports:
            key = port.name
            value = port.get()
            dic[key] = value
        return dic

    def set_name_width(self, w):
        self._name_width = w
        self._qt_label_widget.setFixedWidth(self._name_width)


class PrxNodePortGroup(AbsPrxPortBaseDef):
    ENTRY_TYPE = 'group'
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    PORT_STACK_CLS = PrxPortStack

    def __init__(self, port_path, node, is_pseudo_root=False):
        self._init_prx_port_def_('group', port_path)
        self._set_node(node)
        if is_pseudo_root is True:
            self._set_use_as_pseudo_root()

        self._prx_widget = gui_prx_wgt_container.PrxHToolGroup()
        self._prx_widget.set_height_match_to_minimum()
        self._qt_widget = self._prx_widget.widget
        self._prx_widget.set_name(self.get_label())
        self._prx_widget.set_expanded(True)
        self._port_layout = self._prx_widget._layout
        self._port_layout.setContentsMargins(8, 0, 0, 0)
        self._port_layout.setSpacing(2)
        #
        self._port_stack = self.PORT_STACK_CLS()
        # default use -1
        self._label_width_maximum = -1

    def get_label(self):
        if self.get_is_pseudo_root():
            return self.get_node().get_path()
        return self._label

    def set_label(self, text):
        self._prx_widget.set_name(text)

    def create_child_group(self, name):
        if self.get_is_pseudo_root() is True:
            child_port_path = name
        else:
            child_port_path = '{}.{}'.format(self._port_path, name)
        #
        group = self.__class__(child_port_path, self.get_node())
        group._prx_widget.set_name_font_size(8)
        group._prx_widget.set_name_icon_enable(False)
        group._prx_widget.set_expand_icon_names(
            'qt-style/branch-open', 'qt-style/branch-close'
        )
        group._prx_widget.widget._set_line_draw_enable_(True)
        self._port_layout.addWidget(group._prx_widget._qt_widget)
        self._port_stack.set_object_add(group)
        return group

    def add_child(self, port):
        port_cur = port
        join_next_pre, port_pre = self._get_pre_child_args_()
        join_next_cur = port_cur._get_join_next_flag()
        #
        condition = join_next_pre, join_next_cur
        if condition == (False, False):
            widget_cur = gui_qt_wgt_utility.QtTranslucentWidget()
            self._port_layout.addWidget(widget_cur)
            port_cur.set_main_widget(widget_cur)
            layout_cur = gui_qt_wgt_base.QtHBoxLayout(widget_cur)
            layout_cur.setContentsMargins(0, 0, 0, 0)
            layout_cur._set_align_as_top_()
            port_cur._set_layout_(layout_cur)
            #
            cur_key_widget = gui_qt_wgt_utility.QtTranslucentWidget()
            cur_key_widget.hide()
            port_cur._set_key_widget_(cur_key_widget)
            layout_cur.addWidget(cur_key_widget)
            cur_key_layout = gui_qt_wgt_base.QtHBoxLayout(cur_key_widget)
            cur_key_layout.setContentsMargins(0, 0, 0, 0)
            cur_key_layout._set_align_as_top_()
            # + key
            cur_key_layout.addWidget(port_cur._prx_port_enable._qt_widget)
            cur_key_layout.addWidget(port_cur._prx_port_label._qt_widget)
            # + value
            layout_cur.addWidget(port_cur._prx_port_input._qt_widget)
            if port_cur.KEY_HIDE is False:
                cur_key_widget.show()
            if port_cur.LABEL_HIDED is False:
                port_cur._prx_port_label._qt_widget.show()
                cur_key_widget.show()
        # pre is not join and current join to next
        elif condition == (False, True):
            widget_cur = gui_qt_wgt_utility.QtTranslucentWidget()
            self._port_layout.addWidget(widget_cur)
            port_cur.set_main_widget(widget_cur)
            layout_cur = gui_qt_wgt_base.QtHBoxLayout(widget_cur)
            layout_cur.setContentsMargins(0, 0, 0, 0)
            layout_cur.setSpacing(2)
            layout_cur._set_align_as_top_()
            port_cur._set_layout_(layout_cur)
            key_widget_cur = gui_qt_wgt_utility.QtTranslucentWidget()
            # key_widget_cur.hide()
            port_cur._set_key_widget_(key_widget_cur)
            layout_cur.addWidget(key_widget_cur)
            cur_key_layout = gui_qt_wgt_base.QtHBoxLayout(key_widget_cur)
            cur_key_layout.setContentsMargins(0, 0, 0, 0)
            cur_key_layout._set_align_as_top_()
            # + key
            #   + enable
            cur_key_layout.addWidget(port_cur._prx_port_enable._qt_widget)
            #   + label
            cur_key_layout.addWidget(port_cur._prx_port_label._qt_widget)
            # + value
            #   + input
            layout_cur.addWidget(port_cur._prx_port_input._qt_widget)
            port_cur._update_sub_name()
            # join
            port_cur._register_join_layout(layout_cur)
            if port_cur.KEY_HIDE is False:
                key_widget_cur.show()
            if port_cur.LABEL_HIDED is False:
                port_cur._prx_port_label._qt_widget.show()
                key_widget_cur.show()
        # pre is join and current also
        elif condition == (True, True):
            # hide status and label
            layout_pre = port_pre._get_join_layout()
            layout_pre.addWidget(port_cur._prx_port_enable._qt_widget)
            port_cur._prx_port_enable._qt_widget.hide()
            layout_pre.addWidget(port_cur._prx_port_label._qt_widget)
            port_cur._prx_port_label._qt_widget.hide()
            port_cur._update_sub_name()
            layout_pre.addWidget(port_cur._prx_port_input._qt_widget)
            port_cur._register_join_layout(layout_pre)
        # pre is join but current is not
        elif condition == (True, False):
            # hide status and label
            layout_pre = port_pre._get_join_layout()
            layout_pre.addWidget(port_cur._prx_port_enable._qt_widget)
            port_cur._prx_port_enable._qt_widget.hide()
            layout_pre.addWidget(port_cur._prx_port_label._qt_widget)
            port_cur._prx_port_label._qt_widget.hide()
            port_cur._update_sub_name()
            layout_pre.addWidget(port_cur._prx_port_input._qt_widget)
        #
        port_cur._prx_port_input.set_show()
        #
        self._port_stack.set_object_add(port_cur)
        port_cur.set_group(self)
        #
        self.update_children_name_width()
        return port

    def _get_pre_child_args_(self):
        ports = self._port_stack.get_objects()
        if ports:
            port_pre = ports[-1]
            if hasattr(port_pre, '_get_join_next_flag') is True:
                return port_pre._get_join_next_flag(), port_pre
            return False, port_pre
        return False, None

    def get_child(self, name):
        return self._port_stack.get_object(name)

    def compute_children_name_width(self):
        widths = []
        children = self.get_children()
        for i_child in children:
            if i_child.get_category() == 'group':
                continue
            #
            if i_child.KEY_HIDE is False:
                if i_child.LABEL_HIDED is False:
                    i_width = i_child._prx_port_label.get_name_draw_width()+16
                else:
                    i_width = 0
                #
                if i_child.get_use_enable() is True:
                    i_width += 22
                #
                widths.append(i_width)
        if widths:
            return max(widths)
        return 0

    def update_children_name_width(self):
        width = self.compute_children_name_width()
        children = self.get_children()
        for i_child in children:
            if i_child.get_category() == 'group':
                continue
            #
            i_key_widget = i_child._key_widget
            if i_key_widget is not None:
                i_width = width
                if i_child.KEY_HIDE is False:
                    if i_width > 0:
                        if i_child.LABEL_HIDED is False:
                            i_key_widget.setFixedWidth(i_width)
                        else:
                            if i_child.get_use_enable() is True:
                                i_key_widget.setFixedWidth(22)
                            else:
                                i_key_widget.setFixedWidth(0)
                                i_key_widget.hide()
                    else:
                        i_key_widget.setFixedWidth(0)
                        i_key_widget.hide()
                else:
                    i_key_widget.setFixedWidth(0)
                    i_key_widget.hide()

    def set_expanded(self, boolean):
        self._prx_widget.set_expanded(boolean)

    def set_reset(self):
        pass

    def set_visible(self, boolean):
        self._prx_widget.set_visible(boolean)

    def __str__(self):
        return '{}(node="{}", port_path="{}")'.format(
            self.get_type(),
            self.get_node_path(),
            self.get_port_path()
        )

    def __repr__(self):
        return self.__str__()


class PrxNodePortStack(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(PrxNodePortStack, self).__init__()

    def get_key(self, obj):
        return obj.get_port_path()


class PrxNode(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    PORT_STACK_CLS = PrxNodePortStack
    PORT_CLS_DICT = dict(
        string=PrxPortAsString,
        interge=PrxPortForInteger,
        float=PrxPortAsFloat,
        button=PrxPortAsButton,
        enumerate=PrxPortAsConstantChoose
    )

    def __init__(self, path, *args, **kwargs):
        super(PrxNode, self).__init__(*args, **kwargs)
        self._path_dag_opt = bsc_core.PthNodeOpt(path)
        # debug: do not set minimum height
        # self._qt_widget.setMinimumHeight(24)
        #
        qt_layout_0 = gui_qt_wgt_base.QtVBoxLayout(self._qt_widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(0)

        self._port_stack = self.PORT_STACK_CLS()
        self._port_switch_stack = self.PORT_STACK_CLS()
        #
        self._prx_root_group = self.create_root_group()
        qt_layout_0.addWidget(self._prx_root_group._prx_widget._qt_widget)

    def get_path(self):
        return self._path_dag_opt.get_path()

    path = property(get_path)

    def get_name(self):
        return self._path_dag_opt.get_name()

    name = property(get_name)

    def _get_ports_(self, port_paths):
        return [self._port_stack.get_object(i) for i in port_paths]

    def get_port_paths(self):
        return self._port_stack.get_keys()

    def get_pseudo_root(self):
        return self._prx_root_group

    def add_port(self, port):
        if port.get_is_top_level() is True:
            group = self.get_pseudo_root()
        else:
            group = self._create_group_by_path(port.get_group_path())

        self._register_port(port)
        return group.add_child(port)

    def create_root_group(self):
        group = PrxNodePortGroup(
            'pseudo_root', self, True
        )
        group._prx_widget.get_widget()._set_line_draw_enable_(True)
        return group

    def _create_group_by_path(self, port_path):
        group_cur = self.get_pseudo_root()
        if port_path:
            components = bsc_core.PthPortOpt(port_path).get_components()
            components.reverse()
            for i in components:
                i_path = i.to_string()
                i_port = self.get_port(i_path)
                if i_port is None:
                    i_parent_path = i.get_parent_path()
                    if i_parent_path is None:
                        i_port_parent = self.get_pseudo_root()
                    else:
                        i_port_parent = self.get_port(i_parent_path)

                    i_group = i_port_parent.create_child_group(i.get_name())
                    self._register_port(i_group)

            group_cur = self.get_port(components[-1].to_string())
        return group_cur

    def _register_port(self, port):
        port._set_node(self)
        self._port_stack.set_object_add(port)
        if hasattr(port, 'connect_tab_pressed_to'):
            connect_result = port.connect_tab_pressed_to(functools.partial(self.focus_next_fnc, port))
            if connect_result is True:
                self._port_switch_stack.set_object_add(port)

    def focus_next_fnc(self, port):
        maximum = self._port_switch_stack.get_maximum()
        if maximum > 0:
            index_cur = self._port_switch_stack.get_index(port.get_port_path())
            index_next = index_cur+1
            if index_next > maximum:
                index_next = 0
            #
            port = self._port_switch_stack.get_object_at(index_next)
            port.set_focus_in()

    def get_port(self, port_path):
        return self._port_stack.get_object(port_path)

    def get_ports(self, regex=None):
        return self._port_stack.get_objects(regex)

    def get_all_ports(self):
        return self._port_stack.get_all_objects()

    def to_dict(self):
        dic = {}
        ports = self._port_stack.get_objects()
        for i_port in ports:
            key = i_port.get_port_path()
            if i_port.get_category() not in {'group'}:
                value = i_port.get()
                dic[key] = value
        return dic

    def set_name_width(self, w):
        self._name_width = w
        # self._prx_root_group._qt_label_widget.setFixedWidth(self._name_width)

    def create_ports_by_data(self, configure):
        for k, v in configure.items():
            self.create_port_by_data(k.replace('/', '.'), v)

    def create_port_by_data(self, port_path, option):
        widget_ = option['widget']
        label_ = option.get('label')
        #
        if widget_ in {'group'}:
            group = self._create_group_by_path(port_path)
            if label_:
                group.set_label(label_)
            #
            expand = option.get('expand') or False
            group.set_expanded(expand)

            collapse = option.get('collapse') or False
            group.set_expanded(not collapse)
            #
            group.set_visible_condition(
                option.get('visible_condition')
            )
            return
        #
        key_ = option.get('key')
        value_ = option.get('value')
        enable_ = option.get('enable')
        tool_tip_ = option.get('tool_tip')
        lock_ = option.get('lock') or False
        #
        join_to_next_ = option.get('join_to_next') or False

        if widget_ in {'string'}:
            port = PrxPortAsString(
                port_path,
                node_widget=self.widget
            )
            lock = option.get('lock') or False
            if lock is True:
                port.set_locked(True)
            #
            port.set(value_)
            port.set_default(value_)
        elif widget_ in {'name'}:
            port = PrxPortAsName(
                port_path,
                node_widget=self.widget
            )
            lock = option.get('lock') or False
            if lock is True:
                port.set_locked(True)
            #
            port.set(value_)
            port.set_default(value_)

        elif widget_ in {'integer'}:
            port = PrxPortForInteger(
                port_path,
                node_widget=self.widget
            )
            history_key_ = option.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)

            port.set_default(value_)

            pull_history_latest = option.get('pull_history_latest')
            if pull_history_latest is True:
                if port.pull_history_latest() is False:
                    port.set(value_)
            else:
                port.set(value_)
        
        elif widget_ in {'integer2'}:
            port = PrxPortForIntegerTuple(
                port_path,
                node_widget=self.widget
            )
            history_key_ = option.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)

            port.set_value_size(2)

            port.set_default(value_)

            pull_history_latest = option.get('pull_history_latest')
            if pull_history_latest is True:
                if port.pull_history_latest() is False:
                    port.set(value_)
            else:
                port.set(value_)

            lock = option.get('lock') or False
            if lock is True:
                port.set_locked(True)

        elif widget_ in {'float'}:
            port = PrxPortAsFloat(
                port_path,
                node_widget=self.widget
            )
            history_key_ = option.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)

            port.set_default(value_)

            pull_history_latest = option.get('pull_history_latest')
            if pull_history_latest is True:
                if port.pull_history_latest() is False:
                    port.set(value_)
            else:
                port.set(value_)

        elif widget_ in {'float2'}:
            port = PrxPortForFloatTuple(
                port_path,
                node_widget=self.widget
            )
            port.set_value_size(2)
            port.set(value_)
            port.set_default(value_)
        elif widget_ in {'float3'}:
            port = PrxPortForFloatTuple(
                port_path,
                node_widget=self.widget
            )
            port.set_value_size(3)
            port.set(value_)
            port.set_default(value_)
        #
        elif widget_ in {'rgb', 'rgba'}:
            port = PrxPortAsRgbaChoose(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
        #
        elif widget_ in {'boolean'}:
            port = PrxPortAsBoolean(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)

        elif widget_ in {'enumerate'}:
            port = PrxPortAsConstantChoose(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            #
            default_ = option.get('current') or option.get('default')
            current_index_ = option.get('current_index') or option.get('default_index')
            if default_ is not None:
                port.set(default_)
                port.set_default(default_)
            elif current_index_ is not None:
                port.set(current_index_)
                port.set_default(current_index_)
            else:
                if value_:
                    port.set(value_[0])
                    port.set_default(value_[0])
                    # port.set(value_[-1])
                    # port.set_default(value_[-1])

        elif widget_ in {'icon'}:
            all_application_icon = option.get('all_application_icon')
            if all_application_icon is True:
                value_ = gui_core.GuiIcon.find_all_keys_at('application')
                value_.insert(0, '')
            all_tool_base_icon = option.get('all_tool_base_icon')
            if all_tool_base_icon is True:
                value_ = gui_core.GuiIcon.find_all_keys_at('tool_style')
                value_.insert(0, '')

            port = PrxPortAsIconChoose(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)

            default_ = option.get('default')
            if default_ is not None:
                port.set(default_)
                port.set_default(default_)

        elif widget_ in {'capsule_string'}:
            port = PrxPortAsCapsuleString(
                port_path,
                node_widget=self.widget
            )
            #
            port.set_option(value_)
            #
            value_default = option.get('current') or option.get('default')
            if value_default is not None:
                port.set(value_default)
                port.set_default(value_default)
            else:
                port.set(value_[-1])
                port.set_default(value_[-1])
            #
            lock = option.get('lock') or False
            if lock is True:
                port.set_locked(True)
        #
        elif widget_ in {'capsule_strings'}:
            port = PrxPortAsCapsuleStrings(
                port_path,
                node_widget=self.widget
            )
            #
            port.set_option(value_)
            #
            value_default = option.get('current') or option.get('default')
            if value_default is not None:
                port.set(value_default)
                port.set_default(value_default)
        #
        elif widget_ in {'file'}:
            open_or_save = option.get('open_or_save')
            if open_or_save == 'save':
                port = PrxPortAsFileSave(
                    port_path,
                    node_widget=self.widget
                )
            else:
                port = PrxPortAsFileOpen(
                    port_path,
                    node_widget=self.widget
                )
            #
            history_key_ = option.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)
            #
            port.set(value_)
            port.set_default(value_)
            ext_filter = option.get('ext_filter')
            if ext_filter:
                port.set_ext_filter(ext_filter)

            ext_includes = option.get('ext_includes')
            if ext_includes:
                port.set_ext_includes(ext_includes)

            pull_history_latest = option.get('pull_history_latest')
            if pull_history_latest:
                port.pull_history_latest()
            #
            lock = option.get('lock') or False
            if lock is True:
                port.set_locked(True)
        elif widget_ in {'directory'}:
            open_or_save_ = option.get('open_or_save')
            if open_or_save_ == 'save':
                port = PrxPortAsDirectorySave(
                    port_path,
                    node_widget=self.widget
                )
            else:
                port = PrxPortAsDirectoryOpen(
                    port_path,
                    node_widget=self.widget
                )
            #
            history_key_ = option.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)
            #
            port.set(value_)
            port.set_default(value_)
            #
            pull_history_latest = option.get('pull_history_latest')
            if pull_history_latest:
                port.pull_history_latest()
        # storage array
        elif widget_ in {'directories'}:
            port = PrxPortAsDirectoriesOpen(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
            #
            history_key_ = option.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)
            #
            if 'history_visible' in option:
                port.set_history_button_visible(option['history_visible'])
        elif widget_ in {'files'}:
            port = PrxPortAsFilesOpen(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
            #
            ext_includes = option.get('ext_includes')
            if ext_includes:
                port.set_ext_includes(ext_includes)
            #
            history_key_ = option.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)
            #
            if 'history_visible' in option:
                port.set_history_button_visible(option['history_visible'])
        elif widget_ in {'medias'}:
            port = PrxPortAsMediasOpen(
                port_path,
                node_widget=self.widget
            )
            #
            ext_includes = option.get('ext_includes')
            if ext_includes:
                port.set_ext_includes(ext_includes)

            ext_filter = option.get('ext_filter')
            if ext_filter:
                port.set_ext_filter(ext_filter)
            #
            history_key_ = option.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)
        #
        elif widget_ in {'values'}:
            port = PrxPortForValueArray(
                port_path,
                node_widget=self.widget
            )
        #
        elif widget_ in {'values_choose'}:
            port = PrxPortForValueArrayAsChoose(
                port_path,
                node_widget=self.widget
            )
            port.set_choose_values(value_)

        elif widget_ in {'shotgun_entity_choose'}:
            port = PrxPortAsShotgunEntity(
                port_path,
                node_widget=self.widget
            )
            shotgun_entity_kwargs = option.get('shotgun_entity_kwargs')
            if shotgun_entity_kwargs:
                port.set_shotgun_entity_kwargs(
                    shotgun_entity_kwargs,
                    keyword_filter_fields=option.get('keyword_filter_fields'),
                    tag_filter_fields=option.get('tag_filter_fields')
                )
                port.set(value_)

        elif widget_ in {'shotgun_entities_choose'}:
            port = PrxPortAsShotgunEntities(
                port_path,
                node_widget=self.widget
            )
            shotgun_entity_kwargs = option.get('shotgun_entity_kwargs')
            if shotgun_entity_kwargs:
                port.set_shotgun_entity_kwargs(
                    shotgun_entity_kwargs,
                    keyword_filter_fields=option.get('keyword_filter_fields'),
                    tag_filter_fields=option.get('tag_filter_fields')
                )
                port.set(value_)
        #
        elif widget_ in {'button'}:
            port = PrxPortAsButton(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            if 'option_enable' in option:
                port.set_option_enable(option['option_enable'])

            if 'icon' in option:
                port.set_icon(option['icon'])

        elif widget_ in {'check_button'}:
            port = PrxPortAsCheckButton(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_checked(
                option.get('check', False)
            )

        elif widget_ in {'sub_process_button'}:
            port = PrxSubProcessPort(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
        elif widget_ in {'validator_button'}:
            port = PrxValidatorPort(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
        #
        elif widget_ in {'project'}:
            port = PrxPortAsRsvProjectChoose(
                port_path,
                node_widget=self.widget
            )
            if value_:
                port.set(value_)

            pull_history_latest = option.get('pull_history_latest')
            if pull_history_latest:
                port.pull_history_latest()
        elif widget_ in {'rsv-obj'}:
            port = PrxRsvObjChoosePort(
                port_path,
                node_widget=self.widget
            )
            # port.set(value_)
        elif widget_ in {'scheme'}:
            port = PrxPortAsSchemChoose(
                port_path,
                scheme_key=option['scheme_key'],
                node_widget=self.widget
            )
            port.set(value_)
        elif widget_ in {'script'}:
            port = PrxPortAsScript(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
            if 'external_editor_ext' in option:
                port.set_external_editor_ext(
                    option['external_editor_ext']
                )
        #
        elif widget_ in {'components', 'node_list'}:
            port = PrxNodeListViewPort(
                port_path,
                node_widget=self.widget
            )
        elif widget_ in {'node_tree'}:
            port = PrxNodeTreeViewPort(
                port_path,
                node_widget=self.widget
            )
        #
        elif widget_ in {'file_list'}:
            port = PrxPortAsFileList(
                port_path,
                node_widget=self.widget
            )
        elif widget_ in {'file_tree'}:
            port = PrxPortAsFileTree(
                port_path,
                node_widget=self.widget
            )
        #
        elif widget_ in {'frames'}:
            port = PrxPortAsFrames(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
        #
        else:
            raise TypeError()
        #
        port.ENTRY_TYPE = widget_
        port.set_key(key_)
        port.set_label(label_)
        port.set_use_enable(enable_)
        port.set_tool_tip(tool_tip_ or '...')
        port._set_join_to_next_flag(join_to_next_)
        port.set_locked(lock_)
        #
        height = option.get('height')
        if height:
            port.set_height(height)

        self.add_port(port)

        # run after add
        port.set_visible_condition(
            option.get('visible_condition')
        )

        if 'exclusive_set' in option:
            port.update_exclusive_set(option['exclusive_set'])

    def set_expanded(self, boolean):
        self._prx_root_group.set_expanded(boolean)

    def set_ports_collapse(self, port_paths):
        for i in port_paths:
            self.get_port(
                i.replace('/', '.')
            ).set_expanded(False)

    def set(self, key, value):
        port = self.get_port(key)
        if port is not None:
            port.set(value)
        else:
            bsc_log.Log.trace_method_warning(
                'port set',
                'port="{}" is non-exists'.format(key)
            )

    def connect_input_changed_to(self, key, value):
        port = self.get_port(key)
        if port is not None:
            port.connect_input_changed_to(value)

    def set_default(self, key, value):
        port = self.get_port(key)
        if port is not None:
            port.set_default(value)

    def get(self, key):
        port = self.get_port(key)
        if port is not None:
            return port.get()

    def set_reset(self):
        for i in self.get_ports():
            i.set_reset()

    def get_enumerate_strings(self, key):
        port = self.get_port(key)
        if port is not None:
            return port.get_enumerate_strings()
