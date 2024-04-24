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


class PrxHTabGroup(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_container_for_tab.QtHTabGroup

    def __init__(self, *args, **kwargs):
        super(PrxHTabGroup, self).__init__(*args, **kwargs)

    def add_widget(self, widget, *args, **kwargs):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            qt_widget = widget
        else:
            qt_widget = widget.widget
        #
        self._qt_widget._add_widget_(qt_widget, *args, **kwargs)