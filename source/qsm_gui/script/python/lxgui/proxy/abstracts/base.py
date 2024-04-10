# coding:utf-8
import fnmatch

import uuid

from contextlib import contextmanager

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core
# gui
from ... import core as gui_core
# qt
from ...qt import core as gui_qt_core
# proxy
from .. import core as gui_prx_core


class AbsPrxStateDef(object):
    NORMAL_STATE = gui_core.GuiState.NORMAL
    ENABLE_STATE = gui_core.GuiState.ENABLE
    DISABLE_STATE = gui_core.GuiState.DISABLE
    WARNING_STATE = gui_core.GuiState.WARNING
    ERROR_STATE = gui_core.GuiState.ERROR

    LOCKED_STATE = gui_core.GuiState.LOCKED

    State = gui_core.GuiState


class AbsPrx(object):
    QT_WIDGET_CLS = None
    MODEL_CLS = None
    DCC_OBJ_KEY = 'dcc_obj'
    #
    PRX_CATEGORY = 'dialog_window'
    #
    Status = gui_core.GuiStatus
    ProcessStatus = gui_core.GuiStatus
    ShowStatus = gui_core.GuiShowStatus
    ValidationStatus = gui_core.GuiValidationStatus

    def __init__(self, *args, **kwargs):
        self._init_prx_def_(*args, **kwargs)

    def _init_prx_def_(self, *args, **kwargs):
        self._qt_widget = self.QT_WIDGET_CLS(*args, **kwargs)
        self._qt_widget.gui_proxy = self
        if self.MODEL_CLS is not None:
            self._model = self.MODEL_CLS()
        else:
            self._model = None
        #
        self._custom_raw = {}

    def get_widget(self):
        return self._qt_widget

    widget = property(get_widget)

    def get_model(self):
        return self._model

    model = property(get_model)

    def set_parent_widget(self, widget):
        self._qt_widget.setParent(widget)

    def set_gui_attribute(self, key, value):
        self._custom_raw[key] = value

    def get_gui_attribute(self, key, default=None):
        return self._custom_raw.get(key, default)

    def set_gui_dcc_obj(self, dcc_obj, namespace=None):
        key = self.DCC_OBJ_KEY
        if namespace is not None:
            key = '{}:{}'.format(namespace, self.DCC_OBJ_KEY)
        self.set_gui_attribute(key, dcc_obj)

    def get_gui_dcc_obj(self, namespace=None):
        key = self.DCC_OBJ_KEY
        if namespace is not None:
            key = '{}:{}'.format(namespace, self.DCC_OBJ_KEY)
        return self.get_gui_attribute(key)

    def get_obj_gui(self):
        pass

    def get_custom_raws(self, regex):
        lis = []
        keys = fnmatch.filter(self._custom_raw.keys(), regex) or []
        for key in keys:
            lis.append(self.get_gui_attribute(key))
        return lis

    def get_is_exists(self):
        pass

    def set_visible(self, boolean, **kwargs):
        self.widget.setHidden(not boolean)

    def get_is_visible(self):
        return self.widget.isVisible()

    def set_actions_register(self, action_data):
        pass

    def __str__(self):
        return '{}(widget="{}")'.format(
            self.__class__.__name__,
            self.QT_WIDGET_CLS.__name__
        )


class AbsPrxWidget(AbsPrx):
    def __init__(self, *args, **kwargs):
        super(AbsPrxWidget, self).__init__(*args, **kwargs)
        #
        self._qt_thread_enable = bsc_core.EnvBaseMtd.get_qt_thread_enable()
        #
        self._gui_build_()

    def _gui_build_(self):
        pass

    def set_hide(self, boolean=True):
        if boolean is True:
            self.widget.hide()
        else:
            self.widget.show()

    def set_show(self, boolean=True):
        if boolean is True:
            self.widget.show()
        else:
            self.widget.hide()


class AbsPrxViewDef(object):
    def _set_prx_view_def_init_(self, qt_view):
        self._qt_view = qt_view

    @property
    def view(self):
        return self._qt_view

    def create_item(self, *args, **kwargs):
        raise NotImplementedError()

    #
    def connect_item_select_changed_to(self, fnc):
        self._qt_view.itemSelectionChanged.connect(fnc)

    def connect_focus_changed_to(self, fnc):
        self._qt_view.focus_changed.connect(fnc)

    # select
    def _get_selected_items_(self):
        return self.view.selectedItems()

    def get_selected_items(self):
        return [i.gui_proxy for i in self._get_selected_items_()]

    def get_selected_item_widgets(self):
        pass

    def get_current_item(self):
        pass


