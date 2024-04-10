# coding:utf-8
import six

import os

import functools

import types

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# gui
from ... import core as gui_core
# qt
from ...qt import core as gui_qt_core
# qt widgets
from ...qt.widgets import base as gui_qt_wgt_base

from ...qt.widgets import utility as gui_qt_wgt_utility

from ...qt.widgets import button as gui_qt_wgt_button

from ...qt.widgets import input as gui_qt_wgt_input

from ...qt.widgets import input_for_storage as gui_qt_wgt_input_for_storage
# proxy abstracts
from .. import abstracts as gui_prx_abstracts
# proxy widgets
from . import utility as gui_prx_wdt_utility

from . import port_base as gui_prx_wgt_port_base

from . import view_for_tree as gui_prx_wgt_view_for_tree


# entry
class _AbsPrxInput(gui_prx_abstracts.AbsPrxWidget):
    QT_INPUT_WIDGET_CLS = None

    def __init__(self, *args, **kwargs):
        super(_AbsPrxInput, self).__init__(*args, **kwargs)
        self.widget.setFixedHeight(
            gui_prx_wgt_port_base.AttrConfig.PRX_PORT_HEIGHT
        )

    def _gui_build_(self):
        self._qt_layout = gui_qt_wgt_base.QtHBoxLayout(self._qt_widget)
        self._qt_layout.setContentsMargins(0, 0, 0, 0)
        self._qt_layout.setSpacing(2)
        #
        self._qt_input_widget = self.QT_INPUT_WIDGET_CLS()
        self._qt_layout.addWidget(self._qt_input_widget)
        #
        self._use_as_storage = False

    def get_input_widget(self):
        return self._qt_input_widget

    def add_button(self, widget):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            self._qt_layout.addWidget(widget)
        else:
            self._qt_layout.addWidget(widget.widget)

    def get(self):
        raise NotImplementedError()

    def set(self, *args, **kwargs):
        raise NotImplementedError()

    def set_option(self, *args, **kwargs):
        pass

    def set_default(self, *args, **kwargs):
        pass

    def get_default(self):
        pass

    def get_is_default(self):
        return False

    def set_clear(self):
        pass

    def connect_input_changed_to(self, fnc):
        pass

    def connect_user_input_changed_to(self, fnc):
        pass

    def connect_tab_pressed_to(self, fnc):
        pass

    def set_focus_in(self):
        pass

    def set_use_as_storage(self, boolean=True):
        if hasattr(self._qt_input_widget, '_set_entry_use_as_storage_'):
            self._qt_input_widget._set_entry_use_as_storage_(boolean)

    def _set_file_show_(self):
        bsc_storage.StgFileOpt(self.get()).open_in_system()

    def get_use_as_storage(self):
        return self._use_as_storage

    def set_locked(self, boolean):
        pass

    def set_history_key(self, key):
        self._qt_input_widget._set_history_key_(key)

    def pull_history_latest(self):
        return self._qt_input_widget._pull_history_latest_()

    def set_tool_tip(self, *args, **kwargs):
        if hasattr(self._qt_input_widget, '_set_tool_tip_'):
            self._qt_input_widget._set_tool_tip_(args[0], **kwargs)

    def set_height(self, h):
        self._qt_widget.setFixedHeight(h)

    def set_history_button_visible(self, boolean):
        pass


# storage
class PrxInputAsStorage(_AbsPrxInput):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = gui_qt_wgt_input_for_storage.QtInputAsStorage

    def __init__(self, *args, **kwargs):
        super(PrxInputAsStorage, self).__init__(*args, **kwargs)
        self.set_history_key(
            'gui.storage'
        )

    def set_ext_filter(self, text):
        self._qt_input_widget._set_ext_filter_(text)

    def get_ext_filter(self):
        return self._qt_input_widget._get_ext_filter_()

    def set_ext_includes(self, texts):
        self._qt_input_widget._set_ext_includes_(texts)

    def set_history_key(self, key):
        self._qt_input_widget._set_history_key_(key)

    def get_history_key(self):
        return self._qt_input_widget._get_history_key_()

    def get(self):
        return self._qt_input_widget._get_value_()

    def set(self, raw=None, **kwargs):
        self._qt_input_widget._set_value_(raw)

    def set_default(self, raw, **kwargs):
        self._qt_input_widget._set_value_default_(raw)

    def get_is_default(self):
        return self._qt_input_widget._get_value_is_default_()

    def connect_input_changed_to(self, fnc):
        self._qt_input_widget._connect_input_entry_value_changed_to_(fnc)

    def set_locked(self, boolean):
        self._qt_input_widget._set_entry_enable_(
            not boolean
        )

    def _value_validation_fnc_(self, history):
        return True


#   file open
class PrxInputAsFileOpen(PrxInputAsStorage):
    def __init__(self, *args, **kwargs):
        super(PrxInputAsFileOpen, self).__init__(*args, **kwargs)
        self._qt_input_widget._set_storage_scheme_(
            self._qt_input_widget.StorageScheme.FileOpen
        )
        self.set_history_key('gui.file-open')

    def _value_validation_fnc_(self, path):
        return os.path.isfile(path)


#   file save
class PrxInputAsFileSave(PrxInputAsStorage):
    def __init__(self, *args, **kwargs):
        super(PrxInputAsFileSave, self).__init__(*args, **kwargs)
        self._qt_input_widget._set_storage_scheme_(
            self._qt_input_widget.StorageScheme.FileSave
        )
        self.set_history_key('gui.file-save')

    def _value_validation_fnc_(self, path):
        return os.path.isfile(path)


#   directory open
class PrxInputAsDirectoryOpen(PrxInputAsStorage):
    def __init__(self, *args, **kwargs):
        super(PrxInputAsDirectoryOpen, self).__init__(*args, **kwargs)
        self._qt_input_widget._set_storage_scheme_(
            self._qt_input_widget.StorageScheme.DirectoryOpen
        )
        self.set_history_key('gui.directory-open')

    def _value_validation_fnc_(self, path):
        return os.path.isdir(path)


#   directory open
class PrxInputAsDirectorySave(PrxInputAsStorage):
    def __init__(self, *args, **kwargs):
        super(PrxInputAsDirectorySave, self).__init__(*args, **kwargs)
        self._qt_input_widget._set_storage_scheme_(
            self._qt_input_widget.StorageScheme.DirectorySave
        )
        self.set_history_key('gui.directory-save')

    def _value_validation_fnc_(self, path):
        return os.path.isdir(path)


