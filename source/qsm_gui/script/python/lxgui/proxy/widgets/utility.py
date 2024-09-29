# coding:utf-8
import six

import lxbasic.core as bsc_core
# gui
from ... import core as gui_core
# qt
from ...qt import core as gui_qt_core
# qt widgets
from ...qt.widgets import base as gui_qt_wgt_base

from ...qt.widgets import utility as gui_qt_wgt_utility

from ...qt.widgets import button as gui_qt_wgt_button

from ...qt.widgets import resize as gui_qt_wgt_resize

from ...qt.widgets import input_for_filter as gui_qt_wgt_input_for_filter

from ...qt.widgets import item as gui_qt_wgt_item

from ...qt.widgets import input as gui_qt_wgt_input

from ...qt.widgets import window_base as _qt_window_base

from ...qt.widgets import window as gui_qt_wgt_window

from ...qt.widgets import screenshot as _screenshot
# proxy abstracts
from .. import abstracts as gui_prx_abstracts


class PrxHScrollArea(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtHScrollArea

    def __init__(self, *args, **kwargs):
        super(PrxHScrollArea, self).__init__(*args, **kwargs)
        self._layout = self.widget._layout

    def add_widget(self, widget):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            self._layout.addWidget(widget)
        else:
            self._layout.addWidget(widget.widget)

    def do_clear(self):
        def rcs_fnc_(layout_):
            c = layout_.count()
            for i in range(c):
                i_item = self._layout.takeAt(0)
                if i_item is not None:
                    i_widget = i_item.widget()
                    if i_widget:
                        i_widget.deleteLater()
                    else:
                        _i_layout = i_item.layout()
                        if _i_layout:
                            rcs_fnc_(_i_layout)
                        else:
                            spacer = i_item.spacerItem()
                            if spacer:
                                spacer.deleteLater()

        #
        rcs_fnc_(self._layout)

    def restore(self):
        self.do_clear()


class PrxVScrollArea(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtVScrollArea

    def __init__(self, *args, **kwargs):
        super(PrxVScrollArea, self).__init__(*args, **kwargs)
        self._qt_layout = self._qt_widget._layout

    def add_widget(self, widget):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            self._qt_layout.addWidget(widget)
        else:
            self._qt_layout.addWidget(widget.widget)

    def do_clear(self):
        def rcs_fnc_(layout_):
            c = layout_.count()
            for i in range(c):
                i_item = self._qt_layout.takeAt(0)
                if i_item is not None:
                    i_widget = i_item.widget()
                    if i_widget:
                        i_widget.deleteLater()
                    else:
                        _i_layout = i_item.layout()
                        if _i_layout:
                            rcs_fnc_(_i_layout)
                        else:
                            spacer = i_item.spacerItem()
                            if spacer:
                                spacer.deleteLater()

        rcs_fnc_(self._qt_layout)

    def restore(self):
        self.do_clear()

    def set_margins(self, m_l, m_t, m_r, m_b):
        self._qt_layout.setContentsMargins(m_l, m_t, m_r, m_b)


class Window(gui_prx_abstracts.AbsPrxWindow):
    QT_WIDGET_CLS = _qt_window_base.QtMainWindow

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

    def _gui_build_(self):
        self._qt_main_widget = gui_qt_wgt_utility.QtWidget()
        self._qt_widget.setCentralWidget(self._qt_main_widget)
        self._main_qt_layout = gui_qt_wgt_base.QtHBoxLayout(self._qt_main_widget)

    def get_main_widget(self):
        return self._qt_main_widget

    def add_widget(self, widget):
        self._main_qt_layout.addWidget(widget)


class PrxLayerWidget(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget

    def __init__(self, *args, **kwargs):
        super(PrxLayerWidget, self).__init__(*args, **kwargs)

    def _gui_build_(self):
        qt_layout_0 = gui_qt_wgt_base.QtVBoxLayout(self.widget)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        qt_layout_0.setSpacing(0)
        #
        qt_widget_0 = gui_qt_wgt_utility.QtHFrame()
        qt_widget_0.setMaximumHeight(24)
        qt_widget_0.setMinimumHeight(24)
        qt_layout_0.addWidget(qt_widget_0)
        #
        qt_top_layout_1 = gui_qt_wgt_base.QtHBoxLayout(qt_widget_0)
        qt_top_layout_1.setContentsMargins(0, 0, 0, 0)
        qt_top_layout_1.setSpacing(0)
        self._qt_label_0 = gui_qt_wgt_utility.QtTextItem()
        self._qt_label_0._set_name_text_option_(
            gui_qt_core.QtCore.Qt.AlignHCenter|gui_qt_core.QtCore.Qt.AlignVCenter
        )
        self._qt_label_0._set_name_font_size_(12)
        qt_top_layout_1.addWidget(self._qt_label_0)
        self._button_0 = PrxIconPressButton()
        self._button_0.set_icon_name('window_base/close')
        self._button_0.set_icon_hover_color((255, 0, 63, 127))
        qt_top_layout_1.addWidget(self._button_0.widget)

        self._qt_line = gui_qt_wgt_utility.QtHLine()
        qt_layout_0.addWidget(self._qt_line)
        self._qt_central_widget_0 = gui_qt_wgt_utility.QtWidget()
        self._qt_central_widget_0.setSizePolicy(
            gui_qt_core.QtWidgets.QSizePolicy.Expanding, gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )
        qt_layout_0.addWidget(self._qt_central_widget_0)
        self._qt_layout_0 = gui_qt_wgt_base.QtVBoxLayout(self._qt_central_widget_0)
        self._qt_layout_0.setContentsMargins(2, 2, 2, 2)

    def set_name(self, text):
        self._qt_label_0._set_name_text_(text)

    def set_status(self, status):
        self._qt_label_0._set_status_(status)

    def add_widget(self, widget):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            self._qt_layout_0.addWidget(widget)
        else:
            self._qt_layout_0.addWidget(widget._qt_widget)

    def connect_close_to(self, method):
        self._button_0.widget.press_clicked.connect(method)

    @property
    def central_layout(self):
        return self._qt_layout_0

    def get_layout(self):
        return self._qt_layout_0

    def clear(self):
        layout = self._qt_layout_0
        c = layout.count()
        if c:
            for i in range(c):
                item = layout.itemAt(i)
                if item:
                    widget = item.widget()
                    widget.deleteLater()


class PrxLayer(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    #
    PRX_LAYER_WIDGET_CLS = PrxLayerWidget

    def __init__(self, *args, **kwargs):
        super(PrxLayer, self).__init__(*args, **kwargs)
        self._layer_widget = None

    def get_widget(self):
        return self._layer_widget

    def create_widget(self, key, label=None):
        qt_layout_0 = gui_qt_wgt_base.QtVBoxLayout(self._qt_widget)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        self._layer_widget = self.PRX_LAYER_WIDGET_CLS()
        if label is None:
            label = bsc_core.RawTextMtd.to_prettify(key)
        self._layer_widget.set_name(label)
        qt_layout_0.addWidget(self._layer_widget.widget)
        return self._layer_widget


class PrxTextBrowser(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtWidget

    def __init__(self, *args, **kwargs):
        super(PrxTextBrowser, self).__init__(*args, **kwargs)

    def _gui_build_(self):
        qt_layout_0 = gui_qt_wgt_base.QtVBoxLayout(self.widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        widget = gui_qt_wgt_input.QtInputAsContent()
        widget._set_entry_enable_(False)
        qt_layout_0.addWidget(widget)
        self._qt_entry_widget = widget._entry_widget

    def set_markdown_file_open(self, file_path):
        if file_path:
            import markdown

            with open(file_path) as f:
                raw = f.read()
                raw = raw.decode('utf-8')
                html = markdown.markdown(raw)
                self._qt_entry_widget.setHtml(html)

    def append(self, text):
        if isinstance(text, six.string_types):
            self._qt_entry_widget.append(
                text
            )

    def append_html(self, xml):
        if isinstance(xml, six.string_types):
            self._qt_entry_widget.insertHtml(
                xml
            )

    def add_result(self, text):
        self._qt_entry_widget.append(
            gui_core.GuiXml.get_text(text)
        )

    def add_error(self, text):
        self._qt_entry_widget.append(
            gui_core.GuiXml.get_text(text, text_color=gui_core.GuiXmlColor.TorchRed)
        )

    def add_warning(self, text):
        self._qt_entry_widget.append(
            gui_core.GuiXml.get_text(text, text_color=gui_core.GuiXmlColor.Yellow)
        )

    def trace_log(self, text):
        self._qt_entry_widget._add_value_(text)

    def trace_log_use_thread(self, text):
        self._qt_entry_widget._add_value_with_thread_(text)

    def set_content_with_thread(self, text):
        self._qt_entry_widget._set_value_with_thread_(text)

    def set_content(self, text, as_html=False):
        if as_html is True:
            self._qt_entry_widget.setHtml(
                text
            )
        else:
            self._qt_entry_widget.setText(
                text
            )

    def set_font_size(self, size):
        font = self.widget.font()
        font.setPointSize(size)
        self._qt_entry_widget.setFont(font)

    def get_content(self, as_html=False):
        if as_html is True:
            return self._qt_entry_widget.toHtml()
        return self._qt_entry_widget.toPlainText()

    def set_status(self, status):
        self._qt_widget._set_status_(status)

    def set_focus_enable(self, boolean):
        self._qt_entry_widget._set_entry_focus_enable_(boolean)


class PrxMenu(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtMenu

    def __init__(self, *args, **kwargs):
        super(PrxMenu, self).__init__(*args, **kwargs)

    def set_name(self, name):
        self.widget.setTitle(name)

    def execute(self, menu_raws):
        self.widget._set_menu_data_(menu_raws)

    def set_menu_data(self, menu_raws):
        self.widget._set_menu_data_(menu_raws)

    def set_menu_content(self, content):
        self.widget._set_menu_content_(content)

    def set_show(self, boolean=True):
        self.widget.popup(
            gui_qt_core.QtGui.QCursor().pos()
        )


class PrxIconPressButton(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_button.QtIconPressButton

    def __init__(self, *args, **kwargs):
        super(PrxIconPressButton, self).__init__(*args, **kwargs)
        self._qt_widget.setFixedSize(20, 20)

    def set_name(self, *args, **kwargs):
        self._qt_widget._set_name_text_(*args, **kwargs)

    def get_name(self):
        return self._qt_widget._get_name_text_()

    def set_icon_name(self, icon_name):
        self._qt_widget._set_icon_file_path_(
            gui_core.GuiIcon.get(icon_name)
        )

    def set_icon_sub_name(self, icon_name):
        self._qt_widget._set_icon_sub_file_path_(
            gui_core.GuiIcon.get(icon_name)
        )

    def set_icon_hover_color(self, color):
        self._qt_widget._set_icon_hover_color_(
            color
        )

    def set_icon_by_text(self, text):
        self._qt_widget._set_icon_by_text_(text)

    def set_icon_color(self, rgba):
        self._qt_widget._set_icon_name_rgba_(rgba)

    def set_icon_size(self, w, h):
        self._qt_widget._set_icon_file_draw_size_(w, h)

    def set_icon_frame_size(self, w, h):
        self._qt_widget._set_icon_frame_draw_size_(w, h)

    def connect_press_clicked_to(self, fnc):
        self._qt_widget.press_clicked.connect(fnc)

    def set_tool_tip(self, *args, **kwargs):
        self._qt_widget._set_tool_tip_(*args, **kwargs)

    def set_action_enable(self, boolean):
        self._qt_widget._set_action_enable_(boolean)

    def set_menu_data(self, data):
        self._qt_widget._set_menu_data_(data)

    def set_menu_content(self, content):
        self._qt_widget._set_menu_content_(content)

    def connect_press_dbl_clicked_to(self, fnc):
        self._qt_widget.press_dbl_clicked.connect(fnc)

    def set_drag_enable(self, boolean):
        self._qt_widget._set_drag_enable_(boolean)

    def set_drag_and_drop_scheme(self, text):
        self._qt_widget._set_drag_and_drop_scheme_(text)

    def save_main_icon_to_file(self, file_path):
        self._qt_widget._save_main_icon_to_file_(file_path)


class PrxPressButton(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_button.QtPressButton

    def __init__(self, *args, **kwargs):
        super(PrxPressButton, self).__init__(*args, **kwargs)
        self.widget.setFixedHeight(20)

    def set_enable(self, boolean):
        self._qt_widget._set_action_enable_(boolean)

    def get_is_enable(self):
        return self._qt_widget._get_action_is_enable_()

    def set_check_enable(self, boolean):
        self.widget._set_check_action_enable_(boolean)
        self.widget.update()

    def get_is_checked(self):
        return self.widget._is_checked_()

    def set_checked(self, boolean):
        self._qt_widget._set_checked_(boolean)

    def set_option_click_enable(self, boolean):
        self._qt_widget._set_option_click_enable_(boolean)

    def set_icon_name(self, icon_name):
        self._qt_widget._set_icon_file_path_(
            gui_core.GuiIcon.get(icon_name)
        )

    def set_icon_by_color(self, color):
        self.widget._icon_color_rgb = color
        self.widget._icon_is_enable = True
        self.widget.update()

    def set_icon_by_text(self, text):
        self.widget._set_icon_by_text_(text)

    def set_icon_color_by_name(self, name):
        pass

    def set_width(self, w):
        self.widget.setFixedWidth(w)

    def set_icon_size(self, w, h):
        self.widget._icon_draw_size = w, h

    def set_name(self, text):
        self.widget._set_name_text_(text)

    def set_tool_tip(self, raw):
        self.widget._set_tool_tip_(raw)

    def set_check_clicked_connect_to(self, fnc):
        self.widget.check_clicked.connect(fnc)

    def connect_press_clicked_to(self, fnc):
        self.widget.press_clicked.connect(fnc)

    def set_press_clicked(self):
        self.widget.clicked.emit()

    def set_option_click_connect_to(self, fnc):
        self.widget.option_clicked.connect(fnc)

    def set_status_enable(self, boolean):
        pass

    def set_status(self, status):
        self.widget.status_changed.emit(status)

    def set_status_at(self, index, status):
        self.widget.rate_status_update_at.emit(index, status)

    def set_statuses(self, element_statuses):
        self.widget._set_sub_process_statuses_(element_statuses)

    def set_finished_at(self, index, status):
        self.widget.rate_finished_at.emit(index, status)

    def initialization(self, count, status=gui_core.GuiProcessStatus.Waiting):
        self.widget._initialization_sub_process_(count, status)

    def set_stopped(self, boolean=True):
        self._is_stopped = boolean


class PrxCheckItem(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_button.QtCheckButton

    def __init__(self, *args, **kwargs):
        super(PrxCheckItem, self).__init__(*args, **kwargs)
        self.widget.setMaximumHeight(20)
        self.widget.setMinimumHeight(20)

    def set_check_icon_names(self, icon_name_0, icon_name_1):
        self.widget._set_check_icon_file_paths_(
            gui_core.GuiIcon.get(icon_name_0),
            gui_core.GuiIcon.get(icon_name_1)
        )


class PrxToggleButton(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_button.QtIconToggleButton

    def __init__(self, *args, **kwargs):
        super(PrxToggleButton, self).__init__(*args, **kwargs)
        self._qt_widget._set_size_(20, 20)

    def set_name(self, text):
        self._qt_widget._set_name_text_(text)

    def set_icon_name(self, icon_name):
        self._qt_widget._set_icon_file_path_(
            gui_core.GuiIcon.get(icon_name),
        )

    def set_tool_tip(self, text):
        self._qt_widget._set_tool_tip_(text)

    def set_checked(self, boolean):
        self._qt_widget._set_checked_(boolean)

    def get_is_checked(self):
        return self._qt_widget._is_checked_()

    def execute_swap_check(self):
        self._qt_widget._swap_check_()

    def get_checked(self):
        return self._qt_widget._is_checked_()

    def connect_check_clicked_to(self, fnc):
        self._qt_widget.check_clicked.connect(fnc)

    def connect_check_toggled_to(self, fnc):
        self._qt_widget.check_toggled.connect(fnc)

    def connect_user_check_clicked_to(self, fnc):
        self._qt_widget.user_check_clicked.connect(fnc)

    def connect_user_check_toggled_to(self, fnc):
        self._qt_widget.user_check_toggled.connect(fnc)

    def connect_check_clicked_as_exclusive_to(self, fnc):
        self._qt_widget.user_check_clicked_as_exclusive.connect(fnc)

    def connect_check_changed_as_exclusive_to(self, fnc):
        self._qt_widget.check_changed_as_exclusive.connect(fnc)

    def connect_check_swapped_as_exclusive_to(self, fnc):
        self._qt_widget.check_swapped_as_exclusive.connect(fnc)


class PrxFilterBar(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_input_for_filter.QtInputAsFilter

    def __init__(self, *args, **kwargs):
        super(PrxFilterBar, self).__init__(*args, **kwargs)

    def set_tip(self, text):
        self._qt_widget._set_filter_tip_(text)

    def get_enter_widget(self):
        return self._qt_widget._get_entry_widget_()

    def set_filter_connect_to(self, proxy):
        proxy._set_filter_bar_(self)

    def get_keyword(self):
        return self.get_enter_widget()._get_value_()

    def get_keywords(self):
        return self._qt_widget._get_all_keywords_()

    def get_is_match_case(self):
        return self.widget._get_is_match_case_()

    def get_is_match_word(self):
        return self.widget._get_is_match_word_()

    def set_result_count(self, value):
        self.widget._set_filter_result_count_(value)

    def set_result_index(self, value):
        self.widget._set_filter_result_index_current_(value)

    def set_result_clear(self):
        self.widget._clear_filter_result_()

    def restore(self):
        self._qt_widget._restore_()

    def set_entry_focus(self, boolean):
        self.widget._set_entry_focus_(boolean)

    def set_history_key(self, key):
        self._qt_widget._set_history_key_(key)

    def set_history_filter_fnc(self, fnc):
        pass

    def set_completion_gain_fnc(self, fnc):
        self._qt_widget._set_input_completion_buffer_fnc_(fnc)


class PrxButtonGroup(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtVLine

    def __init__(self, *args, **kwargs):
        super(PrxButtonGroup, self).__init__(*args, **kwargs)
        # self._qt_widget._set_line_draw_enable_(True)
        self._layout = gui_qt_core.QtGridLayout(
            self._qt_widget
        )
        self._layout.setContentsMargins(8, 2, 0, 2)
        self._layout.setSpacing(4)

    def add_widget(self, widget, d=2):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            self._layout._add_widget_(widget, d)
        else:
            self._layout._add_widget_(widget.widget, d)


class PrxFramelessWindow(
    gui_prx_abstracts.AbsPrxWindow,
):
    QT_WIDGET_CLS = gui_qt_wgt_window._QtFramelessWindow

    def __init__(self, *args, **kwargs):
        super(PrxFramelessWindow, self).__init__(*args, **kwargs)
        self.widget.setWindowFlags(gui_qt_core.QtCore.Qt.Window|gui_qt_core.QtCore.Qt.FramelessWindowHint)


class PrxWindow(
    gui_prx_abstracts.AbsPrxWindow,
):
    QT_WIDGET_CLS = gui_qt_wgt_window._QtWindow

    def __init__(self, *args, **kwargs):
        super(PrxWindow, self).__init__(*args, **kwargs)


class PrxWindowNew(
    gui_prx_abstracts.AbsPrxWindow,
):
    QT_WIDGET_CLS = _qt_window_base.QtMainWindow

    def __init__(self, *args, **kwargs):
        super(PrxWindowNew, self).__init__(*args, **kwargs)


class PrxScreenshotFrame(
    gui_prx_abstracts.AbsPrxWidget
):
    QT_WIDGET_CLS = _screenshot.QtScreenshotFrame

    def __init__(self, *args, **kwargs):
        main_window = gui_qt_core.GuiQtDcc.get_qt_active_window()
        super(PrxScreenshotFrame, self).__init__(main_window, *args, **kwargs)

    def do_start(self):
        self._qt_widget._start_screenshot_()

    def connect_started_to(self, fnc):
        self._qt_widget.screenshot_started.connect(fnc)

    def connect_finished_to(self, fnc):
        self._qt_widget.screenshot_finished.connect(fnc)

    def connect_accepted_to(self, fnc):
        self._qt_widget.screenshot_accepted.connect(fnc)

    @classmethod
    def save_to(cls, geometry, file_path):
        cls.QT_WIDGET_CLS._save_screenshot_to_(geometry, file_path)
