# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from . import base as _base

from . import item_base as _item_base


class TagItemMode(_item_base.AbsItemModel):
    WAIT_PLAY_DELAY = 50

    NUMBER_TEXT_FORMAT = '({})'

    def __init__(self, item):
        super(TagItemMode, self).__init__(
            item,
            _base._Data()
        )

    def refresh_force(self):
        self._item._refresh_widget_draw_()

        self._view = self._item._view_widget

    def _update_name(self, text):
        # update when name is changed
        self._item._refresh_widget_all_()
        if self._item._parent_widget is not None:
            self._item._parent_widget._refresh_widget_all_()

    def _update_number(self, value):
        # update when number is changed
        self._item._refresh_widget_all_()
        if self._item._parent_widget is not None:
            self._item._parent_widget._refresh_widget_all_()

    def get_parent(self):
        pass