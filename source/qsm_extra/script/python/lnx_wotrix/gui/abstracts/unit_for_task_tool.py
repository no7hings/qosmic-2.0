# coding:utf-8
import functools

import lxgui.core as gui_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.qt.view_widgets as gui_qt_view_widgets

import lxgui.proxy.widgets as gui_prx_widgets


class AbsPrxNodeViewForTaskTool(gui_prx_widgets.PrxVirtualBaseSubunit):
    def __init__(self, window, page, unit, session):
        super(AbsPrxNodeViewForTaskTool, self).__init__(window, page, unit, session)

        self._qt_tree_widget = gui_qt_view_widgets.QtTreeWidget()
        self._unit._prx_h_splitter.add_widget(self._qt_tree_widget)

        self._qt_tree_widget.refresh.connect(
            functools.partial(self.do_gui_refresh_all, True)
        )
    
    def do_gui_refresh_all(self, force=False):
        pass


class AbsPrxToolsetForTaskTool(gui_prx_widgets.PrxVirtualBaseSubunit):
    def __init__(self, window, page, unit, session):
        super(AbsPrxToolsetForTaskTool, self).__init__(window, page, unit, session)
        
        prx_v_sca = gui_prx_widgets.PrxVScrollArea()

        self._unit._toolset_prx_tab_tool_box.add_widget(
            prx_v_sca,
            key=self.GUI_KEY,
            name=gui_core.GuiUtil.choice_gui_name(
                self._window._language, self._unit._configure.get('build.{}'.format(self.GUI_KEY))
            ),
            icon_name_text=self.GUI_KEY,
            tool_tip=gui_core.GuiUtil.choice_gui_tool_tip(
                self._window._language, self._unit._configure.get('build.{}'.format(self.GUI_KEY))
            )
        )

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            self._window.choice_gui_name(
                self._unit._configure.get('build.{}.options'.format(self.GUI_KEY))
            )
        )
        prx_v_sca.add_widget(self._prx_options_node)

        self._prx_options_node.build_by_data(
            self._unit._configure.get('build.{}.options.parameters'.format(self.GUI_KEY))
        )


class AbsPrxUnitForTaskTool(gui_prx_widgets.PrxBaseUnit):
    GUI_KEY = None

    GUI_RESOURCE_VIEW_CLS = None

    TASK_TOOL_OPT_CLS = None

    def __init__(self, window, page, session, *args, **kwargs):
        super(AbsPrxUnitForTaskTool, self).__init__(window, page, session, *args, **kwargs)
        
        self._gui_task_tool_opt = None
        
        self._configure = self.generate_local_configure()

        self.gui_unit_setup_fnc()

    def _on_gui_left_visible_swap(self, boolean):
        self._prx_h_splitter.swap_contract_left_or_top_at(0)

    def _gui_add_main_tools(self):
        self._left_visible_swap_tool = gui_prx_widgets.PrxToggleButton()
        self._main_prx_tool_box.add_widget(self._left_visible_swap_tool)
        self._left_visible_swap_tool.set_name('task')
        self._left_visible_swap_tool.set_icon_name('tree')
        self._left_visible_swap_tool.set_checked(True)
        self._left_visible_swap_tool.connect_check_toggled_to(self._on_gui_left_visible_swap)

        self._task_qt_button = gui_qt_widgets.QtIconPressButton()
        self._main_prx_tool_box.add_widget(self._task_qt_button)
        self._task_qt_button._set_name_text_('task')
        self._task_qt_button._set_icon_name_('workspace/task')

        self._task_qt_info_label = gui_qt_widgets.QtInfoBubble()
        self._main_prx_tool_box.add_widget(self._task_qt_info_label)
        self._task_qt_info_label._set_text_('N/a')
        self._task_qt_info_label._set_style_(
            self._task_qt_info_label.Style.Frame
        )

    def gui_unit_setup_fnc(self):
        self._top_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        self._qt_layout.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_align_left()
        self._top_prx_tool_bar.set_expanded(True)

        # main tool box
        self._main_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'main'
        )
        self._gui_add_main_tools()

        self._scene_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'scene', size_mode=1
        )

        self._scene_src_qt_input = gui_qt_widgets.QtInputForStorage()
        self._scene_prx_tool_box.add_widget(self._scene_src_qt_input)
        self._scene_src_qt_input._set_storage_scheme_(self._scene_src_qt_input.StorageScheme.FileOpen)
        self._scene_src_qt_input._set_history_key_(
            '{}.{}.scene'.format(self._window.GUI_KEY, self._gui_sub_key)
        )

        prx_v_sca = gui_prx_widgets.PrxVScrollArea()
        self._qt_layout.addWidget(prx_v_sca.widget)

        self._prx_h_splitter = gui_prx_widgets.PrxHSplitter()
        prx_v_sca.add_widget(self._prx_h_splitter)

        self._gui_resource_view_opt = self.GUI_RESOURCE_VIEW_CLS(
            self._window, self._page, self, self._session
        )

        self._toolset_prx_tab_tool_box = gui_prx_widgets.PrxVTabToolBox()
        self._prx_h_splitter.add_widget(self._toolset_prx_tab_tool_box)
        self._toolset_prx_tab_tool_box.set_tab_direction(
            self._toolset_prx_tab_tool_box.TabDirections.RightToLeft
        )
        self._toolset_prx_tab_tool_box.set_history_key(
            [self._window.GUI_KEY, '{}.page'.format(self._gui_path)]
        )

        for i in self.TOOLSET_CLASSES:
            i_tool_set = i(self._window, self._page, self, self._session)
            self._tab_widget_dict[i_tool_set.GUI_KEY] = i_tool_set

        self._toolset_prx_tab_tool_box.load_history()

        self._toolset_prx_tab_tool_box.connect_current_changed_to(
            self.do_gui_refresh_toolsets
        )

        self._prx_h_splitter.set_contract_enable(False)
        self._prx_h_splitter.set_fixed_size_at(0, 320)

    def gui_setup_post_fnc(self):
        self._top_prx_tool_bar.do_gui_refresh()

    def do_gui_refresh_toolsets(self):
        key = self._toolset_prx_tab_tool_box.get_current_key()
        toolset = self.gui_find_page(key)
        if toolset:
            toolset.do_gui_refresh_all()

    def do_gui_refresh_all(self):
        task_session = self._page._task_session
        if task_session is not None:
            task = task_session.properties['task']
            scene_path = task_session.properties['result']
            scene_src_path_pre = self._scene_src_qt_input._get_value_()
            if scene_path != scene_src_path_pre:
                task_tool_opt = self._generate_gui_task_tool_opt_fnc(task_session)
                if task_tool_opt is not None:
                    self._task_qt_info_label._set_text_(task)

                    self._gui_task_tool_opt = task_tool_opt
                    self._scene_src_qt_input._set_value_(scene_path)
                    self._scene_src_qt_input._push_history_(scene_path)

            # refresh all time
            self._gui_resource_view_opt.do_gui_refresh_all()
        else:
            self._gui_task_tool_opt = None

        self.do_gui_refresh_toolsets()

        self._top_prx_tool_bar.do_gui_refresh()

    def _generate_gui_task_tool_opt_fnc(self, task_session):
        if self.TASK_TOOL_OPT_CLS is not None:
            return task_session.generate_opt_for(
                self.TASK_TOOL_OPT_CLS
            )
    
    def generate_gui_task_tool_opt(self):
        task_session = self._page._task_session
        if task_session is not None:
            return self._generate_gui_task_tool_opt_fnc(task_session)
