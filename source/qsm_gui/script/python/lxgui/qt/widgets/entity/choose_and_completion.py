# coding:utf-8
import functools

import lxbasic.core as bsc_core

import lxbasic.pinyin as bsc_pinyin
# qt
from ....qt.core.wrap import *

from ....qt import core as _qt_core

from .... import core as _gui_core

from ...view_models.list import item as _vew_mdl_lst_item

from ...view_models.list import view as _vew_mdl_lst_view

from ...view_widgets.list import item as _vew_wgt_lst_item

from ...view_widgets.list import view as _vew_wgt_lst_view

from .. import base as _qt_wgt_base

from .. import scroll as _wgt_scroll

from ..entry import entry_for_constant as _wgt_ety_constant

from .. import utility as _wgt_utility

from .. import button as _wgt_button


class _EntityItemModel(_vew_mdl_lst_item.ListItemModel):
    def __init__(self, *args, **kwargs):
        super(_EntityItemModel, self).__init__(*args, **kwargs)

    def refresh_pixmap_cache(self):
        return self._pixmap_cache

    def update(self, rect):
        # check rect is change
        if rect != self._data.rect:
            # need rebuild instance
            self._data.rect = qt_rect(rect)

            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()

            bsc_w_0, bsc_h_0 = h, h

            bsc_x, bsc_y, bsc_w, bsc_h = x+2, y+2, bsc_w_0-3, bsc_h_0-3

            self._data.basic.rect.setRect(
                bsc_x, bsc_y, bsc_w, bsc_h
            )

            self._data.select.rect.setRect(
                x+1, y+1, w-2, h-2
            )
            self._data.hover.rect.setRect(
                x+1, y+1, w-2, h-2
            )
            # icon
            item_h = 20
            item_icon_w = 16

            txt_x, txt_y = x+h, y
            # lock
            if self._data.lock_enable is True:
                lck_w = lck_h = int(min(bsc_w, bsc_h)*.75)
                self._data.lock.rect.setRect(
                    bsc_x+(bsc_w-lck_w)/2, bsc_y+(bsc_h-lck_h)/2, lck_w, lck_h
                )

            cck_w = 0
            # check
            if self._data.check_enable is True:
                cck_w = 20
                self._data.check.rect.setRect(
                    txt_x+(cck_w-item_icon_w)/2+1, txt_y+(cck_w-item_icon_w)/2, item_icon_w, item_icon_w
                )

            # icon
            if self._data.icon_enable is True:
                self._data.icon.rect.setRect(
                    bsc_x, bsc_y, bsc_w-1, bsc_h-1
                )

            # name
            txt_w_sub = 0
            if txt_w_sub == 0:
                txt_offset = 2
            else:
                txt_offset = txt_w_sub+2

            self._data.name.rect.setRect(
                txt_x+txt_offset+1, txt_y, w-txt_w_sub-4, item_h
            )
            if self._data.subname_enable is True:
                self._data.subname.rect.setRect(
                    txt_x+txt_offset+1, txt_y+item_h, w-txt_w_sub-4, item_h
                )
            return True
        return False


class _QtEntityItem(_vew_wgt_lst_item.QtListItem):
    MODEL_CLS = _EntityItemModel

    def __init__(self, *args, **kwargs):
        super(_QtEntityItem, self).__init__(*args, **kwargs)


class _EntityViewModel(_vew_mdl_lst_view.ListViewModel):
    def __init__(self, *args, **kwargs):
        super(_EntityViewModel, self).__init__(*args, **kwargs)

    def set_item_frame_size(self, frm_w, frm_h):
        self._data.item.frame_width, self._data.item.frame_height = frm_w, frm_h

        self._data.item.text_height = _gui_core.GuiSize.ItemHeightDefault

        grid_w, grid_h = frm_w, frm_h

        self._data.item.grid_size.setWidth(grid_w)
        self._data.item.grid_size.setHeight(grid_h)
        # set grid size to -1 for disable grid size and update item
        self._widget.setGridSize(QtCore.QSize(-1, -1))
        self.update_all_items_size_hint()


class _QtEntityListView(_vew_wgt_lst_view._QtListView):
    MODEL_CLS = _EntityViewModel

    ITEM_CLS = _QtEntityItem

    def __init__(self, *args, **kwargs):
        super(_QtEntityListView, self).__init__(*args, **kwargs)


