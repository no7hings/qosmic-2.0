# coding:utf-8
from ... import core as _gui_core
# qt
from ...qt import core as _qt_core
# qt widgets
from ...qt.widgets import container_for_tab as _qt_container_for_tab
# proxy abstracts
from .. import abstracts as _prx_abstracts


class _AbsPrxTabToolBox(_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = _qt_container_for_tab.QtHTabToolBox

    TabDirections = _gui_core.GuiDirections

    def __init__(self, *args, **kwargs):
        super(_AbsPrxTabToolBox, self).__init__(*args, **kwargs)

    def add_widget(self, widget, *args, **kwargs):
        if isinstance(widget, _qt_core.QtCore.QObject):
            qt_widget = widget
        else:
            qt_widget = widget.widget
        #
        self._qt_widget._add_widget_(qt_widget, *args, **kwargs)

    def get_current_name(self):
        return self._qt_widget._get_current_name_text_()

    def get_current_key(self):
        return self._qt_widget._get_current_key_text_()

    def connect_current_changed_to(self, fnc):
        self._qt_widget.current_changed.connect(fnc)

    def set_history_key(self, key):
        self._qt_widget._set_history_key_(key)

    def load_history(self):
        self._qt_widget._load_history_()

    def save_history(self):
        self._qt_widget._save_history_()
    
    def set_tab_direction(self, direction):
        self._qt_widget._set_tab_direction_(direction)


class PrxHTabToolBox(_AbsPrxTabToolBox):
    QT_WIDGET_CLS = _qt_container_for_tab.QtHTabToolBox

    def __init__(self, *args, **kwargs):
        super(PrxHTabToolBox, self).__init__(*args, **kwargs)


class PrxVTabToolBox(_AbsPrxTabToolBox):
    QT_WIDGET_CLS = _qt_container_for_tab.QtVTabToolBox

    def __init__(self, *args, **kwargs):
        super(PrxVTabToolBox, self).__init__(*args, **kwargs)
