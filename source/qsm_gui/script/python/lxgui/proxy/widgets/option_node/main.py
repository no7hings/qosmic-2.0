# coding:utf-8
import six

import functools

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxuniverse.abstracts as unr_abstracts
# gui
from .... import core as _gui_core
# qt widgets
from ....qt.widgets import base as _qt_wgt_base

from ....qt.widgets import utility as _qt_wgt_utility
# proxy abstracts
from ... import abstracts as _prx_abstracts
# proxy widgets

from. import _port_for_constant

from. import _port_for_array

from. import _port_for_extra

from. import _port_for_storage

from. import _port_for_stg_array

from. import _port_for_choose

from. import _port_for_capsule

from. import _port_for_tag

from. import _port_for_script

from. import _port_for_tuple

from. import _port_for_button

from. import _port_for_resolver

from. import _port_for_shotgun

from. import _port_for_dcc

from. import _port_for_file

from. import _port_for_group


class _PortStackNode(unr_abstracts.AbsObjStack):
    def __init__(self):
        super(_PortStackNode, self).__init__()

    def get_key(self, obj):
        return obj.get_port_path()


class PrxOptionsNode(_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    PORT_STACK_CLS = _PortStackNode

    def __init__(self, path_or_name, *args, **kwargs):
        super(PrxOptionsNode, self).__init__(*args, **kwargs)
        self._path_dag_opt = bsc_core.BscNodePathOpt(path_or_name)
        # debug: do not set minimum height
        # self._qt_widget.setMinimumHeight(24)

        qt_layout_0 = _qt_wgt_base.QtVBoxLayout(self._qt_widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(0)

        self._port_stack = self.PORT_STACK_CLS()
        self._port_switch_stack = self.PORT_STACK_CLS()

        self._prx_root_group = self.create_root_group()
        qt_layout_0.addWidget(self._prx_root_group._prx_widget._qt_widget)

        self._gui_history_group = None

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
        group = _port_for_group.PrxNodePortGroup(
            'pseudo_root', self, True
        )
        group._prx_widget.get_widget()._set_line_draw_enable_(True)
        return group

    def _create_group_by_path(self, port_path):
        group_cur = self.get_pseudo_root()
        if port_path:
            components = bsc_core.BscPortPathOpt(port_path).get_components()
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
        self._port_stack.add_object(port)
        if hasattr(port, 'connect_tab_pressed_to'):
            connect_result = port.connect_tab_pressed_to(functools.partial(self.focus_next_fnc, port))
            if connect_result is True:
                self._port_switch_stack.add_object(port)

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

    def create_port_by_data(self, port_path, create_options):
        widget_type = create_options['widget']
        widget_name = create_options.get('label') or create_options.get('name')
        tool_tip_ = create_options.get('tool_tip')

        gui_language = _gui_core.GuiUtil.get_language()

        if gui_language == _gui_core.GuiLanguage.CHS:
            if 'name_chs' in create_options:
                widget_name = create_options['name_chs']
            if 'tool_tip_chs' in create_options:
                tool_tip_ = create_options['tool_tip_chs']

        if widget_type in {'group'}:
            prx_group = self._create_group_by_path(port_path)
            if widget_name:
                prx_group.set_gui_name(widget_name)
            #
            expand = create_options.get('expand') or False
            prx_group.set_expanded(expand)

            collapse = create_options.get('collapse') or False
            prx_group.set_expanded(not collapse)
            #
            prx_group.set_visible_condition(
                create_options.get('visible_condition')
            )

            if tool_tip_:
                prx_group.set_tool_tip(tool_tip_)
            #
            if 'visible' in create_options:
                prx_group.set_visible(
                    create_options['visible']
                )
            return

        key_ = create_options.get('key')
        value_ = create_options.get('value')
        enable_ = create_options.get('enable')
        lock_ = create_options.get('lock') or False

        join_to_next_ = create_options.get('join_to_next') or False

        history_key_ = create_options.get('history_key')
        history_group_ = create_options.get('history_group')

        use_history_group_ = create_options.get('use_history_group')
        if not history_group_:
            if use_history_group_:
                history_group_ = self._gui_history_group

        if widget_type in {'string'}:
            port = _port_for_constant.PrxPortForString(
                port_path,
                node_widget=self.widget
            )
            lock = create_options.get('lock') or False
            if lock is True:
                port.set_locked(True)
            #
            port.set(value_)
            port.set_default(value_)
        elif widget_type in {'name'}:
            port = _port_for_constant.PrxPortForName(
                port_path,
                node_widget=self.widget
            )
            lock = create_options.get('lock') or False
            if lock is True:
                port.set_locked(True)
            #
            port.set(value_)
            port.set_default(value_)

        elif widget_type in {'integer'}:
            port = _port_for_constant.PrxPortForInteger(
                port_path,
                node_widget=self.widget
            )

            if history_key_:
                port.set_history_key(history_key_)
            elif history_group_:
                port.set_history_group(history_group_)

            port.set_default(value_)

            pull_history_latest = create_options.get('pull_history_latest')
            if pull_history_latest is True:
                if port.pull_history_latest() is False:
                    port.set(value_)
            else:
                port.set(value_)

        elif widget_type in {'integer2'}:
            port = _port_for_tuple.PrxPortForIntegerTuple(
                port_path,
                node_widget=self.widget
            )

            if history_key_:
                port.set_history_key(history_key_)
            elif history_group_:
                port.set_history_group(history_group_)

            port.set_value_size(2)

            port.set_default(value_)

            pull_history_latest = create_options.get('pull_history_latest')
            if pull_history_latest is True:
                if port.pull_history_latest() is False:
                    port.set(value_)
            else:
                port.set(value_)

            lock = create_options.get('lock') or False
            if lock is True:
                port.set_locked(True)

        elif widget_type in {'float'}:
            port = _port_for_constant.PrxPortForFloat(
                port_path,
                node_widget=self.widget
            )
            if history_key_:
                port.set_history_key(history_key_)
            elif history_group_:
                port.set_history_group(history_group_)

            port.set_default(value_)

            pull_history_latest = create_options.get('pull_history_latest')
            if pull_history_latest is True:
                if port.pull_history_latest() is False:
                    port.set(value_)
            else:
                port.set(value_)
        elif widget_type in {'float2'}:
            port = _port_for_tuple.PrxPortForFloatTuple(
                port_path,
                node_widget=self.widget
            )
            port.set_value_size(2)
            port.set(value_)
            port.set_default(value_)
        elif widget_type in {'float3'}:
            port = _port_for_tuple.PrxPortForFloatTuple(
                port_path,
                node_widget=self.widget
            )
            port.set_value_size(3)
            port.set(value_)
            port.set_default(value_)
        #
        elif widget_type in {'rgb', 'rgba'}:
            port = _port_for_extra.PrxPortForRgbaChoose(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
        # bool
        elif widget_type in {'boolean'}:
            value_ = value_ or False
            port = _port_for_extra.PrxPortForBoolean(
                port_path,
                node_widget=self.widget
            )

            if history_key_:
                port.set_history_key(history_key_)
            elif history_group_:
                port.set_history_group(history_group_)

            port.set_default(value_)

            pull_history_latest = create_options.get('pull_history_latest')
            if pull_history_latest is True:
                if port.pull_history_latest() is False:
                    port.set(value_)
            else:
                port.set(value_)

        elif widget_type in {'enumerate'}:
            port = _port_for_choose.PrxPortForConstantChoose(
                port_path,
                node_widget=self.widget
            )
            if 'options' in create_options:
                options_ = create_options['options']
            else:
                if isinstance(value_, (tuple, list)):
                    options_ = value_
                else:
                    options_ = []
            port.set_options(options_)

            if history_key_:
                port.set_history_key(history_key_)
            elif history_group_:
                port.set_history_group(history_group_)

            default__ = None
            default_ = create_options.get('default')
            default_index = create_options.get('default_index')
            if default_ is not None:
                default__ = default_
            elif default_index is not None:
                default__ = options_[default_index]
            else:
                if options_:
                    default__ = options_[0]

            if default__ is not None:
                port.set_default(default__)

            pull_history_latest = create_options.get('pull_history_latest')
            if pull_history_latest is True:
                if port.pull_history_latest() is False:
                    if default__ is not None:
                        port.set(default__)
            else:
                if default__ is not None:
                    port.set(default__)

        elif widget_type in {'icon'}:
            all_application_icon = create_options.get('all_application_icon')
            if all_application_icon is True:
                value_ = _gui_core.GuiIcon.find_all_keys_at('application')
                value_.insert(0, '')
            all_tool_base_icon = create_options.get('all_tool_base_icon')
            if all_tool_base_icon is True:
                value_ = _gui_core.GuiIcon.find_all_keys_at('tool_style')
                value_.insert(0, '')

            port = _port_for_extra.PrxPortForIconChoose(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)

            default_ = create_options.get('default')
            if default_ is not None:
                port.set(default_)
                port.set_default(default_)

        # capsule
        elif widget_type in {'capsule_string'}:
            port = _port_for_capsule.PrxPortForCapsuleString(
                port_path,
                node_widget=self.widget
            )

            value_options = create_options.get('options')
            if value_options:
                value_names = create_options.get('option_names')
                if gui_language == _gui_core.GuiLanguage.CHS:
                    if 'option_names_chs' in create_options:
                        value_names = create_options['option_names_chs']

                port.set_options(value_options, value_names)

                value_default = create_options.get('default')
                if value_default is not None:
                    port.set(value_default)
                    port.set_default(value_default)
                else:
                    port.set(value_options[-1])
                    port.set_default(value_options[-1])

            lock = create_options.get('lock') or False
            if lock is True:
                port.set_locked(True)

            if history_key_:
                port.set_history_key(history_key_)
            elif history_group_:
                port.set_history_group(history_group_)

            pull_history_latest = create_options.get('pull_history_latest')
            if pull_history_latest is True:
                port.pull_history_latest()

        elif widget_type in {'capsule_strings'}:
            port = _port_for_capsule.PrxPortForCapsuleStrings(
                port_path,
                node_widget=self.widget
            )
            value_options = create_options.get('options')
            value_names = create_options.get('labels')
            if gui_language == _gui_core.GuiLanguage.CHS:
                if 'option_names_chs' in create_options:
                    value_names = create_options['option_names_chs']

            port.set_options(value_options, value_names)

            value_default = create_options.get('default')
            if value_default is not None:
                port.set(value_default)
                port.set_default(value_default)

            lock = create_options.get('lock') or False
            if lock is True:
                port.set_locked(True)

            if history_key_:
                port.set_history_key(history_key_)
            elif history_group_:
                port.set_history_group(history_group_)

            pull_history_latest = create_options.get('pull_history_latest')
            if pull_history_latest is True:
                port.pull_history_latest()

        # tag
        elif widget_type in {'tag_string'}:
            port = _port_for_tag.PrxPortForTagString(
                port_path,
                node_widget=self.widget
            )

            value_options = create_options.get('options')
            if value_options:
                value_names = create_options.get('option_names')
                if gui_language == _gui_core.GuiLanguage.CHS:
                    if 'option_names_chs' in create_options:
                        value_names = create_options['option_names_chs']

                port.set_options(value_options, value_names)

                value_default = create_options.get('default')
                if value_default is not None:
                    port.set(value_default)
                    port.set_default(value_default)
                else:
                    port.set(value_options[-1])
                    port.set_default(value_options[-1])

            lock = create_options.get('lock') or False
            if lock is True:
                port.set_locked(True)

            if history_key_:
                port.set_history_key(history_key_)
            elif history_group_:
                port.set_history_group(history_group_)

            pull_history_latest = create_options.get('pull_history_latest')
            if pull_history_latest is True:
                port.pull_history_latest()

        elif widget_type in {'tag_strings'}:
            port = _port_for_tag.PrxPortForTagStrings(
                port_path,
                node_widget=self.widget
            )
            value_options = create_options.get('options')
            value_names = create_options.get('labels')
            if gui_language == _gui_core.GuiLanguage.CHS:
                if 'option_names_chs' in create_options:
                    value_names = create_options['option_names_chs']

            port.set_options(value_options, value_names)

            value_default = create_options.get('default')
            if value_default is not None:
                port.set(value_default)
                port.set_default(value_default)

            lock = create_options.get('lock') or False
            if lock is True:
                port.set_locked(True)

            if history_key_:
                port.set_history_key(history_key_)
            elif history_group_:
                port.set_history_group(history_group_)

            pull_history_latest = create_options.get('pull_history_latest')
            if pull_history_latest is True:
                port.pull_history_latest()

        elif widget_type in {'file'}:
            open_or_save = create_options.get('open_or_save')
            if open_or_save == 'save':
                port = _port_for_storage.PrxPortForFileSave(
                    port_path,
                    node_widget=self.widget
                )
            else:
                port = _port_for_storage.PrxPortForFileOpen(
                    port_path,
                    node_widget=self.widget
                )

            if history_key_:
                port.set_history_key(history_key_)
            elif history_group_:
                port.set_history_group(history_group_)

            port.set(value_)
            port.set_default(value_)
            ext_filter = create_options.get('ext_filter')
            if ext_filter:
                port.set_ext_filter(ext_filter)

            ext_includes = create_options.get('ext_includes')
            if ext_includes:
                port.set_ext_includes(ext_includes)

            pull_history_latest = create_options.get('pull_history_latest')
            if pull_history_latest:
                port.pull_history_latest()
            #
            lock = create_options.get('lock') or False
            if lock is True:
                port.set_locked(True)
        elif widget_type in {'directory'}:
            open_or_save_ = create_options.get('open_or_save')
            if open_or_save_ == 'save':
                port = _port_for_storage.PrxPortForDirectorySave(
                    port_path,
                    node_widget=self.widget
                )
            else:
                port = _port_for_storage.PrxPortForDirectoryOpen(
                    port_path,
                    node_widget=self.widget
                )

            if history_key_:
                port.set_history_key(history_key_)
            elif history_group_:
                port.set_history_group(history_group_)

            port.set(value_)
            port.set_default(value_)

            pull_history_latest = create_options.get('pull_history_latest')
            if pull_history_latest:
                port.pull_history_latest()
        # storage array
        elif widget_type in {'directories'}:
            port = _port_for_stg_array.PrxPortForDirectoriesOpen(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)

            if history_key_:
                port.set_history_key(history_key_)
            elif history_group_:
                port.set_history_group(history_group_)

            if 'history_visible' in create_options:
                port.set_history_button_visible(create_options['history_visible'])
        elif widget_type in {'files'}:
            port = _port_for_stg_array.PrxPortForFilesOpen(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)

            ext_includes = create_options.get('ext_includes')
            if ext_includes:
                port.set_ext_includes(ext_includes)

            if history_key_:
                port.set_history_key(history_key_)
            elif history_group_:
                port.set_history_group(history_group_)

            if 'history_visible' in create_options:
                port.set_history_button_visible(create_options['history_visible'])
        elif widget_type in {'medias'}:
            port = _port_for_stg_array.PrxPortForMediasOpen(
                port_path,
                node_widget=self.widget
            )
            #
            ext_includes = create_options.get('ext_includes')
            if ext_includes:
                port.set_ext_includes(ext_includes)

            ext_filter = create_options.get('ext_filter')
            if ext_filter:
                port.set_ext_filter(ext_filter)

            if history_key_:
                port.set_history_key(history_key_)
            elif history_group_:
                port.set_history_group(history_group_)

        elif widget_type in {'values'}:
            port = _port_for_array.PrxPortForArray(
                port_path,
                node_widget=self.widget
            )
        #
        elif widget_type in {'values_choose'}:
            port = _port_for_array.PrxPortForArrayChoose(
                port_path,
                node_widget=self.widget
            )
            port.set_choose_values(value_)

        elif widget_type in {'shotgun_entity_choose'}:
            port = _port_for_shotgun.PrxPortForShotgunEntity(
                port_path,
                node_widget=self.widget
            )
            shotgun_entity_kwargs = create_options.get('shotgun_entity_kwargs')
            if shotgun_entity_kwargs:
                port.set_shotgun_entity_kwargs(
                    shotgun_entity_kwargs,
                    keyword_filter_fields=create_options.get('keyword_filter_fields'),
                    tag_filter_fields=create_options.get('tag_filter_fields')
                )
                port.set(value_)

        elif widget_type in {'shotgun_entities_choose'}:
            port = _port_for_shotgun.PrxPortForShotgunEntities(
                port_path,
                node_widget=self.widget
            )
            shotgun_entity_kwargs = create_options.get('shotgun_entity_kwargs')
            if shotgun_entity_kwargs:
                port.set_shotgun_entity_kwargs(
                    shotgun_entity_kwargs,
                    keyword_filter_fields=create_options.get('keyword_filter_fields'),
                    tag_filter_fields=create_options.get('tag_filter_fields')
                )
                port.set(value_)
        #
        elif widget_type in {'button'}:
            port = _port_for_button.PrxPortForPressButton(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            if 'option_enable' in create_options:
                port.set_option_enable(create_options['option_enable'])

            if 'icon' in create_options:
                port.set_icon(create_options['icon'])

            if 'menu_enable' in create_options:
                port.set_menu_enable(create_options['menu_enable'])

            if 'use_name_icon' in create_options:
                port.set_icon_text(widget_name)

            if 'icon_text' in create_options:
                icon_text = create_options['icon_text']
                if gui_language == _gui_core.GuiLanguage.CHS:
                    if 'icon_text_chs' in create_options:
                        icon_text = create_options['icon_text_chs']
                port.set_icon_text(icon_text)

        elif widget_type in {'check_button'}:
            port = _port_for_button.PrxPortForCheckButton(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_checked(
                create_options.get('check', False)
            )

        elif widget_type in {'sub_process_button'}:
            port = _port_for_button.PrxPortForSpcButton(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            if 'icon' in create_options:
                port.set_icon(create_options['icon'])
        elif widget_type in {'validator_button'}:
            port = _port_for_button.PrxPortForValidateButton(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
        #
        elif widget_type in {'project'}:
            port = _port_for_resolver.PrxPortForRsvProjectChoose(
                port_path,
                node_widget=self.widget
            )
            if value_:
                port.set(value_)

            pull_history_latest = create_options.get('pull_history_latest')
            if pull_history_latest:
                port.pull_history_latest()
        elif widget_type in {'rsv-obj'}:
            port = _port_for_resolver.PrxPortForRsvChoose(
                port_path,
                node_widget=self.widget
            )
            # port.set(value_)
        elif widget_type in {'scheme'}:
            port = _port_for_choose.PrxPortForSchemChoose(
                port_path,
                scheme_key=create_options['scheme_key'],
                node_widget=self.widget
            )
            port.set(value_)
        elif widget_type in {'script'}:
            port = _port_for_script.PrxPortForContent(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
            if 'external_editor_ext' in create_options:
                port.set_external_editor_ext(
                    create_options['external_editor_ext']
                )
        #
        elif widget_type in {'node_list'}:
            port = _port_for_dcc.PrxPortForNodeList(
                port_path,
                node_widget=self.widget
            )
        elif widget_type in {'node_tree'}:
            port = _port_for_dcc.PrxPortForNodeTree(
                port_path,
                node_widget=self.widget
            )
        #
        elif widget_type in {'file_list'}:
            port = _port_for_file.PrxPortForFileList(
                port_path,
                node_widget=self.widget
            )
        elif widget_type in {'file_tree'}:
            port = _port_for_file.PrxPortForFileTree(
                port_path,
                node_widget=self.widget
            )
        #
        elif widget_type in {'frames'}:
            port = _port_for_constant.PrxPortForFrameString(
                port_path,
                node_widget=self.widget
            )
            port.set(value_)
            port.set_default(value_)
        #
        else:
            raise TypeError()

        port.WIDGET_TYPE = widget_type
        port.set_key(key_)
        port.set_gui_name(widget_name)
        port.set_use_enable(enable_)
        port.set_tool_tip(tool_tip_ or '...')
        port._set_join_to_next_flag(join_to_next_)
        port.set_locked(lock_)
        #
        height = create_options.get('height')
        if height:
            port.set_height(height)

        self.add_port(port)

        # run after add
        port.set_visible_condition(
            create_options.get('visible_condition')
        )

        if 'visible' in create_options:
            port.set_visible(
                create_options['visible']
            )

        if 'exclusive_set' in create_options:
            port.update_exclusive_set(create_options['exclusive_set'])

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
            bsc_log.Log.trace_method_error(
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

    def set_history_group(self, arg):
        if arg:
            if isinstance(arg, six.string_types):
                key = [arg]
            elif isinstance(arg, (tuple, list)):
                key = list(arg)
            else:
                raise RuntimeError()

            self._gui_history_group = key

    def get_history_group(self):
        return self._gui_history_group
