# coding:utf-8
# gui
from ... import core as gui_core
# qt
from ...qt import core as gui_qt_core
# qt widgets
from ...qt.widgets import base as _qt_wgt_base

from ...qt.widgets import utility as _qt_wgt_utility

from ... qt.widgets import window_base as _qt_window_base

from ... qt.widgets import window_for_dialog as _qt_window_for_dialog

from ...qt.widgets import button as _qt_wgt_button

from ...qt.widgets import chart as _qt_wgt_chart

from ...qt.widgets import chart_for_sprc_task as _chart_for_sprc_task
# proxy abstracts
from .. import abstracts as gui_prx_abstracts
# proxy widgets
from . import utility as gui_prx_wdt_utility

from . import container as gui_prx_wgt_container

from . import option_node as _option_node


class AbsPrxDialogWindow(
    gui_prx_abstracts.AbsPrxWindow,
    gui_prx_abstracts.AbsPrxWaitingDef,
    gui_prx_abstracts.AbsPrxProgressingDef,
):
    PRX_CATEGORY = 'dialog_window'
    #
    QT_WIDGET_CLS = None
    BUTTON_WIDTH = 120
    #
    PROGRESS_WIDGET_CLS = _qt_wgt_utility.QtProgressBar
    #
    QT_WAITING_CHART_CLS = _qt_wgt_chart.QtChartAsWaiting
    QT_PROGRESSING_CHART_CLS = _qt_wgt_chart.QtChartAsProgressing
    #
    ValidationStatus = gui_core.GuiValidationStatus

    def __init__(self, *args, **kwargs):
        super(AbsPrxDialogWindow, self).__init__(*args, **kwargs)
        if kwargs.get('parent'):
            self.widget.setWindowFlags(
                gui_qt_core.QtCore.Qt.Tool
                # | gui_qt_core.QtCore.Qt.WindowStaysOnTopHint
            )
        else:
            self.widget.setWindowFlags(
                gui_qt_core.QtCore.Qt.Window|gui_qt_core.QtCore.Qt.WindowStaysOnTopHint
            )
        #
        self.widget.setWindowModality(
            gui_qt_core.QtCore.Qt.WindowModal
        )
        self._use_thread = True
        self._notify_when_ok_completed = False

        self._completed_content = 'process is completed, press "Close" to continue'

        self.create_window_action_for(self.do_cancel, 'esc')

    def set_window_modality(self, boolean):
        pass

    def _set_modality_swap_(self):
        pass

    def set_ok_completed_notify_enable(self, boolean):
        self._notify_when_ok_completed = boolean

    def _set_central_layout_create_(self):
        self._central_qt_widget = _qt_wgt_utility.QtWidget()
        self._qt_widget.setCentralWidget(self._central_qt_widget)
        self._central_qt_layout = _qt_wgt_base.QtVBoxLayout(self._central_qt_widget)
        self._central_qt_layout.setContentsMargins(*[4]*4)

    def _gui_build_fnc(self):
        self._set_central_layout_create_()
        #
        self._set_waiting_def_init_()
        #
        self._sub_label = _qt_wgt_utility.QtTextItem()
        self._central_qt_layout.addWidget(self._sub_label)
        self._sub_label.setVisible(False)
        self._sub_label.setFixedHeight(20)
        self._sub_label._set_name_draw_font_(gui_qt_core.QtFonts.SubTitle)
        self._sub_label._set_name_text_option_(
            gui_qt_core.QtCore.Qt.AlignHCenter | gui_qt_core.QtCore.Qt.AlignVCenter
        )
        #
        self._init_progressing_def_()
        #
        self._top_toolbar = gui_prx_wgt_container.PrxHToolbar()
        self._top_toolbar.set_hide()
        self._central_qt_layout.addWidget(self._top_toolbar.widget)
        self._top_toolbar.set_expanded(True)
        #
        self._modal_button = gui_prx_wdt_utility.PrxIconToggleButton()
        self._top_toolbar.add_widget(self._modal_button)
        self._modal_button.set_icon_name('window-modal')
        self._modal_button.set_checked(True)
        self._modal_button.connect_check_clicked_to(
            self._set_modality_swap_
        )
        self._modal_button.widget.setToolTip(
            '"LMB-click" to turn window modal "on" / "off"'
        )
        #
        s = gui_prx_wdt_utility.PrxVScrollArea()
        self._central_qt_layout.addWidget(s.widget)
        #
        self._customize_widget = _qt_wgt_utility.QtWidget()
        s.add_widget(self._customize_widget)
        self._customize_widget.setSizePolicy(
            gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )
        #
        self._customize_layout = _qt_wgt_base.QtVBoxLayout(self._customize_widget)
        self._customize_layout.setAlignment(gui_qt_core.QtCore.Qt.AlignTop)
        # option
        self._options_prx_node = _option_node.PrxOptionsNode('options')
        self._customize_layout.addWidget(self._options_prx_node.widget)
        self._options_prx_node.set_hide()
        # tip
        self._tip_prx_tool_group = gui_prx_wgt_container.PrxHToolGroupA()
        self._customize_layout.addWidget(self._tip_prx_tool_group.widget)
        self._tip_prx_tool_group.set_visible(False)
        self._tip_prx_tool_group.set_name('tips')
        self._tip_prx_text_browser = gui_prx_wdt_utility.PrxTextBrowser()
        self._tip_prx_tool_group.add_widget(self._tip_prx_text_browser)
        #
        self._bottom_toolbar = gui_prx_wgt_container.PrxHToolbar()
        self._central_qt_layout.addWidget(self._bottom_toolbar.widget)
        self._bottom_toolbar.set_expanded(True)
        qt_widget_2 = _qt_wgt_utility.QtWidget()
        self._bottom_toolbar.add_widget(qt_widget_2)
        self._input_button_layout = _qt_wgt_base.QtHBoxLayout(qt_widget_2)
        #
        qt_spacer_0 = _qt_wgt_utility._QtSpacer()
        self._input_button_layout.addWidget(qt_spacer_0)
        #
        self._ok_button = gui_prx_wdt_utility.PrxPressButton()
        # self._ok_button.set_visible(False)
        self._input_button_layout.addWidget(self._ok_button.widget)
        self._ok_button.set_name('Ok')
        # self._ok_button.set_icon_name('dialog/yes')
        self._ok_button.set_auto_width()
        self._ok_button.set_width(self.BUTTON_WIDTH)
        self._ok_button.connect_press_clicked_to(self.do_yes)
        #
        self._no_button = gui_prx_wdt_utility.PrxPressButton()
        # self._no_button.set_visible(False)
        self._no_button.set_auto_width()
        self._input_button_layout.addWidget(self._no_button.widget)
        self._no_button.set_name('No')
        # self._no_button.set_icon_name('dialog/no')
        self._no_button.set_width(self.BUTTON_WIDTH)
        self._no_button.connect_press_clicked_to(self.do_no)
        #
        self._cancel_button = gui_prx_wdt_utility.PrxPressButton()
        # self._cancel_button.set_visible(False)
        self._cancel_button.set_auto_width()
        self._input_button_layout.addWidget(self._cancel_button.widget)
        self._cancel_button.set_name('Cancel')
        # self._cancel_button.set_icon_name('dialog/cancel')
        self._cancel_button.set_width(self.BUTTON_WIDTH)
        self._cancel_button.connect_press_clicked_to(self.do_cancel)
        #
        self._ok_methods = []
        self._no_methods = []
        self._cancel_methods = []
        #
        self._result = False
        self._kwargs = {}

    def set_sub_label(self, text):
        self._sub_label.setVisible(True)
        self._sub_label._set_name_text_(text)

    def set_completed_content(self, text):
        self._completed_content = text

    def _set_completed_(self, scheme):
        if scheme == 'yes':
            if self._notify_when_ok_completed is True:
                self._options_prx_node.set_visible(False)
                self.set_ok_visible(False)
                self.set_cancel_visible(False)
                self.set_content(self._completed_content)
                self.set_status(self.ValidationStatus.Correct)
                return
        #
        self.do_close_window_later()

    def _set_failed_(self, log):
        self._options_prx_node.set_visible(False)
        self.set_ok_visible(False)
        self.set_cancel_visible(False)
        self.set_content(log)
        self.set_status(self.ValidationStatus.Error)

    def _execute_methods_(self, methods, scheme):
        def completed_fnc_():
            self._set_completed_(scheme)

        def failed_fnc_(log):
            self._set_failed_(log)

        if self._use_thread is True:
            t = self.widget._create_fnc_thread_()
            t.run_started.connect(self.start_waiting)
            t.run_finished.connect(self.stop_waiting)
            t.completed.connect(completed_fnc_)
            t.failed.connect(failed_fnc_)
            for i in methods:
                t.append_method(i)
            #
            t.start()
        else:
            for i in methods:
                i()
            self.do_close_window_later()

    def set_use_thread(self, boolean):
        self._use_thread = boolean

    def do_no(self):
        self._result = False
        self._kwargs = self.get_options_as_kwargs()
        self._execute_methods_(self._no_methods, scheme='no')

    def do_yes(self):
        self._result = True
        self._kwargs = self.get_options_as_kwargs()
        self._execute_methods_(self._ok_methods, scheme='yes')

    def do_cancel(self):
        self._result = False
        self._kwargs = self.get_options_as_kwargs()
        self._execute_methods_(self._cancel_methods, scheme='cancel')

    def get_result(self):
        return self._result

    def get_kwargs(self):
        return self._kwargs

    def set_ok_visible(self, boolean):
        self._ok_button.set_visible(boolean)

    def set_ok_label(self, text):
        self._ok_button.set_name(text)

    # noinspection PyUnusedLocal
    def connect_ok_to(self, method, args=None):
        self._ok_methods.append(method)

    def set_no_visible(self, boolean):
        self._no_button.set_visible(boolean)

    def set_no_label(self, text):
        self._no_button.set_name(text)

    # noinspection PyUnusedLocal
    def connect_no_to(self, method, args=None):
        self._no_methods.append(method)

    def set_cancel_visible(self, boolean):
        self._cancel_button.set_visible(boolean)

    def set_cancel_label(self, text):
        self._cancel_button.set_name(text)

    # noinspection PyUnusedLocal
    def connect_cancel_method(self, method, args=None):
        self._cancel_methods.append(method)

    def set_status(self, status):
        self._central_qt_widget._set_status_(status)
        self._sub_label._set_status_(status)

    def add_customize_widget(self, widget):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            qt_widget = widget
        else:
            qt_widget = widget.widget
        #
        self._customize_layout.addWidget(qt_widget)

    def set_content(self, text):
        self.set_content_with_thread(text)

    def add_content(self, text):
        self.append_log_use_signal(text)

    def set_content_font_size(self, size):
        self._tip_prx_text_browser.set_font_size(size)

    def set_tip_group_enable(self):
        self._tip_prx_tool_group.set_visible(True)
        self._tip_prx_tool_group.set_expanded(True)

    def set_tip_visible(self, boolean):
        self._tip_prx_tool_group.set_visible(boolean)

    def set_options_group_enable(self):
        self._options_prx_node.set_visible(True)
        self._options_prx_node.set_expanded(True)

    def get_options_as_kwargs(self):
        return self._options_prx_node.to_dict()

    def get_options_node(self):
        return self._options_prx_node

    def set_options_create_by_configure(self, configure):
        self._options_prx_node.build_by_data(configure)

    def append_log_use_signal(self, text):
        self._tip_prx_text_browser.append_log_use_signal(text)

    def set_content_with_thread(self, text):
        self._tip_prx_text_browser.set_content_with_thread(text)

    def set_failed(self):
        pass

    def set_completed(self):
        pass


