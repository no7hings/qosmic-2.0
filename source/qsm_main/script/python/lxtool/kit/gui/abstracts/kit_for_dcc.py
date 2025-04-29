# coding:utf-8
import six

import lxbasic.log as bsc_log

import lxsession.commands as ssn_commands
# gui
import lxgui.proxy.widgets as gui_prx_widgets


class AbsToolKitForDcc(gui_prx_widgets.PrxSessionWindow):
    def __init__(self, session, *args, **kwargs):
        super(AbsToolKitForDcc, self).__init__(session, *args, **kwargs)

    def gui_setup_fnc(self):
        self._top_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        self.add_widget(self._top_prx_tool_bar)
        self._top_prx_tool_bar.set_expanded(True)
        self._top_prx_tool_bar.set_align_left()

        self._switch_tool_box = gui_prx_widgets.PrxHToolBox()
        self._top_prx_tool_bar.add_widget(self._switch_tool_box)
        self._switch_tool_box.set_expanded(True)

        self._filter_tool_box = gui_prx_widgets.PrxHToolBox()
        self._top_prx_tool_bar.add_widget(self._filter_tool_box)

        self._filter_bar = gui_prx_widgets.PrxFilterBar()
        self._filter_tool_box.add_widget(self._filter_bar)

        self._scroll_bar = gui_prx_widgets.PrxVScrollArea()
        self.add_widget(self._scroll_bar)

        self._w_p, self._h_p = .5, .25

        self._w = 440
        self._h = 80

        self._percent_args = [('small', .25, .25), ('medium', 0.5, .25), ('large', 1.0, .25)]

        self.add_layout_buttons()

        self.connect_refresh_action_for(self.refresh_all)

        self.refresh_all()

    def add_layout_buttons(self):
        def click_fnc_(p_):
            _pre = self._w_p, self._h_p
            if p_ != _pre:
                _w_p, _h_p = p_
                self._w_p, self._h_p = _w_p, _h_p
                for k, v in self._view_dict.items():
                    v.set_item_size(
                        self._w*self._w_p, self._h*self._h_p
                    )
                    v.refresh_widget()

        import functools

        tools = []
        for i_key, i_w_p, i_h_p in self._percent_args:
            i_b = gui_prx_widgets.PrxIconToggleButton()
            self._switch_tool_box.add_widget(i_b)
            i_b.set_icon_name('tool/icon-{}'.format(i_key))
            if i_w_p == self._w_p:
                i_b.set_checked(True)
            i_b.connect_check_changed_as_exclusive_to(
                functools.partial(click_fnc_, (i_w_p, i_h_p))
            )
            i_b._qt_widget._set_exclusive_widgets_(tools)
            tools.append(i_b._qt_widget)

    def refresh_all(self):
        import lxresolver.scripts as rsv_scripts

        self._match_dict = rsv_scripts.ScpEnvironment.get_as_dict()

        self.build_tools()

    def build_tools(self):
        self._view_dict = {}
        self._scroll_bar.restore()
        c = self._session.get_configure()
        self.build_tool_by_hook_data(c.get('hooks') or [])
        self.build_tool_by_option_hook_data(c.get('option-hooks') or [])

    def gui_get_view_args(self, group_name):
        group_path = '/{}'.format(group_name)
        if group_path not in self._view_dict:
            tool_group = gui_prx_widgets.PrxHToolGroupNew()
            self._scroll_bar.add_widget(tool_group)
            tool_group.set_expanded(True)
            tool_group.set_name(group_name)
            #
            grid_layout_widget = gui_prx_widgets.PrxToolGridLayoutWidget()
            grid_layout_widget.set_path(group_path)
            self._view_dict[group_path] = grid_layout_widget
            tool_group.add_widget(grid_layout_widget)
            grid_layout_widget.set_item_size(self._w*self._w_p, self._h*self._h_p)
        else:
            grid_layout_widget = self._view_dict[group_path]
        return grid_layout_widget

    def build_tool_by_hook_data(self, data):
        with bsc_log.LogProcessContext.create(maximum=len(data), label='gui-add for hook') as g_p:
            for i_args in data:
                g_p.do_update()
                if isinstance(i_args, six.string_types):
                    i_key = i_args
                    i_extend_kwargs = {}
                    i_hook_args = ssn_commands.get_hook_args(
                        i_key
                    )
                elif isinstance(i_args, dict):
                    i_key = list(i_args.keys())[0]
                    i_extend_kwargs = list(i_args.values())[0]
                    i_hook_args = ssn_commands.get_hook_args(
                        i_key
                    )
                else:
                    raise RuntimeError()
                #
                if i_hook_args is not None:
                    self.add_tool(i_hook_args, i_extend_kwargs)

    def build_tool_by_option_hook_data(self, data):
        with bsc_log.LogProcessContext.create(maximum=len(data), label='gui-add for hook') as g_p:
            for i_args in data:
                g_p.do_update()
                if isinstance(i_args, six.string_types):
                    i_key = i_args
                    i_extend_kwargs = {}
                    i_hook_args = ssn_commands.get_option_hook_args(
                        i_key
                    )
                elif isinstance(i_args, dict):
                    i_key = i_args.keys()[0]
                    i_extend_kwargs = i_args.values()[0]
                    i_hook_args = ssn_commands.get_option_hook_args(
                        i_key
                    )
                else:
                    raise RuntimeError()
                #
                if i_hook_args is not None:
                    self.add_tool(i_hook_args, i_extend_kwargs)

    def add_tool(self, hook_args, kwargs_extend):
        session, execute_fnc = hook_args
        if session.get_is_loadable() is True:
            if session.get_is_match_condition(
                    self._match_dict
            ) is True:
                gui_configure = session.gui_configure
                if 'gui_parent' in kwargs_extend:
                    gui_configure.set('group_name', kwargs_extend.get('gui_parent'))
                #
                group_name = gui_configure.get('group_name')
                grid_layout_widget = self.gui_get_view_args(group_name)
                #
                name = gui_configure.get('name')
                icon_name = gui_configure.get('icon_name')
                tool_tip_ = gui_configure.get('tool_tip') or ''

                press_item = gui_prx_widgets.PrxPressButton()
                grid_layout_widget.add_widget(press_item)
                press_item.set_name(name)
                if icon_name:
                    press_item.set_icon_name(icon_name)
                else:
                    press_item.set_icon_color_by_name(name)

                tool_tip = []
                if session.configure.get('option.type').endswith('-panel'):
                    tool_tip_add = '"LMB-click" to open tool-panel'
                    press_item.set_option_click_enable(True)
                else:
                    tool_tip_add = '"LMB-click" to execute'

                tool_tip.append(tool_tip_add)

                if isinstance(tool_tip_, (tuple, list)):
                    tool_tip.extend(tool_tip_)
                elif isinstance(tool_tip_, six.string_types):
                    tool_tip.append(tool_tip_)

                press_item.set_tool_tip(tool_tip)

                press_item.connect_press_clicked_to(
                    execute_fnc
                )
