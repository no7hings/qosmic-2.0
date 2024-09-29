# coding:utf-8
import copy

import six

import lxbasic.core as bsc_core

import lxbasic.pinyin as bsc_pinyin

from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from . import base as _base


class AbsItemModel(object):
    Status = _gui_core.GuiItemStatus

    NUMBER_TEXT_FORMAT = '{}'

    @classmethod
    def _draw_time_text(cls, painter, rect, text):
        painter.setPen(QtGui.QColor(223, 223, 223))
        painter.drawText(rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, text)

    @classmethod
    def _draw_name(cls, painter, rect, text, color):
        text = painter.fontMetrics().elidedText(
            text,
            QtCore.Qt.ElideMiddle,
            rect.width(),
            QtCore.Qt.TextShowMnemonic
        )
        painter.setPen(color)
        painter.drawText(rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, text)

    @classmethod
    def _draw_rect(cls, painter, rect, color):
        painter.setPen(color)
        painter.setBrush(color)
        painter.drawRect(rect)

    @classmethod
    def _draw_pixmap(cls, painter, rect, pixmap):
        pxm_scaled = pixmap.scaled(
            rect.size(),
            QtCore.Qt.IgnoreAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        painter.drawPixmap(rect, pxm_scaled)

    def do_press_click(self, point):
        if self._data.check_enable is True:
            if self._data.check.rect.contains(point):
                self.swap_check()

    def register_press_dbl_click_fnc(self, fnc):
        self._data.press.dbl_click_fncs.append(fnc)

    def do_press_dbl_click(self, point):
        if self._data.press_enable is True:
            for i_fnc in self._data.press.dbl_click_fncs:
                i_fnc()

    def do_hover_move(self, point):
        pass

    def do_close(self):
        pass

    def __init__(self, item, data):
        self._item = item
        self._data = data

        self._data.rect = QtCore.QRect()
        # path
        self._data.path = _base._Data(
            text=None
        )
        self._data.type = _base._Data(
            enable=False,
            text=None
        )
        # index
        self._data.index = 0
        # text
        self._data.text = _base._Data(
            font=_qt_core.QtFont.generate(size=8),
            color=QtGui.QColor(223, 223, 223),
            action_color=QtGui.QColor(31, 31, 31)
        )
        # frame
        self._data.frame = _base._Data(
            rect=QtCore.QRect(),
            color=QtGui.QColor(223, 223, 223)
        )
        # name
        self._data.name = _base._Data(
            enable=False,
            text=None,
            rect=QtCore.QRect(),
        )
        # number
        self._data.number_enable = False
        self._data.number = _base._Data(
            flag=False,
            value=0,
            text=None,
            rect=QtCore.QRect(),
        )
        # status
        self._data.status = _base._Data(
            enable=False,
            value='normal',
            color=QtGui.QColor(223, 223, 223)
        )
        # lock
        self._data.lock_enable = False
        # icon
        self._data.icon_enable = False
        self._data.icon = _base._Data(
            file=None,
            rect=QtCore.QRect()
        )
        # color
        self._data.color_enable = False
        # action for select
        self._data.select = _base._Data(
            enable=True,
            flag=False,
            rect=QtCore.QRect(),
            color=QtGui.QColor(*_gui_core.GuiRgba.LightAzureBlue),
        )
        # action for hover
        self._data.hover = _base._Data(
            enable=True,
            flag=False,
            rect=QtCore.QRect(),
            color=QtGui.QColor(*_gui_core.GuiRgba.LightOrange),
        )
        # action for check
        self._data.check_enable = False
        # drag
        self._data.drag = _base._Data(
            enable=False,
            data=None
        )
        # tool tip
        self._data.tool_tip = _base._Data(
            enable=False,
            flag=False,
            text=None,
            css=None
        )
        # show
        self._data.show = _base._Data(
            load_flag=False,

            cache_fnc=None,
            build_fnc=None,
        )
        # menu
        self._data.menu = _base._Data(
            content=None,
            data=None,
            data_generate_fnc=None
        )
        # force
        self._data.force_hidden_flag = False
        self._data.force_refresh_flag = True
        # keyword filter
        self._data.keyword_filter = _base._Data(
            key_tgt_set=set()
        )
        # assign
        self._data.assign = _base._Data(
            enable=False,
            path_set=set(),
            path_set_pre=set()
        )
        # sort
        self._data.sort_dict = dict()
        # property
        self._data.property_dict = dict()
        # press
        self._data.press_enable = True
        self._data.press = _base._Data(
            dbl_click_fncs=[]
        )

        self._font = _qt_core.QtFont.generate(size=8)
        self._font_metrics = QtGui.QFontMetrics(self._font)

        self._close_flag = False

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
            # todo: set name to item?
            self._update_name(text)
            return True
        self._data.name.enable = False
        return False

    def _update_name(self, text):
        raise NotImplementedError()

    def get_name(self):
        return self._data.name.text

    # number
    def set_number(self, value):
        if value is not None:
            self._data.number_enable = True
            self._data.number.value = value
            self._data.number.text = self.NUMBER_TEXT_FORMAT.format(value)
            if value > 0:
                self._data.number.flag = True
                self._data.text.font.setItalic(False)
                self._data.text.color = QtGui.QColor(223, 223, 223)
                self._data.text.action_color = QtGui.QColor(31, 31, 31)

                self._font.setItalic(False)
            else:
                self._data.number.flag = False
                self._data.text.font.setItalic(True)
                self._data.text.color = QtGui.QColor(127, 127, 127)
                self._data.text.action_color = QtGui.QColor(127, 127, 127)

                self._font.setItalic(True)

            self._update_number(value)
            return True

        self._data.number_enable = False

        self._data.text.color = QtGui.QColor(223, 223, 223)
        self._data.text.action_color = QtGui.QColor(31, 31, 31)
        return False

    def _update_number(self, value):
        pass

    def get_number(self):
        return self._data.number.value

    def get_number_flag(self):
        if self._data.number_enable is True:
            return self._data.number.flag
        return False

    # index
    def set_index(self, index):
        self._data.index = index

    def get_index(self):
        return self._data.index

    # color
    def set_color_enable(self, boolean):
        self._data.color_enable = boolean
        if boolean is True:
            self._data.color = _base._Data(
                rgb=(255, 255, 255),
                hex='FFFFFF',
                rect=QtCore.QRect()
            )

    def set_color_rgb(self, rgb):
        if self._data.color_enable is True:
            self._data.color.rgb = rgb
            self._data.color.hex = bsc_core.BscColor.rgb2hex(*rgb)

    # icon
    def set_icon_name(self, icon_name):
        # do not check file exists
        self._data.icon_enable = True
        file_path = _gui_core.GuiIcon.get(icon_name)
        self._data.icon.file = file_path

    # assign
    def set_assign_path_set(self, path_set):
        if path_set is not None:
            assert isinstance(path_set, set)

            self._data.assign.enable = True
            self._data.assign.path_set_pre = copy.copy(self._data.assign.path_set)
            self._data.assign.path_set = path_set
            self.set_number(len(path_set))
            return True
        self._data.assign.enable = False
        self._data.assign.path_set.clear()
        self.set_number(None)
        return False

    def get_assign_path_set_for(self):
        return self._data.assign.path_set

    def _update_assign_path_set(self, path_set_addition, path_set_deletion):
        self._data.assign.enable = True

        self._data.assign.path_set_pre = copy.copy(self._data.assign.path_set)

        self._data.assign.path_set.update(path_set_addition)
        self._data.assign.path_set.difference_update(path_set_deletion)
        # update to number
        self.set_number(len(self._data.assign.path_set))

    def intersection_assign_path_set(self, path_set):
        if path_set:
            path_set = set.intersection(path_set, self.data.assign.path_set)
        else:
            path_set = self.data.assign.path_set

        self.set_number(len(path_set))

    def _update_assign_path_set_to_ancestors(self):
        self._update_assign_path_to_parent()

    def _update_assign_path_to_parent(self):
        if self._data.assign.enable is True:
            parent_item = self.get_parent()
            if parent_item:
                path_set = self._data.assign.path_set
                path_set_pre = self._data.assign.path_set_pre

                path_set_addition = path_set.difference(path_set_pre)
                path_set_deletion = path_set_pre.difference(path_set)

                parent_item._item_model._update_assign_path_set(path_set_addition, path_set_deletion)
                parent_item._item_model._update_assign_path_to_parent()

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
        if file_path is None:
            return
        if file_path.endswith('.svg'):
            cls._draw_svg(painter, QtCore.QRectF(rect), file_path)
        else:
            cls._draw_image(painter, rect, file_path)

    @classmethod
    def _draw_color(cls, painter, rect, rgb):
        painter.setPen(
            QtGui.QColor(*_gui_core.GuiRgba.LightGray)
        )
        painter.setBrush(
            QtGui.QColor(*rgb)
        )
        painter.drawRect(
            rect
        )

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

    # lock
    def set_lock_enable(self, boolean):
        self._data.lock_enable = boolean
        if boolean is True:
            self._data.lock = _base._Data(
                flag=False,
                rect=QtCore.QRect(),
                file=_gui_core.GuiIcon.get('lock-watermark'),
            )

    def set_locked(self, boolean):
        if self._data.lock_enable is True:
            if boolean != self._data.lock.flag:
                self._data.lock.flag = boolean

    def is_locked(self):
        if self._data.lock_enable is True:
            return self._data.lock.flag
        return False

    # check
    def set_check_enable(self, boolean):
        self._data.check_enable = boolean
        if boolean is True:
            self._data.check = _base._Data(
                flag=False,
                rect=QtCore.QRect(),
                color=QtGui.QColor(*_gui_core.GuiRgba.LightPurple),

                file=_gui_core.GuiIcon.get('tag-filter-unchecked'),
                on_file=_gui_core.GuiIcon.get('tag-filter-checked'),
                off_file=_gui_core.GuiIcon.get('tag-filter-unchecked'),
            )

    def swap_check(self):
        self.set_checked(not self._data.check.flag)

        self.refresh_force()

    def set_checked(self, boolean):
        if self._data.check_enable is True:
            if boolean != self._data.check.flag:
                self._data.check.flag = boolean
                self._update_check()
                self.view.item_check_changed.emit()

    def is_checked(self):
        if self._data.check_enable is True:
            return self._data.check.flag
        return False

    def _update_check_state(self, boolean):
        if self._data.check_enable is True:
            if boolean != self._data.check.flag:
                self._data.check.flag = boolean
                self._update_check_icon()
                return True
            return False
        return False

    def _update_check_icon(self):
        self._data.check.file = [
            self._data.check.off_file,
            self._data.check.on_file
        ][self._data.check.flag]

    def _update_check(self):
        self._update_check_icon()
        self._update_check_extend()

    def _update_check_extend(self):
        pass

    # drag
    def set_drag_data(self, data):
        if data is not None:
            assert isinstance(data, dict)

            self._data.drag.enable = True
            self._data.drag.data = data

    def get_drag_data(self):
        return self._data.drag.data