# coding:utf-8
import six

import functools

import collections

import lxbasic.core as bsc_core

import lxbasic.pinyin as bsc_pinyin

from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core


class _Data(object):
    def __init__(self, **kwargs):
        self._dict = dict(**kwargs)

    def __getattr__(self, key):
        return self._dict[key]

    def __setattr__(self, key, value):
        if key in {'_dict'}:
            self.__dict__[key] = value
        else:
            self._dict[key] = value

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __str__(self):
        return str(self._dict)

    def __repr__(self):
        return '\n'+self.__str__()


class AbsViewModel(object):
    SortOrder = _gui_core.GuiSortOrder

    @qt_slot()
    def _on_item_check_changed(self):
        self.refresh_info()

    def __init__(self, widget, data):
        self._widget = widget

        self._data = data
        # sort
        self._data.item_sort = _Data(
            enable=False,
            keys=[],
            key_current='index',
            order=0,
        )
        # check
        self._data.item_check = _Data(
            enable=False
        )
        # menu
        self._data.menu = _Data(
            content=None,
            data=None,
            data_generate_fnc=None
        )
        # keyword filter
        self._data.keyword_filter = _Data(
            key_src_set=set()
        )
        # occurrence
        self._data.occurrence = _Data(
            index=None
        )
        # item query
        self._data.item_dict = collections.OrderedDict()
        # information
        self._data.info = ''
        
        self._keyword_filter_keys_cache = None

    # sort
    def get_item_sort_order(self):
        return self._data.item_sort.order

    def set_item_sort_order(self, order):
        self._data.item_sort.order = order
        self._update_item_sort()

    def set_item_sort_keys(self, keys):
        if keys is not None:
            self._data.item_sort.enable = True
            self._data.item_sort.keys = keys
            self._widget.setSortingEnabled(True)
            return True
        self._data.item_sort.enable = False
        return False
    
    def get_item_sort_keys(self):
        return self._data.item_sort.keys
    
    def get_item_sort_key_current(self):
        return self._data.item_sort.key_current

    def sort_item_by(self, key):
        self._data.item_sort.key_current = key
        [x._item_model.apply_sort(key) for x in self.get_all_items()]
        self._update_item_sort()

    def _update_item_sort(self):
        self._sort_items(
            [QtCore.Qt.AscendingOrder, QtCore.Qt.DescendingOrder][self.get_item_sort_order()]
        )

    def _sort_items(self, order):
        raise NotImplementedError()

    def swap_item_sort_order(self):
        if self._data.item_sort.order == self.SortOrder.Ascend:
            self.set_item_sort_order(self.SortOrder.Descend)
        else:
            self.set_item_sort_order(self.SortOrder.Ascend)

    def generate_item_sort_menu_data(self):
        menu_data = []
        keys = self.get_item_sort_keys()
        order = ['ascend', 'descend'][self.get_item_sort_order()]
        icon_name = 'tool/sort-by-name-{}'.format(order)
        for i_key in keys+['index']:
            if i_key != self.get_item_sort_key_current():
                menu_data.append(
                    (i_key, icon_name, functools.partial(self.sort_item_by, i_key))
                )
        return menu_data

    # check
    def set_item_check_enable(self, boolean):
        self._data.item_check.enable = boolean

    def get_item_check_enable(self):
        return self._data.item_check.enable

    # keyword filter
    def set_keyword_filter_key_src(self, texts):
        self._data.keyword_filter.key_src_set = set(texts)

    def refresh_items_visible_by_any_filter(self):
        key_src_set = self._data.keyword_filter.key_src_set

        items = self.get_all_items()
        for i_item in items:
            i_force_hidden_flag = i_item._item_model.get_force_hidden_flag()
            if i_force_hidden_flag is True:
                i_is_hidden = True
            else:
                i_tag_flag = False
                i_semantic_flag = False
                i_keyword_flag = False
                # keyword filter
                if key_src_set:
                    i_enable, i_flag = i_item._item_model.generate_keyword_filter_args(key_src_set)
                    if i_enable is True:
                        i_keyword_flag = i_flag
                # hide item when any flag is True
                if True in [i_tag_flag, i_semantic_flag, i_keyword_flag]:
                    i_is_hidden = True
                else:
                    i_is_hidden = False

            i_item.setHidden(i_is_hidden)

            # for tree
            for i in i_item._item_model.get_ancestors():
                if i_is_hidden is False:
                    i.setHidden(False)

    def get_all_items_keyword_filter_keys(self):
        key_tgt_set = set()
        [key_tgt_set.update(i_item._item_model.get_keyword_filter_key_tgt_set()) for i_item in self.get_all_items()]
        return list(key_tgt_set)
    
    def generate_keyword_filter_completion_cache(self):
        if self._keyword_filter_keys_cache is None:
            self._keyword_filter_keys_cache = self.get_all_items_keyword_filter_keys()
        return self._keyword_filter_keys_cache

    def get_all_items(self):
        raise NotImplementedError()

    def get_visible_items(self):
        raise NotImplementedError()

    def update_widget(self):
        # noinspection PyBroadException
        try:
            self._widget.update()
        except Exception:
            pass

    def set_all_items_checked(self, boolean):
        [x._item_model._update_check_state(boolean) for x in self.get_all_items()]
        self._widget.item_check_changed.emit()
        self.update_widget()

    def set_visible_items_checked(self, boolean):
        [x._item_model._update_check_state(boolean) for x in self.get_all_items()]
        self._widget.item_check_changed.emit()
        self.update_widget()

    def get_checked_items(self):
        return [x for x in self.get_all_items() if x._item_model.is_checked()]

    def get_checked_item_paths(self):
        return [x._item_model.get_path() for x in self.get_checked_items()]

    def get_selected_items(self):
        return self._widget.selectedItems()

    def get_selected_item_paths(self):
        return [x._item_model.get_path() for x in self.get_selected_items()]

    # menu
    def set_menu_content(self, content):
        self._data.menu.content = content

    def get_menu_content(self):
        return self._data.menu.content

    def set_menu_data(self, data):
        self._data.menu.data = data

    def get_menu_data(self):
        return self._data.menu.data

    def set_menu_data_generate_fnc(self, fnc):
        self._data.menu.data_generate_fnc = fnc

    def get_menu_data_generate_fnc(self):
        return self._data.menu.data_generate_fnc

    def refresh_info(self):
        c = len(self.get_checked_items())
        if c:
            info = '{} item is checked ...'.format(c)
        else:
            info = ''

        if info != self._data.info:
            self._widget.info_text_accepted.emit(info)
            self._data.info = info

    def restore(self):
        for i_item in self.get_all_items():
            i_item._item_model.do_close()
        
        self._keyword_filter_keys_cache = None
        self._widget.clear()
        self._data.item_dict.clear()

        self.refresh_info()

    def _register_item(self, path, item):
        self._data.item_dict[path] = item

    def _check_item_exists(self, path):
        return self._data.item_dict.get(path) is not None

    def _get_item(self, path):
        return self._data.item_dict.get(path)

    # assign
    def intersection_all_item_assign_path_set(self, path_set):
        for i_item in self.get_all_items():
            i_item._item_model.intersection_assign_path_set(path_set)


