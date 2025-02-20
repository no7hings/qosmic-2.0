# coding:utf-8
import functools

import six

# qt widgets
from ....qt.widgets import base as _qt_wgt_base

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core
# gui
from .... import core as _gui_core
# qt widgets
from ....qt.widgets import utility as _qt_wgt_utility

from ....qt.widgets import button as _qt_wgt_button

from ....qt.widgets import item as _qt_wgt_item
# proxy abstracts
from ... import abstracts as _prx_abstracts


# port
#   info
class PrxPortInfo(_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = _qt_wgt_button.QtIconPressButton

    def __init__(self, *args, **kwargs):
        super(PrxPortInfo, self).__init__(*args, **kwargs)
        # self.widget.setAlignment(gui_qt_core.QtCore.Qt.AlignRight | gui_qt_core.QtCore.Qt.AlignVCenter)
        self.widget.setMaximumHeight(_gui_core.GuiSize.InputHeight)
        self.widget.setMinimumHeight(_gui_core.GuiSize.InputHeight)
        self.widget.setMaximumWidth(_gui_core.GuiSize.InputHeight)
        self.widget.setMinimumWidth(_gui_core.GuiSize.InputHeight)

    def set(self, boolean):
        self.widget._set_checked_(boolean)


#   status
class PrxPortStatus(_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = _qt_wgt_item._QtStatusItem

    def __init__(self, *args, **kwargs):
        super(PrxPortStatus, self).__init__(*args, **kwargs)
        # self.widget.setAlignment(gui_qt_core.QtCore.Qt.AlignRight | gui_qt_core.QtCore.Qt.AlignVCenter)
        self.widget.setMaximumHeight(_gui_core.GuiSize.InputHeight)
        self.widget.setMinimumHeight(_gui_core.GuiSize.InputHeight)
        self.widget.setMaximumWidth(_gui_core.GuiSize.InputHeight)
        self.widget.setMinimumWidth(_gui_core.GuiSize.InputHeight)
        self.widget._set_tool_tip_text_(
            '"LMB-click" to use value "default" / "local" / "global"'
        )

    def set(self, boolean):
        self.widget._set_checked_(boolean)


#   label
class PrxPortLabel(_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTextItem

    def __init__(self, *args, **kwargs):
        super(PrxPortLabel, self).__init__(*args, **kwargs)
        # self.widget.setAlignment(gui_qt_core.QtCore.Qt.AlignRight | gui_qt_core.QtCore.Qt.AlignVCenter)
        self.widget.setMaximumHeight(_gui_core.GuiSize.InputHeight)
        self.widget.setMinimumHeight(_gui_core.GuiSize.InputHeight)
        # self._qt_widget._set_name_align_(gui_configure.AlignRegion.Top)

    def set_name(self, text):
        self._qt_widget._set_name_text_(text)

    def set_width(self, w):
        self.widget.setMaximumWidth(w)
        self.widget.setMinimumWidth(w)

    def set_info_tool_tip(self, text):
        pass

    def set_name_tool_tip(self, *args, **kwargs):
        if hasattr(self._qt_widget, '_set_tool_tip_'):
            self._qt_widget._set_tool_tip_(args[0], **kwargs)

    def get_name_draw_width(self):
        return self._qt_widget._get_name_text_draw_width_()


class AbsPrxPortBaseDef(object):
    WIDGET_TYPE = 'custom'

    Status = _gui_core.GuiProcessStatus
    ProcessStatus = _gui_core.GuiProcessStatus
    ShowStatus = _gui_core.GuiShowStatus
    ValidationStatus = _gui_core.GuiValidationStatus

    def _init_prx_port_base_def(self, category, port_path, label=None):
        self._prx_node = None
        self._prx_group = None
        #
        self._category = category
        self._port_path = port_path
        self._gui_sub_path = '/{}'.format(self._port_path.replace('.', '/'))
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
        return self.WIDGET_TYPE

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
        return bsc_core.BscPortPathOpt(
            self.get_port_path()
        ).get_parent_path()

    group_path = property(get_group_path)

    def get_gui_name(self):
        return self._label

    label = property(get_gui_name)

    def get_is_top_level(self):
        return bsc_core.BscPortPathOpt(
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
            _ = bsc_core.BscNodePath.find_dag_child_paths(
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
        return '\n'+self.__str__()


class AbsPrxPort(AbsPrxPortBaseDef):
    WIDGET_TYPE = 'custom'
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
        self._init_prx_port_base_def('value', port_path, label)
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

    def set_gui_name(self, text):
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

    def set_action_enable(self, boolean):
        self._prx_port_input.set_action_enable(boolean)

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

    def append(self, value):
        if hasattr(self._prx_port_input, 'append'):
            self._prx_port_input.append(value)

    def remove(self, value):
        if hasattr(self._prx_port_input, 'remove'):
            self._prx_port_input.remove(value)

    def do_clear(self):
        self._prx_port_input.do_clear()

    def set_reset(self):
        default = self.get_default()
        if default is not None:
            self.set(default)

    def set_options(self, values, names=None):
        self._prx_port_input.set_options(values, names)

    def set_tool_tip(self, *args, **kwargs):
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

    def set_menu_content(self, raw):
        self._prx_port_input.set_menu_content(raw)

    def to_custom_widget(self, label_width=80):
        if self._custom_widget is not None:
            return self._custom_widget
        else:
            widget = _qt_wgt_utility.QtTranslucentWidget()
            layout = _qt_wgt_base.QtHBoxLayout(widget)
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

    def set_history_group(self, arg):
        if isinstance(arg, six.string_types):
            key = [arg, self._gui_sub_path]
        elif isinstance(arg, (tuple, list)):
            key = list(arg)+[self._gui_sub_path]
        else:
            raise RuntimeError()

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
                _gui_core.GuiIcon.get('radio_unchecked'),
                _gui_core.GuiIcon.get('radio_checked')
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


class AbsPrxPortForConstant(AbsPrxPort):
    WIDGET_TYPE = 'constant'
    ENABLE_CLS = PrxPortStatus
    LABEL_CLS = PrxPortLabel
    PRX_PORT_INPUT_CLS = None

    def __init__(self, *args, **kwargs):
        super(AbsPrxPortForConstant, self).__init__(*args, **kwargs)

    def set_name(self, text):
        super(AbsPrxPortForConstant, self).set_name(text)

        self.get_input_widget()._set_name_text_(text)

    def set_locked(self, boolean):
        self._prx_port_input.set_locked(boolean)