class _WaitingContext(object):
    def __init__(self, proxy):
        self._proxy = proxy

    def start(self):
        self._proxy.start_waiting()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._proxy.stop_waiting()


class AbsPrxWaitingDef(object):
    QT_WAITING_CHART_CLS = None

    @property
    def widget(self):
        raise NotImplementedError()

    def waiting(self):
        return _WaitingContext(self)

    def _set_waiting_def_init_(self):
        self._qt_waiting_char = self.QT_WAITING_CHART_CLS(self.widget)
        self._qt_waiting_char.hide()
        #
        self._auto_stop_timer = gui_qt_core.QtCore.QTimer(self.widget)
        #
        self.widget._set_size_changed_connect_to_(self._refresh_waiting_draw_)

    def start_waiting(self, auto_stop_time=None):
        self.widget.setCursor(gui_qt_core.QtCore.Qt.BusyCursor)
        self._qt_waiting_char.show()
        gui_qt_core.GuiQtApplicationOpt().set_process_run_0()
        self._qt_waiting_char._start_waiting_()
        if isinstance(auto_stop_time, (int, float)):
            self._auto_stop_timer.singleShot(
                auto_stop_time, self.stop_waiting
            )

    def update_waiting(self):
        self._qt_waiting_char.update()
        gui_qt_core.GuiQtApplicationOpt().set_process_run_0()

    def stop_waiting(self):
        self.widget.unsetCursor()
        self._qt_waiting_char.hide()
        gui_qt_core.GuiQtApplicationOpt().set_process_run_0()
        self._qt_waiting_char._stop_waiting_()

    def _refresh_waiting_draw_(self):
        x, y = 0, 0
        w, h = self.widget.width(), self.widget.height()
        self._qt_waiting_char.setGeometry(
            x, y, w, h
        )


# noinspection PyUnusedLocal
class AbsPrxWindow(AbsPrx):
    WINDOW_LOADING_SIZE = 480, 320

    def __init__(self, *args, **kwargs):
        super(AbsPrxWindow, self).__init__(*args, **kwargs)
        self._init_window_def_(*args, **kwargs)

    def _init_window_def_(self, *args, **kwargs):
        self._window_unicode_id = str(uuid.uuid1()).upper()
        #
        if kwargs.get('parent'):
            pass
            # print kwargs['parent']
        else:
            main_window = gui_qt_core.GuiQtDcc.get_qt_main_window()
            # print main_window.font()
            if main_window != self.widget:
                self.widget.setParent(
                    main_window, gui_qt_core.QtCore.Qt.Window
                )
        #
        self._main_window_geometry = None
        #
        self._definition_window_size = self.WINDOW_LOADING_SIZE
        #
        self._qt_widget.setBaseSize(
            gui_qt_core.QtCore.QSize(*self._definition_window_size)
        )
        #
        self._window_title = None

        self._close_methods = []
        #
        self._status = self.ValidationStatus.Normal

        self._gui_build_()

    def get_window_unique_id(self):
        return self._window_unicode_id

    def _gui_build_(self):
        pass

    def set_main_window_geometry(self, geometry):
        self._main_window_geometry = geometry
        self._qt_widget._main_window_geometry = geometry

    def get_definition_window_size(self):
        return self._definition_window_size

    def set_definition_window_size(self, size):
        if size is not None:
            self._definition_window_size = size
            self._qt_widget.setBaseSize(
                gui_qt_core.QtCore.QSize(*self._definition_window_size)
            )

    def set_window_show(self, pos=None, size=None, exclusive=True):
        # show unique
        if exclusive is True:
            gui_proxies = gui_prx_core.GuiProxyUtil.find_widget_proxy_by_class(self.__class__)
            for i in gui_proxies:
                if hasattr(i, '_window_unicode_id'):
                    if i._window_unicode_id != self._window_unicode_id:
                        bsc_log.Log.trace_method_warning(
                            'close exists window for "{}"'.format(
                                self.__class__.__name__
                            )
                        )
                        i.set_window_close()
        #
        gui_qt_core.GuiQtUtil.show_qt_window(self._qt_widget, pos, size)

    def set_close_method(self, method):
        self._close_methods.append(method)

    def connect_window_close_to(self, method):
        self._close_methods.append(method)

    def set_window_close(self):
        for i in self._close_methods:
            i()
        #
        self._qt_widget.close()
        self._qt_widget.deleteLater()

    def close_window_later(self, delay_time=1000):
        self._qt_widget.hide()
        self._qt_widget._close_later_(delay_time)

    def set_window_title(self, *args):
        text = args[0]
        self._window_title = text
        self._qt_widget.setWindowTitle(text)
        self._qt_widget._set_icon_name_text_(text)

    def get_window_title(self):
        return self._window_title

    def set_window_icon_name_text(self, text):
        self.widget._set_icon_name_text_(text)

    def set_window_icon_by_name(self, icon_name):
        self.widget._set_icon_name_(icon_name)

    def set_window_system_tray_icon(self, widget):
        self.widget._set_window_system_tray_icon_(widget)

    def set_status(self, status):
        self._status = status

    def connect_refresh_action_for(self, fnc):
        self._qt_widget._create_window_shortcut_action_for_(
            fnc, 'F5'
        )

    def create_window_action_for(self, fnc, hotkey):
        self._qt_widget._create_window_shortcut_action_for_(
            fnc, hotkey
        )

    def create_widget_action_for(self, fnc, hotkey):
        self._qt_widget._create_widget_shortcut_action_for_(
            fnc, hotkey
        )

    def connect_window_activate_changed_to(self, fnc):
        self._qt_widget.window_activate_changed.connect(fnc)

    def get_is_active_window(self):
        return self._qt_widget.isActiveWindow()