class PrxDialogWindow0(AbsPrxDialogWindow):
    QT_WIDGET_CLS = _qt_window_base.QtMainWindow

    def __init__(self, *args, **kwargs):
        super(PrxDialogWindow0, self).__init__(*args, **kwargs)
        self._tip_prx_tool_group.set_visible(True)
        self._tip_prx_tool_group.set_expanded(True)
        self.set_content_font_size(10)

        # self._top_toolbar.set_show()

    def show_window_auto(self, pos=None, size=None, exclusive=True):
        # do not show unique
        gui_qt_core.QtUtil.show_qt_window(
            self.widget,
            pos,
            size
        )

    def _set_modality_swap_(self):
        def get_geometry_args_fnc_():
            w = self._qt_widget.centralWidget()
            p = w.pos()
            p_ = self._qt_widget.mapToGlobal(p)
            return p_.x(), p_.y(), w.width(), w.height()

        geometry_args = get_geometry_args_fnc_()
        self._qt_widget.hide()
        self._qt_widget.setWindowModality(
            [gui_qt_core.QtCore.Qt.NonModal, gui_qt_core.QtCore.Qt.WindowModal][
                self._modal_button.get_checked()]
        )
        self._qt_widget.show()
        self._qt_widget.setGeometry(*geometry_args)

    def set_window_modality(self, boolean):
        self.widget.setWindowModality(
            [gui_qt_core.QtCore.Qt.NonModal, gui_qt_core.QtCore.Qt.WindowModal][boolean]
        )