# storage array
class PrxInputAsStorageArray(_AbsPrxInput):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = gui_qt_wgt_input.QtInputAsList

    def __init__(self, *args, **kwargs):
        super(PrxInputAsStorageArray, self).__init__(*args, **kwargs)
        self._history_key = None
        # drop
        self._qt_input_widget._set_input_entry_drop_enable_(True)
        # entry
        self._qt_input_widget._set_entry_enable_(True)
        self._qt_input_widget._set_resize_enable_(True)
        self._qt_input_widget._get_resize_handle_()._set_resize_target_(self._qt_widget)
        self._qt_input_widget._get_resize_handle_()._set_resize_minimum_(42)
        self._qt_input_widget._set_size_policy_height_fixed_mode_()
        self._qt_input_widget._get_entry_widget_()._set_entry_use_as_storage_(True)
        self._qt_input_widget._get_entry_widget_()._set_value_validation_fnc_(self._value_validation_fnc_)
        self._qt_input_widget._get_entry_widget_().entry_value_added.connect(self.update_history)
        self._qt_input_widget._get_choose_popup_widget_()._set_popup_auto_resize_enable_(True)
        self._qt_input_widget._set_value_choose_button_icon_file_path_(
            gui_core.GuiIcon.get('history')
        )
        self._qt_input_widget._set_choose_button_state_icon_file_path_(
            gui_core.GuiIcon.get('state/popup')
        )
        self._qt_input_widget._set_value_choose_button_name_text_('choose history')

        self.widget.setFixedHeight(gui_prx_wgt_port_base.AttrConfig.PRX_PORT_HEIGHT_2)

        self._ext_filter = 'All File (*.*)'

        self._ext_includes = []

        self._open_button = gui_prx_wdt_utility.PrxIconPressButton()
        self._qt_input_widget._add_input_button_(self._open_button.widget)
        self._open_button.connect_press_clicked_to(self.open_with_dialog_fnc)
        self._open_button.set_name('open file')
        self._open_button.set_icon_name('file/file')
        self._open_button.set_icon_frame_size(18, 18)
        self._open_button.set_tool_tip(
            [
                '"LMB-click" to open file by "dialog"'
            ]
        )

    def open_with_dialog_fnc(self):
        raise NotImplementedError()

    def set_ext_filter(self, ext_filter):
        self._ext_filter = ext_filter
        self._qt_input_widget._get_entry_widget_()._set_empty_sub_text_(
            self._ext_filter
        )

    def set_ext_includes(self, texts):
        self._ext_includes = texts
        self.set_ext_filter(
            'All File ({})'.format(' '.join(map(lambda x: '*{}'.format(x), texts)))
        )

    def append(self, value):
        self._qt_input_widget._append_value_(
            value
        )

    def extend(self, values):
        self._qt_input_widget._extend_values_(
            values
        )

    def set(self, raw=None, **kwargs):
        self._qt_input_widget._set_values_(
            raw
        )

    def get(self):
        return self._qt_input_widget._get_values_()

    def set_history_key(self, key):
        self._history_key = key
        self.update_history()

    def _value_validation_fnc_(self, value):
        return True

    def update_history(self):
        if self._history_key is not None:
            values = self._qt_input_widget._get_values_()
            if values:
                value = values[-1]
                if value:
                    if self._value_validation_fnc_(value) is True:
                        gui_core.GuiHistory.append(
                            self._history_key,
                            value
                        )
            #
            histories = gui_core.GuiHistory.get_all(
                self._history_key
            )
            if histories:
                histories.reverse()
            #
            histories = [i for i in histories if self._value_validation_fnc_(i) is True]
            #
            self._qt_input_widget._set_choose_values_(
                histories
            )

    def pull_history_latest(self):
        if self._history_key is not None:
            _ = gui_core.GuiHistory.get_latest(self._history_key)
            if _:
                self._qt_input_widget._append_value_(_)

    def set_history_button_visible(self, boolean):
        pass


#   many directories open
# noinspection PyUnusedLocal
class PrxInputAsDirectoriesOpen(PrxInputAsStorageArray):
    def __init__(self, *args, **kwargs):
        super(PrxInputAsDirectoriesOpen, self).__init__(*args, **kwargs)
        self._open_button.set_name('open directory')
        self._open_button.set_icon_name('file/folder')
        self._open_button.set_tool_tip(
            [
                '"LMB-click" to open directory by "dialog"'
            ]
        )
        self._qt_input_widget._set_choose_popup_item_icon_file_path_(
            gui_core.GuiIcon.get('file/folder')
        )
        self._qt_input_widget._set_entry_item_icon_file_path_(
            gui_core.GuiIcon.get('file/folder')
        )
        self.set_history_key('gui.directories-open')

    def set_locked(self, boolean):
        self._qt_input_widget._set_entry_enable_(not boolean)
        self._qt_input_widget._set_input_entry_drop_enable_(not boolean)
        self._qt_input_widget._set_input_choose_enable_(not boolean)
        self._open_button.widget._set_action_enable_(not boolean)

    def set_history_button_visible(self, boolean):
        self._qt_input_widget._set_input_choose_visible_(boolean)

    def open_with_dialog_fnc(self):
        f = gui_qt_core.QtWidgets.QFileDialog()
        options = f.Options()
        # options |= f.DontUseNativeDialog
        s = f.getExistingDirectory(
            self.widget,
            'Open Directory',
            self.get()[-1] if self.get() else '',
        )
        if s:
            self.append(s)
            self.update_history()

    def _value_validation_fnc_(self, value):
        if value:
            return os.path.isdir(value)
        return False

    def set(self, *args, **kwargs):
        self._qt_input_widget._clear_all_values_()
        self._qt_input_widget._set_values_(args[0])


#   many files open
class PrxInputAsFilesOpen(PrxInputAsStorageArray):
    def __init__(self, *args, **kwargs):
        super(PrxInputAsFilesOpen, self).__init__(*args, **kwargs)
        self._ext_filter = 'All File (*.*)'
        #
        self._open_button.set_name('open file')
        self._open_button.set_icon_name('file/file')
        self._open_button.set_tool_tip(
            [
                '"LMB-click" to open file by "dialog"'
            ]
        )
        self._qt_input_widget._set_choose_popup_item_icon_file_path_(
            gui_core.GuiIcon.get('file/file')
        )
        self._qt_input_widget._set_entry_item_icon_file_path_(
            gui_core.GuiIcon.get('file/file')
        )
        self._qt_input_widget._get_entry_widget_()._set_entry_use_as_file_(True)
        self._qt_input_widget._get_entry_widget_()._set_entry_use_as_file_multiply_(True)

    def open_with_dialog_fnc(self):
        f = gui_qt_core.QtWidgets.QFileDialog()
        # options |= f.DontUseNativeDialog
        s = f.getOpenFileNames(
            self.widget,
            'Open Files',
            self.get()[-1] if self.get() else '',
            filter=self._ext_filter
        )
        if s:
            # s = files, filter
            values = s[0]
            if values:
                values = bsc_storage.StgFileMtdForMultiply.merge_to(
                    values,
                    ['*.<udim>.####.*', '*.####.*']
                )
                self.extend(values)
                self.update_history()

    def _value_validation_fnc_(self, value):
        if value:
            if self._ext_includes:
                ext = os.path.splitext(value)[-1]
                if ext not in self._ext_includes:
                    return False
            return bsc_storage.StgFileMtdForMultiply.get_is_exists(value)
        return False


#   many medias open
class PrxInputAsMediasOpen(PrxInputAsFilesOpen):
    def __init__(self, *args, **kwargs):
        super(PrxInputAsMediasOpen, self).__init__(*args, **kwargs)
        self._create_button = gui_prx_wdt_utility.PrxIconPressButton()
        self._qt_input_widget._add_input_button_(self._create_button.widget)
        self._create_button.connect_press_clicked_to(self.__dot_screenshot_create)
        self._create_button.set_name('create file')
        self._create_button.set_icon_name('camera')
        self._create_button.set_icon_sub_name('action/add')
        self._create_button.set_icon_frame_size(18, 18)
        self._create_button.set_tool_tip(
            [
                '"LMB-click" create file by "screenshot"'
            ]
        )

    @staticmethod
    def __get_screenshot_temporary_file_path():
        d = bsc_core.SysBaseMtd.get_home_directory()
        return six.u('{}/screenshot/untitled-{}.jpg').format(d, bsc_core.TimeExtraMtd.generate_time_tag_36())

    def __do_screenshot_save(self, g):
        f = self.__get_screenshot_temporary_file_path()
        gui_prx_wdt_utility.PrxScreenshotFrame.save_to(
            g, f
        )
        self.append(f)
        self.update_history()

    def __dot_screenshot_create(self):
        active_window = gui_qt_core.GuiQtUtil.get_qt_active_window()
        w = gui_prx_wdt_utility.PrxScreenshotFrame()
        w.set_started_connect_to(active_window.hide)
        w.set_start()
        w.set_accepted_connect_to(self.__do_screenshot_save)
        w.set_finished_connect_to(active_window.show)


# any array
class PrxInputAsArray(_AbsPrxInput):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = gui_qt_wgt_input.QtInputAsList

    def __init__(self, *args, **kwargs):
        super(PrxInputAsArray, self).__init__(*args, **kwargs)
        self._history_key = 'gui.values'
        #
        self._qt_input_widget._set_entry_enable_(True)
        self._qt_input_widget._get_resize_handle_()._set_resize_target_(self.widget)
        self._qt_input_widget._set_resize_enable_(True)
        self._qt_input_widget._get_resize_handle_()._set_resize_minimum_(42)
        self._qt_input_widget._set_size_policy_height_fixed_mode_()
        self._qt_input_widget._set_value_choose_button_icon_file_path_(
            gui_core.GuiIcon.get('attribute')
        )

        self.widget.setFixedHeight(gui_prx_wgt_port_base.AttrConfig.PRX_PORT_HEIGHT_2)

        self._add_button = gui_prx_wdt_utility.PrxIconPressButton()
        self._qt_input_widget._add_input_button_(self._add_button.widget)
        self._add_button.connect_press_clicked_to(self._set_add_)
        self._add_button.set_name('add')
        self._add_button.set_icon_name('add')
        self._add_button.set_icon_frame_size(18, 18)
        self._add_button.set_tool_tip(
            [
                '"LMB-click" add a value'
            ]
        )

    def _set_add_(self):
        pass

    def get(self):
        return self._qt_input_widget._get_values_()

    def set(self, raw=None, **kwargs):
        pass

    def append(self, value):
        self._qt_input_widget._append_value_(
            value
        )


