# coding=utf-8
# qt
from ....qt.core.wrap import *

from ...view_models import item_for_tree as _vew_mod_item_for_tree


class QtTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, *args, **kwargs):
        super(QtTreeItem, self).__init__(*args)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled
        )
        self._item_model = _vew_mod_item_for_tree.TreeItemModel(self)

    def __str__(self):
        return '{}(path={})'.format(
            self.__class__.__name__,
            self._item_model.get_path()
        )

    def __repr__(self):
        return '\n'+self.__str__()
