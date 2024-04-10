# coding:utf-8
import lxbasic.core as bsc_core
# qt
from .wrap import *


class GuiQtModForTabItem(object):
    def __init__(self, layout_view, widget):
        self._layout_view = layout_view
        self.__widget = widget
        self.__key_text = None
        self.__name_text = None
        self._icon_text = None
        self.__rect = QtCore.QRect()
        self.__draw_rect = QtCore.QRect()
        self._popup_rect = QtCore.QRect()

        self.__is_drawable = False

    def get_widget(self):
        return self.__widget

    widget = property(get_widget)

    def set_key(self, text):
        self.__key_text = text

    def get_key(self):
        return self.__key_text

    def set_name(self, text):
        self.__name_text = text

    def get_name(self):
        return self.__name_text

    name_text = property(get_name)

    def set_icon_text(self, text):
        self._icon_text = text

    def get_icon_text(self):
        return self._icon_text

    icon_text = property(get_icon_text)

    def get_rect(self):
        return self.__rect

    rect = property(get_rect)

    def get_draw_rect(self):
        return self.__draw_rect

    draw_rect = property(get_draw_rect)

    def get_popup_rect(self):
        return self._popup_rect

    rect_popup = property(get_popup_rect)

    def delete(self):
        pass
        # self.__widget.close()
        # self.__widget.deleteLater()

    def set_drawable(self, boolean):
        self.__is_drawable = boolean

    def get_is_drawable(self):
        return self.__is_drawable


class GuiQtModForTabItemStack(object):
    ITEM_CLS = GuiQtModForTabItem

    def __init__(self, widget):
        self.__widget = widget
        self.__count = 0
        self.__items = []

    def create_item(self, widget):
        item = self.ITEM_CLS(self.__widget, widget)
        self.__items.append(item)
        #
        self.__count += 1
        return item

    def get_item_at(self, index):
        if self.__items:
            if index <= self.get_index_maximum():
                return self.__items[index]

    def delete_item_at(self, index):
        item = self.__items[index]
        item.delete()
        self.__items.pop(index)
        self.__count -= 1

    def delete_item(self, item):
        index = self.__items.index(item)
        item.delete()
        self.__items.pop(index)
        self.__count -= 1

    def get_index_by_name(self, text):
        for i_index, i_item in enumerate(self.__items):
            if i_item.get_name() == text:
                return i_index

    def get_index_by_key(self, text):
        for i_index, i_item in enumerate(self.__items):
            if i_item.get_key() == text:
                return i_index

    def get_name_at(self, index):
        item = self.get_item_at(index)
        if item:
            return item.get_name()

    def get_key_at(self, index):
        item = self.get_item_at(index)
        if item:
            return item.get_key()

    def get_all_names(self):
        return [i.get_name() for i in self.get_all_items()]

    def get_all_keys(self):
        return [i.get_key() for i in self.get_all_items()]

    def get_count(self):
        return self.__count

    def get_index_maximum(self):
        return self.__count-1

    def get_all_items(self):
        return self.__items

    def insert_item_between(self, index_0, index_1):
        if index_0 != index_1:
            item_0 = self.__items[index_0]
            self.__items.pop(index_0)
            self.__items.insert(index_1, item_0)


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

    def get_is_valid(self):
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
            # print self.__maximum, self.__minimum, v, self.__value
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
        self.__count = 0
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
        self.__count = value

    def set_item_size(self, item_w, item_h):
        self.__item_w, self.__item_h = item_w, item_h

    def set_pos(self, x, y):
        self.__x, self.__y = x, y

    def set_size(self, w, h):
        self.__w, self.__h = w, h

    def update(self):
        # left，top，right，bottom
        if self.__count:
            m_l, m_t, m_r, m_b = self._item_margins
            item_w, item_h = self.__item_w+m_l+m_r, self.__item_h+m_t+m_b
            self.__column_count = GuiQtModForGrid.to_column_count(self.__w, item_w)
            self.__column_count = min(self.__column_count, self.__count)
            self.__row_count = GuiQtModForGrid.get_row_count(self.__count, self.__column_count)
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