class _QtEntityChooseWidget(QtWidgets.QWidget):
    TOOL_BAR_W = 26

    CHUNK_SIZE_MINIMUM = 16
    THREAD_MAXIMUM = 128

    TAG_ALL = 'All'

    key_enter_pressed = qt_signal()
    key_escape_pressed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(_QtEntityChooseWidget, self).__init__(*args, **kwargs)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self._mrg = 4

        self._grid_lot = _qt_wgt_base.QtGridLayout(self)
        self._grid_lot.setContentsMargins(*[self._mrg]*4)
        self._grid_lot.setSpacing(2)

        # top
        self._top_scroll_box = _wgt_scroll.QtHScrollBox()
        self._grid_lot.addWidget(self._top_scroll_box, 0, 0, 1, 2)
        self._top_scroll_box._set_layout_align_left_or_top_()
        self._top_scroll_box.setFixedHeight(self.TOOL_BAR_W)

        # tag view
        self._tag_view = _QtEntityListView()
        self._grid_lot.addWidget(self._tag_view, 1, 0, 1, 1)
        self._tag_view.setFixedWidth(80)
        self._tag_view_model = self._tag_view._view_model
        self._tag_view_model.set_item_mode(self._tag_view_model.ItemMode.List)
        self._tag_view_model.set_item_frame_size(20, 20)
        # do not sort
        # self._tag_view_model.set_item_sort_enable(True)

        # view
        self._view = _QtEntityListView()
        self._grid_lot.addWidget(self._view, 1, 1, 1, 1)
        self._view_model = self._view._view_model
        self._view_model.set_item_mode(self._view_model.ItemMode.List)
        self._view_model.set_item_frame_size(40, 40)
        self._view_model.set_item_sort_enable(True)
        self._view_model.set_item_sort_enable(True)

        self._occ_current = self._view_model

        self._build_top_tools()
        self._tag_view.item_select_changed.connect(self._on_any_filer)

        self._name_texts = []
        self._subname_dict = {}
        self._tag_filter_dict = {}
        self._keyword_filter_dict = {}

        self._keyword_filter_entry.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self._keyword_filter_entry:
            if event.type() == QtCore.QEvent.FocusIn:
                self.update()
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() in {QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter}:
                    self.key_enter_pressed.emit()
                elif event.key() == QtCore.Qt.Key_Escape:
                    self.key_escape_pressed.emit()
        return False

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        mrg = self._mrg
        x, y, w, h = 0, 0, self.width(), self.height()

        f_x, f_y, f_w, f_h = x+1, y+1, w-2, h-2
        rect = QtCore.QRect(f_x, f_y, f_w, f_h)

        is_focus = self._keyword_filter_entry.hasFocus()
        pen = QtGui.QPen(QtGui.QColor(*[(71, 71, 71, 255), _gui_core.GuiRgba.LightAzureBlue][is_focus]))
        pen_width = [1, 2][is_focus]

        pen.setWidth(pen_width)
        painter.setPen(pen)
        painter.setBrush(QtGui.QColor(*_gui_core.GuiRgba.Dim))
        painter.drawRect(rect)

        tol_w = self.TOOL_BAR_W
        x_t, y_t, w_t, h_t = x+mrg, y+mrg, w-mrg*2, h-mrg*2

        top_rect = QtCore.QRect(
            x_t, y_t, w_t, tol_w
        )
        painter.setPen(QtGui.QColor(*_gui_core.GuiRgba.Basic))
        painter.setBrush(QtGui.QColor(*_gui_core.GuiRgba.Basic))
        painter.drawRect(top_rect)

        if self._keyword_filter_entry._get_value_():
            pass
        else:
            _qt_core.QtItemDrawBase._draw_name_text(
                painter,
                rect=top_rect,
                text=(
                    'press "Up" or "Down" to switch and press "Enter" to accept, '
                    'press "ESC" to cancel.'
                ),
                text_color=QtGui.QColor(*_gui_core.GuiRgba.TxtTemporary),
                text_option=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                text_font=_qt_core.QtFont.generate()
            )

        t_x = self._tag_view.x()+self._tag_view.width()

        line = QtCore.QLine(t_x, y_t+tol_w, t_x, y+h-mrg)
        painter.setPen(QtGui.QColor(*_gui_core.GuiRgba.Basic))
        painter.setBrush(QtGui.QColor(*_gui_core.GuiRgba.Transparent))
        painter.drawLine(line)

    def _set_data(self, data):
        self._name_texts = data.get('name_texts') or []
        self._subname_dict = data.get('subname_dict') or {}
        self._tag_filter_dict = data.get('tag_filter_dict') or {}
        self._keyword_filter_dict = data.get('keyword_filter_dict') or {}

        if self._name_texts:
            self._load()

    def _load(self):
        names_map = bsc_core.BscList.split_to(
            self._name_texts, self.THREAD_MAXIMUM, self.CHUNK_SIZE_MINIMUM
        )
        gui_thread_flag = 0

        ts = []
        for i_names in names_map:
            i_r = self._view._generate_thread_(
                functools.partial(
                    self._cache_fnc, i_names, gui_thread_flag
                ),
                self._build_fnc,
                post_fnc=self._view_model.update_widget
            )
            ts.append(i_r)

        [x.do_start() for x in ts]

        for i_name in self._to_tags(self._tag_filter_dict):
            i_path = u'/{}'.format(i_name)
            i_flag, i_item = self._tag_view_model.create_item(i_path)
            i_item_model = i_item._item_model
            i_item_model.set_icon_text(i_item_model.get_name())

    def _to_tags(self, tag_filter_dict):
        tags = list(set([i for k, v in tag_filter_dict.items() for i in v]))
        # sort tag by default, and make sure "all" is first
        tags = bsc_core.BscTexts.sort_by_number(tags)
        if self.TAG_ALL in tags:
            tags.remove(self.TAG_ALL)
            tags.insert(0, self.TAG_ALL)
        return tags

    def _cache_fnc(self, names, gui_thread_flag):
        args_list = []
        for i_name in names:
            i_subname = self._subname_dict.get(i_name)
            i_tag_filter_keys = self._tag_filter_dict.get(i_name)
            i_keyword_filter_keys = self._keyword_filter_dict.get(i_name)
            args_list.append((i_name, i_subname, i_tag_filter_keys, i_keyword_filter_keys))
        return [args_list, gui_thread_flag]

    def _build_fnc(self, data):
        if data:
            args_list, gui_thread_flag = data
            for i_args in args_list:
                i_name, i_subname, i_tag_filter_keys, i_keyword_filter_keys = i_args
                i_path = u'/{}'.format(i_name)
                i_flag, i_item = self._view_model.create_item(i_path)
                i_item_model = i_item._item_model

                i_item_model.set_icon_text(i_name)
                i_item_model.set_subname(i_subname)
                i_item_model.register_tag_filter_keys(i_tag_filter_keys)
                i_item_model.register_keyword_filter_keys(i_keyword_filter_keys)

                i_item_model.set_tool_tip(i_path)

    def _build_top_tools(self):
        self._keyword_filter_entry = _wgt_ety_constant.QtEntryForConstant(self)
        self._keyword_filter_entry.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self._top_scroll_box.addWidget(self._keyword_filter_entry)
        self._keyword_filter_entry.entry_value_changed.connect(self._on_any_filer)

        self._tag_view.setFocusProxy(self._keyword_filter_entry)
        self._view.setFocusProxy(self._keyword_filter_entry)
        self.setFocusProxy(self._keyword_filter_entry)

        self._keyword_filter_entry.key_right_pressed.connect(self._on_swap_occ_current)
        self._keyword_filter_entry.key_left_pressed.connect(self._on_swap_occ_current)
        self._keyword_filter_entry.key_up_pressed.connect(self._on_occ_previous)
        self._keyword_filter_entry.key_down_pressed.connect(self._on_occ_next)

        self._close_button = _wgt_button.QtIconPressButton()
        self._top_scroll_box.addWidget(self._close_button)
        self._close_button._set_icon_name_('window/close')

    def _get_tag_filter_key_src(self):
        return [x._item_model.get_name() for x in self._tag_view_model.get_selected_items()]

    def _on_any_filer(self):
        self._view_model.set_tag_filter_key_src(
            self._get_tag_filter_key_src()
        )
        self._view_model.set_keyword_filter_key_src(
            [self._keyword_filter_entry._get_value_()]
        )
        self._view_model.refresh_items_visible_by_any_filter()

    def _set_focus_in(self):
        self._keyword_filter_entry._set_entry_focus_in_()

    def _clear_keyword_filter(self):
        self._keyword_filter_entry._set_value_('')

    def _on_swap_occ_current(self):
        if self._occ_current == self._view_model:
            self._occ_current = self._tag_view_model
        else:
            self._occ_current = self._view_model

    def _on_occ_previous(self):
        self._occ_current.occurrence_item_previous()

    def _on_occ_next(self):
        self._occ_current.occurrence_item_next()

    def _connect_to_stack(self, widget):
        self._view.press_released.connect(widget._on_accept)
        self.key_enter_pressed.connect(widget._on_accept)
        self._close_button.press_clicked.connect(widget._on_cancel)
        self.key_escape_pressed.connect(widget._on_cancel)

    def _get_current_name(self):
        items = self._view_model.get_selected_items()
        if items:
            return items[0]._item_model.get_name()

    def _startup(self):
        self._set_focus_in()
        self._clear_keyword_filter()

    def _resize(self):
        w = self.width()
        tag_w = int(w*.25)
        self._tag_view.setFixedWidth(tag_w)


