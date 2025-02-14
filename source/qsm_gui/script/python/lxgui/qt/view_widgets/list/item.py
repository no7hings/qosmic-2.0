# coding=utf-8
# qt
from ....qt.core.wrap import *

from ...view_models.list import item as _vew_mod_item


class QtListItem(QtWidgets.QListWidgetItem):
    GROUP_FLAG = False

    def __init__(self, *args, **kwargs):
        super(QtListItem, self).__init__(*args)

        self._item_model = _vew_mod_item.ListItemModel(self)

    def __hash__(self):
        return hash(self._item_model.get_path())


class QtListGroupItem(QtWidgets.QListWidgetItem):
    GROUP_FLAG = True

    HEIGHT = 20

    def __init__(self, *args, **kwargs):
        super(QtListGroupItem, self).__init__(*args)
        self.setFlags(
            QtCore.Qt.NoItemFlags
        )

        self._item_model = _vew_mod_item.ListGroupItemModel(self)

    def sizeHint(self):
        return QtCore.QSize(self.listWidget().viewport().width(), self.HEIGHT)
