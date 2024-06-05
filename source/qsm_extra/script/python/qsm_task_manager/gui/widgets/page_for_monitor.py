# coding:utf-8
import functools

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.abstracts as prx_abstracts

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_task.core as qsm_task_core

import qsm_task.process as qsm_tsk_process

import qsm_task.process.server as qsm_tsk_prc_server


class _GuiBaseOpt(object):
    GUI_NAMESPACE = 'task'

    def __init__(self, window, page, session):
        self._window = window
        self._page = page
        self._session = session


class _GuiTaskOpt(
    _GuiBaseOpt,
    prx_abstracts.AbsGuiPrxTreeViewOpt
):
    CYCLE_MSEC = 5000
    THREAD_STEP = 16

    ITEM_MAXIMUM = 200

    GROUP_NAMESPACE = 'batch'
    TASK_NAMESPACE = 'task'

    def do_gui_show_task_log(self, entity):
        self._window.switch_current_layer_to('task_log')
        log = entity.read_log()
        if log:
            self._page._task_log_prx_text_browser.set_content(
                log
            )
        else:
            self._page._task_log_prx_text_browser.set_content('')

    def do_open_output_directory(self, entity):
        file_path = entity.get('output_file')
        if file_path is not None:
            bsc_storage.StgFileOpt(file_path).open_in_system()
    
    def do_gui_show_task_properties(self, entity):
        self._window.switch_current_layer_to('task_properties')
        properties = entity.get_properties()
        self._page._task_properties_prx_options_node.set_dict(properties)

    def do_requeue_tasks(self):
        prc_tasks = self.gui_get_selected_prc_tasks()
        if prc_tasks:
            qsm_tsk_process.TaskProcessClient.requeue_tasks(
                [x.id for x in prc_tasks]
            )
            # [qsm_tsk_process.TaskProcessClient.requeue_task(x.id) for x in prc_tasks]

    def do_stop_tasks(self):
        prc_tasks = self.gui_get_selected_prc_tasks()
        if prc_tasks:
            qsm_tsk_process.TaskProcessClient.stop_tasks(
                [x.id for x in prc_tasks]
            )

    def do_delete_tasks(self):
        prc_task_args = self.gui_get_selected_prc_task_args()
        if prc_task_args:
            for i_prx_item, i_prc_task in prc_task_args:
                key = i_prx_item.get_key()
                self._item_dict.pop(key)
                i_prx_item.do_delete()
                self._entity_pool.send_entity_to_trash(
                    i_prc_task.id
                )

    def gui_get_selected_prc_task_args(self):
        list_ = []
        _ = self._prx_tree_view.get_selected_items()
        for i in _:
            i_task = i.get_gui_dcc_obj(self.TASK_NAMESPACE)
            if i_task is not None:
                list_.append((i, i_task))
        return list_
    
    def gui_get_selected_prc_tasks(self):
        list_ = []
        _ = self._prx_tree_view.get_selected_items()
        for i in _:
            i_task = i.get_gui_dcc_obj(self.TASK_NAMESPACE)
            if i_task is not None:
                list_.append(i_task)
        return list_ 
    
    def __init__(self, window, page, session, task_pool, prx_tree_view):
        super(_GuiTaskOpt, self).__init__(window, page, session)
        self._init_tree_view_opt_(prx_tree_view, self.GUI_NAMESPACE)

        if self._window._language == 'chs':
            header_data = [
                ('名字', 4),
                ('状态', 2),
                ('进度', 2),
                ('发布时间', 2),
                ('开始时间', 2),
                ('结束时间', 2),
                ('索引', 2),
            ]
        else:
            header_data = [
                ('name', 4),
                ('status', 2),
                ('progress', 2),
                ('sumit time', 2),
                ('start time', 2),
                ('finish time', 2),
                ('index', 2),
            ]

        self._prx_tree_view.create_header_view(header_data, 1280-32)
        self._prx_tree_view.set_selection_use_extend()
        self._prx_tree_view._qt_view.header().setSortIndicatorShown(True)

        self._entity_pool = task_pool
        self._prx_tree_view = prx_tree_view

        self._status_name_mapper = bsc_core.BasProcessStatus.to_mapper()

        self._auto_update_timer = gui_qt_core.QtCore.QTimer(self._prx_tree_view.widget)
        self._auto_update_timer.timeout.connect(
            self._do_gui_entities_auto_update
        )
        self._refresh_cycle_msec = self.CYCLE_MSEC
        self._refresh_finish_flag = True

        self._status_dict = {}

        self._running_threads_stacks = []

        self._startup_flag = True

        self._worker_queue = dict(
            waiting=[],
            running=[]
        )

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

    def gui_add_prc_group(self, entity):
        group = entity.get('group')
        if group is None:
            return False, self.gui_get('/')

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
        prx_item.set_gui_dcc_obj(path_opt, self.GROUP_NAMESPACE)
        self.gui_register(path, prx_item)
        return True, prx_item

    def gui_add_entity(self, entity):
        group = entity.get('group')
        task_id = entity.id
        if group is None:
            path = '/{}'.format(task_id)
        else:
            path = '/{}/{}'.format(group, task_id)

        if self.gui_is_exists(path) is True:
            return False, self.gui_get(path)

        content = entity.content

        _, parent_gui = self.gui_add_prc_group(entity)

        status = content.get('process.status')

        icon_name = entity.get('icon_name')

        if icon_name is not None:
            icon = gui_core.GuiIcon.get(icon_name)
        else:
            icon = gui_core.GuiIcon.get('file/python')

        prx_item = parent_gui.prepend_child(
            name='...',
            icon=icon,
        )
        prx_item.set_names(
            [
                content.get('properties.name'),
                self._status_name_mapper[content.get('process.status')],
                str(content.get('process.progress') or 0),
                content.get('process.submit_time') or 'N/a',
                content.get('process.start_time') or 'N/a',
                content.get('process.finish_time') or 'N/a',
                str(entity.get('index'))
            ]
        )
        if self._window._language == 'chs':
            menu_data = [
                ('custom',),
                ('显示任务日志', 'log', lambda: self.do_gui_show_task_log(entity)),
                ('打开输出文件夹', 'file/folder', lambda: self.do_open_output_directory(entity)),
                ('extra',),
                ('重新提交任务', 'tool/maya/requeue-task', self.do_requeue_tasks),
                ('停止任务', 'tool/maya/stop-task', self.do_stop_tasks),
                ('移动任务到回收站', 'trash', self.do_delete_tasks),
            ]
        else:
            menu_data = [
                ('custom',),
                ('show task log', 'log', lambda: self.do_gui_show_task_log(entity)),
                ('open output directory', 'file/folder', lambda: self.do_open_output_directory(entity)),
                ('extra',),
                ('requeue tasks', 'tool/maya/requeue-task', self.do_requeue_tasks),
                ('stop tasks', 'tool/maya/stop-task', self.do_stop_tasks),
                ('send tasks to trash', 'trash', self.do_delete_tasks),
            ]

        prx_item.set_gui_menu_data(
            menu_data
        )
        if self._startup_flag is True:
            if status == entity.Status.Waiting:
                if task_id not in self._worker_queue['waiting']:
                    status = entity.Status.Stopped
                    entity.set_status(status)
                    prx_item.set_process_status(status)
                    status_name = self._status_name_mapper[status]
                    prx_item.set_name(status_name, 1)
            elif status == entity.Status.Running:
                if task_id not in self._worker_queue['running']:
                    status = entity.Status.Killed
                    entity.set_status(status)
                    prx_item.set_process_status(status)
                    status_name = self._status_name_mapper[status]
                    prx_item.set_name(status_name, 1)
            else:
                prx_item.set_process_status(status)
        else:
            prx_item.set_process_status(status)

        prx_item.set_gui_dcc_obj(entity, self.TASK_NAMESPACE)
        prx_item.set_key(path)
        prx_item.set_keyword_filter_keys_tgt(entity.get_properties().values())
        prx_item.connect_press_dbl_clicked_to(
            lambda: self.do_gui_show_task_properties(entity)
        )
        self.gui_register(path, prx_item)

        return True, prx_item

    def do_gui_refresh_entities_force(self):
        self._index_thread_batch += 1
        self._auto_update_timer.stop()
        # noinspection PyBroadException
        try:
            self.restore()
            self.do_gui_add_entities_batch()
        except Exception:
            pass

    def do_gui_refresh_entities(self):
        self.do_gui_add_entities_batch()

    def do_gui_add_entities_batch(self):
        self._index_thread_batch += 1

        self.gui_add_root()

        if self._window.SERVER_FLAG is True:
            self._worker_queue = qsm_tsk_process.TaskProcessClient.get_worker_queue()
        else:
            self._worker_queue = dict(
                waiting=[],
                running=[]
            )

        t = gui_qt_core.QtBuildThread(self._prx_tree_view.get_widget())
        t.set_cache_fnc(
            functools.partial(
                self._gui_add_entities_batch_cache_fnc, self._index_thread_batch
            )
        )
        t.cache_value_accepted.connect(self._gui_add_entities_batch_build_fnc)
        #
        t.start()

    def _gui_add_entities_batch_cache_fnc(self, thread_stack_index):
        if thread_stack_index != self._index_thread_batch:
            return []

        self._entity_pool.do_update()
        entity_ids = self._entity_pool.find_entity_ids(ignore_delete=True)[:self.ITEM_MAXIMUM]
        return [
            entity_ids,
            thread_stack_index
        ]

    def _gui_add_entities_batch_build_fnc(self, *args):
        def post_fnc_():
            self._startup_flag = False

            self._do_gui_entities_auto_update()
            self._auto_update_timer.start(self._refresh_cycle_msec)

        def quit_fnc_():
            ts.do_quit()

        if not args[0]:
            return

        entity_ids, thread_stack_index = args[0]
        if thread_stack_index != self._index_thread_batch:
            return

        if entity_ids:
            task_ids_map = bsc_core.RawListMtd.grid_to(
                entity_ids, self.THREAD_STEP
            )

            ts = gui_qt_core.QtBuildThreadStack(self._window.widget)
            self._running_threads_stacks.append(ts)
            ts.run_finished.connect(post_fnc_)
            for i_task_ids in task_ids_map:
                ts.register(
                    functools.partial(
                        self._gui_add_entities_cache_fnc, i_task_ids, thread_stack_index
                    ),
                    self._gui_add_entities_build_fnc
                )
            #
            ts.do_start()
            #
            self._window.connect_window_close_to(quit_fnc_)
        else:
            post_fnc_()

    def _gui_add_entities_cache_fnc(self, entity_ids, thread_stack_index):
        if thread_stack_index != self._index_thread_batch:
            return []
        return [
            self._entity_pool.find_entities(entity_ids),
            thread_stack_index
        ]

    def _gui_add_entities_build_fnc(self, *args):
        if not args[0]:
            return

        prc_tasks, thread_stack_index = args[0]
        if thread_stack_index != self._index_thread_batch:
            return

        with self._prx_tree_view.gui_bustling():
            for i_prc_task in prc_tasks:
                self.gui_add_entity(i_prc_task)

    def _do_gui_entities_auto_update(self):
        if self._refresh_finish_flag is True:

            self._refresh_finish_flag = False

            self._do_gui_refresh_server_status()

            self._do_gui_add_entities_new()

            self._status_dict = {}
            for k, i_prx_item in self._item_dict.items():
                i_data = self._do_gui_refresh_task(i_prx_item)
                if i_data is not None:
                    i_task_id, i_status_name = i_data
                    self._status_dict.setdefault(
                        i_status_name, []
                    ).append(i_task_id)
                    self._status_dict.setdefault(
                        'total', []
                    ).append(i_task_id)

                i_batch_name = i_prx_item.get_gui_dcc_obj(self.GROUP_NAMESPACE)
                if i_batch_name is not None:
                    i_status = i_prx_item.get_process_status_args_from_children()
                    i_status_name = self._status_name_mapper[i_status]
                    i_prx_item.set_process_status(i_status)
                    # i_prx_item.set_name(i_status_name, 2)

            self._page.gui_refresh_task_info(self._status_dict)

            self._refresh_finish_flag = True

    def _do_gui_refresh_task(self, prx_item):
        entity = prx_item.get_gui_dcc_obj(self.TASK_NAMESPACE)
        if entity is not None:
            # update first
            task_id = entity.id
            if entity.do_update() is True:
                status = entity.get_status()
                status_name = self._status_name_mapper[status]
                progress = entity.get_progress() or 0
                start_time = entity.get_start_time() or 'N/a'
                finish_time = entity.get_finish_time() or 'N/a'
                prx_item.set_process_status(status)
                prx_item.set_name(status_name, 1)
                prx_item.set_name(str(progress), 2)
                prx_item.set_name(start_time, 4)
                prx_item.set_name(finish_time, 5)
            else:
                status_name = prx_item.get_name(1)
            return task_id, status_name

    def _do_gui_refresh_server_status(self):
        def cache_fnc_():
            pool_status = qsm_tsk_process.TaskProcessClient.get_worker_status()
            return [pool_status]

        def build_fnc_(data):
            self._page._task_pool_status_chart._set_value_(int(data[0]['value']))

        t = gui_qt_core.QtBuildThread(self._prx_tree_view.get_widget())
        t.set_cache_fnc(cache_fnc_)
        t.cache_value_accepted.connect(build_fnc_)
        #
        t.start()

    def _do_gui_add_entities_new(self):
        def cache_fnc_():
            _entity_ids_new = self._entity_pool.do_update()
            _prc_tasks_new = self._entity_pool.find_entities(_entity_ids_new)
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
                    self.gui_add_entity(_i_prc_task)

        def post_fnc_():
            pass

        t = gui_qt_core.QtBuildThread(self._prx_tree_view.get_widget())
        t.set_cache_fnc(cache_fnc_)
        t.cache_value_accepted.connect(build_fnc_)
        t.run_finished.connect(post_fnc_)
        #
        t.start()