class AbsPrxLayerBaseDef(object):
    PRX_LAYER_CLS = None
    QT_LAYER_STACK_CLS = None

    def _init_layer_base_def_(self, layout):
        self._qt_layer_unit_layout = layout
        self._qt_layer_stack = self.QT_LAYER_STACK_CLS()
        self._qt_layer_unit_layout.addWidget(self._qt_layer_stack)

        self._layer_keys = []
        self._layer_dict = {}

    def create_layer(self, key):
        layer = self.PRX_LAYER_CLS()
        layer._qt_widget.hide()
        # self._qt_layer_unit_layout.addWidget(layer._qt_widget)
        self._qt_layer_stack._add_widget_(layer._qt_widget)
        self._layer_keys.append(key)
        self._layer_dict[key] = layer
        return layer

    def get_layer(self, key):
        return self._layer_dict[key]

    def get_layer_widget(self, key):
        return self.get_layer(key).get_widget()

    def get_layer_layout(self, key):
        return self.get_layer_widget(key).get_layout()

    def switch_current_layer_to(self, key):
        if key in self._layer_dict:
            self._qt_layer_stack._switch_current_widget_to_(
                self._layer_dict[key]._qt_widget
            )

    def set_current_layer(self, key):
        if key in self._layer_dict:
            self._qt_layer_stack._set_current_widget_(
                self._layer_dict[key]._qt_widget
            )

    def get_current_layer_key(self):
        current_index = self._qt_layer_stack._get_current_index_() or 0
        return self._layer_keys[current_index]

    def show_next_layer(self):
        pass


class AbsPrxProgressingDef(object):
    QT_PROGRESSING_CHART_CLS = None
    GUI_PROGRESS_MODEL_CLS = gui_prx_core.GuiPrxModForProgress
    PROGRESS_WIDGET_CLS = None

    @property
    def widget(self):
        raise NotImplementedError()

    def _set_progressing_def_init_(self):
        self._qt_progressing_char = self.QT_PROGRESSING_CHART_CLS(self.widget)
        self._qt_progressing_char.hide()

        self.widget._set_size_changed_connect_to_(self._refresh_progressing_draw_)

        self._current_progress = None

    def _refresh_progressing_draw_(self):
        x, y = 0, 0
        w, h = self.widget.width(), self.widget.height()
        self._qt_progressing_char.setGeometry(
            x, y, w, h
        )
        self._qt_progressing_char._refresh_widget_draw_()

    def set_progress_create(self, maximum, label=None):
        g_p = self.GUI_PROGRESS_MODEL_CLS(
            proxy=self,
            qt_progress=self._qt_progressing_char,
            maximum=maximum,
            label=label
        )
        if self._current_progress is None:
            self._current_progress = g_p
        else:
            if self._current_progress.get_is_stop() is True:
                self._current_progress = g_p
            else:
                self._current_progress.add_child(g_p)
        return g_p

    @contextmanager
    def gui_progressing(self, maximum, label=None):
        g_p = self.set_progress_create(maximum, label)
        yield g_p
        g_p.set_stop()


