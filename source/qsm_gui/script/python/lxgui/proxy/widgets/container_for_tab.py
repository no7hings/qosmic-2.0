# coding:utf-8
# qt
from ...qt import core as gui_qt_core
# qt widgets
from ...qt.widgets import base as gui_qt_wgt_base

from ...qt.widgets import container_for_tab as gui_qt_wgt_container_for_tab

from ...qt.widgets import head as gui_qt_wgt_head

from ...qt.widgets import scroll as gui_qt_wgt_scroll
# proxy abstracts
from .. import abstracts as gui_prx_abstracts


class PrxHTabBox(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_container_for_tab.QtHTabToolGroup

    def __init__(self, *args, **kwargs):
        super(PrxHTabBox, self).__init__(*args, **kwargs)

    def add_widget(self, widget, *args, **kwargs):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
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