class AbsItemModel(object):
    Status = _gui_core.GuiItemStatus

    def do_press_click(self, point):
        if self._data.check.enable is True:
            if self._data.check.rect.contains(point):
                self.swap_check()

    def do_press_dbl_click(self, point):
        pass

    def do_hover_move(self, point):
        pass

    def do_close(self):
        pass

    def __init__(self, item, data):
        self._item = item
        self._data = data
        # path
        self._data.path = _Data(
            text=None
        )
        self._data.type = _Data(
            enable=False,
            text=None
        )
        # index
        self._data.index = 0
        # name
        self._data.name = _Data(
            enable=False,
            text=None,
            rect=QtCore.QRect(),
            color=QtGui.QColor(223, 223, 223),
            hover_color=QtGui.QColor(31, 31, 31)
        )
        # number
        self._data.number = _Data(
            enable=False,
            value=0,
            text=None,
            rect=QtCore.QRect(),
            color=QtGui.QColor(127, 127, 127),
        )
        self._data.status = _Data(
            enable=False,
            value='normal',
            color=QtGui.QColor(223, 223, 223)
        )
        # icon
        self._data.icon = _Data(
            enable=False,
            file=None,
            rect=QtCore.QRect()
        )
        # action for select
        self._data.select = _Data(
            enable=True,
            flag=False,
            rect=QtCore.QRect(),
            color=QtGui.QColor(*_gui_core.GuiRgba.LightAzureBlue),
        )
        # action for hover
        self._data.hover = _Data(
            enable=True,
            flag=False,
            rect=QtCore.QRect(),
            color=QtGui.QColor(*_gui_core.GuiRgba.LightOrange),
        )
        # action for check
        self._data.check = _Data(
            enable=False,
            flag=False,
            rect=QtCore.QRect(),
            file=_gui_core.GuiIcon.get('tag-filter-unchecked'),
            on_file=_gui_core.GuiIcon.get('tag-filter-checked'),
            off_file=_gui_core.GuiIcon.get('tag-filter-unchecked'),
        )
        # tool tip
        self._data.tool_tip = _Data(
            enable=False,
            flag=False,
            text=None,
            css=None
        )
        # show
        self._data.show = _Data(
            load_flag=False,

            cache_fnc=None,
            build_fnc=None,
        )
        # menu
        self._data.menu = _Data(
            content=None,
            data=None,
            data_generate_fnc=None
        )
        # force
        self._data.force_hidden_flag = False
        self._data.force_refresh_flag = True
        # keyword filter
        self._data.keyword_filter = _Data(
            key_tgt_set=set()
        )
        # assign
        self._data.assign = _Data(
            enable=False,
            path_set=set()
        )
        # sort
        self._data.sort_dict = dict()
        # property
        self._data.property_dict = dict()

        self._font = _qt_core.QtFont.generate(size=8)
        self._font_metrics = QtGui.QFontMetrics(self._font)

    def compute_text_width_by(self, text):
        return self._font_metrics.width(text)+16
    
    @property
    def data(self):
        return self._data

    @property
    def item(self):
        return self._item

    @property
    def view(self):
        raise NotImplementedError()

    def get_force_hidden_flag(self):
        return self._data.force_hidden_flag

    # path
    def set_path(self, text):
        self._data.path.text = text

    def get_path(self):
        return self._data.path.text

    # type
    def set_type(self, text):
        if text is not None:
            self._data.type.enable = True
            self._data.type.text = text
            return True
        self._data.type.enable = False
        return False

    def get_type(self):
        return self._data.type.text

    # name
    def set_name(self, text):
        if text is not None:
            self._data.name.enable = True
            self._data.name.text = text
            return True
        self._data.name.enable = False
        return False

    def get_name(self):
        return self._data.name.text

    # number
    def set_number(self, value):
        if value is not None:
            self._data.number.enable = True
            self._data.number.value = value
            self._data.number.text = str(value)
            return True
        self._data.number.enable = False
        return False

    def get_number(self):
        return self._data.number.value

    # index
    def set_index(self, index):
        self._data.index = index

    def get_index(self):
        return self._data.index

    # icon
    def set_icon_name(self, icon_name):
        # do not check file exists
        file_path = _gui_core.GuiIcon.get(icon_name)
        self._data.icon.enable = True
        self._data.icon.file = file_path

    # assign
    def set_assign_path_set(self, path_set):
        if path_set is not None:
            assert isinstance(path_set, set)

            self._data.assign.enable = True
            self._data.assign.path_set = path_set
            self.set_number(len(path_set))
            return True
        self._data.assign.enable = False
        self._data.assign.path_set.clear()
        self.set_number(None)
        return False

    def get_assign_path_set(self):
        return self._data.assign.path_set

    def _update_assign_path_set(self, path_set):
        if path_set:
            self._data.assign.enable = True
            self._data.assign.path_set.update(path_set)
            self.set_number(len(self._data.assign.path_set))

    def intersection_assign_path_set(self, path_set):
        if path_set:
            path_set = set.intersection(path_set, self.data.assign.path_set)
        else:
            path_set = self.data.assign.path_set

        print path_set

        self.set_number(len(path_set))

    def _update_assign_path_set_to_ancestors(self):
        self._update_assign_path_to_parent()

        for i in self.get_ancestors():
            i._item_model._update_assign_path_to_parent()

    def _update_assign_path_to_parent(self):
        if self._data.assign.enable is True:
            parent_item = self.get_parent()
            if parent_item:
                parent_item._item_model._update_assign_path_set(self._data.assign.path_set)

    # tool tip
    def set_tool_tip(self, text):
        if text:
            self._data.tool_tip.css = _qt_core.QtUtil.generate_tool_tip_css(
                self._data.name.text, text
            )

    # menu
    def set_menu_content(self, content):
        self._data.menu.content = content

    def get_menu_content(self):
        return self._data.menu.content

    def set_menu_data(self, data):
        self._data.menu.data = data

    def get_menu_data(self):
        return self._data.menu.data

    def set_menu_data_generate_fnc(self, fnc):
        self._data.menu.data_generate_fnc = fnc

    def get_menu_data_generate_fnc(self):
        return self._data.menu.data_generate_fnc

    # sort
    def register_sort_dict(self, dict_):
        self._data.sort_dict.update(dict_)

    def apply_sort(self, key):
        if key == 'index':
            index = self._data.index
            self._item.setText(
                str(index).zfill(4)
            )
        else:
            value = self._data.sort_dict.get(key, '')
            self._item.setText(value)
            # self.set_name(value)

    # show
    def _update_show_auto(self):
        if self._data.show.load_flag is True:
            self._data.show.load_flag = False
            self._do_load_show_fnc()

    def _do_load_show_fnc(self):
        trd = self.view._generate_thread_(
            self._data.show.cache_fnc, self._data.show.build_fnc, post_fnc=self.refresh_force
        )
        trd.start()

    def set_show_fnc(self, cache_fnc, build_fnc):
        if cache_fnc is not None and build_fnc is not None:
            if self._data.show.cache_fnc is None and self._data.show.build_fnc is None:
                self._data.show.load_flag = True

                self._data.show.cache_fnc = cache_fnc
                self._data.show.build_fnc = build_fnc

    def refresh_force(self):
        self.mark_force_refresh(True)
        self.update_view()

    def mark_force_refresh(self, boolean):
        self._data.force_refresh_flag = boolean

    # keyword filter
    def generate_keyword_filter_args(self, key_src_set):
        # todo: use match all mode then, maybe use match one mode also
        if key_src_set:
            context = self.get_keyword_filter_context()
            context = context.lower()
            for i_text in key_src_set:
                # fixme: chinese word
                # do not encode, keyword can be use unicode
                i_text = i_text.lower()
                if '*' in i_text:
                    i_filter_key = six.u('*{}*').format(i_text.lstrip('*').rstrip('*'))
                    if not bsc_core.BscFnmatch.filter([context], i_filter_key):
                        return True, True
                else:
                    context = bsc_core.auto_unicode(context)
                    if i_text not in context:
                        return True, True
            return True, False
        return False, False

    def register_keyword_filter_keys(self, texts):
        keys = []
        keys.extend(texts)
        for i_text in texts:
            i_texts = bsc_pinyin.Text.split_any_to_letters(i_text)
            keys.extend(i_texts)

        self._data.keyword_filter.key_tgt_set = set(keys)

    def get_keyword_filter_key_tgt_set(self):
        _ = self._data.keyword_filter.key_tgt_set
        if _:
            return _
        return {self.get_name()}

    def get_keyword_filter_context(self):
        return '+'.join(self.get_keyword_filter_key_tgt_set())

    @classmethod
    def _draw_icon(cls, painter, rect, file_path):
        if file_path.endswith('.svg'):
            cls._draw_svg(painter, QtCore.QRectF(rect), file_path)
        else:
            cls._draw_image(painter, rect, file_path)

    @classmethod
    def _draw_svg(cls, painter, rect_f, svg_path):
        svg_render = QtSvg.QSvgRenderer(svg_path)
        svg_render.render(painter, rect_f)

    @classmethod
    def _draw_image(cls, painter, rect, file_path):
        pixmap = QtGui.QPixmap()
        pixmap.load(file_path)
        if pixmap.isNull() is False:
            pxm_scaled = pixmap.scaled(
                rect.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
            )
            painter.drawPixmap(rect, pxm_scaled)

    @classmethod
    def _draw_name_text(cls, painter, rect, text, color, option):
        text = painter.fontMetrics().elidedText(
            text,
            QtCore.Qt.ElideMiddle,
            rect.width(),
            QtCore.Qt.TextShowMnemonic
        )
        painter.setPen(color)
        painter.drawText(rect, option, text)

    def update_view(self):
        # todo: use update() error in maya 2017?
        # noinspection PyBroadException
        try:
            self.view.update()
        except Exception:
            pass

    def _update_hover(self, flag):
        if flag != self._data.hover.flag:
            self._data.hover.flag = flag

    def _update_select(self, flag):
        if flag != self._data.select.flag:
            self._data.select.flag = flag

    # DAG
    def get_parent(self):
        raise NotImplementedError()

    def get_ancestors(self):
        return []

    def get_children(self):
        return []

    def get_descendants(self):
        return []

    # check
    def swap_check(self):
        self.set_checked(not self._data.check.flag)

    def set_check_enable(self, boolean):
        self._data.check.enable = boolean

    def set_checked(self, boolean):
        if boolean != self._data.check.flag:
            self._data.check.flag = boolean
            self._update_check()
            self.view.item_check_changed.emit()

    def is_checked(self):
        return self._data.check.flag

    def _update_check_state(self, boolean):
        if boolean != self._data.check.flag:
            self._data.check.flag = boolean
            self._update_check_icon()
            return True
        return False

    def _update_check_icon(self):
        self._data.check.file = [
            self._data.check.off_file,
            self._data.check.on_file
        ][self._data.check.flag]

    def _update_check(self):
        self._update_check_icon()
        self._update_check_extend()
        # self.update_view()

    def _update_check_extend(self):
        pass


class AbsView(object):
    item_check_changed = qt_signal()
    item_select_changed = qt_signal()

    press_released = qt_signal()
    info_text_accepted = qt_signal(str)