# any array choose
# noinspection PyUnusedLocal
class PrxInputAsArrayWithChoose(_AbsPrxInput):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = gui_qt_wgt_input.QtInputAsListWithChoose

    def __init__(self, *args, **kwargs):
        super(PrxInputAsArrayWithChoose, self).__init__(*args, **kwargs)
        self._history_key = 'gui.values_choose'
        #
        self._qt_input_widget._set_entry_enable_(True)
        self._qt_input_widget._get_resize_handle_()._set_resize_target_(self.widget)
        self._qt_input_widget._set_resize_enable_(True)
        self._qt_input_widget._get_resize_handle_()._set_resize_minimum_(42)
        self._qt_input_widget._set_size_policy_height_fixed_mode_()
        self._qt_input_widget._set_value_choose_button_icon_file_path_(
            gui_core.GuiIcon.get('attribute')
        )

        self.widget.setFixedHeight(gui_prx_wgt_port_base.AttrConfig.PRX_PORT_HEIGHT_2)

    def _set_add_(self):
        pass

    def get(self):
        pass

    def set(self, *args, **kwargs):
        pass

    def set_choose_values(self, *args, **kwargs):
        self._qt_input_widget._clear_choose_values_()
        self._qt_input_widget._restore_choose_popup_()
        self._qt_input_widget._set_choose_values_(args[0])

    def append(self, value):
        pass


#   entity
class PrxInputAsShotgunEntityWithChoose(_AbsPrxInput):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = gui_qt_wgt_input.QtInputAsConstantWithChoose

    def __init__(self, *args, **kwargs):
        super(PrxInputAsShotgunEntityWithChoose, self).__init__(*args, **kwargs)
        self._shotgun_entity_kwargs = {}
        # entry
        self._qt_input_widget._set_entry_enable_(True)
        # choose
        self._qt_input_widget._set_choose_popup_auto_resize_enable_(False)
        self._qt_input_widget._set_choose_index_show_enable_(True)
        self._qt_input_widget._set_choose_popup_tag_filter_enable_(True)
        self._qt_input_widget._set_choose_popup_keyword_filter_enable_(True)
        self._qt_input_widget._set_choose_popup_item_size_(40, 40)
        self._qt_input_widget._set_value_choose_button_icon_file_path_(
            gui_core.GuiIcon.get('application/shotgrid')
        )
        self._qt_input_widget._set_choose_button_state_icon_file_path_(
            gui_core.GuiIcon.get('state/popup')
        )

        self._data = []

        self._stg_entity_dict = {}

    def get(self):
        return self._qt_input_widget._get_value_()

    def set(self, *args, **kwargs):
        self._qt_input_widget._set_value_(args[0])

    def get_stg_entity(self):
        _ = self.get()
        if _ in self._stg_entity_dict:
            return self._stg_entity_dict[self.get()]

    def set_clear(self):
        self._stg_entity_dict = {}
        self._qt_input_widget._clear_input_()

    def set_shotgun_entity_kwargs(
        self,
        shotgun_entity_kwargs,
        name_field=None,
        image_field=None,
        keyword_filter_fields=None,
        tag_filter_fields=None
    ):
        def post_fnc_():
            pass

        def cache_fnc_():
            import lxbasic.shotgun as bsc_shotgun
            return [
                bsc_shotgun.StgConnector.generate_stg_gui_args(
                    shotgun_entity_kwargs, name_field, image_field, keyword_filter_fields, tag_filter_fields
                )
            ]

        def build_fnc_(data_):
            self._stg_entity_dict, names, image_url_dict, keyword_filter_dict, tag_filter_dict = data_[0]
            #
            self._qt_input_widget._set_choose_values_(names)
            # for popup
            #   image
            self._qt_input_widget._set_choose_popup_item_image_url_dict_(image_url_dict)
            #   filter
            self._qt_input_widget._set_choose_popup_item_keyword_filter_dict_(keyword_filter_dict)
            self._qt_input_widget._set_choose_popup_item_tag_filter_dict_(tag_filter_dict)

        self._qt_input_widget._run_build_use_thread_(
            cache_fnc_, build_fnc_, post_fnc_
        )

    def connect_input_changed_to(self, fnc):
        # clear
        self._qt_input_widget.user_input_value_cleared.connect(
            fnc
        )
        # completion
        self._qt_input_widget.user_input_completion_finished.connect(
            fnc
        )
        # choose
        self._qt_input_widget.user_input_choose_changed.connect(
            fnc
        )

    def connect_tab_pressed_to(self, fnc):
        self._qt_input_widget.user_key_tab_pressed.connect(fnc)
        return True

    def set_focus_in(self):
        self._qt_input_widget._set_input_entry_focus_in_()

    def run_as_thread(self, cache_fnc, build_fnc, post_fnc):
        self._qt_input_widget._run_build_use_thread_(
            cache_fnc, build_fnc, post_fnc
        )


#   entities
class PrxInputAsShotgunEntitiesWithChoose(_AbsPrxInput):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = gui_qt_wgt_input.QtInputAsList

    def __init__(self, *args, **kwargs):
        super(PrxInputAsShotgunEntitiesWithChoose, self).__init__(*args, **kwargs)
        self._shotgun_entity_kwargs = {}
        # entry
        self._qt_input_widget._get_entry_widget_()._set_grid_size_(80, 20)
        self._qt_input_widget._get_entry_widget_()._set_grid_mode_()
        self._qt_input_widget._set_entry_enable_(True)
        # resize
        self._qt_input_widget._set_resize_enable_(True)
        self._qt_input_widget._get_resize_handle_()._set_resize_target_(self.widget)
        self._qt_input_widget._get_resize_handle_()._set_resize_minimum_(42)
        self._qt_input_widget._set_size_policy_height_fixed_mode_()
        #
        self._qt_input_widget._set_choose_popup_auto_resize_enable_(False)
        self._qt_input_widget._set_choose_popup_tag_filter_enable_(True)
        self._qt_input_widget._set_choose_popup_keyword_filter_enable_(True)
        self._qt_input_widget._set_choose_popup_item_size_(40, 40)
        self._qt_input_widget._set_value_choose_button_icon_file_path_(
            gui_core.GuiIcon.get('application/shotgrid')
        )
        self._qt_input_widget._set_choose_button_state_icon_file_path_(
            gui_core.GuiIcon.get('state/popup')
        )
        #
        self.widget.setFixedHeight(gui_prx_wgt_port_base.AttrConfig.PRX_PORT_HEIGHT_2)
        #
        self._data = []

        self._stg_entity_dict = {}

    def get(self):
        return self._qt_input_widget._get_values_()

    def set(self, *args, **kwargs):
        self._qt_input_widget._set_values_(args[0])

    def append(self, value):
        self._qt_input_widget._append_value_(
            value
        )

    def set_clear(self):
        self._qt_input_widget._set_clear_()

    def set_shotgun_entity_kwargs(
        self,
        shotgun_entity_kwargs,
        name_field=None,
        image_field=None,
        keyword_filter_fields=None,
        tag_filter_fields=None
    ):
        def post_fnc_():
            pass

        def cache_fnc_():
            import lxbasic.shotgun as bsc_shotgun
            return [
                bsc_shotgun.StgConnector.generate_stg_gui_args(
                    shotgun_entity_kwargs, name_field, image_field, keyword_filter_fields, tag_filter_fields
                )
            ]

        def build_fnc_(data_):
            self._stg_entity_dict, names, image_url_dict, keyword_filter_dict, tag_filter_dict = data_[0]
            # for popup
            self._qt_input_widget._set_choose_values_(names)
            #   image
            self._qt_input_widget._set_choose_popup_item_image_url_dict_(image_url_dict)
            #   filter
            self._qt_input_widget._set_choose_popup_item_keyword_filter_dict_(keyword_filter_dict)
            self._qt_input_widget._set_choose_popup_item_tag_filter_dict_(tag_filter_dict)

        self._qt_input_widget._run_build_use_thread_(
            cache_fnc_, build_fnc_, post_fnc_
        )

    def run_as_thread(self, cache_fnc, build_fnc, post_fnc):
        self._qt_input_widget._run_build_use_thread_(
            cache_fnc, build_fnc, post_fnc
        )