class PrxDialogWindow1(AbsPrxDialogWindow):
    QT_WIDGET_CLS = _qt_window_for_dialog.QtBaseDialog

    def __init__(self, *args, **kwargs):
        super(PrxDialogWindow1, self).__init__(*args, **kwargs)
        self._tip_prx_tool_group.set_visible(True)
        self._tip_prx_tool_group.set_expanded(True)
        self.set_content_font_size(10)

    def _set_central_layout_create_(self):
        layout = _qt_wgt_base.QtVBoxLayout(self.widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self._central_qt_widget = _qt_wgt_utility.QtWidget()
        layout.addWidget(self._central_qt_widget)
        self._central_qt_layout = _qt_wgt_base.QtVBoxLayout(self._central_qt_widget)
        self._central_qt_layout.setContentsMargins(*[4]*4)

    def do_yes(self):
        self._result = True
        self._kwargs = self.get_options_as_kwargs()
        for i in self._ok_methods:
            i()
        #
        self._qt_widget._do_ok_()

    def do_no(self):
        self._result = False
        self._kwargs = self.get_options_as_kwargs()
        for i in self._no_methods:
            i()
        #
        self._qt_widget._do_no_()

    def do_cancel(self):
        self._result = None
        self._kwargs = self.get_options_as_kwargs()
        for i in self._cancel_methods:
            i()
        #
        self._qt_widget._do_cancel_()

    def show_window_auto(self, pos=None, size=None, exclusive=True):
        # do not show unique
        gui_qt_core.QtUtil.show_qt_window(
            self.widget,
            pos,
            size,
            use_exec=True
        )


class PrxTipWindow(PrxDialogWindow0):
    def __init__(self, *args, **kwargs):
        super(PrxTipWindow, self).__init__(*args, **kwargs)
        self._tip_prx_tool_group.set_visible(True)
        self._tip_prx_tool_group.set_expanded(True)
        self.set_content_font_size(10)

    def do_no(self):
        self._result = False
        for i in self._no_methods:
            i()
        self.do_close_window_later()

    def do_yes(self):
        self._result = True
        for i in self._ok_methods:
            i()
        self.do_close_window_later()

    def do_cancel(self):
        self._result = False
        for i in self._cancel_methods:
            i()
        self.do_close_window_later()


class PrxWindowForException(PrxTipWindow):
    PRX_CATEGORY = 'exception_window'

    def __init__(self, *args, **kwargs):
        super(PrxWindowForException, self).__init__(*args, **kwargs)

        self.set_ok_label('Close')
        self.set_no_visible(False)
        self.set_cancel_visible(False)


class PrxMonitorWindow(
    gui_prx_abstracts.AbsPrxWindow,
    gui_prx_abstracts.AbsPrxWaitingDef,
    gui_prx_abstracts.AbsPrxProgressingDef,
):
    ValidationStatus = gui_core.GuiValidationStatus
    #
    QT_WIDGET_CLS = _qt_window_base.QtMainWindow
    #
    QT_WAITING_CHART_CLS = _qt_wgt_chart.QtChartAsWaiting
    QT_PROGRESSING_CHART_CLS = _qt_wgt_chart.QtChartAsProgressing

    def __init__(self, *args, **kwargs):
        super(PrxMonitorWindow, self).__init__(*args, **kwargs)
        if kwargs.get('parent'):
            self.widget.setWindowFlags(
                gui_qt_core.QtCore.Qt.Tool | gui_qt_core.QtCore.Qt.WindowStaysOnTopHint
            )
        else:
            self.widget.setWindowFlags(
                gui_qt_core.QtCore.Qt.Window | gui_qt_core.QtCore.Qt.WindowStaysOnTopHint
            )
        self.widget.setWindowModality(
            gui_qt_core.QtCore.Qt.WindowModal
        )

    def _gui_build_fnc(self):
        self._central_qt_widget = _qt_wgt_utility.QtWidget()
        self._qt_widget.setCentralWidget(self._central_qt_widget)
        self._central_qt_layout = _qt_wgt_base.QtVBoxLayout(self._central_qt_widget)
        #
        self._tip_prx_text_browser = gui_prx_wdt_utility.PrxTextBrowser()
        self._central_qt_layout.addWidget(self._tip_prx_text_browser.widget)
        #
        qt_widget_1 = _qt_wgt_utility.QtWidget()
        self._central_qt_layout.addWidget(qt_widget_1)
        #
        self._input_button_layout = _qt_wgt_base.QtHBoxLayout(qt_widget_1)
        #
        self._status_button = gui_prx_wdt_utility.PrxPressButton()
        self._input_button_layout.addWidget(self._status_button.widget)
        self._status_button.set_name('process')
        self._status_button.set_icon_by_text('process')

        self._set_waiting_def_init_()
        self._init_progressing_def_()

    def set_status(self, status):
        self._central_qt_widget._set_status_(status)

    def get_status_button(self):
        return self._status_button

    def set_logging(self, *args):
        self._tip_prx_text_browser.append_log_use_signal(*args)

    def set_status_at(self, *args):
        self._status_button.set_status_at(*args)

    def set_finished_at(self, *args):
        self._status_button.set_finished_at(*args)


class PrxSprcTaskWindow(
    gui_prx_abstracts.AbsPrxWindow,
    gui_prx_abstracts.AbsPrxProgressingDef,
):
    QT_WIDGET_CLS = _qt_window_base.QtMainWindow

    def __init__(self, *args, **kwargs):
        super(PrxSprcTaskWindow, self).__init__(*args, **kwargs)
        if isinstance(kwargs.get('parent'), gui_qt_core.QtWidgets.QMainWindow):
            self.widget.setWindowFlags(
                gui_qt_core.QtCore.Qt.Tool | gui_qt_core.QtCore.Qt.WindowStaysOnTopHint
            )
            self.get_widget().setParent(kwargs['parent'])
        else:
            self.widget.setWindowFlags(
                gui_qt_core.QtCore.Qt.Window | gui_qt_core.QtCore.Qt.WindowStaysOnTopHint
            )

        self.set_definition_window_size((480, 240))

    def _gui_build_fnc(self):
        self._central_qt_widget = _qt_wgt_utility.QtWidget()
        self._qt_widget.setCentralWidget(self._central_qt_widget)
        self._central_qt_layout = _qt_wgt_base.QtVBoxLayout(self._central_qt_widget)
        #
        self._task_qt_chart = _chart_for_sprc_task.QtChartForSprcTask()
        self._central_qt_layout.addWidget(self._task_qt_chart)
        #
        self._tip_prx_text_browser = gui_prx_wdt_utility.PrxTextBrowser()
        self._central_qt_layout.addWidget(self._tip_prx_text_browser.widget)

        self._bottom_toolbar = gui_prx_wgt_container.PrxHToolbar()
        self._central_qt_layout.addWidget(self._bottom_toolbar.widget)
        self._bottom_toolbar.set_expanded(True)
        self._bottom_toolbar.set_align_right()

        self.register_window_close_method(self.kill_processing)

        self._stop_button = _qt_wgt_button.QtPressButton()
        self._bottom_toolbar.add_widget(self._stop_button)
        self._stop_button._set_name_text_('Stop')
        self._stop_button._set_icon_name_('stop')
        self._stop_button.setFixedWidth(80)

        self._stop_button.press_clicked.connect(self.kill_processing)

        self._close_button = _qt_wgt_button.QtPressButton()
        self._bottom_toolbar.add_widget(self._close_button)
        self._close_button._set_name_text_('Close')
        self._close_button._set_icon_name_('close-hover')
        self._close_button.setFixedWidth(80)
        self._close_button.press_clicked.connect(self.close_window)

        self._task_qt_chart.log_update.connect(self.log_update)

    def start(self, fnc, *args, **kwargs):
        t = self._task_qt_chart._generate_thread_(self._qt_widget)
        t.set_fnc(fnc, *args, **kwargs)
        t.start()
        t.finished.connect(self._on_finished)
        return t

    def _on_finished(self):
        self._stop_button.hide()

    def kill_processing(self):
        self._task_qt_chart._do_close_()

    def is_killed(self):
        return self._task_qt_chart._is_killed_()

    def log_update(self, text):
        self._tip_prx_text_browser.append_log_use_signal(text)