class PrxPageForMonitor(prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = qt_widgets.QtTranslucentWidget

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForMonitor, self).__init__(*args, **kwargs)
        self._window = window
        self._session = session
        
        self._refresh_flag = False

        self.gui_setup_page()

    def _message_process_(self, text):
        print text, 'abc'

    def _gui_add_main_tools(self):
        for i in [
            ('filter', 'tool/filter', '', self.gui_filter_update_visible)
        ]:
            i_key, i_icon_name, i_tool_tip, i_fnc = i
            i_tool = gui_prx_widgets.PrxToggleButton()
            self._main_prx_tool_box.add_widget(i_tool)
            i_tool.set_name(i_key)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip(i_tool_tip)
            i_tool.connect_check_toggled_to(i_fnc)

    def _gui_add_task_log_layer(self):
        layer_widget = self._window.create_layer_widget('task_log', 'Task Log')
        prx_sca = gui_prx_widgets.PrxVScrollArea()
        layer_widget.add_widget(prx_sca)

        self._task_log_prx_text_browser = gui_prx_widgets.PrxTextBrowser()
        prx_sca.add_widget(self._task_log_prx_text_browser)

    def _gui_add_task_properties_layer(self):
        layer_widget = self._window.create_layer_widget('task_properties', 'Task Properties')
        prx_sca = gui_prx_widgets.PrxVScrollArea()
        layer_widget.add_widget(prx_sca)

        self._task_properties_prx_options_node = gui_prx_widgets.PrxOptionsNode('Options')
        prx_sca.add_widget(self._task_properties_prx_options_node)
        self._task_properties_prx_options_node.create_ports_by_data(
            self._session.configure.get('build.task_properties.parameters'),
        )
        #
        tool_bar = gui_prx_widgets.PrxHToolBar()
        layer_widget.add_widget(tool_bar.widget)
        tool_bar.set_expanded(True)
        button = gui_prx_widgets.PrxPressButton()
        tool_bar.add_widget(button)
        button.set_name('Save')
        button.set_enable(False)
        # button.connect_press_clicked_to(
        #     self.__create_layer_apply_fnc
        # )

    def gui_refresh_task_info(self, status_dict):
        texts = []
        keys = [
            'total',
            'running',
            # 'suspended',
            'completed', 
            'failed'
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

    def gui_setup_page(self):
        self._entity_pool = qsm_task_core.TaskPool.generate()

        self._gui_add_task_log_layer()
        self._gui_add_task_properties_layer()

        self._qt_widget.setSizePolicy(
            gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )
        qt_lot = qt_widgets.QtVBoxLayout(self._qt_widget)
        qt_lot.setContentsMargins(*[0]*4)
        qt_lot.setSpacing(2)

        self._top_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        qt_lot.addWidget(self._top_prx_tool_bar.widget)
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
        
        self._task_pool_status_chart = qt_widgets.QtChartAsPoolStatus()
        self._info_prx_tool_box.add_widget(self._task_pool_status_chart)
        self._task_pool_status_chart._set_maximum_(
            qsm_tsk_prc_server.TaskProcessWorker.MAXIMUM_INITIAL
        )

        self._prx_h_splitter = gui_prx_widgets.PrxHSplitter()
        qt_lot.addWidget(self._prx_h_splitter.widget)

        self._task_filter_prx_tree_view = gui_prx_widgets.PrxTreeView()
        self._prx_h_splitter.add_widget(self._task_filter_prx_tree_view)

        self._task_prx_tree_view = gui_prx_widgets.PrxTreeView()
        self._prx_h_splitter.add_widget(self._task_prx_tree_view)
        self._gui_entity_opt = _GuiTaskOpt(
            self._window, self, self._session, self._entity_pool,
            self._task_prx_tree_view
        )

        self._prx_h_splitter.set_fixed_size_at(0, 240)
        self._prx_h_splitter.swap_contract_left_or_top_at(0)
        self._prx_h_splitter.set_contract_enable(False)

    def do_gui_refresh_all(self, force=False):
        if self._refresh_flag is False:
            self._gui_entity_opt.do_gui_refresh_entities()
            self._refresh_flag = True

        if force is True:
            self._gui_entity_opt.do_gui_refresh_entities_force()
