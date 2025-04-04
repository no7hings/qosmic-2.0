# coding:utf-8
# qt
from .wrap import *


class GuiQtModForTabItem(object):
    def __init__(self, layout_view, widget):
        self._layout_view = layout_view
        self._widget = widget
        self._key_text = None
        self._name_text = None
        self._name_icon_text = None
        self._tool_tip = 'N/a'
        self._rect = qt_rect()
        self._draw_rect = qt_rect()
        self._popup_rect = qt_rect()

        self._is_drawable = False

    def get_widget(self):
        return self._widget

    widget = property(get_widget)

    def set_key(self, text):
        self._key_text = text

    def get_key(self):
        return self._key_text

    def set_name(self, text):
        self._name_text = text

    def get_name(self):
        return self._name_text

    name_text = property(get_name)

    def set_icon_text(self, text):
        self._name_icon_text = text

    def get_icon_text(self):
        return self._name_icon_text

    icon_text = property(get_icon_text)

    def set_tool_tip(self, tool_tip):
        self._tool_tip = tool_tip

    def get_tool_tip(self):
        return self._tool_tip

    tool_tip = property(get_tool_tip)

    def get_rect(self):
        return self._rect

    rect = property(get_rect)

    def get_draw_rect(self):
        return self._draw_rect

    draw_rect = property(get_draw_rect)

    def get_popup_rect(self):
        return self._popup_rect

    rect_popup = property(get_popup_rect)

    def delete(self):
        pass
        # self._widget.close()
        # self._widget.deleteLater()

    def set_drawable(self, boolean):
        self._is_drawable = boolean

    def get_is_drawable(self):
        return self._is_drawable


class GuiQtModForTabItemStack(object):
    ITEM_CLS = GuiQtModForTabItem

    def __init__(self, widget):
        self._widget = widget
        self._item_count = 0
        self._items = []

    def create_item(self, widget):
        item = self.ITEM_CLS(self._widget, widget)
        self._items.append(item)
        self._item_count += 1
        return item

    def get_item_at(self, index):
        if self._items:
            if index <= self.get_index_maximum():
                return self._items[index]

    def delete_item_at(self, index):
        item = self._items[index]
        item.delete()
        self._items.pop(index)
        self._item_count -= 1

    def delete_item(self, item):
        index = self._items.index(item)
        item.delete()
        self._items.pop(index)
        self._item_count -= 1

    def get_index_by_name(self, name_text):
        for i_index, i_item in enumerate(self._items):
            if i_item.get_name() == name_text:
                return i_index

    def get_index_by_key(self, key_text):
        for i_index, i_item in enumerate(self._items):
            if i_item.get_key() == key_text:
                return i_index

    def get_item_index(self, item):
        return self._items.index(item)

    def get_name_at(self, index):
        item = self.get_item_at(index)
        if item:
            # noinspection PyUnresolvedReferences
            return item.get_name()

    def get_rect_at(self, index):
        item = self.get_item_at(index)
        if item:
            # noinspection PyUnresolvedReferences
            return item.get_rect()

    def get_tool_tip_at(self, index):
        item = self.get_item_at(index)
        if item:
            # noinspection PyUnresolvedReferences
            return item.get_tool_tip()

    def get_key_at(self, index):
        item = self.get_item_at(index)
        if item:
            # noinspection PyUnresolvedReferences
            return item.get_key()

    def get_all_names(self):
        return [i.get_name() for i in self.get_all_items()]

    def get_all_keys(self):
        return [i.get_key() for i in self.get_all_items()]

    def get_count(self):
        return self._item_count

    def get_index_maximum(self):
        return self._item_count-1

    def get_all_items(self):
        return self._items

    def insert_item_between(self, index_0, index_1):
        if index_0 != index_1:
            item_0 = self._items[index_0]
            self._items.pop(index_0)
            self._items.insert(index_1, item_0)


class GuiQtModForScroll(object):
    def __init__(self):
        self._is_valid = False
        #
        self.__w_or_h = 0
        self.__abs_w_or_h = 0
        self.__maximum = 0
        self.__minimum = 0
        self.__value = 0
        self.__value_step = 0

    def set_w_or_h(self, v):
        self.__w_or_h = v

    def set_abs_w_or_h(self, v):
        self.__abs_w_or_h = v

    def is_valid(self):
        return self._is_valid

    def set_step(self, v):
        self.__value_step = v

    def step_to_previous(self):
        return self.adjust_value(-self.__value_step)

    def step_to_next(self):
        return self.adjust_value(self.__value_step)

    def adjust_value(self, v):
        return self.accept_value(self.__value+v)

    def accept_value(self, v):
        if self._is_valid:
            value_pre = self.__value
            self.__value = int(max(min(v, self.__maximum), self.__minimum))
            if self.__value != value_pre:
                return True
            return False
        #
        self.__value = 0
        return False

    def get_value(self):
        return self.__value

    def update(self):
        if self.__abs_w_or_h > self.__w_or_h:
            self.__maximum = self.__abs_w_or_h-self.__w_or_h
            self._is_valid = True
            self.accept_value(self.__value)
        else:
            self.__maximum = 0
            self.__value = 0
            self._is_valid = False

    def get_is_maximum(self):
        return self.__value == self.__maximum

    def get_is_minimum(self):
        return self.__value == self.__minimum


