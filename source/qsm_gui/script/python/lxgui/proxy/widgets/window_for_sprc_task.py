# coding:utf-8
from ... import core as _gui_core
# qt
from ...qt import core as _qt_core
# qt widgets
from ...qt.widgets import base as _qt_wgt_base

from ...qt.widgets import utility as _qt_wgt_utility

from ... qt.widgets import window_base as _qt_window_base

from ...qt.widgets import chart as _qt_wgt_chart

from ...qt.widgets import chart_for_sprc_task as _qt_chart_for_sprc_task

from ...qt.widgets import spc_task as _qt_wgt_for_sprc_task
# proxy abstracts
from .. import abstracts as gui_prx_abstracts
# proxy widgets
from . import utility as gui_prx_wdt_utility

from . import container as _container


class PrxSprcTaskWindow(
    gui_prx_abstracts.AbsPrxWindow,
    gui_prx_abstracts.AbsPrxProgressingDef,
):
    QT_WIDGET_CLS = _qt_window_base.QtMainWindow

    QT_PROGRESSING_CHART_CLS = _qt_wgt_chart.QtChartAsProgressing

    def __init__(self, *args, **kwargs):
        super(PrxSprcTaskWindow, self).__init__(*args, **kwargs)
        self.widget.setWindowFlags(
            _qt_core.QtCore.Qt.Window
            |_qt_core.QtCore.Qt.WindowStaysOnTopHint
            |_qt_core.QtCore.Qt.CustomizeWindowHint
            |_qt_core.QtCore.Qt.WindowMinimizeButtonHint
        )
        
        self._init_progressing_def_()
        
        self._qt_widget._thread_worker_maximum = 2

        self.set_definition_window_size((480, 320))

    def set_thread_maximum(self, value):
        self._qt_widget._thread_worker_maximum = value

    def _gui_build_(self):
        self._language = _gui_core.GuiUtil.get_language()
        self._central_qt_widget = _qt_wgt_utility.QtWidget()
        self._qt_widget.setCentralWidget(self._central_qt_widget)
        self._central_qt_layout = _qt_wgt_base.QtVBoxLayout(self._central_qt_widget)

        self._task_prx_tool_group = _container.PrxHToolGroupNew()
        self._central_qt_layout.addWidget(self._task_prx_tool_group.widget)
        self._task_prx_tool_group.set_expanded(True)

        self._prx_scroll_area = gui_prx_wdt_utility.PrxVScrollArea()
        self._task_prx_tool_group.add_widget(self._prx_scroll_area)

        self._tip_prx_tool_group = _container.PrxHToolGroupNew()
        self._central_qt_layout.addWidget(self._tip_prx_tool_group.widget)
        self._tip_prx_tool_group.set_expanded(True)
        self._tip_prx_tool_group.set_height_match_to_maximum()

        self._tip_prx_text_browser = gui_prx_wdt_utility.PrxTextBrowser()
        self._tip_prx_tool_group.add_widget(self._tip_prx_text_browser.widget)
        self._tip_prx_text_browser._qt_widget.setMaximumHeight(80)

        self._bottom_prx_tool_bar = _container.PrxHToolBar()
        self._central_qt_layout.addWidget(self._bottom_prx_tool_bar.widget)
        self._bottom_prx_tool_bar.set_expanded(True)

        self._stop_and_close_prx_button = gui_prx_wdt_utility.PrxPressButton()
        self._bottom_prx_tool_bar.add_widget(self._stop_and_close_prx_button)
        self._stop_and_close_prx_button.connect_press_clicked_to(self._do_stop_and_close)

        self._subprocess_widgets = []

        if self._language == 'chs':
            self._task_prx_tool_group.set_name('进度')
            self._tip_prx_tool_group.set_name('提示')
            self._stop_and_close_prx_button.set_name('关闭')
        else:
            self._task_prx_tool_group.set_name('Progress')
            self._tip_prx_tool_group.set_name('Tip')
            self._stop_and_close_prx_button.set_name('Close')

    def _do_gui_stop(self):
        # kill first
        [x._do_kill_() for x in self._subprocess_widgets]
        [x._do_quit_() for x in self._subprocess_widgets]

    def _do_stop_and_close(self):
        self._do_gui_stop()
        self.close_window()

    def set_tip(self, text):
        self._tip_prx_text_browser.set_content(text)

    def submit(
        self,
        tag, name, cmd_script,
        completed_fnc=None, failed_fnc=None,
        check_memory_prc_name=None
    ):
        wgt = _qt_chart_for_sprc_task.QtChartForSprcTask()
        self._prx_scroll_area.add_widget(wgt)
        self._subprocess_widgets.append(wgt)
        # task name
        wgt._set_tag_text_(tag)
        wgt._set_text_(name)
        trd = wgt._generate_thread_(self._qt_widget)
        trd.set_fnc(cmd_script)
        if completed_fnc is not None:
            if isinstance(completed_fnc, (tuple, list)):
                [trd.completed.connect(x) for x in completed_fnc]
            else:
                trd.completed.connect(completed_fnc)
        if check_memory_prc_name is not None:
            trd.check_memory_for(check_memory_prc_name)
        trd.start()
        return wgt


