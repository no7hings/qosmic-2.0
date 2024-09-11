# coding=utf-8
# qt
from ...qt.core.wrap import *

from .. import view_models as _view_models


class QtListItem(QtWidgets.QListWidgetItem):
    def __init__(self, *args, **kwargs):
        super(QtListItem, self).__init__(*args, **kwargs)

        self._item_model = _view_models.ItemModelForList(self)
