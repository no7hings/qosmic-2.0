# coding:utf-8
from .. import base as _base

from .. import item_base as _item_base


class TagItemModel(_item_base.AbsItemModel):
    WAIT_PLAY_DELAY = 50

    NUMBER_TEXT_FORMAT = '({})'

    def __init__(self, item):
        super(TagItemModel, self).__init__(
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

    def set_expanded(self, boolean, use_record=True):
        if use_record is True:
            widget = self._item._view_widget
            if widget._view_model._data.item_expand_record_enable is True:
                self._item._set_expanded_(
                    widget._view_model._data.item_expand_record.data.get(self._data.path.text, boolean)
                )
            else:
                self._item._set_expanded_(boolean)
        else:
            self._item._set_expanded_(boolean)