class GuiQtModForLayoutItem(object):
    def __init__(self, stack, layout_view, widget):
        self.__stack = stack
        self.__layout_view = layout_view
        self.__widget = widget

        self.__drag_and_drop_scheme = None
        self.__drag_and_drop_key = None

    def get_layout_view(self):
        return self.__layout_view

    def get_widget(self):
        return self.__widget

    def start_drag_and_drop(self, scheme):
        self.set_drag_and_drop_scheme(scheme)
        self.__stack.discard_drag_and_drop_cache(self)

    def set_drag_and_drop_scheme(self, scheme):
        self.__drag_and_drop_scheme = scheme

    def get_drag_and_drop_scheme(self):
        return self.__drag_and_drop_scheme

    def set_drag_and_drop_key(self, key):
        self.__drag_and_drop_key = key

    def get_drag_and_drop_key(self):
        return self.__drag_and_drop_key


class GuiQtModForLayoutItemStack(object):
    ITEM_CLS = GuiQtModForLayoutItem

    DRAG_AND_DROP_CACHE = None

    def __init__(self, widget):
        self.__key_text = bsc_core.UuidMtd.generate_new()

        self.__widget = widget
        self.__items = []
        self.__count = 0
        self.__key_dict = {}

    def discard_drag_and_drop_cache(self, item):
        self.__class__.DRAG_AND_DROP_CACHE = item

    def fetch_drag_and_drop_cache(self):
        return self.__class__.DRAG_AND_DROP_CACHE

    def get_key(self):
        return self.__key_text

    def create_item(self, widget):
        item = self.ITEM_CLS(self, self.__widget, widget)
        widget._set_layout_item_(item)
        self.append_item(item)

    def append_item(self, item):
        self.__items.append(item)
        index_cur = self.__count
        key_cur = '{}/{}'.format(self.__key_text, index_cur)
        item.set_drag_and_drop_key(key_cur)
        self.__key_dict[key_cur] = item
        self.__count += 1

    def get_count(self):
        return self.__count

    def get_index_maximum(self):
        return self.__count-1

    def get_indices(self):
        return range(self.__count)

    def get_all_items(self):
        return self.__items

    def get_all_widgets(self):
        return [i.get_widget() for i in self.__items]

    def sort_widgets_by_names(self, names):
        if names:
            items = self.get_all_items()
            if items:
                sort_dict = {}
                index_maximum = len(names)-1
                exists_names = self.get_all_widget_names()
                names_ = [i for i in names if i in exists_names]
                for i_item in items:
                    i_widget = i_item.get_widget()
                    i_name_text = i_widget._get_name_text_()
                    if i_name_text in names:
                        i_index = names_.index(i_name_text)
                    else:
                        i_index = index_maximum+1
                        index_maximum += 1

                    sort_dict[i_index] = i_item

                c = len(items)

                self.__items = []
                for i in range(c):
                    self.__items.append(sort_dict[i])

    def get_all_widget_names(self):
        return [i._get_name_text_() for i in self.get_all_widgets()]

    def get_item_at(self, index):
        if self.__items:
            if index <= self.get_index_maximum():
                return self.__items[index]

    def get_widget_at(self, index):
        item = self.get_item_at(index)
        if item:
            return item.get_widget()

    def get_item_by(self, key):
        if key in self.__key_dict:
            return self.__key_dict[key]

    def get_all_item_names(self):
        return self.__key_dict.keys()

    def get_index_by(self, item):
        if item in self.__items:
            return self.__items.index(item)

    def insert_item_between(self, index_0, index_1):
        if index_0 != index_1:
            item_0 = self.__items[index_0]
            self.__items.pop(index_0)
            self.__items.insert(index_1, item_0)

    def restore(self):
        for i in self.__items:
            i_widget = i.get_widget()
            i_widget.close()
            i_widget.deleteLater()
        #
        self.__items = []
        self.__count = 0
        self.__key_dict = {}

    # noinspection PyUnusedLocal
    def drop_item_to(self, item, index):
        self.append_item(item)
        widget = item.get_widget()
        widget.setParent(self.__widget)
