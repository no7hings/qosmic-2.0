# coding:utf-8
import functools

import lxbasic.core as bsc_core

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.abstracts as prx_abstracts

import lxgui.proxy.widgets as prx_widgets

from ... import core as _task_core


class _GuiBaseOpt(object):
    DCC_NAMESPACE = 'task'

    def __init__(self, window, session):
        self._window = window
        self._session = session


class _GuiTaskOpt(
    _GuiBaseOpt,
    prx_abstracts.AbsGuiPrxTreeViewOpt
):
    CYCLE_MSEC = 5000
    
    BATCH_NAMESPACE = 'batch'
    TASK_NAMESPACE = 'task'

    THREAD_STEP = 16

    def __init__(self, window, session, task_pool, prx_tree_view):
        super(_GuiTaskOpt, self).__init__(window, session)
        self._init_tree_view_opt_(prx_tree_view, self.DCC_NAMESPACE)

        self._prx_tree_view.create_header_view(
            [('name', 6), ('progress', 2), ('status', 2), ('sumit time', 2), ('start time', 2), ('finish time', 2)],
            1280-32
        )
        self._prx_tree_view.set_selection_use_extend()
        self._prx_tree_view._qt_view.header().setSortIndicatorShown(True)

        self._task_pool = task_pool
        self._prx_tree_view = prx_tree_view

        self._status_name_mapper = bsc_core.BscStatus.to_mapper()

        self._refresh_timer = gui_qt_core.QtCore.QTimer(self._prx_tree_view.widget)
        self._refresh_timer.timeout.connect(
            self.gui_refresh_tasks_all
        )
        self._refresh_cycle_msec = self.CYCLE_MSEC
        self._refresh_is_finished = True

        self._status_dict = {}

        self._running_threads_stacks = []

    def gui_add_root(self):
        path = '/'
        if self.gui_is_exists(path) is True:
            return False, self.gui_get(path)

        prx_item = self._prx_tree_view.prepend_item(
            self.ROOT_NAME,
            icon=gui_core.GuiIcon.get('database/all'),
        )

        self.gui_register(path, prx_item)

        prx_item.set_expanded(True)
        prx_item.set_emit_send_enable(True)
        return True, prx_item

    def gui_add_prc_batch(self, prc_task):
        group = prc_task.group
        path = '/{}'.format(group)
        if self.gui_is_exists(path):
            return False, self.gui_get(path)

        path_opt = bsc_core.PthNodeOpt(path)
        parent_gui = self.gui_get(path_opt.get_parent_path())

        prx_item = parent_gui.prepend_child(
            name=group,
            icon=gui_core.GuiIcon.get('database/group'),
        )
        # prx_item.set_expanded(True)
        prx_item.set_gui_dcc_obj(path_opt, self.BATCH_NAMESPACE)
        self.gui_register(path, prx_item)
        return True, prx_item

    def gui_add_prc_task(self, prc_task):
        group = prc_task.group
        path = '/{}/{}'.format(group, prc_task.task_id)
        if self.gui_is_exists(path) is True:
            return False, self.gui_get(path)

        content = prc_task.content

        path_opt = bsc_core.PthNodeOpt(path)

        _, parent_gui = self.gui_add_prc_batch(prc_task)

        status = content.get('process.status')

        prx_item = parent_gui.prepend_child(
            name='...',
            icon=gui_core.GuiIcon.get('file/python'),
        )
        prx_item.set_names(
            [
                content.get('properties.name'),
                '0%',
                self._status_name_mapper[content.get('process.status')],
                content.get('process.submit_time') or 'N/a',
                content.get('process.start_time') or 'N/a',
                content.get('process.finish_time') or 'N/a',
            ]
        )
        prx_item.set_gui_menu_raw(
            [
                ('custom',),
                ('show task log', 'log', lambda: self._window.gui_show_task_log(prc_task))
            ]
        )
        prx_item.set_process_status(status)
        prx_item.set_gui_dcc_obj(prc_task, self.TASK_NAMESPACE)
        self.gui_register(path, prx_item)

        return True, prx_item

    def gui_add_prc_tasks_batch(self):
        self._index_thread_batch += 1

        self.gui_add_root()

        self._refresh_timer.start(self._refresh_cycle_msec)

        t = gui_qt_core.QtBuildThread(self._prx_tree_view.get_widget())
        t.set_cache_fnc(
            functools.partial(
                self._gui_add_prc_tasks_batch_cache_fnc, self._index_thread_batch
            )
        )
        t.cache_value_accepted.connect(self._gui_add_prc_tasks_batch_build_fnc)
        #
        t.start()

    def _gui_add_prc_tasks_batch_cache_fnc(self, thread_stack_index):
        if thread_stack_index != self._index_thread_batch:
            return []

        self._task_pool.do_update()
        task_ids = self._task_pool.get_task_ids()
        return [
            task_ids,
            thread_stack_index
        ]

    def _gui_add_prc_tasks_batch_build_fnc(self, *args):
        def post_fnc_():
            self.gui_refresh_tasks_all()

        def quit_fnc_():
            ts.do_quit()

        if not args[0]:
            return

        task_ids, thread_stack_index = args[0]
        if thread_stack_index != self._index_thread_batch:
            return

        if task_ids:
            task_ids_map = bsc_core.RawListMtd.grid_to(
                task_ids, self.THREAD_STEP
            )

            ts = gui_qt_core.QtBuildThreadStack(self._window.widget)
            self._running_threads_stacks.append(ts)
            ts.run_finished.connect(post_fnc_)
            for i_task_ids in task_ids_map:
                ts.register(
                    functools.partial(
                        self._gui_add_prc_task_cache_fnc, i_task_ids, thread_stack_index
                    ),
                    self._gui_add_prc_tasks_build_fnc
                )
            #
            ts.do_start()
            #
            self._window.connect_window_close_to(quit_fnc_)

    def _gui_add_prc_task_cache_fnc(self, task_ids, thread_stack_index):
        if thread_stack_index != self._index_thread_batch:
            return []
        return [
            self._task_pool.find_tasks(task_ids),
            thread_stack_index
        ]

    def _gui_add_prc_tasks_build_fnc(self, *args):
        if not args[0]:
            return

        prc_tasks, thread_stack_index = args[0]
        if thread_stack_index != self._index_thread_batch:
            return

        with self._prx_tree_view.gui_bustling():
            for i_prc_task in prc_tasks:
                self.gui_add_prc_task(i_prc_task)

    def gui_refresh_tasks_all(self):
        if self._refresh_is_finished is True:
            self._refresh_is_finished = False

            self.gui_refresh_tasks_new()

            self._status_dict = {}
            for k, i_prx_item in self._item_dict.items():
                i_prc_task = i_prx_item.get_gui_dcc_obj(self.TASK_NAMESPACE)
                if i_prc_task is not None:
                    i_prc_task.do_update()
                    i_task_id = i_prc_task.task_id
                    i_status = i_prc_task.get_status()
                    i_status_name = self._status_name_mapper[i_status]
                    i_start_time = i_prc_task.get_start_time() or 'N/a'
                    i_finish_time = i_prc_task.get_finish_time() or 'N/a'
                    i_prx_item.set_process_status(i_status)
                    i_prx_item.set_name(i_status_name, 2)
                    i_prx_item.set_name(i_start_time, 4)
                    i_prx_item.set_name(i_finish_time, 5)
                    self._status_dict.setdefault(
                        i_status_name, []
                    ).append(i_task_id)
                    self._status_dict.setdefault(
                        'total', []
                    ).append(i_task_id)

                i_batch_name = i_prx_item.get_gui_dcc_obj(self.BATCH_NAMESPACE)
                if i_batch_name is not None:
                    i_status = i_prx_item.get_process_status_args_from_children()
                    i_status_name = self._status_name_mapper[i_status]
                    i_prx_item.set_process_status(i_status)
                    # i_prx_item.set_name(i_status_name, 2)

            self._window.gui_refresh_task_info(self._status_dict)

            self._refresh_is_finished = True

    def gui_refresh_tasks_new(self):
        def cache_fnc_():
            _task_ids_new = self._task_pool.do_update()
            _prc_tasks_new = self._task_pool.find_tasks(_task_ids_new)
            return [
                self._index_thread_batch,
                _prc_tasks_new
            ]

        def build_fnc_(*args):
            _index_thread_batch_current, _prc_tasks_new = args[0]
            with self._prx_tree_view.gui_bustling():
                for _i_prc_task in _prc_tasks_new:
                    if _index_thread_batch_current != self._index_thread_batch:
                        break
                    self.gui_add_prc_task(_i_prc_task)

        def post_fnc_():
            pass

        t = gui_qt_core.QtBuildThread(self._prx_tree_view.get_widget())
        t.set_cache_fnc(cache_fnc_)
        t.cache_value_accepted.connect(build_fnc_)
        t.run_finished.connect(post_fnc_)
        #
        t.start()


