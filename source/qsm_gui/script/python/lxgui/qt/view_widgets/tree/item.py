# coding=utf-8
# qt
from ....qt.core.wrap import *

from ...view_models.tree import item as _vew_mod_item


class QtTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, *args, **kwargs):
        super(QtTreeItem, self).__init__(*args)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled
        )
        self._item_model = _vew_mod_item.TreeItemModel(self)

    def _do_delete_(self):
        if self.parent():
            index = self.parent().indexOfChild(self)
            self.parent().takeChild(index)
        else:
            tree_widget = self.treeWidget()
            if isinstance(tree_widget, QtWidgets.QTreeWidget):
                if tree_widget:
                    index = tree_widget.indexOfTopLevelItem(self)
                    tree_widget.takeTopLevelItem(index)

    def __str__(self):
        return '{}(path={})'.format(
            self.__class__.__name__,
            self._item_model.get_path()
        )

    def __repr__(self):
        return '\n'+self.__str__()