class AbsPrxMenuDef(object):
    def _set_prx_menu_def_init_(self):
        pass

    @property
    def widget(self):
        raise NotImplementedError()

    def set_menu_title(self, text):
        self.widget._set_menu_title_text_(text)

    def set_menu_data(self, raw):
        self.widget._set_menu_data_(raw)

    def set_menu_raw_add(self, raw):
        self.widget._add_menu_data_(raw)

    def set_menu_raw_extend(self, raw):
        self.widget._extend_menu_data_(raw)

    def get_menu_raw(self):
        return self.widget._get_menu_data_()

    def set_menu_content(self, content):
        self.widget._set_menu_content_(content)

    def set_menu_content_generate_fnc(self, fnc):
        self.widget._set_menu_content_generate_fnc_(fnc)


class AbsPrxItemFilterTgtDef(object):
    @property
    def item(self):
        raise NotImplementedError()

    def set_tag_filter_tgt_mode(self, *args, **kwargs):
        self.item._set_item_tag_filter_mode_(*args, **kwargs)

    def get_tag_filter_tgt_mode(self):
        return self.item._get_item_tag_filter_mode_()

    def set_tag_filter_tgt_key_add(self, *args, **kwargs):
        self.item._add_item_tag_filter_key_tgt_(*args, **kwargs)

    def get_tag_filter_tgt_keys(self):
        return self.item._get_item_tag_filter_keys_tgt_()

    def set_tag_filter_tgt_statistic_enable(self, *args, **kwargs):
        self.item._set_item_tag_filter_tgt_statistic_enable_(*args, **kwargs)

    def get_tag_filter_tgt_statistic_enable(self):
        return self.item._get_item_tag_filter_tgt_statistic_enable_()

    def get_states(self):
        return self.item._get_state_()

    def set_keyword_filter_keys_tgt(self, keys):
        self.item._set_item_keyword_filter_keys_tgt_(keys)

    def update_keyword_filter_keys_tgt(self, keys):
        self.item._update_item_keyword_filter_keys_tgt_(keys)

    def get_keyword_filter_keys_tgt(self):
        return self.item._get_keyword_filter_keys_tgt_()


class AbsPrxViewFilterTagDef(object):
    @property
    def view(self):
        raise NotImplementedError()

    @property
    def filter_bar(self):
        raise NotImplementedError()

    def get_tag_filter_tgt_statistic_raw(self):
        return self.view._get_view_tag_filter_tgt_statistic_raw_()

    def set_tag_filter_all_keys_src(self, *args, **kwargs):
        self.view._set_view_tag_filter_data_src_(*args, **kwargs)
        self.refresh_items_visible_by_any_filter()
        self.view._refresh_view_all_items_viewport_showable_()

    def get_item_states(self, items):
        return self.view._get_view_item_states_(items)

    def get_item_state_colors(self, items):
        return self.view._get_view_item_state_colors_(items)

    def refresh_items_visible_by_any_filter(self):
        self.view._set_view_keyword_filter_data_src_(self.filter_bar.get_keywords())
        self.view._refresh_view_items_visible_by_any_filter_()


class AbsPrxItemVisibleConnectionDef(object):
    @property
    def item(self):
        raise NotImplementedError()

    def set_visible_connect_to(self, key, prx_item_tgt):
        self.item._set_item_visible_connect_to_(key, prx_item_tgt.item)

    def set_visible_src_key(self, key):
        self.item._set_item_visible_src_key_(key)

    def get_visible_src_key(self):
        return self.item._get_item_visible_src_key_()

    def set_visible_tgt_key(self, key):
        self.item._set_item_visible_tgt_key_(key)

    def get_visible_tgt_key(self):
        return self.item._get_item_visible_tgt_key_()

    def set_visible_tgt_view(self, prx_view):
        self.item._set_item_visible_tgt_view_(prx_view.view)

    def get_visible_tgt_view(self):
        return self.item._get_item_visible_tgt_view_()

    def set_visible_connection_refresh(self):
        self.item._set_item_visible_connection_refresh_()


class AbsPrxViewVisibleConnectionDef(object):
    @property
    def view(self):
        raise NotImplementedError()

    def set_visible_tgt_raw(self, raw):
        self.view._set_view_visible_tgt_raw_(raw)

    def get_visible_tgt_raw(self):
        return self.view._get_view_visible_tgt_raw_()

    def set_visible_tgt_raw_clear(self):
        self.view._set_view_visible_tgt_raw_clear_()

    def set_visible_tgt_raw_update(self):
        self.view._set_view_visible_tgt_raw_update_()
