# coding:utf-8
import lxbasic.core as bsc_core
# qt
from ....qt.core.wrap import *

from .... import core as _gui_core

from .. import base as _base

from .. import item_base as _item_base


class TreeItemModel(_item_base.AbsItemModel):
    WAIT_PLAY_DELAY = 50

    def __init__(self, item):
        super(TreeItemModel, self).__init__(
            item,
            _base._Data(
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

    def clear_descendants(self):
        widget = self._item.treeWidget()
        item_dict = widget._view_model._data.item_dict
        paths = item_dict.keys()
        path = self.get_path()
        descendants = bsc_core.BscNodePath.find_dag_descendant_paths(
            path, paths
        )

        self._item.takeChildren()
        for i in descendants:
            item_dict.pop(i)

    def is_checked_for_descendants(self):
        for i in self.get_descendants():
            if i._item_model.is_checked():
                return True
        return False

    def update(self, rect):
        # check rect is change
        if rect != self._data.rect or self._data.force_refresh_flag is True:
            # need re instance
            self._data.rect = qt_rect(rect)
            item_h = 20
            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
            # check icon
            icn_w = 16
            icn_y = y+(h-item_h+(item_h-icn_w)/2)
            check_frm_w = 0
            if self._data.check_enable is True:
                check_frm_w = 20
                self._data.check.rect.setRect(
                    x+(check_frm_w-icn_w)/2, icn_y, icn_w, icn_w
                )
            # color
            color_frm_w = 0
            if self._data.color_enable is True:
                color_frm_w = 20
                self._data.color.rect.setRect(
                    x+check_frm_w+(color_frm_w-icn_w)/2, icn_y, icn_w, icn_w
                )
            # icon
            icon_frm_w = 0
            if self._data.icon_enable is True:
                icon_frm_w = 20
                self._data.icon.rect.setRect(
                    x+check_frm_w+color_frm_w+(icon_frm_w-icn_w)/2, icn_y, icn_w, icn_w
                )

            txt_y = y+h-item_h
            # subname
            number_w_left_sub = w-(check_frm_w+color_frm_w+icon_frm_w)
            subname_frm_w = 0
            if self._data.number_enable is True:
                subname_frm_w = self.compute_text_width_by(self._data.number.text)
                subname_frm_w = min(number_w_left_sub, subname_frm_w)
                self._data.number.rect.setRect(
                    x+w-subname_frm_w-2, txt_y, subname_frm_w, item_h
                )

            elif self._data.subname_enable is True:
                subname_frm_w = self.compute_text_width_by(self._data.subname.text)
                subname_frm_w = min(number_w_left_sub, subname_frm_w)
                self._data.subname.rect.setRect(
                    x+w-subname_frm_w-2, txt_y, subname_frm_w, item_h
                )
            # name
            name_w_left_sub = check_frm_w+color_frm_w+icon_frm_w
            self._data.name.rect.setRect(
                x+name_w_left_sub+1, txt_y, w-(name_w_left_sub+subname_frm_w)-2, item_h
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
        self.draw_texts(painter, option, index)
        # number
        if column == 0:
            if self._data.number_enable is True:
                text_color = [
                    self._data.text.color, self._data.text.action_color
                ][self._data.select.flag or self._data.hover.flag]
                painter.setFont(self._font)
                self._draw_name_text(
                    painter, self._data.number.rect, self._data.number.text, text_color,
                    QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter
                )
            elif self._data.subname_enable is True:
                painter.setFont(self._font)
                self._draw_name_text(
                    painter, self._data.subname.rect, self._data.subname.text, self._data.subname.color,
                    QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter
                )
        painter.restore()

    def draw_background(self, painter, option, index):
        x, y, w, h = option.rect.x(), option.rect.y(), option.rect.width(), option.rect.height()
        column = index.column()
        rect = qt_rect(x+1, y+1, w-1, h-2)
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
                self._draw_icon_by_file(painter, self._data.check.rect, self._data.check.file)
            # draw color
            if self._data.color_enable is True:
                rgb = self._data.color.rgb
                if self._data.number_enable is True:
                    if self._data.number.flag is False:
                        rgb = _gui_core.GuiRgba.DarkGray

                self._draw_color(painter, self._data.color.rect, rgb)
            # draw icon
            if self._data.icon_enable is True:
                if self._data.icon.file_flag is True:
                    self._draw_icon_by_file(painter, self._data.icon.rect, self._data.icon.file)
                elif self._data.icon.pixmap_flag is True:
                    self._draw_icon_by_pixmap(painter, self._data.icon.rect, self._data.icon.pixmap)

    def draw_texts(self, painter, option, index):
        column = index.column()
        self.draw_name_at(painter, option, column)

    def draw_name_at(self, painter, option, column):
        x, y, w, h = option.rect.x(), option.rect.y(), option.rect.width(), option.rect.height()

        if column == 0:
            rect = self._data.name.rect
            text = self.get_name()
        else:
            rect = qt_rect(x, y, w, h)
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

    def apply_sort_key(self, sort_key):
        if self._data.sort_enable is True:
            self._data.sort.key = sort_key

            self._item.setText(0, self._generate_current_sort_name_text())

    def _update_name(self, text):
        self._item.setText(0, text)

    def set_expanded(self, boolean, use_record=True):
        if use_record is True:
            widget = self._item.treeWidget()
            if widget._view_model._data.item_expand_record_enable is True:
                self._item.setExpanded(
                    widget._view_model._data.item_expand_record.data.get(self._data.path.text, boolean)
                )
            else:
                self._item.setExpanded(boolean)
        else:
            self._item.setExpanded(boolean)

    # select
    def focus_select(self):
        self.expand_to_ancestors()
        widget = self._item.treeWidget()
        widget.scrollToItem(self._item, widget.PositionAtTop)
        widget.setCurrentItem(self._item)