class PrxInputAsRsvProject(_AbsPrxInput):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = gui_qt_wgt_input.QtInputAsConstantWithChoose
    #
    HISTORY_KEY = 'gui.projects'

    def __init__(self, *args, **kwargs):
        super(PrxInputAsRsvProject, self).__init__(*args, **kwargs)
        #
        self._qt_input_widget._set_entry_enable_(True)
        #
        self.update_history()
        #
        self._qt_input_widget._connect_input_user_entry_value_finished_to_(self.update_history)
        self._qt_input_widget.user_input_choose_changed.connect(self.update_history)

    def get(self):
        return self._qt_input_widget._get_value_()

    def set(self, raw=None, **kwargs):
        self._qt_input_widget._set_value_(raw)

    def set_default(self, raw, **kwargs):
        self._qt_input_widget._set_value_default_(raw)

    def get_is_default(self):
        return self._qt_input_widget._get_value_is_default_()

    def connect_input_changed_to(self, fnc):
        self._qt_input_widget._connect_input_entry_value_changed_to_(fnc)

    #
    def update_history(self):
        project = self._qt_input_widget._get_value_()
        if project:
            import lxresolver.core as rsv_core

            resolver = rsv_core.RsvBase.generate_root()
            #
            rsv_project = resolver.get_rsv_project(project=project)
            project_directory_path = rsv_project.get_directory_path()
            work_directory_path = '{}/work'.format(project_directory_path)
            if bsc_storage.StgPathOpt(work_directory_path).get_is_exists() is True:
                gui_core.GuiHistory.append(
                    self.HISTORY_KEY,
                    project
                )
        #
        histories = gui_core.GuiHistory.get_all(
            self.HISTORY_KEY
        )
        if histories:
            histories = [i for i in histories if i]
            histories.reverse()
            #
            self._qt_input_widget._set_choose_values_(
                histories
            )

    def pull_history_latest(self):
        _ = gui_core.GuiHistory.get_latest(self.HISTORY_KEY)
        if _:
            self._qt_input_widget._set_value_(_)

    def get_histories(self):
        return gui_core.GuiHistory.get_all(
            self.HISTORY_KEY
        )


class PrxInputAsSchemeWithChoose(_AbsPrxInput):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = gui_qt_wgt_input.QtInputAsConstantWithChoose
    #
    HISTORY_KEY = 'gui.schemes'

    def __init__(self, *args, **kwargs):
        super(PrxInputAsSchemeWithChoose, self).__init__(*args, **kwargs)
        #
        self._qt_input_widget._set_entry_enable_(True)
        #
        self._scheme_key = None
        #
        self.update_history()
        #
        self._qt_input_widget._connect_input_user_entry_value_finished_to_(self.update_history)
        self._qt_input_widget.user_input_choose_changed.connect(self.update_history)

    def get(self):
        return self._qt_input_widget._get_value_()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (tuple, list)):
            self.set_history_add(raw[0])
            self.update_history()
            self.pull_history_latest()

    def set_default(self, raw, **kwargs):
        self._qt_input_widget._set_value_default_(raw)

    def get_is_default(self):
        return self._qt_input_widget._get_value_is_default_()

    def set_scheme_key(self, key):
        self._scheme_key = key

    def connect_input_changed_to(self, fnc):
        self._qt_input_widget._connect_input_entry_value_changed_to_(fnc)

    #
    def get_histories(self):
        if self._scheme_key is not None:
            return gui_core.GuiHistory.get_all(
                self._scheme_key
            )
        return []

    def set_history_add(self, scheme):
        if self._scheme_key is not None:
            gui_core.GuiHistory.append(
                self._scheme_key,
                scheme
            )

    #
    def update_history(self):
        if self._scheme_key is not None:
            scheme = self._qt_input_widget._get_value_()
            if scheme:
                gui_core.GuiHistory.append(
                    self._scheme_key,
                    scheme
                )
            #
            histories = gui_core.GuiHistory.get_all(
                self._scheme_key
            )
            if histories:
                histories = [i for i in histories if i]
                histories.reverse()
                #
                self._qt_input_widget._set_choose_values_(
                    histories
                )

    def pull_history_latest(self):
        if self._scheme_key is not None:
            _ = gui_core.GuiHistory.get_latest(self._scheme_key)
            if _:
                self._qt_input_widget._set_value_(_)


# any constant choose, etc. enumerate
class PrxInputAsConstantWithChoose(_AbsPrxInput):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = gui_qt_wgt_input.QtInputAsConstantWithChoose

    def __init__(self, *args, **kwargs):
        super(PrxInputAsConstantWithChoose, self).__init__(*args, **kwargs)
        self.widget.setFocusProxy(self._qt_input_widget)
        self._qt_input_widget._set_entry_enable_(True)
        self._qt_input_widget._set_choose_index_show_enable_(True)

    def get(self):
        return self._qt_input_widget._get_value_()

    def get_enumerate_strings(self):
        return self._qt_input_widget._get_choose_values_()

    def set(self, *args, **kwargs):
        _ = args[0]
        if isinstance(_, (tuple, list)):
            self._qt_input_widget._set_choose_values_(_)
            if _:
                self.set(_[-1])
                self.set_default(_[-1])
            else:
                self.set('')
                self.set_default('')
        elif isinstance(_, six.string_types):
            self._qt_input_widget._set_value_(_)
        elif isinstance(_, (int, float)):
            self._qt_input_widget._set_choose_value_by_index_(int(_))

    def set_option(self, *args, **kwargs):
        self._qt_input_widget._set_choose_values_(args[0])

    def set_icon_file_as_value(self, value, file_path):
        self._qt_input_widget._set_choose_popup_item_icon_file_path_for_(
            value, file_path
        )

    def set_default(self, *args, **kwargs):
        _ = args[0]
        if isinstance(_, six.string_types):
            self._qt_input_widget._set_value_default_(_)
        elif isinstance(_, (int, float)):
            self._qt_input_widget._set_choose_value_default_by_index_(_)

    def get_default(self):
        return self._qt_input_widget._get_value_default_()

    def get_is_default(self):
        return self._qt_input_widget._get_value_is_default_()

    def connect_input_changed_to(self, fnc):
        self._qt_input_widget.input_choose_changed.connect(fnc)

    def set_locked(self, boolean):
        self._qt_input_widget._set_entry_enable_(not boolean)


# icon choose
class PrxInputAsIconWithChoose(_AbsPrxInput):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = gui_qt_wgt_input.QtInputAsIcon

    def __init__(self, *args, **kwargs):
        super(PrxInputAsIconWithChoose, self).__init__(*args, **kwargs)
        self.widget.setFocusProxy(self._qt_input_widget)

    def get(self):
        return self._qt_input_widget._get_value_()

    def set(self, *args, **kwargs):
        _ = args[0]
        if isinstance(_, (tuple, list)):
            self._qt_input_widget._set_choose_values_(_)
            if _:
                self.set(_[-1])
                self.set_default(_[-1])
        elif isinstance(_, six.string_types):
            self._qt_input_widget._set_value_(_)
        elif isinstance(_, (int, float)):
            self._qt_input_widget._set_choose_value_by_index_(int(_))

    def set_default(self, *args, **kwargs):
        _ = args[0]
        if isinstance(_, six.string_types):
            self._qt_input_widget._set_value_default_(_)
        elif isinstance(_, (int, float)):
            self._qt_input_widget._set_choose_value_default_by_index_(_)

    def get_default(self):
        return self._qt_input_widget._get_value_default_()

    def set_locked(self, boolean):
        self._qt_input_widget._set_entry_enable_(not boolean)