class GuiQtModForGrid(object):
    @staticmethod
    def to_column_count(w, item_w):
        if item_w > 0:
            return max(int(w/item_w), 1)
        return 1

    @staticmethod
    def to_row_count(h, item_h):
        if item_h > 0:
            return max(int(h/item_h), 1)
        return 1

    @staticmethod
    def get_row_count(item_count, column_count):
        return int((item_count+column_count-1)/column_count)

    @staticmethod
    def get_index_between(column, row, column_count):
        return int(column+row*column_count)

    @staticmethod
    def get_column_loc(x, item_w):
        return int(x/item_w)

    @staticmethod
    def get_column_at(index, column_count):
        return int(index%column_count)

    @staticmethod
    def get_row_loc(y, item_h):
        return int(y/item_h)

    @staticmethod
    def get_row_at(index, column_count):
        return int(index/column_count)

    @staticmethod
    def map_to_item_pos(x, y, item_w, item_h, offset_x, offset_y, column, row):
        return int(x+offset_x-column*item_w), int(y+offset_y-row*item_h)

    @classmethod
    def get_abs_size(cls, item_w, item_h, column_count, row_count):
        return column_count*item_w, row_count*item_h


class GuiQtModForGridLayout(object):
    def __init__(self):
        self._item_count = 0
        self.__x, self.__y = 0, 0
        self.__w, self.__h = 48, 48
        self.__item_w, self.__item_h = 48, 48
        self.__column_count, self.__row_count = 1, 1
        self.__abs_w, self.__abs_h = 48, 48
        # left，top，right，bottom
        self._item_margins = 2, 2, 2, 2

    def get_item_column_at(self, index):
        return GuiQtModForGrid.get_column_at(index, self.__column_count)

    def get_item_row_at(self, index):
        return GuiQtModForGrid.get_row_at(index, self.__column_count)

    def get_pos_at(self, index, offset_x=0, offset_y=0):
        m_l, m_t, m_r, m_b = self._item_margins
        item_w, item_h = self.__item_w+m_l+m_r, self.__item_h+m_t+m_b
        return (
            self.__x+self.get_item_column_at(index)*item_w-offset_x+m_l,
            self.__y+self.get_item_row_at(index)*item_h-offset_y+m_t
        )

    def set_count(self, value):
        self._item_count = value

    def set_item_size(self, item_w, item_h):
        self.__item_w, self.__item_h = item_w, item_h

    def set_pos(self, x, y):
        self.__x, self.__y = x, y

    def set_size(self, w, h):
        self.__w, self.__h = w, h

    def update(self):
        # left，top，right，bottom
        if self._item_count:
            m_l, m_t, m_r, m_b = self._item_margins
            item_w, item_h = self.__item_w+m_l+m_r, self.__item_h+m_t+m_b
            self.__column_count = GuiQtModForGrid.to_column_count(self.__w, item_w)
            self.__column_count = min(self.__column_count, self._item_count)
            self.__row_count = GuiQtModForGrid.get_row_count(self._item_count, self.__column_count)
            self.__abs_w, self.__abs_h = GuiQtModForGrid.get_abs_size(item_w, item_h, self.__column_count, self.__row_count)

    def get_geometry_at(self, index):
        x, y = self.get_pos_at(index)
        w, h = self.__item_w, self.__item_h
        return x, y, w, h

    def get_abs_size(self):
        return self.__abs_w, self.__abs_h

    def get_coord_loc(self, x, y):
        column = GuiQtModForGrid.get_column_loc(x, self.__item_w)
        row = GuiQtModForGrid.get_row_loc(y, self.__item_h)
        return column, row

    def get_index_between(self, column, row):
        return GuiQtModForGrid.get_index_between(column, row, self.__column_count)

    def get_index_loc(self, x, y):
        pass


# noinspection PyUnusedLocal
class GuiQtModForVLayout(object):
    def __init__(self):
        self.__x, self.__y = 0, 0

        self.__w, self.__h = 20, 20
        self.__item_w, self.__item_h = 20, 20

    def set_pos(self, x, y):
        self.__x, self.__y = x, y

    def set_size(self, w, h):
        self.__w, self.__h = w, h

    def set_item_h(self, h):
        self.__item_h = h

    def get_y_at(self, index):
        return (index*self.__item_h)+self.__y

    def get_geometry_at(self, index):
        return self.__x, self.get_y_at(index), self.__w, self.__item_h

    def get_index_loc(self, x, y):
        return int(y/self.__item_h)
