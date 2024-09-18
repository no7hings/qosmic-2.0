# coding:utf-8
from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from . import base as _base


class TreeItemModel(_base.AbsItemModel):
    WAIT_PLAY_DELAY = 50

    def __init__(self, item):
        # if not isinstance(item, QtWidgets.QTreeWidgetItem):
        #     raise RuntimeError()
        # self._item = item

        super(TreeItemModel, self).__init__(
            item,
            _base._Data(
                rect=QtCore.QRect(),

                select=_base._Data(
                    flag=False,
                    rect=QtCore.QRect(),
                    color=QtGui.QColor(*_gui_core.GuiRgba.LightAzureBlue),
                ),
                hover=_base._Data(
                    flag=False,
                    rect=QtCore.QRect(),
                    color=QtGui.QColor(*_gui_core.GuiRgba.LightOrange),
                ),

                check=_base._Data(
                    enable=True,
                    flag=False,
                    rect_f=QtCore.QRectF(),
                    svg=_gui_core.GuiIcon.get('tag-filter-unchecked'),
                    on_svg=_gui_core.GuiIcon.get('tag-filter-checked'),
                    off_svg=_gui_core.GuiIcon.get('tag-filter-unchecked'),
                ),

                force_refresh_flag=False,
            )
        )

    @property
    def view(self):
        return self._item.treeWidget()

    def _update_check_extend(self):
        if self._data.check.enable is True:
            [x._item_model._update_check_state(self.is_checked()) for x in self.get_descendants()]
            [i._item_model._update_check_state(i._item_model.is_checked_for_descendants()) for i in self.get_ancestors()]

            self.update_view()

    def get_parent(self):
        return self._item.parent()

    def get_descendants(self):
        def rcs_fnc_(item_):
            _child_count = item_.childCount()
            for _child_index in range(_child_count):
                _child_item = item_.child(_child_index)
                list_.append(_child_item)
                rcs_fnc_(_child_item)

        list_ = []
        rcs_fnc_(self._item)
        return list_

    def get_children(self):
        return [self._item.child(x) for x in range(self._item.childCount())]

    def get_ancestors(self):
        def rcs_fnc_(item_):
            _parent_item = item_.parent()
            if _parent_item is not None:
                list_.append(_parent_item)
                rcs_fnc_(_parent_item)

        list_ = []
        rcs_fnc_(self._item)
        return list_

    def is_checked_for_descendants(self):
        for i in self.get_descendants():
            if i._item_model.is_checked():
                return True
        return False

    def update(self, rect):
        # check rect is change
        if rect != self._data.rect or self._data.force_refresh_flag is True:
            # need re instance
            self._data.rect = QtCore.QRect(rect)
            item_h = 20
            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
            # check icon
            icn_w = 16
            icn_y = y+(h-item_h+(item_h-icn_w)/2)
            check_frm_w = 0
            if self._data.check.enable is True:
                check_frm_w = 20
                self._data.check.rect.setRect(
                    x+(check_frm_w-icn_w)/2+1, icn_y, icn_w, icn_w
                )
            # icon
            icon_frm_w = 0
            if self._data.icon.enable is True:
                icon_frm_w = 20
                self._data.icon.rect.setRect(
                    x+check_frm_w+(icon_frm_w-icn_w)/2+1, icn_y, icn_w, icn_w
                )
            less_w = w-(check_frm_w+icon_frm_w)
            # number
            txt_y = y+h-item_h
            number_frm_w = 0
            if self._data.number.enable is True:
                number_frm_w = self.compute_text_width_by(self._data.number.text)
                number_frm_w = min(less_w, number_frm_w)
                self._data.number.rect.setRect(
                    x+w-number_frm_w-2, txt_y, number_frm_w, item_h
                )
            # name
            self._data.name.rect.setRect(
                x+(check_frm_w+icon_frm_w)+1, txt_y, w-(check_frm_w+icon_frm_w+number_frm_w)-2, item_h
            )
            return True
        return False

    def refresh_pixmap_cache(self, rect, force=False):
        pass

    def draw(self, painter, option, index):
        painter.save()
        column = index.column()
        # update for column 1
        if column == 0:
            self.update(option.rect)

        self._update_select(not not option.state & QtWidgets.QStyle.State_Selected)
        self._update_hover(not not option.state & QtWidgets.QStyle.State_MouseOver)

        self._update_show_auto()

        self.draw_background(painter, option, index)
        self.draw_names(painter, option, index)
        if self._data.number.enable is True:
            if column == 0:
                self._draw_name_text(
                    painter, self._data.number.rect, self._data.number.text, self._data.number.color,
                    QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter
                )
        painter.restore()

    def draw_background(self, painter, option, index):
        x, y, w, h = option.rect.x(), option.rect.y(), option.rect.width(), option.rect.height()
        rect = QtCore.QRect()
        if self._data.select.flag:
            rect.setRect(
                x+1, y+1, w-1, h-2
            )
            painter.setPen(self._data.select.color)
            painter.setBrush(self._data.select.color)
            painter.drawRect(rect)

        if self._data.hover.flag:
            rect.setRect(
                x+1, y+1, w-1, h-2
            )
            painter.setPen(self._data.hover.color)
            painter.setBrush(self._data.hover.color)
            painter.drawRect(rect)
        # when view is QTreeWidget draw check in first colum
        column = index.column()
        if column == 0:
            # draw check
            if self._data.check.enable is True:
                self._draw_icon(painter, self._data.check.rect, self._data.check.file)
            # draw icon
            if self._data.icon.enable is True:
                self._draw_icon(painter, self._data.icon.rect, self._data.icon.file)

    def draw_names(self, painter, option, index):
        column = index.column()
        self.draw_name_at(painter, option, column)

    def draw_name_at(self, painter, option, column):
        x, y, w, h = option.rect.x(), option.rect.y(), option.rect.width(), option.rect.height()

        if column == 0:
            rect = self._data.name.rect
            text = self.get_name()
        else:
            rect = QtCore.QRect(x, y, w, h)
            text = self._item.text(column)

        color = [self._data.name.color, self._data.name.hover_color][self._data.select.flag or self._data.hover.flag]
        self._draw_name_text(painter, rect, text, color, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)

    # expand
    def expand_to_ancestors(self):
        for i in self.get_ancestors():
            i.setExpanded(True)

    def apply_sort(self, key):
        if key == 'index':
            index = self._data.index
            self._item.setText(
                0, str(index).zfill(6)
            )
        elif key == 'number':
            number = self._data.number.value
            self._item.setText(
                0, str(number).zfill(6)
            )
        else:
            value = self._data.sort_dict.get(key, '')
            self._item.setText(0, value)
