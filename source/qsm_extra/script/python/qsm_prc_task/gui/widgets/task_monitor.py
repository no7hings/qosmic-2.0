# coding:utf-8
import lxbasic.core as bsc_core

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

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
    def __init__(self, window, session, task_connection, prx_tree_view):
        super(_GuiTaskOpt, self).__init__(window, session)
        self._init_tree_view_opt_(prx_tree_view, self.DCC_NAMESPACE)

        self._prx_tree_view.create_header_view(
            [('name', 6), ('progress', 2), ('status', 2), ('sumit time', 2), ('start time', 2), ('finish time', 2)],
            960
        )

        self._task_connection = task_connection
        self._prx_tree_view = prx_tree_view

        self._status_mapper = bsc_core.BscStatus.to_mapper()

    def gui_add_root(self):
        path = '/'
        if self.gui_is_exists(path) is True:
            return False, self.gui_get(path)

        prx_item = self._prx_tree_view.create_item(
            self.ROOT_NAME,
            icon=gui_core.GuiIcon.get('database/all'),
        )

        self.gui_register(path, prx_item)

        prx_item.set_expanded(True)
        prx_item.set_emit_send_enable(True)
        return True, prx_item

    def gui_add_prc_batch(self, prc_task):
        batch_name = prc_task.batch_name
        path = '/{}'.format(batch_name)
        if self.gui_is_exists(path):
            return False, self.gui_get(path)

        path_opt = bsc_core.PthNodeOpt(path)
        parent_gui = self.gui_get(path_opt.get_parent_path())

        prx_item = parent_gui.add_child(
            name=batch_name,
            icon=gui_core.GuiIcon.get('database/group'),
        )
        self.gui_register(path, prx_item)
        return True, prx_item

    def gui_add_prc_task(self, prc_task):
        batch_name = prc_task.batch_name
        print batch_name
        path = '/{}/{}'.format(batch_name, prc_task.task_id)
        if self.gui_is_exists(path) is True:
            return False, self.gui_get(path)

        content = prc_task.content

        path_opt = bsc_core.PthNodeOpt(path)

        _, parent_gui = self.gui_add_prc_batch(prc_task)

        status = content.get('process.status')

        prx_item = parent_gui.add_child(
            name='...',
            icon=gui_core.GuiIcon.get('file/python'),
        )
        prx_item.set_names(
            [
                content.get('properties.name'),
                '0%',
                self._status_mapper[content.get('process.status')],
                content.get('process.submit_time') or 'N/a',
                content.get('process.start_time') or 'N/a',
                content.get('process.finish_time') or 'N/a',
            ]
        )
        prx_item.set_process_status(status)
        self.gui_register(path, prx_item)

        return True, prx_item

    def gui_add_all_prc_tasks(self):
        def cache_fnc_():
            _prc_tasks = self._task_connection.get_tasks()
            return [
                self._index_thread_batch,
                _prc_tasks
            ]

        def build_fnc_(*args):
            _index_thread_batch_current, _prc_tasks = args[0]
            with self._prx_tree_view.gui_bustling():
                for _i_prc_task in _prc_tasks:
                    if _index_thread_batch_current != self._index_thread_batch:
                        break
                    self.gui_add_prc_task(_i_prc_task)

        def post_fnc_():
            pass

        self._index_thread_batch += 1

        self.gui_add_root()

        t = gui_qt_core.QtBuildThread(self._prx_tree_view.get_widget())
        t.set_cache_fnc(cache_fnc_)
        t.cache_value_accepted.connect(build_fnc_)
        t.run_finished.connect(post_fnc_)
        #
        t.start()


class PnlTaskMonitor(prx_widgets.PrxSessionWindow):
    def __init__(self, session, *args, **kwargs):
        super(PnlTaskMonitor, self).__init__(session, *args, **kwargs)

    def gui_add_main_tools(self):
        for i in [
            'filter', 'tool/filter'
        ]:
            pass

    def set_all_setup(self):
        self._task_connection = _task_core.Connection.generate()

        sca = prx_widgets.PrxVScrollArea()
        self.add_widget(sca)

        self._top_prx_tool_bar = prx_widgets.PrxHToolBar()
        sca.add_widget(self._top_prx_tool_bar)
        self._top_prx_tool_bar.set_expanded(True)

        self._main_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'main'
        )

        slt_h = prx_widgets.PrxHSplitter()
        sca.add_widget(slt_h)

        self._task_filter_prx_tree_view = prx_widgets.PrxTreeView()
        slt_h.add_widget(self._task_filter_prx_tree_view)

        self._task_prx_tree_view = prx_widgets.PrxTreeView()
        slt_h.add_widget(self._task_prx_tree_view)
        self._gui_task_opt = _GuiTaskOpt(
            self, self._session, self._task_connection,
            self._task_prx_tree_view
        )

        slt_h.set_fixed_size_at(0, 240)
        slt_h.set_visible_at(0, False)

        self.gui_refresh_all()

    def gui_refresh_all(self):
        self._gui_task_opt.restore()

        self._gui_task_opt.gui_add_all_prc_tasks()
