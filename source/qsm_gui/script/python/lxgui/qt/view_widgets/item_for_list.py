# coding=utf-8
# qt
from ...qt.core.wrap import *

from ..view_models import item_for_list as _vew_mod_item_for_list


class QtListItem(QtWidgets.QListWidgetItem):
    def __init__(self, *args, **kwargs):
        super(QtListItem, self).__init__(*args)

        self._item_model = _vew_mod_item_for_list.ListItemModel(self)


class QtListGroupItem(QtWidgets.QListWidgetItem):
    HEIGHT = 20

    def __init__(self, *args, **kwargs):
        super(QtListGroupItem, self).__init__(*args)

        self._item_model = _vew_mod_item_for_list.ListItemModel(self)

    def sizeHint(self):
        return QtCore.QSize(self.listWidget().viewport().width(), self.HEIGHT)
