# coding:utf-8
import functools

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.qt.view_widgets as gui_qt_view_widgets

import lxgui.proxy.widgets as gui_prx_widgets


class _GuiBaseOpt(object):
    def __init__(self, window, page, session):
        self._window = window
        self._page = page
        self._session = session

        self._gui_thread_flag = 0

    def gui_update_thread_flag(self):
        self._gui_thread_flag += 1


class AbsGuiNodeOpt(_GuiBaseOpt):
    def __init__(self, window, page, session):
        super(AbsGuiNodeOpt, self).__init__(window, page, session)

        self._qt_tree_widget = gui_qt_view_widgets.QtTreeWidget()
        self._page._prx_h_splitter.add_widget(self._qt_tree_widget)

        self._qt_tree_widget.refresh.connect(
            functools.partial(self.do_gui_refresh_all, True)
        )
    
    def do_gui_refresh_all(self, force=False):
        pass


class AbsPrxToolset(gui_prx_widgets.PrxBaseUnit):
    UNIT_KEY = None

    GUI_NODE_OPT_CLS = None

    def __init__(self, window, page, session, *args, **kwargs):
        super(AbsPrxToolset, self).__init__(window, page, session, *args, **kwargs)
        
        self._task_worker = None

        self.gui_build_unit()

    def _gui_update_task_visible(self, boolean):
        pass
        # self._prx_h_splitter.swap_contract_left_or_top_at(0)

    def _gui_add_main_tools(self):
        for i in [
            ('task', 'tree', '', self._gui_update_task_visible)
        ]:
            i_key, i_icon_name, i_tool_tip, i_fnc = i
            i_tool = gui_prx_widgets.PrxToggleButton()
            self._main_prx_tool_box.add_widget(i_tool)
            i_tool.set_name(i_key)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip(i_tool_tip)
            i_tool.set_checked(True)
            i_tool.connect_check_toggled_to(i_fnc)

    def gui_build_unit(self):
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
            'scene'
        )

        self._scene_qt_info_label = gui_qt_widgets.QtInfoLabel()
        self._scene_prx_tool_box.add_widget(self._scene_qt_info_label)

        prx_v_sca = gui_prx_widgets.PrxVScrollArea()
        self._qt_layout.addWidget(prx_v_sca.widget)

        self._prx_h_splitter = gui_prx_widgets.PrxHSplitter()
        prx_v_sca.add_widget(self._prx_h_splitter)

        self._gui_node_opt = self.GUI_NODE_OPT_CLS(self._window, self, self._session)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            self._window.choice_name(
                self._window._configure.get('build.{}.{}.options'.format(self._page.PAGE_KEY, self.UNIT_KEY))
            )
        )
        self._prx_h_splitter.add_widget(self._prx_options_node)

        self._prx_options_node.build_by_data(
            self._window._configure.get('build.{}.{}.options.parameters'.format(self._page.PAGE_KEY, self.UNIT_KEY)),
        )

        self._prx_h_splitter.set_fixed_size_at(1, 400)

    def do_gui_refresh_all(self):
        task_session = self._page._task_session
        if task_session is not None:
            scene_path = task_session.properties['result']
            pre_scene_path = self._scene_qt_info_label._get_info_()
            if scene_path != pre_scene_path:
                self._task_worker = task_session.generate_task_worker()

                self._scene_qt_info_label._set_info_(scene_path)

            # refresh all time
            self._gui_node_opt.do_gui_refresh_all()
