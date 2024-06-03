# coding:utf-8
import functools

import lxbasic.core as bsc_core

import lxbasic.log as bsc_log

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.abstracts as prx_abstracts

import lxgui.proxy.widgets as prx_widgets

import qsm_task.core as qsm_task_core

import qsm_task.process as qsm_tsk_process


class _GuiBaseOpt(object):
    DCC_NAMESPACE = 'task'

    def __init__(self, window, page, session):
        self._window = window
        self._page = page
        self._session = session


class _GuiHistoryOpt(
    _GuiBaseOpt,
):
    CYCLE_MSEC = 5000
    THREAD_STEP = 16

    ITEM_MAXIMUM = 200

    def __init__(self, window, page, session):
        super(_GuiHistoryOpt, self).__init__(window, page, session)

        self._refresh_finish_flag = True

        self._date_tag = bsc_core.SysBaseMtd.get_date_tag()

        self._qt_history_view = qt_widgets.QtViewForHistoryEntity()

        self._page._main_layout.addWidget(self._qt_history_view)
        
        self._entity_pool = qsm_task_core.HistoryPool.generate()

        self._status_name_mapper = bsc_core.BasProcessStatus.to_mapper()

        self._auto_update_timer = gui_qt_core.QtCore.QTimer(self._qt_history_view)
        self._auto_update_timer.timeout.connect(
            self._do_gui_entities_auto_update
        )
        self._refresh_cycle_msec = self.CYCLE_MSEC
        self._refresh_is_finished = True

        self._status_dict = {}

        self._running_threads_stacks = []

        self._startup_flag = True

        self._index_thread_batch = 0

    def restore(self):
        self._qt_history_view._restore_()

    def _delete_entity_fnc(self, widget):
        entity_id = widget._get_key_text_()

        self._entity_pool.send_entity_to_trash(entity_id)

    def gui_add_entity(self, entity):
        time_text = entity.get('time')
        group_name = bsc_core.DateTime.to_period(
            time_text,
            self._window._language
        )
        qt_item = self._qt_history_view._prepend_item_(
            entity.id, group_name, entity.get('name')
        )
        qt_item._set_time_text_(time_text)
        qt_item._set_associated_entity_id_(
            entity.get('task')
        )
        qt_item._set_file_path_(
            entity.get('file')
        )
        qt_item._connect_delete_to_(
            self._delete_entity_fnc
        )

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

        if self._window.SERVER_FLAG is True:
            self._worker_queue = qsm_tsk_process.TaskProcessClient.get_worker_queue()
        else:
            self._worker_queue = dict(
                waiting=[],
                running=[]
            )

        t = gui_qt_core.QtBuildThread(self._qt_history_view)
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
            entity_ids_map = bsc_core.RawListMtd.grid_to(
                entity_ids, self.THREAD_STEP
            )

            ts = gui_qt_core.QtBuildThreadStack(self._window.widget)
            self._running_threads_stacks.append(ts)
            ts.run_finished.connect(post_fnc_)
            for i_entity_ids in entity_ids_map:
                ts.register(
                    functools.partial(
                        self._gui_add_entities_cache_fnc, i_entity_ids, thread_stack_index
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

        entities, thread_stack_index = args[0]
        if thread_stack_index != self._index_thread_batch:
            return

        with self._qt_history_view._gui_bustling_():
            for i_entity in entities:
                self.gui_add_entity(i_entity)
    
    def _do_gui_entities_auto_update(self):
        if self._refresh_finish_flag is True:
            self._refresh_finish_flag = False

            date_tag = bsc_core.SysBaseMtd.get_date_tag()
            if date_tag != self._date_tag:
                bsc_log.Log.trace_result(
                    'date is change, refresh force'
                )
                self.do_gui_refresh_entities_force()
            else:
                self._do_gui_add_entities_new()

            self._refresh_finish_flag = True
    
    def _do_gui_add_entities_new(self):
        def cache_fnc_():
            _entity_ids_new = self._entity_pool.do_update()
            _entities_new = self._entity_pool.find_entities(_entity_ids_new)
            return [
                self._index_thread_batch,
                _entities_new
            ]

        def build_fnc_(*args):
            _index_thread_batch_current, _entities_new = args[0]
            with self._qt_history_view._gui_bustling_():
                for _i_entity in _entities_new:
                    if _index_thread_batch_current != self._index_thread_batch:
                        break
                    self.gui_add_entity(_i_entity)

        def post_fnc_():
            pass

        t = gui_qt_core.QtBuildThread(self._qt_history_view)
        t.set_cache_fnc(cache_fnc_)
        t.cache_value_accepted.connect(build_fnc_)
        t.run_finished.connect(post_fnc_)
        #
        t.start()
        

class PrxPageForNotice(prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = qt_widgets.QtTranslucentWidget

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForNotice, self).__init__(*args, **kwargs)
        self._window = window
        self._session = session

        self._refresh_flag = False

        self.gui_setup_page()

    def gui_setup_page(self):
        self._main_layout = qt_widgets.QtVBoxLayout(self._qt_widget)
        self._main_layout.setContentsMargins(*[0]*4)
        self._main_layout.setSpacing(2)

        self._top_prx_tool_bar = prx_widgets.PrxHToolBar()
        self._main_layout.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_expanded(True)
        self._top_prx_tool_bar.set_align_left()

        self._gui_entity_opt = _GuiHistoryOpt(
            self._window, self, self._session
        )
    
    def do_gui_refresh_all(self, force=False):
        if self._refresh_flag is False:
            self._gui_entity_opt.do_gui_refresh_entities()
            self._refresh_flag = True

        if force is True:
            self._gui_entity_opt.do_gui_refresh_entities_force()