# any
class PrxInputAsConstant(_AbsPrxInput):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = gui_qt_wgt_input.QtInputAsConstant

    def __init__(self, *args, **kwargs):
        super(PrxInputAsConstant, self).__init__(*args, **kwargs)
        # self._qt_input_widget.setAlignment(gui_qt_core.QtCore.Qt.AlignLeft | gui_qt_core.QtCore.Qt.AlignVCenter)
        #
        self.widget.setFocusProxy(self._qt_input_widget)

    def set_value_type(self, value_type):
        self._qt_input_widget._set_value_type_(value_type)

    def set_use_as_frames(self):
        self._qt_input_widget._set_value_validator_use_as_frames_()

    def set_use_as_rgba(self):
        self._qt_input_widget._set_value_validator_use_as_rgba_()

    def get(self):
        return self._qt_input_widget._get_value_()

    def set(self, raw=None, **kwargs):
        self._qt_input_widget._set_value_(raw)

    def set_default(self, raw, **kwargs):
        self._qt_input_widget._set_value_default_(raw)

    def get_default(self):
        return self._qt_input_widget._get_value_default_()

    def get_is_default(self):
        return self._qt_input_widget._get_value_is_default_()

    def connect_input_changed_to(self, fnc):
        self._qt_input_widget._connect_input_entry_value_changed_to_(fnc)

    def set_maximum(self, value):
        self._qt_input_widget._set_value_maximum_(value)

    def get_maximum(self):
        return self._qt_input_widget._get_value_maximum_()

    def set_minimum(self, value):
        self._qt_input_widget._set_value_minimum_(value)

    def get_minimum(self):
        return self._qt_input_widget._get_value_minimum_()

    def set_range(self, maximum, minimum):
        self._qt_input_widget._set_value_range_(maximum, minimum)

    def get_range(self):
        return self._qt_input_widget._get_value_range_()

    def set_locked(self, boolean):
        self._qt_input_widget._set_entry_enable_(not boolean)


#   text
class PrxInputAsText(PrxInputAsConstant):
    def __init__(self, *args, **kwargs):
        super(PrxInputAsText, self).__init__(*args, **kwargs)
        self.set_value_type(str)


#   script
class PrxInputAsScript(_AbsPrxInput):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = gui_qt_wgt_input.QtInputAsContent

    def __init__(self, *args, **kwargs):
        super(PrxInputAsScript, self).__init__(*args, **kwargs)
        self.widget.setFixedHeight(gui_prx_wgt_port_base.AttrConfig.PRX_PORT_HEIGHT_2)
        #
        self._qt_input_widget._get_resize_handle_()._set_resize_target_(self.widget)
        self._qt_input_widget._set_resize_enable_(True)
        self._qt_input_widget._set_input_entry_drop_enable_(True)
        self._qt_input_widget._set_item_value_entry_enable_(True)
        self._qt_input_widget._set_size_policy_height_fixed_mode_()

    def get(self):
        return self._qt_input_widget._get_value_()

    def set(self, raw=None, **kwargs):
        self._qt_input_widget._set_value_(raw)

    def set_external_editor_ext(self, ext):
        self._qt_input_widget._set_external_editor_ext_(ext)

    def set_default(self, raw, **kwargs):
        self._qt_input_widget._set_value_default_(raw)

    def get_is_default(self):
        return self._qt_input_widget._get_value_is_default_()

    def set_locked(self, boolean):
        self._qt_input_widget._set_entry_enable_(not boolean)


#   string
class PrxInputAsString(PrxInputAsConstant):
    def __init__(self, *args, **kwargs):
        super(PrxInputAsString, self).__init__(*args, **kwargs)
        self.set_value_type(str)


#   integer
class PrxInputAsInteger(PrxInputAsConstant):
    def __init__(self, *args, **kwargs):
        super(PrxInputAsInteger, self).__init__(*args, **kwargs)
        self.set_value_type(int)


#   boolean as check box
class PrxInputAsBoolean(_AbsPrxInput):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = gui_qt_wgt_button.QtCheckButton

    def __init__(self, *args, **kwargs):
        super(PrxInputAsBoolean, self).__init__(*args, **kwargs)

    def get(self):
        return self._qt_input_widget._get_is_checked_()

    def set(self, raw=None, **kwargs):
        self._qt_input_widget._set_checked_(raw)

    def set_default(self, raw, **kwargs):
        self._qt_input_widget._set_value_default_(raw)

    def get_default(self):
        return self._qt_input_widget._get_value_default_()

    def get_is_default(self):
        return self._qt_input_widget._get_value_is_default_()

    def connect_input_changed_to(self, fnc):
        self._qt_input_widget._set_item_check_changed_connect_to_(fnc)


#   float
class PrxInputAsFloat(PrxInputAsConstant):
    def __init__(self, *args, **kwargs):
        super(PrxInputAsFloat, self).__init__(*args, **kwargs)
        self.set_value_type(float)


#   press button
class PrxInputAsPressButton(_AbsPrxInput):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = gui_qt_wgt_button.QtPressButton

    def __init__(self, *args, **kwargs):
        super(PrxInputAsPressButton, self).__init__(*args, **kwargs)

    def get(self):
        return None

    @gui_core.GuiModifier.run_with_exception_catch
    def __exec_fnc(self, fnc):
        fnc()

    @staticmethod
    @gui_core.GuiModifier.run_with_exception_catch
    def __exec_scp(script):
        exec script

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (types.MethodType, types.FunctionType)):
            self._qt_input_widget.press_clicked.connect(
                functools.partial(self.__exec_fnc, raw)
            )
        elif isinstance(raw, six.string_types):
            self._qt_input_widget.press_clicked.connect(
                functools.partial(self.__exec_scp, raw)
            )

    def set_menu_data(self, raw):
        self._qt_input_widget._set_menu_data_(raw)

    def set_option_enable(self, boolean):
        self._qt_input_widget._set_option_click_enable_(boolean)


#   sub process button
class PrxInputAsSubProcessButton(_AbsPrxInput):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = gui_qt_wgt_button.QtPressButton

    def __init__(self, *args, **kwargs):
        super(PrxInputAsSubProcessButton, self).__init__(*args, **kwargs)
        self._stop_button = gui_prx_wdt_utility.PrxIconPressButton()
        self.add_button(self._stop_button)
        self._stop_button.set_name('Stop Process')
        self._stop_button.set_icon_by_name('Stop Process')
        self._stop_button.set_tool_tip('press to stop process')

    def get(self):
        return None

    @gui_core.GuiModifier.run_with_exception_catch
    def __exec_fnc(self, fnc):
        fnc()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (types.MethodType, types.FunctionType)):
            self._qt_input_widget.press_clicked.connect(
                functools.partial(self.__exec_fnc, raw)
            )

    def set_menu_data(self, raw):
        self._qt_input_widget._set_menu_data_(raw)

    def set_stop(self, raw):
        if isinstance(raw, (types.MethodType, types.FunctionType)):
            self._stop_button.widget.press_clicked.connect(
                functools.partial(self.__exec_fnc, raw)
            )

    def set_stop_connect_to(self, fnc):
        self._stop_button.widget.press_clicked.connect(
            functools.partial(self.__exec_fnc, fnc)
        )


#   validation button
class PrxInputAsValidationButton(_AbsPrxInput):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = gui_qt_wgt_button.QtPressButton

    def __init__(self, *args, **kwargs):
        super(PrxInputAsValidationButton, self).__init__(*args, **kwargs)

    def get(self):
        return None

    @gui_core.GuiModifier.run_with_exception_catch
    def __exec_fnc(self, fnc):
        fnc()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (types.MethodType, types.FunctionType)):
            self._qt_input_widget.press_clicked.connect(
                functools.partial(self.__exec_fnc, raw)
            )

    def set_menu_data(self, raw):
        self._qt_input_widget._set_menu_data_(raw)


#   capsule
class PrxInputAsCapsule(_AbsPrxInput):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = gui_qt_wgt_input.QtInputAsCapsule

    def __init__(self, *args, **kwargs):
        super(PrxInputAsCapsule, self).__init__(*args, **kwargs)

    def get(self):
        return self._qt_input_widget._get_value_()

    def set(self, *args, **kwargs):
        self._qt_input_widget._set_value_(
            args[0]
        )

    def set_locked(self, boolean):
        self._qt_input_widget._set_entry_enable_(not boolean)

    def set_default(self, *args, **kwargs):
        self._qt_input_widget._set_value_default_(
            args[0]
        )

    def get_default(self):
        return self._qt_input_widget._get_value_default_()

    def get_is_default(self):
        return self._qt_input_widget._get_value_is_default_()

    def set_option(self, *args, **kwargs):
        self._qt_input_widget._set_value_options_(
            args[0]
        )

    def connect_input_changed_to(self, fnc):
        self._qt_input_widget.input_value_changed.connect(fnc)