class PnlTaskMonitor(prx_widgets.PrxSessionWindow):
    def __init__(self, session, *args, **kwargs):
        super(PnlTaskMonitor, self).__init__(session, *args, **kwargs)

    def _gui_add_main_tools(self):
        for i in [
            ('filter', 'tool/filter', '', self.gui_filter_update_visible)
        ]:
            i_key, i_icon_name, i_tool_tip, i_fnc = i
            i_tool = prx_widgets.PrxToggleButton()
            self._main_prx_tool_box.add_widget(i_tool)
            i_tool.set_name(i_key)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip(i_tool_tip)
            i_tool.connect_check_toggled_to(i_fnc)

    def _gui_add_task_log_layer(self):
        layer_widget = self.create_layer_widget('task_log', 'Task Log')
        prx_sca = prx_widgets.PrxVScrollArea()
        layer_widget.add_widget(prx_sca)

        self._task_log_prx_text_browser = prx_widgets.PrxTextBrowser()
        prx_sca.add_widget(self._task_log_prx_text_browser)

    def gui_show_task_log(self, prc_task):
        self.switch_current_layer_to('task_log')
        log = prc_task.read_log()
        if log:
            self._task_log_prx_text_browser.set_content(
                log
            )
        else:
            self._task_log_prx_text_browser.set_content('')

    def gui_refresh_task_info(self, status_dict):
        texts = []
        keys = [
            'total', 'running', 'suspended', 'completed', 'failed'
        ]
        for i_key in keys:
            if i_key in status_dict:
                i_count = len(status_dict[i_key])
            else:
                i_count = 0
            texts.append('{} {}'.format(i_count, i_key))

        self._task_info_label._set_info_(
            ', '.join(texts)
        )

    def gui_filter_update_visible(self, boolean):
        self._prx_h_splitter.swap_contract_left_or_top_at(0)

    def gui_setup_window(self):
        self._gui_add_task_log_layer()

        self._task_pool = _task_core.Pool.generate()

        sca = prx_widgets.PrxVScrollArea()
        self.add_widget(sca)

        self._top_prx_tool_bar = prx_widgets.PrxHToolBar()
        sca.add_widget(self._top_prx_tool_bar)
        self._top_prx_tool_bar.set_expanded(True)
        self._top_prx_tool_bar.set_align_left()

        self._main_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'main'
        )
        self._gui_add_main_tools()

        self._info_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'info', size_mode=1
        )
        self._task_info_label = qt_widgets.QtInfoLabel()
        self._info_prx_tool_box.add_widget(self._task_info_label)
        self._task_info_label._set_info_(
            '0 total'
        )

        self._prx_h_splitter = prx_widgets.PrxHSplitter()
        sca.add_widget(self._prx_h_splitter)

        self._task_filter_prx_tree_view = prx_widgets.PrxTreeView()
        self._prx_h_splitter.add_widget(self._task_filter_prx_tree_view)

        self._task_prx_tree_view = prx_widgets.PrxTreeView()
        self._prx_h_splitter.add_widget(self._task_prx_tree_view)
        self._gui_task_opt = _GuiTaskOpt(
            self, self._session, self._task_pool,
            self._task_prx_tree_view
        )

        self._prx_h_splitter.set_fixed_size_at(0, 240)
        self._prx_h_splitter.swap_contract_left_or_top_at(0)
        self._prx_h_splitter.set_contract_enable(False)

        self.gui_refresh_all()

        self.connect_refresh_action_for(self._gui_task_opt.gui_refresh_tasks_all)

    def gui_refresh_all(self):
        self._gui_task_opt.restore()

        self._gui_task_opt.gui_add_prc_tasks_batch()
