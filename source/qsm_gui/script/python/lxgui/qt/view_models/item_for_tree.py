# coding:utf-8
from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from . import base as _base

from . import item_base as _item_base


class TreeItemModel(_item_base.AbsItemModel):
    WAIT_PLAY_DELAY = 50

    def __init__(self, item):
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
        if self._data.check_enable is True:
            [x._item_model._update_check_state(self.is_checked()) for x in self.get_descendants()]
            [i._item_model._update_check_state(i._item_model.is_checked_for_descendants()) for i in self.get_ancestors()]

            self.update_view()

    def get_parent(self):
        return self._item.parent()

    def get_ancestors(self):
        def rcs_fnc_(item_):
            _parent_item = item_.parent()
            if _parent_item is not None:
                list_.append(_parent_item)
                rcs_fnc_(_parent_item)

        list_ = []
        rcs_fnc_(self._item)
        return list_

    def get_children(self):
        return [self._item.child(x) for x in range(self._item.childCount())]

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
            if self._data.check_enable is True:
                check_frm_w = 20
                self._data.check.rect.setRect(
                    x+(check_frm_w-icn_w)/2+1, icn_y, icn_w, icn_w
                )
            # color
            color_frm_w = 0
            if self._data.color_enable is True:
                color_frm_w = 20
                self._data.color.rect.setRect(
                    x+check_frm_w+(color_frm_w-icn_w)/2+1, icn_y, icn_w, icn_w
                )
            # icon
            icon_frm_w = 0
            if self._data.icon_enable is True:
                icon_frm_w = 20
                self._data.icon.rect.setRect(
                    x+check_frm_w+color_frm_w+(icon_frm_w-icn_w)/2+1, icn_y, icn_w, icn_w
                )

            txt_y = y+h-item_h
            # number
            number_w_left_sub = w-(check_frm_w+color_frm_w+icon_frm_w)
            number_frm_w = 0
            if self._data.number_enable is True:
                number_frm_w = self.compute_text_width_by(self._data.number.text)
                number_frm_w = min(number_w_left_sub, number_frm_w)
                self._data.number.rect.setRect(
                    x+w-number_frm_w-2, txt_y, number_frm_w, item_h
                )
            # name
            name_w_left_sub = check_frm_w+color_frm_w+icon_frm_w
            self._data.name.rect.setRect(
                x+name_w_left_sub+1, txt_y, w-(name_w_left_sub+number_frm_w)-2, item_h
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
        # number
        if self._data.number_enable is True:
            if column == 0:
                text_color = [
                    self._data.text.color, self._data.text.action_color
                ][self._data.select.flag or self._data.hover.flag]
                painter.setFont(self._font)
                self._draw_name_text(
                    painter, self._data.number.rect, self._data.number.text, text_color,
                    QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter
                )
        painter.restore()

    def draw_background(self, painter, option, index):
        x, y, w, h = option.rect.x(), option.rect.y(), option.rect.width(), option.rect.height()
        column = index.column()
        rect = QtCore.QRect(x+1, y+1, w-1, h-2)
        condition = (self._data.hover.flag, self._data.select.flag)
        # hover
        if condition == (True, False):
            painter.setPen(self._data.hover.color)
            painter.setBrush(self._data.hover.color)
            painter.drawRect(rect)
        # select
        elif condition == (False, True):
            painter.setPen(self._data.select.color)
            painter.setBrush(self._data.select.color)
            painter.drawRect(rect)
        # hover and select
        elif condition == (True, True):
            if column == 0:
                # left to right
                color = QtGui.QLinearGradient(
                    rect.topLeft(), rect.topRight()
                )
                color.setColorAt(
                    0, self._data.hover.color
                )
                color.setColorAt(
                    1, self._data.select.color
                )
                painter.setPen(QtGui.QPen(QtGui.QBrush(color), 1))
                painter.setBrush(color)
                painter.drawRect(rect)
            else:
                if self._data.select.flag:
                    painter.setPen(self._data.select.color)
                    painter.setBrush(self._data.select.color)
                    painter.drawRect(rect)

        # when view is QTreeWidget draw check in first colum
        if column == 0:
            # draw check
            if self._data.check_enable is True:
                self._draw_icon(painter, self._data.check.rect, self._data.check.file)
            # draw color
            if self._data.color_enable is True:
                self._draw_color(painter, self._data.color.rect, self._data.color.rgb)
            # draw icon
            if self._data.icon_enable is True:
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

        status_color = self._get_status_color()
        if status_color is not None:
            text_color = status_color
        else:
            text_color = [
                self._data.text.color, self._data.text.action_color
            ][self._data.select.flag or self._data.hover.flag]

        painter.setFont(self._font)
        self._draw_name_text(painter, rect, text, text_color, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)

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

    def _update_name(self, text):
        self._item.setText(0, text)

    def set_expanded(self, boolean):
        self._item.setExpanded(boolean)