# any2, any3
class PrxInputAsTuple(_AbsPrxInput):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = gui_qt_wgt_input.QtInputAsTuple

    def __init__(self, *args, **kwargs):
        super(PrxInputAsTuple, self).__init__(*args, **kwargs)

    def set_value_type(self, value_type):
        self._qt_input_widget._set_value_type_(value_type)

    def set_value_size(self, size):
        self._qt_input_widget._set_value_size_(size)

    def get(self):
        return self._qt_input_widget._get_value_()

    def set(self, raw=None, **kwargs):
        self._qt_input_widget._set_value_(
            raw
        )

    def set_default(self, raw, **kwargs):
        self._qt_input_widget._set_value_default_(raw)

    def get_is_default(self):
        return self._qt_input_widget._get_value_is_default_()

    def connect_input_changed_to(self, fnc):
        self._qt_input_widget._connect_input_entry_value_changed_to_(fnc)


#   integer2, 3, ...
class PrxInputAsIntegerTuple(PrxInputAsTuple):
    def __init__(self, *args, **kwargs):
        super(PrxInputAsIntegerTuple, self).__init__(*args, **kwargs)
        self._qt_input_widget._build_input_entry_(2, int)


#   float2, 3, ...
class PrxInputAsFloatTuple(PrxInputAsTuple):
    def __init__(self, *args, **kwargs):
        super(PrxInputAsFloatTuple, self).__init__(*args, **kwargs)
        self._qt_input_widget._build_input_entry_(2, float)


#   rgba
class PrxInputAsRgbaChoose(PrxInputAsConstant):
    QT_INPUT_WIDGET_CLS = gui_qt_wgt_input.QtInputAsRgba

    def __init__(self, *args, **kwargs):
        super(PrxInputAsRgbaChoose, self).__init__(*args, **kwargs)


# proxy
# noinspection PyMethodMayBeStatic
class _AbsPrxInputExtra(gui_prx_abstracts.AbsPrxWidget):
    PRX_INPUT_CLS = None

    def __init__(self, *args, **kwargs):
        super(_AbsPrxInputExtra, self).__init__(*args, **kwargs)

    def _gui_build_(self):
        self._qt_layout = gui_qt_wgt_base.QtHBoxLayout(self._qt_widget)
        self._qt_layout.setContentsMargins(0, 0, 0, 0)
        self._qt_layout.setSpacing(2)
        #
        self._prx_input = self.PRX_INPUT_CLS()
        self._qt_layout.addWidget(self._prx_input.widget)

    def get(self):
        raise NotImplementedError()

    def set(self, raw=None, **kwargs):
        raise NotImplementedError()

    def get_default(self):
        return None

    def set_default(self, raw=None, **kwargs):
        pass

    def get_is_default(self):
        return False

    def set_tool_tip(self, *args, **kwargs):
        if hasattr(self._prx_input._qt_widget, '_set_tool_tip_'):
            if args[0]:
                self._prx_input._qt_widget._set_tool_tip_(args[0], **kwargs)

    def set_clear(self):
        pass

    def connect_input_changed_to(self, fnc):
        pass

    def set_locked(self, boolean):
        pass

    def set_height(self, h):
        self._qt_widget.setFixedHeight(h)

    def connect_tab_pressed_to(self, fnc):
        pass


# resolver
#   entity
# noinspection PyUnusedLocal
class PrxInputAsResolverEntity(_AbsPrxInputExtra):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    PRX_INPUT_CLS = gui_prx_wgt_view_for_tree.PrxTreeView
    NAMESPACE = 'resolver'

    def __init__(self, *args, **kwargs):
        super(PrxInputAsResolverEntity, self).__init__(*args, **kwargs)
        self.widget.setMaximumHeight(160)
        self.widget.setMinimumHeight(160)
        self._prx_input.set_header_view_create(
            [('name', 2), ('update', 1)],
            320
        )
        self._prx_input.set_selection_use_single()
        self._prx_input.set_size_policy_height_fixed_mode()
        # resize
        self._prx_input.set_resize_target(self.widget)
        self._prx_input.set_resize_enable(True)
        self._prx_input.set_resize_minimum(82)
        self._item_dict = {}

    def __set_item_comp_add_as_tree_(self, obj, use_show_thread=False):
        obj_path = obj.path
        obj_type = obj.type
        if obj_path in self._item_dict:
            prx_item = self._item_dict[obj_path]
            return False, prx_item, None
        else:
            create_kwargs = dict(
                name='loading ...',
                icon_name_text=obj_type,
                filter_key=obj_path
            )
            parent = obj.get_parent()
            if parent is not None:
                prx_item_parent = self._item_dict[parent.path]
                prx_item = prx_item_parent.add_child(
                    **create_kwargs
                )
            else:
                prx_item = self._prx_input.create_item(
                    **create_kwargs
                )
            # prx_item.set_checked(True)
            prx_item.update_keyword_filter_keys_tgt([obj_path, obj_type])
            obj.set_obj_gui(prx_item)
            prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
            self._item_dict[obj_path] = prx_item
            #
            if use_show_thread is True:
                prx_item.set_show_build_fnc(
                    lambda *args, **kwargs: self.__item_show_deferred_fnc(prx_item)
                )
                return True, prx_item, None
            else:
                self.__item_show_deferred_fnc(prx_item)
                return True, prx_item, None

    def __item_show_deferred_fnc(self, prx_item, use_as_tree=True):
        obj = prx_item.get_gui_dcc_obj(namespace=self.NAMESPACE)
        obj_type_name = obj.type_name
        obj_name = obj.name
        obj_path = obj.path
        menu_raw = []
        menu_raw.extend(
            obj.get_gui_menu_raw() or []
        )
        menu_raw.extend(
            obj.get_gui_extend_menu_raw() or []
        )
        #
        if use_as_tree is True:
            menu_raw.extend(
                [
                    ('expanded',),
                    ('expand branch', 'expand', prx_item.set_expand_branch),
                    ('collapse branch', 'collapse', prx_item.set_collapse_branch),
                ]
            )
        #
        result = obj.get('result')
        update = obj.get('update')
        prx_item.set_icon_by_name(obj_type_name)
        prx_item.set_names([obj_name, update])
        prx_item.set_tool_tip(obj.description)
        if result:
            if bsc_storage.StgPathOpt(result).get_is_file():
                prx_item.set_icon_by_file(gui_core.GuiIcon.get_by_file(result))
        #
        prx_item.set_gui_menu_raw(menu_raw)
        prx_item.set_menu_content(obj.get_gui_menu_content())

    def __add_item_as_tree(self, obj):
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            for i_rsv_obj in ancestors:
                ancestor_path = i_rsv_obj.path
                if ancestor_path not in self._item_dict:
                    self.__set_item_comp_add_as_tree_(i_rsv_obj, use_show_thread=True)
        #
        self.__set_item_comp_add_as_tree_(obj, use_show_thread=True)

    def __add_item_as_list(self, obj):
        obj_path = obj.path
        obj_type = obj.type
        #
        create_kwargs = dict(
            name='...',
            filter_key=obj_path
        )
        prx_item = self._prx_input.create_item(
            **create_kwargs
        )
        # prx_item.set_checked(True)
        prx_item.update_keyword_filter_keys_tgt([obj_path, obj_type])
        obj.set_obj_gui(prx_item)
        prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
        self._item_dict[obj_path] = prx_item
        #
        prx_item.set_show_build_fnc(
            functools.partial(
                self.__item_show_deferred_fnc, prx_item, False
            )
        )

    def __set_item_selected(self, obj):
        item = obj.get_obj_gui()
        self._prx_input.set_item_selected(
            item, exclusive=True
        )

    def __clear_items_(self):
        self._prx_input.set_clear()

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (tuple, list)):
            self.__clear_items_()
            objs = raw
            if objs:
                with bsc_log.LogProcessContext.create(maximum=len(objs), label='gui-add for resolver object') as g_p:
                    for i in objs:
                        g_p.do_update()
                        #
                        self.__add_item_as_list(i)
                    #
                    self.__set_item_selected(
                        objs[-1]
                    )
        else:
            pass

    def get(self):
        _ = self._prx_input.get_current_item()
        if _:
            return _.get_gui_dcc_obj(namespace=self.NAMESPACE)

    def connect_input_changed_to(self, fnc):
        self._prx_input.connect_item_select_changed_to(
            fnc
        )


