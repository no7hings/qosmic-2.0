# coding:utf-8
import functools

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxuniverse.abstracts as unr_abstracts
# gui
from ... import core as _gui_core
# qt
from ...qt import core as _qt_core
# qt widgets
from ...qt.widgets import base as _qt_wgt_base

from ...qt.widgets import utility as _qt_wgt_utility

from ...qt.widgets import split as _qt_wgt_split
# proxy abstracts
from .. import abstracts as _prx_abstracts
# proxy widgets
from . import container as _container

from . import port as _port


# node
class PrxPortStack(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(PrxPortStack, self).__init__()

    def get_key(self, obj):
        return obj.name


class PrxNodeOld(_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    PORT_STACK_CLS = PrxPortStack
    LABEL_WIDTH = 160
    PORT_CLS_DICT = dict(
        string=_port.PrxPortAsString,
        interge=_port.PrxPortForInteger,
        float=_port.PrxPortAsFloat,
        button=_port.PrxPortAsButton,
        enumerate=_port.PrxPortAsConstantChoose
    )

    @classmethod
    def get_port_cls(cls, type_name):
        return cls.PORT_CLS_DICT[type_name]

    def __init__(self, *args, **kwargs):
        super(PrxNodeOld, self).__init__(*args, **kwargs)
        qt_layout_0 = _qt_wgt_base.QtHBoxLayout(self.widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        #
        qt_splitter_0 = _qt_wgt_split.QtHSplitterOld()
        qt_layout_0.addWidget(qt_splitter_0)
        #
        self._qt_label_widget = _qt_wgt_utility.QtTranslucentWidget()
        # self._qt_label_widget.setMaximumWidth(self.LABEL_WIDTH)
        self._name_width = 160
        self._qt_label_widget.setFixedWidth(self._name_width)
        qt_splitter_0.addWidget(self._qt_label_widget)
        self._qt_label_layout = _qt_wgt_base.QtVBoxLayout(self._qt_label_widget)
        self._qt_label_layout.setAlignment(_qt_core.QtCore.Qt.AlignTop)
        self._qt_label_layout.setContentsMargins(2, 0, 2, 0)
        #
        qt_entry_widget = _qt_wgt_utility.QtTranslucentWidget()
        qt_splitter_0.addWidget(qt_entry_widget)
        self._qt_entry_layout = _qt_wgt_base.QtVBoxLayout(qt_entry_widget)
        self._qt_entry_layout.setAlignment(_qt_core.QtCore.Qt.AlignTop)
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
        if isinstance(port, _port._AbsPrxPortBase):
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
                enter_widget_cur = _qt_wgt_utility.QtTranslucentWidget()
                self._qt_entry_layout.addWidget(
                    enter_widget_cur
                )
                enter_layout_cur = _qt_wgt_base.QtHBoxLayout(enter_widget_cur)
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


class PrxNodePortGroup(_port.AbsPrxPortBaseDef):
    ENTRY_TYPE = 'group'
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    PORT_STACK_CLS = PrxPortStack

    def __init__(self, port_path, node, is_pseudo_root=False):
        self._init_prx_port_def_('group', port_path)
        self._set_node(node)
        if is_pseudo_root is True:
            self._set_use_as_pseudo_root()

        self._prx_widget = _container.PrxHToolGroup()
        self._prx_widget.set_height_match_to_minimum()
        self._qt_widget = self._prx_widget.widget
        self._prx_widget.set_name(self.get_gui_name())
        self._prx_widget.set_expanded(True)
        self._port_layout = self._prx_widget._layout
        self._port_layout.setContentsMargins(8, 0, 0, 0)
        self._port_layout.setSpacing(2)
        #
        self._port_stack = self.PORT_STACK_CLS()
        # default use -1
        self._label_width_maximum = -1

    def get_gui_name(self):
        if self.get_is_pseudo_root():
            return self.get_node().get_path()
        return self._label

    def set_gui_name(self, text):
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
        join_next_pre, port_pre = self._get_pre_child_args()
        join_next_cur = port_cur._get_join_next_flag()
        #
        condition = join_next_pre, join_next_cur
        if condition == (False, False):
            widget_cur = _qt_wgt_utility.QtTranslucentWidget()
            self._port_layout.addWidget(widget_cur)
            port_cur.set_main_widget(widget_cur)
            layout_cur = _qt_wgt_base.QtHBoxLayout(widget_cur)
            layout_cur.setContentsMargins(0, 0, 0, 0)
            layout_cur._set_align_top_()
            port_cur._set_layout_(layout_cur)
            #
            cur_key_widget = _qt_wgt_utility.QtTranslucentWidget()
            cur_key_widget.hide()
            port_cur._set_key_widget_(cur_key_widget)
            layout_cur.addWidget(cur_key_widget)
            cur_key_layout = _qt_wgt_base.QtHBoxLayout(cur_key_widget)
            cur_key_layout.setContentsMargins(0, 0, 0, 0)
            cur_key_layout._set_align_top_()
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
            widget_cur = _qt_wgt_utility.QtTranslucentWidget()
            self._port_layout.addWidget(widget_cur)
            port_cur.set_main_widget(widget_cur)
            layout_cur = _qt_wgt_base.QtHBoxLayout(widget_cur)
            layout_cur.setContentsMargins(0, 0, 0, 0)
            layout_cur.setSpacing(2)
            layout_cur._set_align_top_()
            port_cur._set_layout_(layout_cur)
            key_widget_cur = _qt_wgt_utility.QtTranslucentWidget()
            # key_widget_cur.hide()
            port_cur._set_key_widget_(key_widget_cur)
            layout_cur.addWidget(key_widget_cur)
            cur_key_layout = _qt_wgt_base.QtHBoxLayout(key_widget_cur)
            cur_key_layout.setContentsMargins(0, 0, 0, 0)
            cur_key_layout._set_align_top_()
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

    def _get_pre_child_args(self):
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


class PrxOptionsNode(_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    PORT_STACK_CLS = PrxNodePortStack

    def __init__(self, path_or_name, *args, **kwargs):
        super(PrxOptionsNode, self).__init__(*args, **kwargs)
        self._path_dag_opt = bsc_core.BscPathOpt(path_or_name)
        # debug: do not set minimum height
        # self._qt_widget.setMinimumHeight(24)
        #
        qt_layout_0 = _qt_wgt_base.QtVBoxLayout(self._qt_widget)
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

    def build_by_data(self, configure):
        for k, v in configure.items():
            self.create_port_by_data(k.replace('/', '.'), v)

    def create_port_by_data(self, port_path, variants):
        widget_ = variants['widget']
        label_ = variants.get('label') or variants.get('name')
        tool_tip_ = variants.get('tool_tip')
        #
        ui_language = _gui_core.GuiUtil.get_language()
        #
        if ui_language == 'chs':
            if 'name_chs' in variants:
                label_ = variants['name_chs']
            if 'tool_tip_chs' in variants:
                tool_tip_ = variants['tool_tip_chs']
        #
        if widget_ in {'group'}:
            group = self._create_group_by_path(port_path)
            if label_:
                group.set_gui_name(label_)
            #
            expand = variants.get('expand') or False
            group.set_expanded(expand)

            collapse = variants.get('collapse') or False
            group.set_expanded(not collapse)
            #
            group.set_visible_condition(
                variants.get('visible_condition')
            )
            #
            if 'visible' in variants:
                group.set_visible(
                    variants['visible']
                )
            return
        #
        key_ = variants.get('key')
        value_ = variants.get('value')
        enable_ = variants.get('enable')
        lock_ = variants.get('lock') or False
        #
        join_to_next_ = variants.get('join_to_next') or False

        if widget_ in {'string'}:
            port = _port.PrxPortAsString(
                port_path,
                node_widget=self.widget
            )
            lock = variants.get('lock') or False
            if lock is True:
                port.set_locked(True)
            #
            port.set(value_)
            port.set_default(value_)
        elif widget_ in {'name'}:
            port = _port.PrxPortAsName(
                port_path,
                node_widget=self.widget
            )
            lock = variants.get('lock') or False
            if lock is True:
                port.set_locked(True)
            #
            port.set(value_)
            port.set_default(value_)

        elif widget_ in {'integer'}:
            port = _port.PrxPortForInteger(
                port_path,
                node_widget=self.widget
            )
            history_key_ = variants.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)

            port.set_default(value_)

            pull_history_latest = variants.get('pull_history_latest')
            if pull_history_latest is True:
                if port.pull_history_latest() is False:
                    port.set(value_)
            else:
                port.set(value_)
        
        elif widget_ in {'integer2'}:
            port = _port.PrxPortForIntegerTuple(
                port_path,
                node_widget=self.widget
            )
            history_key_ = variants.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)

            port.set_value_size(2)

            port.set_default(value_)

            pull_history_latest = variants.get('pull_history_latest')
            if pull_history_latest is True:
                if port.pull_history_latest() is False:
                    port.set(value_)
            else:
                port.set(value_)

            lock = variants.get('lock') or False
            if lock is True:
                port.set_locked(True)

        elif widget_ in {'float'}:
            port = _port.PrxPortAsFloat(
                port_path,
                node_widget=self.widget
            )
            history_key_ = variants.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)

            port.set_default(value_)

            pull_history_latest = variants.get('pull_history_latest')
            if pull_history_latest is True:
                if port.pull_history_latest() is False:
                    port.set(value_)
            else:
                port.set(value_)

        elif widget_ in {'float2'}:
            port = _port.PrxPortForFloatTuple(
                port_path,
                node_widget=self.widget
            )
            port.set_value_size(2)
            port.set(value_)
            port.set_default(value_)
        elif widget_ in {'float3'}:
            port = _port.PrxPortForFloatTuple(
                port_path,
                node_widget=self.widget
            )
            port.set_value_size(3)
            port.set(value_)
            port.set_default(value_)
        #
        elif widget_ in {'rgb', 'rgba'}:
            port = _port.PrxPortAsRgbaChoose(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
        # bool
        elif widget_ in {'boolean'}:
            value_ = value_ or False
            port = _port.PrxPortAsBoolean(
                port_path,
                node_widget=self.widget
            )

            history_key_ = variants.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)

            port.set_default(value_)

            pull_history_latest = variants.get('pull_history_latest')
            if pull_history_latest is True:
                if port.pull_history_latest() is False:
                    port.set(value_)
            else:
                port.set(value_)

        elif widget_ in {'enumerate'}:
            port = _port.PrxPortAsConstantChoose(
                port_path,
                node_widget=self.widget
            )
            if 'options' in variants:
                options_ = variants['options']
            else:
                if isinstance(value_, (tuple, list)):
                    options_ = value_
                else:
                    options_ = []
            port.set_options(options_)

            history_key_ = variants.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)

            default__ = None
            default_ = variants.get('default')
            default_index = variants.get('default_index')
            if default_ is not None:
                default__ = default_
            elif default_index is not None:
                default__ = options_[default_]
            else:
                if options_:
                    default__ = options_[0]

            if default_ is not None:
                port.set_default(default__)

            pull_history_latest = variants.get('pull_history_latest')
            if pull_history_latest is True:
                if port.pull_history_latest() is False:
                    if default_ is not None:
                        port.set(default_)
            else:
                if default_ is not None:
                    port.set(default_)

        elif widget_ in {'icon'}:
            all_application_icon = variants.get('all_application_icon')
            if all_application_icon is True:
                value_ = _gui_core.GuiIcon.find_all_keys_at('application')
                value_.insert(0, '')
            all_tool_base_icon = variants.get('all_tool_base_icon')
            if all_tool_base_icon is True:
                value_ = _gui_core.GuiIcon.find_all_keys_at('tool_style')
                value_.insert(0, '')

            port = _port.PrxPortAsIconChoose(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)

            default_ = variants.get('default')
            if default_ is not None:
                port.set(default_)
                port.set_default(default_)
        # capsule
        elif widget_ in {'capsule_string'}:
            port = _port.PrxPortAsCapsuleString(
                port_path,
                node_widget=self.widget
            )

            value_options = variants.get('options')
            if value_options:
                value_names = variants.get('option_names')
                if ui_language == 'chs':
                    if 'option_names_chs' in variants:
                        value_names = variants['option_names_chs']

                port.set_options(value_options, value_names)

                value_default = variants.get('default')
                if value_default is not None:
                    port.set(value_default)
                    port.set_default(value_default)
                else:
                    port.set(value_options[-1])
                    port.set_default(value_options[-1])

            lock = variants.get('lock') or False
            if lock is True:
                port.set_locked(True)

            history_key_ = variants.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)

            pull_history_latest = variants.get('pull_history_latest')
            if pull_history_latest is True:
                port.pull_history_latest()

        elif widget_ in {'capsule_strings'}:
            port = _port.PrxPortAsCapsuleStrings(
                port_path,
                node_widget=self.widget
            )
            value_options = variants.get('options')
            value_names = variants.get('labels')
            if ui_language == 'chs':
                if 'option_names_chs' in variants:
                    value_names = variants['option_names_chs']

            port.set_options(value_options, value_names)

            value_default = variants.get('default')
            if value_default is not None:
                port.set(value_default)
                port.set_default(value_default)

            lock = variants.get('lock') or False
            if lock is True:
                port.set_locked(True)

            history_key_ = variants.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)

            pull_history_latest = variants.get('pull_history_latest')
            if pull_history_latest is True:
                port.pull_history_latest()

        elif widget_ in {'file'}:
            open_or_save = variants.get('open_or_save')
            if open_or_save == 'save':
                port = _port.PrxPortAsFileSave(
                    port_path,
                    node_widget=self.widget
                )
            else:
                port = _port.PrxPortAsFileOpen(
                    port_path,
                    node_widget=self.widget
                )
            #
            history_key_ = variants.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)
            #
            port.set(value_)
            port.set_default(value_)
            ext_filter = variants.get('ext_filter')
            if ext_filter:
                port.set_ext_filter(ext_filter)

            ext_includes = variants.get('ext_includes')
            if ext_includes:
                port.set_ext_includes(ext_includes)

            pull_history_latest = variants.get('pull_history_latest')
            if pull_history_latest:
                port.pull_history_latest()
            #
            lock = variants.get('lock') or False
            if lock is True:
                port.set_locked(True)
        elif widget_ in {'directory'}:
            open_or_save_ = variants.get('open_or_save')
            if open_or_save_ == 'save':
                port = _port.PrxPortAsDirectorySave(
                    port_path,
                    node_widget=self.widget
                )
            else:
                port = _port.PrxPortAsDirectoryOpen(
                    port_path,
                    node_widget=self.widget
                )
            #
            history_key_ = variants.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)
            #
            port.set(value_)
            port.set_default(value_)
            #
            pull_history_latest = variants.get('pull_history_latest')
            if pull_history_latest:
                port.pull_history_latest()
        # storage array
        elif widget_ in {'directories'}:
            port = _port.PrxPortAsDirectoriesOpen(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
            #
            history_key_ = variants.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)
            #
            if 'history_visible' in variants:
                port.set_history_button_visible(variants['history_visible'])
        elif widget_ in {'files'}:
            port = _port.PrxPortAsFilesOpen(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)

            ext_includes = variants.get('ext_includes')
            if ext_includes:
                port.set_ext_includes(ext_includes)

            history_key_ = variants.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)
            #
            if 'history_visible' in variants:
                port.set_history_button_visible(variants['history_visible'])
        elif widget_ in {'medias'}:
            port = _port.PrxPortAsMediasOpen(
                port_path,
                node_widget=self.widget
            )
            #
            ext_includes = variants.get('ext_includes')
            if ext_includes:
                port.set_ext_includes(ext_includes)

            ext_filter = variants.get('ext_filter')
            if ext_filter:
                port.set_ext_filter(ext_filter)
            #
            history_key_ = variants.get('history_key')
            if history_key_:
                port.set_history_key(history_key_)
        #
        elif widget_ in {'values'}:
            port = _port.PrxPortForValueArray(
                port_path,
                node_widget=self.widget
            )
        #
        elif widget_ in {'values_choose'}:
            port = _port.PrxPortForValueArrayAsChoose(
                port_path,
                node_widget=self.widget
            )
            port.set_choose_values(value_)

        elif widget_ in {'shotgun_entity_choose'}:
            port = _port.PrxPortAsShotgunEntity(
                port_path,
                node_widget=self.widget
            )
            shotgun_entity_kwargs = variants.get('shotgun_entity_kwargs')
            if shotgun_entity_kwargs:
                port.set_shotgun_entity_kwargs(
                    shotgun_entity_kwargs,
                    keyword_filter_fields=variants.get('keyword_filter_fields'),
                    tag_filter_fields=variants.get('tag_filter_fields')
                )
                port.set(value_)

        elif widget_ in {'shotgun_entities_choose'}:
            port = _port.PrxPortAsShotgunEntities(
                port_path,
                node_widget=self.widget
            )
            shotgun_entity_kwargs = variants.get('shotgun_entity_kwargs')
            if shotgun_entity_kwargs:
                port.set_shotgun_entity_kwargs(
                    shotgun_entity_kwargs,
                    keyword_filter_fields=variants.get('keyword_filter_fields'),
                    tag_filter_fields=variants.get('tag_filter_fields')
                )
                port.set(value_)
        #
        elif widget_ in {'button'}:
            port = _port.PrxPortAsButton(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            if 'option_enable' in variants:
                port.set_option_enable(variants['option_enable'])

            if 'icon' in variants:
                port.set_icon(variants['icon'])

        elif widget_ in {'check_button'}:
            port = _port.PrxPortAsCheckButton(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_checked(
                variants.get('check', False)
            )

        elif widget_ in {'sub_process_button'}:
            port = _port.PrxSubProcessPort(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            if 'icon' in variants:
                port.set_icon(variants['icon'])
        elif widget_ in {'validator_button'}:
            port = _port.PrxValidatorPort(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
        #
        elif widget_ in {'project'}:
            port = _port.PrxPortAsRsvProjectChoose(
                port_path,
                node_widget=self.widget
            )
            if value_:
                port.set(value_)

            pull_history_latest = variants.get('pull_history_latest')
            if pull_history_latest:
                port.pull_history_latest()
        elif widget_ in {'rsv-obj'}:
            port = _port.PrxRsvObjChoosePort(
                port_path,
                node_widget=self.widget
            )
            # port.set(value_)
        elif widget_ in {'scheme'}:
            port = _port.PrxPortAsSchemChoose(
                port_path,
                scheme_key=variants['scheme_key'],
                node_widget=self.widget
            )
            port.set(value_)
        elif widget_ in {'script'}:
            port = _port.PrxPortAsScript(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
            if 'external_editor_ext' in variants:
                port.set_external_editor_ext(
                    variants['external_editor_ext']
                )
        #
        elif widget_ in {'components', 'node_list'}:
            port = _port.PrxNodeListViewPort(
                port_path,
                node_widget=self.widget
            )
        elif widget_ in {'node_tree'}:
            port = _port.PrxNodeTreeViewPort(
                port_path,
                node_widget=self.widget
            )
        #
        elif widget_ in {'file_list'}:
            port = _port.PrxPortAsFileList(
                port_path,
                node_widget=self.widget
            )
        elif widget_ in {'file_tree'}:
            port = _port.PrxPortAsFileTree(
                port_path,
                node_widget=self.widget
            )
        #
        elif widget_ in {'frames'}:
            port = _port.PrxPortAsFrames(
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
        port.set_gui_name(label_)
        port.set_use_enable(enable_)
        port.set_tool_tip(tool_tip_ or '...')
        port._set_join_to_next_flag(join_to_next_)
        port.set_locked(lock_)
        #
        height = variants.get('height')
        if height:
            port.set_height(height)

        self.add_port(port)

        # run after add
        port.set_visible_condition(
            variants.get('visible_condition')
        )

        if 'visible' in variants:
            port.set_visible(
                variants['visible']
            )

        if 'exclusive_set' in variants:
            port.update_exclusive_set(variants['exclusive_set'])

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

    def set_dict(self, dict_):
        for k, v in dict_.items():
            i_port = self.get_port(k)
            if i_port is not None:
                i_port.set(v)

    def get_enumerate_strings(self, key):
        port = self.get_port(key)
        if port is not None:
            return port.get_enumerate_strings()