class QtEntityChooseStack(QtWidgets.QWidget):
    value_accepted = qt_signal(str)

    @classmethod
    def _get_popup_pos_from(cls, widget):
        rect = widget.rect()
        p = widget.mapToGlobal(rect.topLeft())
        o_x, o_y = 0, 0
        return p.x()+o_x, p.y()+o_y

    @classmethod
    def _get_popup_size_from(cls, widget):
        rect = widget.rect()
        return rect.width(), rect.height()

    def __init__(self, *args, **kwargs):
        super(QtEntityChooseStack, self).__init__(*args, **kwargs)

        self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowDoesNotAcceptFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        lot = QtWidgets.QVBoxLayout(self)
        lot.setAlignment(QtCore.Qt.AlignTop)
        lot.setContentsMargins(*[0]*4)
        lot.setSpacing(0)

        self._stack = QtWidgets.QStackedWidget()
        lot.addWidget(self._stack)

        self._input_widget = None

        self._dict = {}

    def _load_data(self, data):
        key = bsc_core.BscHash.to_hash_key(data)
        if key in self._dict:
            gui = self._dict[key]

        # new
        else:
            gui = _QtEntityChooseWidget()
            self._stack.addWidget(gui)
            gui._set_data(data)
            gui._connect_to_stack(self)
            self._dict[key] = gui

        gui._startup()
        self._stack.setCurrentWidget(gui)
        return gui

    def _popup(self):
        x, y = self._get_popup_pos_from(self._input_widget)
        w, h = self._get_popup_size_from(self._input_widget)
        self.show()

        self.setGeometry(
            x, y, w, 320
        )

        self._resize_current()

    def _set_input_widget(self, widget):
        self._input_widget = widget

    def _resize_current(self):
        gui = self._stack.currentWidget()
        if gui:
            gui._resize()

    def _on_cancel(self):
        self.hide()

    def _on_accept(self):
        gui = self._stack.currentWidget()
        if gui:
            name = gui._get_current_name()
            if name:
                self.value_accepted.emit(name)
        self._on_cancel()


