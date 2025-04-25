# coding:utf-8
import copy

import six

import lxbasic.core as bsc_core

import lxbasic.pinyin as bsc_pinyin

from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core


class ItemThreadPoolFactory:

    @staticmethod
    def push(fnc):
        def wrapper(self, *args, **kwargs):
            self._view._generate_thread_(*fnc(self, *args, **kwargs)).start()
            return None
        return wrapper


class AbsItemModel(object):
    Status = _gui_core.GuiItemStatus

    SortOrder = _gui_core.GuiItemSortOrder
    SortKey = _gui_core.GuiItemSortKey

    GroupKey = _gui_core.GuiItemGroupKey

    TagFilterMode = _gui_core.GuiTagFilterMode

    NUMBER_TEXT_FORMAT = '{}'

    NAME_H = 20

    @classmethod
    def _draw_status_frame(cls, painter, rect, color):
        w, h = rect.width(), rect.height()
        x_c, y_c = int(w/2), int(h/2)
        r_c = min(x_c, y_c)
        p1, p2, p3, p4 = rect.topLeft(), rect.topRight(), rect.bottomRight(), rect.bottomLeft()
        (x1, y1), (x2, y2), (x3, y3), (x4, y4) = (p1.x(), p1.y()), (p2.x(), p2.y()), (p3.x(), p3.y()), (p4.x(), p4.y())
        point_coords = (
            # top left
            (((x1, y1+r_c), (x1, y1), (x1+r_c, y1)), (x1, y1), (x1+r_c, y1+r_c)),
            # top right
            (((x2-r_c, y2), (x2, y2), (x2, y2+r_c)), (x2, y2), (x2-r_c, y1+r_c)),
            # bottom right
            (((x3, y3-r_c), (x3, y3), (x3-r_c, y3)), (x3, y3), (x3-r_c, y3-r_c)),
            # bottom left
            (((x4+r_c, y4), (x4, y4), (x4, y4-r_c)), (x4, y4), (x4+r_c, y4-r_c))
        )
        for i_points, i_s, i_e in point_coords:
            i_start = QtCore.QPoint(*i_s)
            i_end = QtCore.QPoint(*i_e)
            i_c = QtGui.QLinearGradient(i_start, i_end)
            i_c.setColorAt(0, color)
            i_c.setColorAt(.5, QtGui.QColor(0, 0, 0, 0))
            i_c.setColorAt(1, QtGui.QColor(0, 0, 0, 0))
            i_brush = QtGui.QBrush(i_c)
            i_pen = QtGui.QPen(i_brush, 2)
            i_pen.setJoinStyle(QtCore.Qt.RoundJoin)
            painter.setPen(i_pen)
            painter.setBrush(_qt_core.QtRgba.Transparent)
            i_path = QtGui.QPainterPath()
            i_points_f = [QtCore.QPointF(x, y) for x, y in i_points]
            i_path.addPolygon(QtGui.QPolygonF(i_points_f))
            painter.drawPath(i_path)

    @classmethod
    def _draw_time_text(cls, painter, rect, text):
        painter.setPen(QtGui.QColor(223, 223, 223))
        painter.drawText(rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, text)

    @classmethod
    def _draw_text(cls, painter, rect, text, color, option=None):
        text = painter.fontMetrics().elidedText(
            text,
            QtCore.Qt.ElideMiddle,
            rect.width(),
            QtCore.Qt.TextShowMnemonic
        )
        painter.setPen(color)
        option = option or QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter

        painter.drawText(rect, option, text)

    @classmethod
    def _draw_rect(cls, painter, rect, color):
        painter.setPen(color)
        painter.setBrush(color)
        painter.drawRect(rect)

    @classmethod
    def _draw_rect_0(cls, painter, rect, color):
        painter.setPen(QtGui.QColor(0, 0, 0, 0))
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

        # main
        self._data.rect = qt_rect()

        # basic
        self._data.basic = _gui_core.DictOpt(
            rect=qt_rect(),
            size=QtCore.QSize(),
        )

        # text option for draw
        self._data.text = _gui_core.DictOpt(
            font=_qt_core.QtFont.generate(size=8),
            color=QtGui.QColor(223, 223, 223),
            action_color=QtGui.QColor(31, 31, 31),

            # all text height
            height=20
        )

        # frame for draw
        self._data.frame = _gui_core.DictOpt(
            rect=qt_rect(),
            color=QtGui.QColor(*_gui_core.GuiRgba.Dark),
            brush=QtGui.QBrush(QtGui.QColor(*_gui_core.GuiRgba.Dim))
        )

        # index
        self._data.index_enable = True
        self._data.index = 0

        # path
        self._data.path = _gui_core.DictOpt(
            text=None
        )

        # category
        self._data.category_enable = False
        self._data.category = _gui_core.DictOpt(
            text=None
        )

        # type
        self._data.type_enable = False
        self._data.type = _gui_core.DictOpt(
            text=None
        )

        # name
        self._data.name_enable = True
        self._data.name = _gui_core.DictOpt(
            text=None,
            text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
            rect=qt_rect(),
        )

        # subname
        self._data.subname_enable = False
        self._data.subname = _gui_core.DictOpt(
            text=None,
            text_option=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
            rect=qt_rect(),
            color=QtGui.QColor(*_gui_core.GuiRgba.TxtTemporary)
        )

        # mtime
        self._data.mtime_enable = False
        self._data.user_enable = False

        # number
        self._data.number_enable = False
        self._data.number = _gui_core.DictOpt(
            flag=False,
            value=0,
            text=None,
            rect=qt_rect(),
        )

        # status
        self._data.status_enable = False

        # lock
        self._data.lock_enable = False

        # icon
        self._data.icon_enable = False
        self._data.icon = _gui_core.DictOpt(
            file_flag=False,
            file=None,

            text_flag=False,
            text=None,
            
            image_flag=False,
            image=None,

            pixmap_flag=False,
            pixmap=None,

            rect=qt_rect(),
        )

        # color
        self._data.color_enable = False

        # hover
        self._data.hover = _gui_core.DictOpt(
            enable=True,
            flag=False,
            rect=qt_rect(),
            color=QtGui.QColor(*_gui_core.GuiRgba.LightOrange),
        )

        # select
        self._data.select = _gui_core.DictOpt(
            enable=True,
            flag=False,
            rect=qt_rect(),
            color=QtGui.QColor(*_gui_core.GuiRgba.LightAzureBlue),
        )

        # check
        self._data.check_enable = False
        self._data.check = None

        # drag
        self._data.drag = _gui_core.DictOpt(
            enable=False,
            data=None
        )

        # tool tip
        self._data.tool_tip = _gui_core.DictOpt(
            enable=False,
            flag=False,
            text=None,
            css=None
        )

        # show
        self._data.show = _gui_core.DictOpt(
            load_flag=False,

            cache_fnc=None,
            build_fnc=None,
        )

        # menu
        self._data.menu = _gui_core.DictOpt(
            content=None,
            content_generate_fnc=None,
            data=None,
            data_generate_fnc=None,
            name_dict=dict()
        )

        # force
        self._data.force_hidden_flag = False
        self._data.force_refresh_flag = True

        # keyword filter
        self._data.keyword_filter = _gui_core.DictOpt(
            key_tgt_set=set()
        )

        # tag filter
        self._data.tag_filter = _gui_core.DictOpt(
            key_tgt_set=set(),
            mode=self.TagFilterMode.MatchOne
        )

        # assign
        self._data.assign_enable = True
        self._data.assign = _gui_core.DictOpt(
            path_set=set(),
            path_set_pre=set(),
            file=None,
            directory=None,
            properties=None
        )

        # sort
        self._data.sort_enable = False

        # property
        self._data.property_dict = dict()

        # press
        self._data.press_enable = True
        self._data.press = _gui_core.DictOpt(
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

    def draw(self, painter, option, index):
        raise NotImplementedError()

    def get_force_hidden_flag(self):
        return self._data.force_hidden_flag

    # path
    def set_path(self, text):
        self._data.path.text = text

    def get_path(self):
        return self._data.path.text

    # category
    def set_category_enable(self, boolean):
        self._data.category_enable = boolean

    def set_category(self, text):
        if text is not None:
            self._data.category_enable = True
            self._data.category.text = text
            return True
        self._data.category_enable = False
        return False

    def get_category(self):
        return self._data.category.text

    # type
    def set_type_enable(self, boolean):
        self._data.type_enable = boolean

    def set_type(self, text):
        if text is not None:
            self._data.type_enable = True
            self._data.type.text = text
            return True
        self._data.type_enable = False
        return False

    def get_type(self):
        return self._data.type.text

    # index
    def set_index(self, index):
        self._data.index = index

    def get_index(self):
        return self._data.index

    # name
    def set_name(self, text):
        if text is not None:
            self._data.name_enable = True
            self._data.name.text = text
            # todo: set name to item?
            self._update_name(text)
            return True
        self._data.name_enable = False
        return False

    def _update_name(self, text):
        raise NotImplementedError()

    def get_name(self):
        return self._data.name.text

    # subname
    def set_subname(self, text):
        if text is not None:
            self._data.subname_enable = True
            self._data.subname.text = text
            return True

        self._data.subname_enable = False
        return False

    # mtime
    def set_mtime_enable(self, boolean):
        self._data.mtime_enable = boolean
        if boolean is True:
            self._data.mtime = _gui_core.DictOpt(
                timestamp=0,
                text='',
                text_color=_qt_core.QtRgba.TxtMtime,
                text_option=QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter,
                rect=qt_rect(),
            )

    def set_mtime(self, timestamp):
        if self._data.mtime_enable is False:
            self.set_mtime_enable(True)

        self._data.mtime.timestamp = timestamp
        self._data.mtime.text = bsc_core.BscTimePrettify.to_prettify_by_timestamp_(
            timestamp, language=_gui_core.GuiUtil.get_language()
        )

    # user
    def set_user_enable(self, boolean):
        self._data.user_enable = boolean
        if boolean is True:
            self._data.user = _gui_core.DictOpt(
                text='',
                text_color=_qt_core.QtRgba.TxtUser,
                text_option=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter,
                rect=qt_rect(),
            )

    def set_user(self, user_name):
        if self._data.user_enable is False:
            self.set_user_enable(True)

        self._data.user.text = user_name

    # number
    def set_number_enable(self, boolean):
        self._data.number_enable = boolean

    def get_number_enable(self):
        return self._data.number_enable

    def set_number(self, value):
        if value is not None:
            self._data.number_enable = True
            self._data.number.value = value
            self._data.number.text = self.NUMBER_TEXT_FORMAT.format(value)
            if value > 0:
                self._data.number.flag = True
                # todo: do not set italic?
                # self._data.text.font.setItalic(False)
                self._data.text.color = QtGui.QColor(223, 223, 223)
                self._data.text.action_color = QtGui.QColor(31, 31, 31)

                # self._font.setItalic(False)
            else:
                self._data.number.flag = False
                # self._data.text.font.setItalic(True)
                self._data.text.color = QtGui.QColor(127, 127, 127)
                self._data.text.action_color = QtGui.QColor(127, 127, 127)

                # self._font.setItalic(True)

            self._update_number(value)
            return True

        self._data.number_enable = False

        self._data.text.color = QtGui.QColor(223, 223, 223)
        self._data.text.action_color = QtGui.QColor(31, 31, 31)
        return False

    def get_number(self):
        return self._data.number.value

    def get_number_flag(self):
        if self._data.number_enable is True:
            return self._data.number.flag
        return False

    def _update_number(self, value):
        pass

    # color
    def set_color_enable(self, boolean):
        self._data.color_enable = boolean
        if boolean is True:
            self._data.color = _gui_core.DictOpt(
                rgb=(255, 255, 255),
                hex='FFFFFF',
                rect=qt_rect()
            )

    def set_color_rgb(self, rgb):
        if self._data.color_enable is False:
            self.set_color_enable(True)

        if self._data.color_enable is True:
            self._data.color.rgb = rgb
            self._data.color.hex = bsc_core.BscColor.rgb2hex(*rgb)

    # icon
    def set_icon_name(self, icon_name):
        if icon_name:
            self.set_icon_file(_gui_core.GuiIcon.get(icon_name))

    def set_icon(self, icon):
        if isinstance(icon, QtGui.QIcon):
            pixmap = icon.pixmap(20, 20)
            self._data.icon_enable = True
            self._data.icon.pixmap_flag = True
            self._data.icon.pixmap = pixmap

    def set_icon_file(self, file_path):
        # do not check file exists
        if file_path:
            self._data.icon_enable = True
            self._data.icon.file_flag = True
            self._data.icon.file = file_path

    def set_icon_text(self, text):
        if text:
            self._data.icon_enable = True
            self._data.icon.text_flag = True
            self._data.icon.text = text
            
    def set_icon_data(self, data):
        if data:
            # noinspection PyBroadException
            try:
                image = QtGui.QImage()
                image.loadFromData(data)
                if image.isNull() is False:
                    self._data.icon_enable = True
                    self._data.icon.image_flag = True
                    self._data.icon.image = image
            except Exception:
                pass

    # assign
    def set_assign_path_set(self, path_set):
        if path_set is not None:
            assert isinstance(path_set, set)

            self._data.assign_enable = True
            self._data.assign.path_set_pre = copy.copy(self._data.assign.path_set)
            self._data.assign.path_set = path_set
            self.set_number(len(path_set))
            return True

        self._data.assign_enable = False
        self._data.assign.path_set.clear()
        self.set_number(None)
        return False

    def get_assign_path_set_for(self):
        return self._data.assign.path_set

    def _update_assign_path_set(self, path_set_addition, path_set_deletion):
        self._data.assign_enable = True

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
        if self._data.assign_enable is True:
            parent_item = self.get_parent()
            if parent_item:
                path_set = self._data.assign.path_set
                path_set_pre = self._data.assign.path_set_pre

                path_set_addition = path_set.difference(path_set_pre)
                path_set_deletion = path_set_pre.difference(path_set)

                parent_item._item_model._update_assign_path_set(path_set_addition, path_set_deletion)
                parent_item._item_model._update_assign_path_to_parent()
    
    def _update_assign_path_from_descendants(self):
        descendants = self.get_descendants()
        for i_item in descendants:
            print(i_item)

    def set_assign_directory(self, directory_path):
        self._data.assign.directory = directory_path

    def get_assign_directory(self):
        return self._data.assign.directory

    def set_assign_file(self, file_path):
        self._data.assign.file = file_path

    def get_assign_file(self):
        return self._data.assign.file

    def set_assign_properties(self, properties):
        self._data.assign.properties = properties

    def get_assign_properties(self):
        return self._data.assign.properties

    def set_assign_data(self, key, value):
        self._data.assign[key] = value

    def get_assign_data(self, key):
        return self._data.assign.get(key)

    # status
    def set_status_enable(self, boolean):
        self._data.status_enable = boolean
        if boolean is True:
            self._data.status = _gui_core.DictOpt(
                file=_gui_core.GuiIcon.get('star'),
                value=self.Status.Normal,
                rect=qt_rect()
            )

        self._update_status_rect(self._data.rect)
        self.update_view()

    def set_status(self, status):
        if self._data.status_enable is False:
            self.set_status_enable(True)

        self._data.status.value = status
        self._update_status_rect(self._data.rect)
        self.update_view()

    def clear_status(self):
        self.set_status(self.Status.Normal)

    def get_status(self):
        if self._data.status_enable is True:
            return self._data.status.value

    def _update_status_rect(self, rect):
        pass

    def _get_status_color(self):
        if self._data.status_enable is True:
            status = self._data.status.value
            if status == self.Status.Warning:
                return _qt_core.QtRgba.Yellow
            elif status == self.Status.Error:
                return _qt_core.QtRgba.Red
            elif status == self.Status.Correct:
                return _qt_core.QtRgba.Green
            elif status == self.Status.Disable:
                return _qt_core.QtRgba.TxtDisable

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

    def set_menu_name_dict(self, dict_):
        if isinstance(dict_, dict):
            self._data.menu.name_dict = dict_

    def get_menu_name_dict(self):
        return self._data.menu.name_dict

    # sort
    def set_sort_enable(self, boolean):
        self._data.sort_enable = boolean
        if boolean is True:
            self._data.sort = _gui_core.DictOpt(
                key=self.SortKey.Name,
                order=self.SortOrder.Ascending,
                dict=dict()
            )

    def set_sort_dict(self, dict_):
        if self._data.sort_enable is True:
            self._data.sort.dict.update(dict_)

    def _generate_current_sort_name_text(self):
        if self._data.sort_enable is True:
            key = self._data.sort.key
            if key == self.SortKey.Default:
                return str(self._data.index).zfill(4)
            elif key == self.SortKey.Category:
                return self._data.category.text
            elif key == self.SortKey.Type:
                return self._data.type.text
            elif key == self.SortKey.Name:
                return self._data.name.text
            elif key == self.SortKey.Number:
                return str(self._data.number.value).zfill(6)
            return self._data.name.text
        return self._data.name.text

    def apply_sort_key(self, sort_key):
        if self._data.sort_enable is True:
            self._data.sort.key = sort_key

            self._update_name(self._generate_current_sort_name_text())

    def apply_sort_order(self, sort_order):
        if self._data.sort_enable is True:
            self._data.sort.order = sort_order

            self._update_name(self._generate_current_sort_name_text())

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
    def generate_keyword_filter_hidden_args(self, key_src_set):
        # todo: use match all mode then, maybe use match one mode also
        if key_src_set:
            contexts_src = map(bsc_core.ensure_unicode, key_src_set)
            context_tgt = self.get_keyword_filter_context()
            context_tgt = context_tgt.lower()
            for i_text in contexts_src:
                # fixme: chinese word
                # do not encode, keyword can be use unicode
                i_text = i_text.lower()
                if '*' in i_text:
                    i_filter_key = six.u('*{}*').format(i_text.lstrip('*').rstrip('*'))
                    if not bsc_core.BscFnmatch.filter([context_tgt], i_filter_key):
                        return True, True
                else:
                    if i_text not in context_tgt:
                        return True, True
            return True, False
        return False, False

    def register_keyword_filter_keys(self, texts):
        if not texts:
            return

        keys = []
        # add pinyin to keyword filter
        for i_text in texts:
            if not i_text:
                continue

            i_texts = bsc_pinyin.Text.split_any_to_words_extra(i_text)
            keys.append(i_text)
            keys.extend(i_texts)

        self._data.keyword_filter.key_tgt_set = set(keys)

    def get_keyword_filter_key_tgt_set(self):
        _ = self._data.keyword_filter.key_tgt_set
        if _:
            return _
        return {bsc_core.ensure_unicode(self.get_name())}

    def get_keyword_filter_context(self):
        return '+'.join(self.get_keyword_filter_key_tgt_set())

    # tag filter
    def register_tag_filter_keys(self, texts):
        if not texts:
            return

        self._data.tag_filter.key_tgt_set = set(texts)

    def generate_tag_filter_hidden_args(self, key_src_set):
        key_tgt_set = self._data.tag_filter.key_tgt_set
        mode = self._data.tag_filter.mode
        if key_tgt_set:
            if mode == self.TagFilterMode.MatchAll:
                for i_key_tgt in key_tgt_set:
                    if i_key_tgt not in key_src_set:
                        return True, True
                return True, False
            elif mode == self.TagFilterMode.MatchOne:
                for i_key_tgt in key_tgt_set:
                    if i_key_tgt in key_src_set:
                        return True, False
                return True, True
            return True, False
        return False, False

    @classmethod
    def _draw_icon_by_file(cls, painter, rect, file_path):
        if file_path is None:
            return
        if file_path.endswith('.svg'):
            cls._draw_svg(painter, rect, file_path)
        else:
            cls._draw_image_file(painter, rect, file_path)

    @classmethod
    def _draw_icon_by_pixmap(cls, painter, rect, pixmap):
        pxm_scaled = pixmap.scaled(
            rect.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
        )
        painter.drawPixmap(rect, pxm_scaled)

    @classmethod
    def _draw_svg(cls, painter, rect, svg_path):
        svg_render = QtSvg.QSvgRenderer(svg_path)
        svg_render.render(painter, QtCore.QRectF(rect))

    @classmethod
    def _draw_image_file(cls, painter, rect, file_path):
        pixmap = QtGui.QPixmap()
        pixmap.load(file_path)
        if pixmap.isNull() is False:
            pxm_scaled = pixmap.scaled(
                rect.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
            )
            painter.drawPixmap(rect, pxm_scaled)

    @classmethod
    def _fill_icon(cls, painter, rect, file_path, color):
        if file_path is None:
            return
        if file_path.endswith('.svg'):
            cls._fill_svg(painter, rect, file_path, color)
        else:
            cls._fill_image(painter, rect, file_path)

    @classmethod
    def _fill_svg(cls, painter, rect, file_path, color):
        w, h = rect.width(), rect.height()
        i_new = QtGui.QImage(
            w, h, QtGui.QImage.Format_ARGB32
        )
        mask_color = QtCore.Qt.black

        i_new.fill(mask_color)
        ptr = QtGui.QPainter(i_new)
        svg_render = QtSvg.QSvgRenderer(file_path)
        svg_render.render(ptr, QtCore.QRectF(0, 0, w, h))
        ptr.end()

        pxm_mask = QtGui.QPixmap(i_new).createMaskFromColor(mask_color)
        p_over = QtGui.QPixmap(i_new)
        p_over.fill(color)
        p_over.setMask(pxm_mask)
        painter.drawPixmap(rect, p_over)

    @classmethod
    def _fill_image(cls, painter, rect, file_path):
        pass

    @classmethod
    def _draw_color(cls, painter, rect, rgb):
        painter.setPen(
            QtGui.QColor(*_gui_core.GuiRgba.Gray)
        )
        painter.setBrush(
            QtGui.QColor(*rgb)
        )
        painter.drawRect(
            rect
        )

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
    
    # select
    def _update_select(self, flag):
        if flag != self._data.select.flag:
            self._data.select.flag = flag
    
    def focus_select(self):
        self._item.setSelected(True)

    def set_selected(self, boolean=True):
        self._item.setSelected(boolean)

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
            self._data.lock = _gui_core.DictOpt(
                flag=False,
                rect=qt_rect(),
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
            self._data.check = _gui_core.DictOpt(
                flag=False,
                rect=qt_rect(),
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

    def do_delete(self):
        raise NotImplementedError()
