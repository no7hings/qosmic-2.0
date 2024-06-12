# coding:utf-8
import lxbasic.core as bsc_core


class GuiQtModForLayoutItem(object):
    def __init__(self, stack, layout_view, widget):
        self._stack = stack
        self._layout_view = layout_view
        self._widget = widget

        self._drag_and_drop_scheme = None
        self._drag_and_drop_key = None

    def get_layout_view(self):
        return self._layout_view

    def get_widget(self):
        return self._widget

    def start_drag_and_drop(self, scheme):
        self.set_drag_and_drop_scheme(scheme)
        self._stack.discard_drag_and_drop_cache(self)

    def set_drag_and_drop_scheme(self, scheme):
        self._drag_and_drop_scheme = scheme

    def get_drag_and_drop_scheme(self):
        return self._drag_and_drop_scheme

    def set_drag_and_drop_key(self, key):
        self._drag_and_drop_key = key

    def get_drag_and_drop_key(self):
        return self._drag_and_drop_key


class GuiQtModForLayoutItemStack(object):
    ITEM_CLS = GuiQtModForLayoutItem

    DRAG_AND_DROP_CACHE = None

    def __init__(self, widget):
        self._key_text = bsc_core.BscUuid.generate_new()

        self._widget = widget
        self._items = []
        self._item_count = 0
        self._item_dict = {}

    def discard_drag_and_drop_cache(self, item):
        self.__class__.DRAG_AND_DROP_CACHE = item

    def fetch_drag_and_drop_cache(self):
        return self.__class__.DRAG_AND_DROP_CACHE

    def get_key(self):
        return self._key_text

    def create_item(self, widget):
        item = self.ITEM_CLS(self, self._widget, widget)
        widget._set_layout_item_(item)
        self.append_item(item)

    def append_item(self, item):
        self._items.append(item)
        index_cur = self._item_count
        key_cur = '{}/{}'.format(self._key_text, index_cur)
        item.set_drag_and_drop_key(key_cur)
        self._item_dict[key_cur] = item
        self._item_count += 1

    def get_count(self):
        return self._item_count

    def get_index_maximum(self):
        return self._item_count-1

    def get_indices(self):
        return range(self._item_count)

    def get_all_items(self):
        return self._items

    def get_all_widgets(self):
        return [i.get_widget() for i in self._items]

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

                self._items = []
                for i in range(c):
                    self._items.append(sort_dict[i])

    def get_all_widget_names(self):
        return [i._get_name_text_() for i in self.get_all_widgets()]

    def get_item_at(self, index):
        if self._items:
            if index <= self.get_index_maximum():
                return self._items[index]

    def get_widget_at(self, index):
        item = self.get_item_at(index)
        if item:
            # noinspection PyUnresolvedReferences
            return item.get_widget()

    def get_item_by(self, key):
        if key in self._item_dict:
            return self._item_dict[key]

    def get_all_item_names(self):
        return self._item_dict.keys()

    def get_index_by(self, item):
        if item in self._items:
            return self._items.index(item)

    def insert_item_between(self, index_0, index_1):
        if index_0 != index_1:
            item_0 = self._items[index_0]
            self._items.pop(index_0)
            self._items.insert(index_1, item_0)

    def restore(self):
        for i in self._items:
            i_widget = i.get_widget()
            i_widget.close()
            i_widget.deleteLater()
        #
        self._items = []
        self._item_count = 0
        self._item_dict = {}

    # noinspection PyUnusedLocal
    def drop_item_to(self, item, index):
        self.append_item(item)
        widget = item.get_widget()
        widget.setParent(self._widget)