class PrxSpcTaskWindow(
    gui_prx_abstracts.AbsPrxWindow,
    gui_prx_abstracts.AbsPrxProgressingDef,
):
    QT_WIDGET_CLS = _qt_window_base.QtMainWindow

    QT_PROGRESSING_CHART_CLS = _qt_wgt_chart.QtChartAsProgressing

    def __init__(self, *args, **kwargs):
        super(PrxSpcTaskWindow, self).__init__(*args, **kwargs)
        self.widget.setWindowFlags(
            _qt_core.QtCore.Qt.Window
            | _qt_core.QtCore.Qt.WindowStaysOnTopHint
            | _qt_core.QtCore.Qt.CustomizeWindowHint
            | _qt_core.QtCore.Qt.WindowMinimizeButtonHint
        )

        self._init_progressing_def_()

        self._qt_widget._thread_worker_maximum = 2

        self.set_definition_window_size((480, 480))

    def set_thread_maximum(self, value):
        self._qt_widget._thread_worker_maximum = value

    def _gui_build_(self):
        self._language = _gui_core.GuiUtil.get_language()
        self._central_qt_widget = _qt_wgt_utility.QtWidget()
        self._qt_widget.setCentralWidget(self._central_qt_widget)
        self._central_qt_layout = _qt_wgt_base.QtVBoxLayout(self._central_qt_widget)

        self._task_prx_tool_group = _container.PrxHToolGroupNew()
        self._central_qt_layout.addWidget(self._task_prx_tool_group.widget)
        self._task_prx_tool_group.set_expanded(True)
        
        self._spc_task_widget = _qt_wgt_for_sprc_task.QtSpcTaskWidget()
        self._task_prx_tool_group.add_widget(self._spc_task_widget)

        self._tip_prx_tool_group = _container.PrxHToolGroupNew()
        self._central_qt_layout.addWidget(self._tip_prx_tool_group.widget)
        self._tip_prx_tool_group.set_expanded(True)
        self._tip_prx_tool_group.set_height_match_to_maximum()

        self._tip_prx_text_browser = gui_prx_wdt_utility.PrxTextBrowser()
        self._tip_prx_tool_group.add_widget(self._tip_prx_text_browser.widget)
        self._tip_prx_text_browser._qt_widget.setMaximumHeight(80)

        self._bottom_prx_tool_bar = _container.PrxHToolBar()
        self._central_qt_layout.addWidget(self._bottom_prx_tool_bar.widget)
        self._bottom_prx_tool_bar.set_expanded(True)

        self._stop_and_close_prx_button = gui_prx_wdt_utility.PrxPressButton()
        self._bottom_prx_tool_bar.add_widget(self._stop_and_close_prx_button)
        self._stop_and_close_prx_button.connect_press_clicked_to(self._do_stop_and_close)

        if self._language == 'chs':
            self._task_prx_tool_group.set_name('进度')
            self._tip_prx_tool_group.set_name('提示')
            self._stop_and_close_prx_button.set_name('关闭')
        else:
            self._task_prx_tool_group.set_name('Progress')
            self._tip_prx_tool_group.set_name('Tip')
            self._stop_and_close_prx_button.set_name('Close')

    def _do_gui_stop(self):
        self._spc_task_widget._view_model.do_quit()

    def _do_stop_and_close(self):
        self._do_gui_stop()
        self.close_window()

    def set_tip(self, text):
        self._tip_prx_text_browser.set_content(text)

    def submit(
        self,
        type_name, name, cmd_script,
        completed_fnc=None, failed_fnc=None,
        check_memory_prc_name=None,
        application='python'
    ):
        return self._spc_task_widget._view_model.submit_cmd_script(
            type_name=type_name, name=name, cmd_script=cmd_script,
            completed_fnc=completed_fnc, failed_fnc=failed_fnc,
            check_memory_prc_name=check_memory_prc_name,
            application=application
        )
