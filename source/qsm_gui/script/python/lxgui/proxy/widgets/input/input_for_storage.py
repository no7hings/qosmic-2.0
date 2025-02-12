# coding:utf-8
import os

from ....qt.widgets.input import input_for_storage as _qt_wgt_ipt_for_storage

from ....qt.widgets import utility as _qt_wgt_utility

from . import _input_base


# storage
class AbsPrxInputForStorage(_input_base.AbsPrxInput):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = _qt_wgt_ipt_for_storage.QtInputForStorage

    def __init__(self, *args, **kwargs):
        super(AbsPrxInputForStorage, self).__init__(*args, **kwargs)
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
class PrxInputForFileOpen(AbsPrxInputForStorage):
    def __init__(self, *args, **kwargs):
        super(PrxInputForFileOpen, self).__init__(*args, **kwargs)
        self._qt_input_widget._set_storage_scheme_(
            self._qt_input_widget.StorageScheme.FileOpen
        )
        self.set_history_key('gui.file-open')

    def _value_validation_fnc_(self, path):
        return os.path.isfile(path)


#   file save
class PrxInputForFileSave(AbsPrxInputForStorage):
    def __init__(self, *args, **kwargs):
        super(PrxInputForFileSave, self).__init__(*args, **kwargs)
        self._qt_input_widget._set_storage_scheme_(
            self._qt_input_widget.StorageScheme.FileSave
        )
        self.set_history_key('gui.file-save')

    def _value_validation_fnc_(self, path):
        return os.path.isfile(path)


#   directory open
class PrxInputForDirectoryOpen(AbsPrxInputForStorage):
    def __init__(self, *args, **kwargs):
        super(PrxInputForDirectoryOpen, self).__init__(*args, **kwargs)
        self._qt_input_widget._set_storage_scheme_(
            self._qt_input_widget.StorageScheme.DirectoryOpen
        )
        self.set_history_key('gui.directory-open')

    def _value_validation_fnc_(self, path):
        return os.path.isdir(path)


#   directory open
class PrxInputForDirectorySave(AbsPrxInputForStorage):
    def __init__(self, *args, **kwargs):
        super(PrxInputForDirectorySave, self).__init__(*args, **kwargs)
        self._qt_input_widget._set_storage_scheme_(
            self._qt_input_widget.StorageScheme.DirectorySave
        )
        self.set_history_key('gui.directory-save')

    def _value_validation_fnc_(self, path):
        return os.path.isdir(path)