class QtEntityCompletionWidget(QtWidgets.QWidget):
    TOOL_BAR_W = 26

    value_accepted = qt_signal(str)

    @classmethod
    def _get_popup_pos_from(cls, widget):
        rect = widget.rect()
        p = widget.mapToGlobal(rect.bottomLeft())
        o_x, o_y = 0, 0
        return p.x()+o_x, p.y()+o_y

    @classmethod
    def _get_popup_size_from(cls, widget):
        rect = widget.rect()
        return rect.width(), rect.height()

    def __init__(self, *args, **kwargs):
        super(QtEntityCompletionWidget, self).__init__(*args, **kwargs)

        self.setWindowFlags(
            QtCore.Qt.ToolTip
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.WindowDoesNotAcceptFocus
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setMinimumSize(40, 40)
        self.setMaximumSize(166667, 166667)

        self._mrg = 4

        self._grid_lot = _qt_wgt_base.QtGridLayout(self)
        self._grid_lot.setContentsMargins(*[self._mrg]*4)
        self._grid_lot.setSpacing(2)

        # top
        self._top_scroll_box = _wgt_scroll.QtHScrollBox()
        self._grid_lot.addWidget(self._top_scroll_box, 0, 0, 1, 2)
        self._top_scroll_box._set_layout_align_left_or_top_()
        self._top_scroll_box.setFixedHeight(self.TOOL_BAR_W)

        # view
        self._view = _QtEntityListView()
        self._grid_lot.addWidget(self._view, 1, 1, 1, 1)
        self._view_model = self._view._view_model
        self._view_model.set_item_mode(self._view_model.ItemMode.List)
        self._view_model.set_item_frame_size(40, 40)
        self._view_model.set_item_sort_enable(True)

        self._view_model.set_single_selection()

        self.setFocusProxy(self._view)

        self._build_top_tools()

        self._input_widget = None

        self._input_pos = 0, 0

        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(50)
        self._timer.timeout.connect(self._auto_cancel)
        self._timer.start()

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            pass
        return False

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        mrg = self._mrg
        x, y, w, h = 0, 0, self.width(), self.height()

        f_x, f_y, f_w, f_h = x+1, y+1, w-2, h-2
        rect = QtCore.QRect(f_x, f_y, f_w, f_h)

        is_focus = True
        pen = QtGui.QPen(QtGui.QColor(*[(71, 71, 71, 255), _gui_core.GuiRgba.LightAzureBlue][is_focus]))
        pen_width = [1, 2][is_focus]

        pen.setWidth(pen_width)
        painter.setPen(pen)
        painter.setBrush(QtGui.QColor(*_gui_core.GuiRgba.Dim))
        painter.drawRect(rect)

        tol_w = self.TOOL_BAR_W
        x_t, y_t, w_t, h_t = x+mrg, y+mrg, w-mrg*2, h-mrg*2

        top_rect = QtCore.QRect(
            x_t, y_t, w_t, tol_w
        )
        painter.setPen(QtGui.QColor(*_gui_core.GuiRgba.Basic))
        painter.setBrush(QtGui.QColor(*_gui_core.GuiRgba.Basic))
        painter.drawRect(top_rect)

        _qt_core.QtItemDrawBase._draw_name_text(
            painter,
            rect=top_rect,
            text=(
                'press "Up" or "Down" to switch and press "Enter" to accept, '
                'press "ESC" to cancel.'
            ),
            text_color=QtGui.QColor(*_gui_core.GuiRgba.TxtTemporary),
            text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
            text_font=_qt_core.QtFont.generate()
        )

    def _build_top_tools(self):
        wgt = _wgt_utility.QtTranslucentWidget()
        wgt.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self._top_scroll_box.addWidget(wgt)

        self._close_button = _wgt_button.QtIconPressButton()
        self._top_scroll_box.addWidget(self._close_button)
        self._close_button._set_icon_name_('window/close')

        self._close_button.press_clicked.connect(self._on_cancel)
        self._view.press_released.connect(self._on_accept)

    def _set_data(self, data, keyword):
        self._view_model.restore()

        self._name_texts = data.get('name_texts') or []
        self._keyword = keyword

        self._subname_dict = data.get('subname_dict') or {}
        self._keyword_filter_dict = data.get('keyword_filter_dict') or {}

        if self._name_texts and self._keyword:
            return self._load_and_filter()
        return False

    def _load_and_filter(self):
        matches = []
        texts_src = {self._keyword}

        for i_name in self._name_texts:
            if i_name in self._keyword_filter_dict:
                i_texts_tgt = self._keyword_filter_dict[i_name]
            else:
                i_texts_tgt = [i_name]

            i_enable, i_flag = bsc_pinyin.KeywordFilter.generate_hidden_args(texts_src, i_texts_tgt)
            if i_enable:
                if i_flag is False:
                    matches.append(i_name)

        if matches:
            matches = bsc_core.BscTexts.sort_by_number(matches)
            for i_idx, i_name in enumerate(matches[:50]):
                i_path = u'/{}'.format(i_name)
                i_flag, i_item = self._view_model.create_item(i_path)

                i_item_model = i_item._item_model
                i_item_model.set_icon_text(i_name)
                if i_name in self._subname_dict:
                    i_item_model.set_subname(self._subname_dict[i_name])

            self._view_model.scroll_to_item_top_auto()
            return True
        return False

    def _get_current_name(self):
        items = self._view_model.get_selected_items()
        if items:
            return items[0]._item_model.get_name()

    def _on_cancel(self):
        self.hide()

    def _on_accept(self):
        name = self._get_current_name()
        if name:
            self.value_accepted.emit(name)
        self._on_cancel()

    def _popup(self):
        x, y = self._get_popup_pos_from(self._input_widget)
        w, h = self._get_popup_size_from(self._input_widget)

        self.show()
        self._input_pos = (x, y)

        h = self._compute_height()
        self.setGeometry(
            x, y, w, h
        )

    def _set_input_widget(self, widget):
        self._input_widget = widget

    def _auto_cancel(self):
        """
        method for close when input is move
        @return: bool
        """
        if self.isVisible():
            pos = self._get_popup_pos_from(self._input_widget)
            # cancel when pos changed
            if pos != self._input_pos:
                self._input_pos = pos
                self._on_cancel()
                return True
            # cancel when focus lost
            if self._input_widget._entry_widget.hasFocus() is False:
                self._on_cancel()
                return True
        return False

    def _compute_height(self):
        widget = self._view
        rects = [widget.visualItemRect(widget.item(i)) for i in range(widget.count())[:5]]
        return sum([i.height() for i in rects])+self.TOOL_BAR_W+self._mrg*2+3

    def _on_occ_previous(self):
        self._view_model.occurrence_item_previous()

    def _on_occ_next(self):
        self._view_model.occurrence_item_next()