# array
#   nodes
class PrxInputAsNodes(_AbsPrxInputExtra):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    PRX_INPUT_CLS = gui_prx_wgt_view_for_tree.PrxTreeView
    NAMESPACE = 'dcc'

    def __init__(self, *args, **kwargs):
        super(PrxInputAsNodes, self).__init__(*args, **kwargs)
        self.widget.setMaximumHeight(162)
        self.widget.setMinimumHeight(162)
        self._prx_input.set_header_view_create(
            [('name', 1)],
            320
        )
        self._prx_input.set_selection_use_single()
        self._prx_input.set_size_policy_height_fixed_mode()
        self._prx_input.set_resize_target(self.widget)
        self._prx_input.set_resize_enable(True)
        self._prx_input.set_resize_minimum(82)
        #
        self._item_dict = self._prx_input._item_dict

        self._view_mode = 'list'

    def __add_item_comp_as_tree_(self, obj, use_show_thread=False):
        obj_path = obj.path
        obj_type = obj.type
        if obj_path in self._item_dict:
            prx_item = self._item_dict[obj_path]
            return False, prx_item, None
        else:
            create_kwargs = dict(
                name='loading ...',
                icon=obj.icon,
                filter_key=obj_path
            )
            parent = obj.get_parent()
            if parent is not None:
                prx_item_parent = self._item_dict[parent.path]
                prx_item = prx_item_parent.add_child(
                    **create_kwargs
                )
            else:
                prx_item = self._prx_input.create_item(
                    **create_kwargs
                )
            #
            prx_item.set_checked(True)
            prx_item.update_keyword_filter_keys_tgt([obj_path, obj_type])
            obj.set_obj_gui(prx_item)
            prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
            self._item_dict[obj_path] = prx_item
            #
            if use_show_thread is True:
                prx_item.set_show_build_fnc(
                    lambda *args, **kwargs: self.__item_show_deferred_fnc(prx_item)
                )
                return True, prx_item, None
            else:
                self.__item_show_deferred_fnc(prx_item)
                return True, prx_item, None

    def __item_show_deferred_fnc(self, prx_item, use_as_tree=True):
        obj = prx_item.get_gui_dcc_obj(namespace=self.NAMESPACE)
        prx_item.set_name(
            obj.get_name()
        )
        prx_item.set_tool_tip(
            (
                'type: {}\n'
                'path: {}\n'
            ).format(obj.get_type_name(), obj.get_path())
        )
        menu_raw = []
        menu_raw.extend(
            obj.get_gui_menu_raw() or []
        )
        menu_raw.extend(
            obj.get_gui_extend_menu_raw() or []
        )
        #
        if use_as_tree is True:
            menu_raw.extend(
                [
                    ('expanded',),
                    ('expand branch', 'expand', prx_item.set_expand_branch),
                    ('collapse branch', 'collapse', prx_item.set_collapse_branch),
                ]
            )
        #
        prx_item.set_gui_menu_raw(menu_raw)
        prx_item.set_menu_content(obj.get_gui_menu_content())
        #
        # self._prx_input.set_loading_update()

    def __add_item_as_tree(self, obj):
        ancestors = obj.get_ancestors()
        if ancestors:
            ancestors.reverse()
            for i_rsv_obj in ancestors:
                ancestor_path = i_rsv_obj.path
                if ancestor_path not in self._item_dict:
                    i_is_create, i_prx_item, _ = self.__add_item_comp_as_tree_(i_rsv_obj, use_show_thread=True)
                    if i_is_create is True:
                        i_prx_item.set_expanded(True)

        self.__add_item_comp_as_tree_(obj, use_show_thread=True)

    def __add_item_as_list(self, obj):
        path = obj.path
        type_name = obj.type_name
        #
        create_kwargs = dict(
            name='loading ...',
            icon_name_text=type_name,
            filter_key=path
        )
        prx_item = self._prx_input.create_item(
            **create_kwargs
        )
        #
        prx_item.set_checked(True)
        prx_item.update_keyword_filter_keys_tgt([path, type_name])
        obj.set_obj_gui(prx_item)
        prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
        prx_item.set_tool_tip(path)
        self._item_dict[path] = prx_item
        #
        self.__item_show_deferred_fnc(prx_item, use_as_tree=False)

    def __set_item_selected(self, obj):
        item = obj.get_obj_gui()
        self._prx_input.set_item_selected(
            item, exclusive=True
        )

    def __clear_items_(self):
        self._prx_input.set_clear()

    def set_view_mode(self, mode):
        self._view_mode = mode

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (tuple, list)):
            self.__clear_items_()
            objs = raw
            if objs:
                for i in objs:
                    if self._view_mode == 'list':
                        self.__add_item_as_list(i)
                    elif self._view_mode == 'tree':
                        self.__add_item_as_tree(i)

                self.__set_item_selected(
                    objs[-1]
                )
        else:
            pass

    def set_checked_by_include_paths(self, paths):
        _ = self._prx_input.get_all_items()
        if _:
            for i in _:
                if i.get_gui_dcc_obj(namespace=self.NAMESPACE).path in paths:
                    i.set_checked(True, extra=False)

    def set_unchecked_by_include_paths(self, paths):
        _ = self._prx_input.get_all_items()
        if _:
            for i in _:
                if i.get_gui_dcc_obj(namespace=self.NAMESPACE).path not in paths:
                    i.set_checked(False, extra=False)

    def set_all_items_checked(self, boolean):
        self._prx_input._qt_view._set_all_items_checked_(boolean)

    def get(self):
        _ = self._prx_input.get_all_items()
        if _:
            return [i.get_gui_dcc_obj(namespace=self.NAMESPACE) for i in _ if i.get_is_checked()]
        return []

    def get_all(self):
        _ = self._prx_input.get_all_items()
        if _:
            return [i.get_gui_dcc_obj(namespace=self.NAMESPACE) for i in _]
        return []

    def connect_input_changed_to(self, fnc):
        self._prx_input.connect_item_select_changed_to(
            fnc
        )


#   files
# noinspection PyUnusedLocal
class PrxInputAsFiles(_AbsPrxInputExtra):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTranslucentWidget
    PRX_INPUT_CLS = gui_prx_wgt_view_for_tree.PrxTreeView
    NAMESPACE = 'storage'

    def __init__(self, *args, **kwargs):
        super(PrxInputAsFiles, self).__init__(*args, **kwargs)
        self._qt_widget.setFixedHeight(162)
        self._prx_input.set_header_view_create(
            [('name', 3), ('update', 1)],
            480
        )
        self._prx_input.set_selection_use_single()
        self._prx_input.set_size_policy_height_fixed_mode()
        self._prx_input.set_resize_target(self.widget)
        self._prx_input.set_resize_enable(True)
        self._prx_input.set_resize_minimum(82)
        #
        self._prx_input.connect_refresh_action_for(self.refresh)
        #
        self._item_dict = self._prx_input._item_dict

        self._root_location = None

        self._view_mode = 'list'

        self._paths = []

    def __add_item_comp_as_tree_(self, obj, scheme):
        path = obj.path
        type_name = obj.type
        if path in self._item_dict:
            prx_item = self._item_dict[path]
            return False, prx_item, None

        create_kwargs = dict(
            name='...',
            filter_key=path
        )
        parent_path = obj.get_parent_path()
        if parent_path is not None:
            prx_item_parent = self._item_dict[parent_path]
            prx_item = prx_item_parent.add_child(
                **create_kwargs
            )
        else:
            prx_item = self._prx_input.create_item(
                **create_kwargs
            )
        #
        prx_item.set_checked(True)
        prx_item.update_keyword_filter_keys_tgt([path, type_name])
        obj.set_gui(prx_item)
        prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
        self._item_dict[path] = prx_item
        #
        prx_item.set_show_build_fnc(
            lambda *args, **kwargs: self.__item_show_deferred_fnc(prx_item, scheme)
        )
        return True, prx_item, None

    def __item_show_deferred_fnc(self, prx_item, scheme, use_as_tree=True):
        def rpc_lock_folder_fnc_():
            bsc_storage.StgPathPermissionMtd.change_mode(path, mode='555')
            prx_item.set_status(
                prx_item.ValidationStatus.Locked
            )

        def rpc_unlock_folder_fnc_():
            bsc_storage.StgPathPermissionMtd.change_mode(path, mode='775')
            prx_item.set_status(
                prx_item.ValidationStatus.Normal
            )

        def rpc_lock_files_fnc_():
            file_paths = bsc_storage.StgDirectoryOpt(path).get_all_file_paths()
            with bsc_log.LogProcessContext.create(maximum=len(file_paths), label='rpc unlock files (555)') as g_p:
                for i_file_path in file_paths:
                    bsc_storage.StgPathPermissionMtd.change_mode(i_file_path, mode='555')
                    g_p.do_update()

                prx_item.set_status(
                    prx_item.ValidationStatus.Normal
                )

        def rpc_unlock_files_fnc_():
            file_paths = bsc_storage.StgDirectoryOpt(path).get_all_file_paths()
            with bsc_log.LogProcessContext.create(maximum=len(file_paths), label='rpc unlock files (775)') as g_p:
                for i_file_path in file_paths:
                    i_file_opt = bsc_storage.StgFileOpt(i_file_path)
                    bsc_storage.StgPathPermissionMtd.change_mode(i_file_path, mode='775')
                    g_p.do_update()

                prx_item.set_status(
                    prx_item.ValidationStatus.Normal
                )

        obj = prx_item.get_gui_dcc_obj(namespace=self.NAMESPACE)
        path = obj.get_path()
        if obj.get_is_exists() is True:
            update = bsc_core.TimePrettifyMtd.to_prettify_by_timestamp(
                obj.get_modify_timestamp(),
                language=1
            )
        else:
            update = 'non-exists'
        if use_as_tree is True:
            prx_item.set_names([obj.get_name(), update])
        else:
            prx_item.set_names([obj.get_path_prettify(), update])

        if scheme == 'folder':
            prx_item.set_icon_by_file(
                gui_core.GuiIcon.get_directory()
            )
        else:
            prx_item.set_icon_by_file(
                gui_core.GuiIcon.get_by_file(path)
            )

        prx_item.set_tool_tip(
            (
                'type: {}\n'
                'path: {}\n'
            ).format(obj.get_type_name(), obj.get_path())
        )
        menu_raw = [
            ('open folder', 'file/folder', obj.open_in_system)
        ]
        if use_as_tree is True:
            menu_raw.extend(
                [
                    ('expanded',),
                    ('expand branch', 'expand', prx_item.set_expand_branch),
                    ('collapse branch', 'collapse', prx_item.set_collapse_branch),
                ]
            )
        #
        if scheme == 'file':
            prx_item.set_drag_enable(True)
            prx_item.set_drag_urls([obj.get_path()])
            # for katana
            prx_item.set_drag_data(
                {
                    'nodegraph/fileref': str(obj.get_path())
                }
            )
        elif scheme == 'folder':
            menu_raw.extend(
                [
                    ('rpc folder permission',),
                    ('rpc lock folder (555)', 'lock', rpc_lock_folder_fnc_),
                    ('rpc unlock folder (775)', 'lock', rpc_unlock_folder_fnc_),
                    ('rpc file permission',),
                    ('rpc lock files (555)', 'lock', rpc_lock_files_fnc_),
                    ('rpc unlock files (775)', 'lock', rpc_unlock_files_fnc_),
                ]
            )
        #
        prx_item.set_gui_menu_raw(menu_raw)
        #
        if obj.get_is_exists() is False:
            prx_item.set_status(
                prx_item.ValidationStatus.Lost
            )
        elif obj.get_is_readable() is False:
            prx_item.set_status(
                prx_item.ValidationStatus.Unreadable
            )
        elif obj.get_is_writable() is False:
            prx_item.set_status(
                prx_item.ValidationStatus.Unwritable
            )

    def __add_item_as_tree(self, obj, scheme):
        if self._root_location is not None:
            i_is_create, i_prx_item, _ = self.__add_item_as_list(self._root_obj, scheme)
            if i_is_create is True:
                i_prx_item.set_expanded(True)
            ancestor_paths = obj.get_ancestor_paths()
            ancestor_paths.reverse()
            if self._root_location in ancestor_paths:
                index = ancestor_paths.index(self._root_location)
                for i_path in ancestor_paths[index:]:
                    if i_path not in self._item_dict:
                        i_obj = self._root_obj.create_dag_fnc(i_path)
                        i_is_create, i_prx_item, _ = self.__add_item_comp_as_tree_(i_obj, scheme='folder')
                        if i_is_create is True:
                            i_prx_item.set_expanded(True)
            else:
                return
        else:
            ancestor_paths = obj.get_ancestor_paths()
            if ancestor_paths:
                ancestor_paths.reverse()
                for i_path in ancestor_paths:
                    i_obj = self._root_obj.create_dag_fnc(i_path)
                    if i_path not in self._item_dict:
                        i_is_create, i_prx_item, _ = self.__add_item_comp_as_tree_(i_obj, scheme='folder')
                        if i_is_create is True:
                            i_prx_item.set_expanded(True)
        #
        self.__add_item_comp_as_tree_(obj, scheme)

    def __add_item_as_list(self, obj, scheme):
        path = obj.get_path()
        type_name = obj.get_type_name()
        if path in self._item_dict:
            prx_item = self._item_dict[path]
            return False, prx_item, None
        #
        create_kwargs = dict(
            name='...',
            filter_key=path
        )
        prx_item = self._prx_input.create_item(
            **create_kwargs
        )
        #
        prx_item.set_checked(True)
        prx_item.update_keyword_filter_keys_tgt([path, type_name])
        obj.set_gui(prx_item)
        prx_item.set_gui_dcc_obj(obj, namespace=self.NAMESPACE)
        prx_item.set_tool_tip(path)
        self._item_dict[path] = prx_item
        #
        prx_item.set_show_build_fnc(
            lambda *args, **kwargs: self.__item_show_deferred_fnc(prx_item, scheme, use_as_tree=False)
        )
        return True, prx_item, None

    def __set_item_selected(self, obj):
        item = obj.get_gui()
        self._prx_input.set_item_selected(
            item, exclusive=True
        )

    def restore(self):
        self._prx_input.set_clear()

    def refresh(self):
        self.set(self._paths)

    def set_view_mode(self, mode):
        self._view_mode = mode

    def set(self, raw=None, **kwargs):
        if isinstance(raw, (tuple, list)):
            self.restore()
            self._paths = raw
            if self._paths:
                obj_cur = None
                for i_path in self._paths:
                    if bsc_storage.StgPathOpt(i_path).get_is_file():
                        i_obj = bsc_storage.StgFileOpt(i_path)
                        i_scheme = 'file'
                    else:
                        i_obj = bsc_storage.StgDirectoryOpt(i_path)
                        i_scheme = 'folder'
                    #
                    obj_cur = i_obj
                    #
                    if self._view_mode == 'list':
                        self.__add_item_as_list(i_obj, i_scheme)
                    elif self._view_mode == 'tree':
                        self.__add_item_as_tree(i_obj, i_scheme)
                #
                self.__set_item_selected(obj_cur)
        else:
            pass

    def set_root(self, path):
        self._root_location = path
        self._root_obj = bsc_storage.StgDirectoryOpt(self._root_location)

    def set_checked_by_include_paths(self, paths):
        _ = self._prx_input.get_all_items()
        if _:
            for i in _:
                if i.get_gui_dcc_obj(namespace=self.NAMESPACE).path in paths:
                    i.set_checked(True, extra=False)

    def set_unchecked_by_include_paths(self, paths):
        _ = self._prx_input.get_all_items()
        if _:
            for i in _:
                if i.get_gui_dcc_obj(namespace=self.NAMESPACE).path not in paths:
                    i.set_checked(False, extra=False)

    def set_all_items_checked(self, boolean):
        self._prx_input._qt_view._set_all_items_checked_(boolean)

    def get(self):
        _ = self._prx_input.get_all_items()
        if _:
            return [i.get_gui_dcc_obj(namespace=self.NAMESPACE).get_path() for i in _ if i.get_is_selected()]
        return []

    def get_all(self, check_only=False):
        _ = self._prx_input.get_all_items()
        if _:
            if check_only is True:
                return [i.get_gui_dcc_obj(namespace=self.NAMESPACE).get_path() for i in _ if i.get_is_checked() is True]
            return [i.get_gui_dcc_obj(namespace=self.NAMESPACE).get_path() for i in _]
        return []

    def connect_input_changed_to(self, fnc):
        self._prx_input.connect_item_select_changed_to(
            fnc
        )

    def connect_refresh_action_for(self, fnc):
        self._prx_input.connect_refresh_action_for(fnc)
