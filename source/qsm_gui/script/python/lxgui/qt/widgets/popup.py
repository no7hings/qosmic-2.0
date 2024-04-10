# coding=utf-8
import six

import os

import lxbasic.core as bsc_core
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import core as gui_qt_core

from .. import abstracts as gui_qt_abstracts
# qt widgets
from ..widgets import utility as gui_qt_wgt_utility

from ..widgets import button as gui_qt_wgt_button

from ..widgets import chart as gui_qt_wgt_chart

from ..widgets import entry as gui_qt_wgt_entry


# use for popup
#   constant
class _QtViewForPopup(gui_qt_abstracts.AbsQtListWidget):
    def __init__(self, *args, **kwargs):
        super(_QtViewForPopup, self).__init__(*args, **kwargs)
        self.setDragDropMode(self.DragOnly)
        self.setDragEnabled(False)
        self.setSelectionMode(QtWidgets.QListWidget.SingleSelection)
        self.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.setViewMode(QtWidgets.QListWidget.ListMode)
        self.setPalette(gui_qt_core.GuiQtDcc.generate_qt_palette())

    def paintEvent(self, event):
        pass

    def _compute_height_maximum_(self, row_maximum, includes=None):
        adjust = 1+8
        if includes is not None:
            rects = [self.visualItemRect(i) for i in includes[:row_maximum]]
        else:
            rects = [self.visualItemRect(self.item(i)) for i in range(self.count())[:row_maximum]]
        if rects:
            return sum([i.height() for i in rects])+adjust
        return 20+adjust


#   icon
class _QtViewAsIconForPopup(gui_qt_abstracts.AbsQtListWidget):
    def __init__(self, *args, **kwargs):
        super(_QtViewAsIconForPopup, self).__init__(*args, **kwargs)
        self.setDragDropMode(self.DragOnly)
        self.setDragEnabled(False)
        self.setSelectionMode(QtWidgets.QListWidget.SingleSelection)
        self.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.setViewMode(QtWidgets.QListWidget.IconMode)
        self.setPalette(gui_qt_core.GuiQtDcc.generate_qt_palette())

    # noinspection PyUnusedLocal
    def _compute_height_maximum_(self, row_maximum, includes=None):
        # w, h = self.viewport().width(), self.viewport().height()
        c_w, c_h = self.gridSize().width(), self.gridSize().height()
        # print w, c_w
        # row_count = int(w/c_w)
        # print row_count
        adjust = 1+5
        return c_h*row_maximum+adjust


class _AbsQtPopupAsChoose(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtFrameBaseDef,
    gui_qt_abstracts.AbsQtPopupBaseDef,
):
    HEIGHT_MAX = 160
    TAG_ALL = 'All'

    QT_POPUP_VIEW_CLS = _QtViewForPopup

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        h_top_tbr = self._h_popup_top_toolbar
        spacing = 2
        if self._popup_style == self.PopupStyle.FromFrame:
            spacing = 2
            c_x, c_y = x+1, y+1
            c_w, c_h = w-2, h-2

            self._rect_frame_draw.setRect(
                c_x, c_y, c_w, c_h
            )

            self._rect_popup_top_toolbar.setRect(
                c_x+2, c_y, c_w-4, h_top_tbr
            )
            tbr_w = c_w
            # close button
            self.__popup_cancel_button.setGeometry(
                c_x+c_w-h_top_tbr*1, c_y, h_top_tbr, h_top_tbr
            )
            tbr_w -= (h_top_tbr+spacing)

            if self._popup_item_multiply_is_enable is True:
                self._popup_all_checked_button.show()
                self._popup_all_unchecked_button.show()
                self._popup_all_checked_button.setGeometry(
                    c_x+c_w-(h_top_tbr*3+spacing*2), c_y, h_top_tbr, h_top_tbr
                )
                tbr_w -= (h_top_tbr+spacing)
                self._popup_all_unchecked_button.setGeometry(
                    c_x+c_w-(h_top_tbr*2+spacing*1), c_y, h_top_tbr, h_top_tbr
                )
                tbr_w -= (h_top_tbr+spacing)

            self._rect_popup_top_toolbar_tool_tip.setRect(
                c_x, c_y, tbr_w-h_top_tbr, h_top_tbr
            )
            self._popup_keyword_filter_entry.setGeometry(
                c_x, c_y, tbr_w-h_top_tbr, h_top_tbr
            )

            c_y += h_top_tbr
            c_h -= h_top_tbr

            if self._popup_item_tag_filter_is_enable is True:
                t_f_w = c_w*self._popup_tag_filter_width_percent
                self._popup_tag_filter_view.setGeometry(
                    c_x+1, c_y+1, t_f_w-2, c_h-2
                )
                self._rect_tag_filter_view.setRect(
                    c_x, c_y, t_f_w, c_h
                )
                c_x += t_f_w
                c_w -= t_f_w
            #
            self._popup_tag_filter_view.updateGeometries()

            self._popup_view.setGeometry(
                c_x+1, c_y+1, c_w-2, c_h-2
            )
            self._popup_view.updateGeometries()
        else:
            side = self._popup_side
            margin = self._popup_margin
            shadow_radius = self._popup_shadow_radius

            c_x, c_y = x+margin+side+1, y+margin+side+1
            c_w, c_h = w-margin*2-side*2-shadow_radius-2, h-margin*2-side*2-shadow_radius-2

            tbr_w = c_w

            self._rect_popup_top_toolbar.setRect(
                c_x+2, c_y, c_w-4, h_top_tbr
            )
            self._rect_popup_top_toolbar_tool_tip.setRect(
                c_x, c_y, tbr_w-h_top_tbr, h_top_tbr
            )
            self._popup_keyword_filter_entry.show()
            self._popup_keyword_filter_entry.setGeometry(
                c_x, c_y, tbr_w-h_top_tbr, h_top_tbr
            )
            # close button
            self.__popup_cancel_button.setGeometry(
                c_x+c_w-h_top_tbr*1, c_y, h_top_tbr, h_top_tbr
            )
            tbr_w -= (h_top_tbr+spacing)
            c_y += h_top_tbr
            c_h -= h_top_tbr
            #
            self._popup_view.setGeometry(
                c_x, c_y, c_w, c_h
            )
            self._popup_view.updateGeometries()

    def __init__(self, *args, **kwargs):
        super(_AbsQtPopupAsChoose, self).__init__(*args, **kwargs)
        # use popup?
        self.setWindowFlags(QtCore.Qt.ToolTip | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowDoesNotAcceptFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self._init_frame_base_def_(self)
        self._init_popup_base_def_(self)
        # icon
        self._popup_item_icon_file_path = None
        self._popup_item_icon_file_path_dict = {}
        # image
        self._popup_item_image_url_dict = {}
        # filter
        self._popup_item_keyword_filter_dict = {}
        self._popup_item_tag_filter_dict = {}

        self._popup_use_as_icon_choose = False

        self._w_popup_item, self._h_popup_item = 20, 20
        self._popup_tag_filter_item_width, self._popup_tag_filter_item_height = 20, 20

        self.__popup_cancel_button = gui_qt_wgt_button.QtIconPressButton(self)
        self.__popup_cancel_button._set_name_text_('cancel popup')
        self.__popup_cancel_button._set_icon_file_path_(gui_core.GuiIcon.get('cancel'))
        self.__popup_cancel_button._set_icon_frame_draw_size_(18, 18)
        self.__popup_cancel_button._set_tool_tip_text_(
            '"LMB-click" to cancel'
        )
        self.__popup_cancel_button.press_clicked.connect(self._do_popup_close_)
        #
        self._popup_item_multiply_is_enable = False
        self._popup_all_checked_button = gui_qt_wgt_button.QtIconPressButton(self)
        self._popup_all_checked_button.hide()
        self._popup_all_checked_button._set_icon_file_path_(gui_core.GuiIcon.get('all_checked'))
        self._popup_all_checked_button._set_icon_frame_draw_size_(18, 18)
        self._popup_all_checked_button.setToolTip(
            '"LMB-click" to checked all'
        )
        self._popup_all_checked_button.press_clicked.connect(self._execute_popup_all_checked_)
        #
        self._popup_all_unchecked_button = gui_qt_wgt_button.QtIconPressButton(self)
        self._popup_all_unchecked_button.hide()
        self._popup_all_unchecked_button._set_icon_file_path_(gui_core.GuiIcon.get('all_unchecked'))
        self._popup_all_unchecked_button._set_icon_frame_draw_size_(18, 18)
        self._popup_all_unchecked_button.setToolTip(
            '"LMB-click" to unchecked all'
        )
        self._popup_all_unchecked_button.press_clicked.connect(self._execute_popup_all_unchecked_)
        # keyword filter
        self._popup_item_keyword_filter_is_enable = False
        self._popup_keyword_filter_entry = gui_qt_wgt_entry.QtEntryAsConstant(self)
        self._popup_keyword_filter_entry.hide()
        self._popup_keyword_filter_entry._set_entry_enable_(True)
        self._popup_keyword_filter_entry.setAlignment(
            QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter
        )
        self._popup_keyword_filter_entry.installEventFilter(self)
        # tag filter
        self._popup_item_tag_filter_is_enable = False
        self._popup_tag_filter_width_percent = 0.375
        self._rect_tag_filter_view = QtCore.QRect()
        self._popup_tag_filter_view = _QtViewForPopup(self)
        self._popup_tag_filter_view.hide()
        self._popup_tag_filter_view.setGridSize(
            QtCore.QSize(self._w_popup_item, self._h_popup_item)
        )
        self._popup_tag_filter_view.setSpacing(2)
        self._popup_tag_filter_view.setUniformItemSizes(True)
        # popup view
        self._popup_view = self.QT_POPUP_VIEW_CLS(self)
        #
        self._popup_item_row_maximum = 10
        self._popup_view.setGridSize(
            QtCore.QSize(self._w_popup_item, self._h_popup_item)
        )
        self._popup_view.setSpacing(2)
        self._popup_view.setUniformItemSizes(True)
        #
        self._choose_index = None
        #
        self._frame_border_color = gui_qt_core.QtBackgroundColors.Light
        self._hovered_frame_border_color = gui_qt_core.QtBackgroundColors.Hovered
        self._selected_frame_border_color = gui_qt_core.QtBackgroundColors.Hovered
        #
        self._frame_background_color = gui_qt_core.QtBackgroundColors.Dark

        self._read_only_mark = None

        self._popup_name_text = None

        self.setToolTip(
            gui_qt_core.GuiQtUtil.generate_tool_tip_css(
                'choose popup',
                [
                    'press "Up" or "Down" to switch',
                    'press "Enter" to accept or "ESC" to cancel',
                    'when tag filter is enable, press "ALT + Up" or "ALT + Down" to switch current tag filter item',
                ]
            )
        )

        self._popup_quick_start_enable = False

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)

        if self._popup_style == self.PopupStyle.FromFrame:
            painter._draw_frame_by_rect_(
                self._rect_frame_draw,
                border_color=gui_qt_core.QtColors.PopupBorder,
                background_color=self._frame_background_color,
                border_radius=1,
                border_width=2
            )
            painter._draw_line_by_points_(
                point_0=self._rect_popup_top_toolbar.bottomLeft(),
                point_1=self._rect_popup_top_toolbar.bottomRight(),
                border_color=self._frame_border_color,
            )
            c = self._popup_view._get_all_item_count_()
            if self._popup_item_keyword_filter_is_enable is True:
                if not self._popup_keyword_filter_entry.text():
                    tool_tip_text = 'all is {}, press any word to filter, hover to show more tips ...'.format(c)
                else:
                    tool_tip_text = ''
            else:
                if self._popup_name_text:
                    tool_tip_text = self._popup_name_text
                else:
                    tool_tip_text = 'all is {}, hover to show more tips ...'.format(c)

            if tool_tip_text:
                painter._draw_text_by_rect_(
                    rect=self._rect_popup_top_toolbar_tool_tip,
                    text=tool_tip_text,
                    font=gui_qt_core.QtFonts.NameNormal,
                    font_color=gui_qt_core.QtColors.TextDisable,
                    text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                )
            #
            if self._popup_item_tag_filter_is_enable is True:
                painter._draw_line_by_points_(
                    point_0=self._rect_tag_filter_view.topRight(),
                    point_1=self._rect_tag_filter_view.bottomRight(),
                    border_color=self._frame_border_color,
                )
        else:
            x, y = 0, 0
            w, h = self.width(), self.height()
            #
            bck_rect = QtCore.QRect(
                x, y, w-1, h-1
            )
            #
            painter._draw_popup_frame_(
                bck_rect,
                margin=self._popup_margin,
                side=self._popup_side,
                shadow_radius=self._popup_shadow_radius,
                region=self._popup_region,
                border_color=gui_qt_core.QtColors.PopupBorder,
                background_color=self._frame_background_color,
                border_width=2
            )
            painter._draw_line_by_points_(
                point_0=self._rect_popup_top_toolbar.bottomLeft(),
                point_1=self._rect_popup_top_toolbar.bottomRight(),
                border_color=self._frame_border_color,
            )
            #
            if not self._popup_keyword_filter_entry.text():
                painter._draw_text_by_rect_(
                    self._rect_popup_top_toolbar_tool_tip,
                    'entry to filter ...',
                    font=gui_qt_core.QtFonts.NameNormal,
                    font_color=gui_qt_core.QtColors.TextDisable,
                    text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self._entry_widget:
            if event.type() == QtCore.QEvent.FocusOut:
                self._do_popup_close_()
            elif event.type() == QtCore.QEvent.WindowDeactivate:
                self._do_popup_close_()
            elif event.type() == QtCore.QEvent.Hide:
                self._do_popup_close_()
            elif event.type() == QtCore.QEvent.InputMethod:
                self._popup_keyword_filter_entry.inputMethodEvent(event)
            elif event.type() == QtCore.QEvent.KeyPress:
                if self._get_popup_is_activated_():
                    if event.key() == QtCore.Qt.Key_Up and event.modifiers() == QtCore.Qt.AltModifier:
                        self._do_popup_tag_filter_view_scroll_to_pre_()
                        return True
                    elif event.key() == QtCore.Qt.Key_Up:
                        self._do_popup_view_scroll_to_pre_()
                        return True
                    elif event.key() == QtCore.Qt.Key_Down and event.modifiers() == QtCore.Qt.AltModifier:
                        self._do_popup_tag_filter_view_scroll_to_next_()
                        return True
                    elif event.key() == QtCore.Qt.Key_Down:
                        self._do_popup_view_scroll_to_next_()
                        return True
                    elif event.key() == QtCore.Qt.Key_Escape:
                        self._do_popup_close_()
                        return True
                    elif event.key() in {QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter}:
                        self._do_popup_end_()
                        return True
                    else:
                        self._popup_keyword_filter_entry.keyPressEvent(event)
                        # ignore entry widget key press
                        return True
                else:
                    if self._popup_quick_start_enable is True:
                        if event.key() == QtCore.Qt.Key_Down and event.modifiers() == QtCore.Qt.AltModifier:
                            self._do_popup_start_()
        return False

    def _set_entry_widget_(self, widget):
        self._entry_widget = widget
        self._entry_widget.installEventFilter(self._widget)
        self._widget.setFocusProxy(self._entry_widget)

        self._popup_keyword_filter_entry.setFocusProxy(self._entry_widget)
        self._popup_tag_filter_view.setFocusProxy(self._entry_widget)
        self._popup_view.setFocusProxy(self._entry_widget)

    # extra data
    def _set_popup_item_icon_file_path_(self, file_path):
        self._popup_item_icon_file_path = file_path

    def _set_popup_item_icon_file_path_dict_(self, dict_):
        self._popup_item_icon_file_path_dict = dict_

    def _set_popup_item_icon_file_path_for_(self, text, file_path):
        self._popup_item_icon_file_path_dict[text] = file_path

    def _set_popup_item_image_url_dict_(self, dict_):
        self._popup_item_image_url_dict = dict_

    def _set_popup_item_keyword_filter_dict_(self, dict_):
        self._popup_item_keyword_filter_dict = dict_

    def _set_popup_item_tag_filter_dict_(self, dict_):
        self._popup_item_tag_filter_dict = dict_

    def _restore_popup_(self):
        # icon
        self._popup_item_icon_file_path = None
        self._popup_item_icon_file_path_dict = {}
        # image
        self._popup_item_image_url_dict = {}
        # filter
        self._popup_item_keyword_filter_dict = {}
        self._popup_item_tag_filter_dict = {}

    def _set_popup_item_keyword_filter_enable_(self, boolean):
        self._popup_item_keyword_filter_is_enable = boolean
        if boolean is True:
            self._popup_keyword_filter_entry.show()
            self._popup_keyword_filter_entry.entry_value_changed.connect(
                self._do_popup_filter_
            )

    def _set_popup_item_tag_filter_enable_(self, boolean):
        self._popup_item_tag_filter_is_enable = boolean
        if boolean is True:
            self._popup_tag_filter_view.show()
            self._popup_tag_filter_view.itemSelectionChanged.connect(
                self._do_popup_filter_
            )

    def _set_popup_item_multiply_enable_(self, boolean):
        self._popup_item_multiply_is_enable = boolean

    def _get_popup_item_multiply_is_enable_(self):
        return self._popup_item_multiply_is_enable

    def _set_popup_name_text_(self, text):
        self._popup_name_text = text

    def _do_popup_view_scroll_to_pre_(self):
        if self._popup_is_activated is True:
            self._popup_view._scroll_to_pre_item_()

    def _do_popup_view_scroll_to_next_(self):
        if self._popup_is_activated is True:
            self._popup_view._scroll_to_next_item_()

    def _do_popup_tag_filter_view_scroll_to_pre_(self):
        if self._popup_is_activated is True:
            self._popup_tag_filter_view._scroll_to_pre_item_()

    def _do_popup_tag_filter_view_scroll_to_next_(self):
        if self._popup_is_activated is True:
            self._popup_tag_filter_view._scroll_to_next_item_()

    # show deferred
    @staticmethod
    def _popup_item_show_deferred_fnc_(item, item_widget, data):
        def cache_fnc_():
            return data

        def build_fnc_(data_):
            _image_url, = data_
            item_widget._set_image_url_(_image_url)

        item._set_item_show_fnc_(cache_fnc_, build_fnc_)
        item_widget._set_image_draw_enable_(True)

    @staticmethod
    def _popup_item_show_deferred_fnc_1_(item, item_widget, data):
        def cache_fnc_():
            return data

        def build_fnc_(data_):
            _icon_name, = data_
            if _icon_name == '':
                _icon_name = 'state-disable'
            item_widget._set_icon_name_(_icon_name)

        item._set_item_show_fnc_(cache_fnc_, build_fnc_)
        item_widget._set_image_draw_enable_(True)

    def _get_popup_width_(self, texts):
        count = len(texts)
        _ = max([self.fontMetrics().width(i) for i in texts])+32
        _count_width = self.fontMetrics().width(str(count))
        if count > self._popup_item_row_maximum:
            return _+_count_width+24
        return _+_count_width

    def _do_popup_start_(self):
        if self._popup_is_activated is False:
            self._popup_view._set_clear_()
            self._popup_tag_filter_view._set_clear_()
            self._popup_keyword_filter_entry._set_clear_()
            values = self._get_popup_values_()
            if values and isinstance(values, (tuple, list)):
                # icon
                icon_file_path = self._popup_item_icon_file_path
                icon_file_path_dict = self._popup_item_icon_file_path_dict
                # image
                image_url_dict = self._popup_item_image_url_dict
                # filter
                keyword_filter_dict = self._popup_item_keyword_filter_dict
                tag_filter_dict = self._popup_item_tag_filter_dict
                #
                values_cur = self._get_popup_values_current_()
                for index, i_value in enumerate(values):
                    i_item_widget = gui_qt_wgt_utility._QtHItem()
                    i_item = gui_qt_wgt_utility.QtListWidgetItem()
                    i_item.setSizeHint(QtCore.QSize(self._w_popup_item, self._h_popup_item))

                    self._popup_view.addItem(i_item)
                    self._popup_view.setItemWidget(i_item, i_item_widget)
                    i_item._connect_item_show_()

                    i_item_widget._set_name_text_(i_value)
                    i_item_widget._set_tool_tip_('"LMB-click" to choose')
                    # use multiply choose
                    if self._get_popup_item_multiply_is_enable_() is True:
                        i_item_widget._set_check_action_enable_(True)
                        i_item_widget._set_check_enable_(True)

                    if self._popup_use_as_icon_choose is True:
                        self._popup_item_show_deferred_fnc_1_(
                            i_item, i_item_widget, [i_value]
                        )
                    else:
                        if i_value in image_url_dict:
                            self._popup_item_show_deferred_fnc_(
                                i_item, i_item_widget, [image_url_dict[i_value]]
                            )
                        else:
                            if icon_file_path:
                                i_item_widget._set_icon_file_path_(icon_file_path)
                            else:
                                if i_value in icon_file_path_dict:
                                    i_icon_file_path = icon_file_path_dict[i_value]
                                    i_item_widget._set_icon_file_path_(i_icon_file_path)
                                else:
                                    i_item_widget._set_icon_name_text_(i_value)
                    #
                    if i_value in keyword_filter_dict:
                        i_filter_keys = keyword_filter_dict[i_value]
                        i_item._update_item_keyword_filter_keys_tgt_(i_filter_keys)
                        i_item_widget._set_name_texts_(i_filter_keys)
                        i_item_widget._set_tool_tip_('"LMB-click" to choose')
                    else:
                        i_item._update_item_keyword_filter_keys_tgt_([i_value])
                    #
                    if i_value in tag_filter_dict:
                        i_filter_keys = tag_filter_dict[i_value]
                        i_item._set_item_tag_filter_mode_(i_item.TagFilterMode.MatchOne)
                        i_item._update_item_tag_filter_keys_tgt_(i_filter_keys)
                    #
                    if values_cur:
                        # auto select last item
                        if isinstance(values_cur, (tuple, list)):
                            if i_value == values_cur[-1]:
                                i_item.setSelected(True)
                        elif isinstance(values_cur, six.string_types):
                            if i_value == values_cur:
                                i_item.setSelected(True)
                        # scroll to selected
                        self._popup_view._set_scroll_to_selected_item_top_()
                    else:
                        pass
                    #
                    i_item_widget.press_clicked.connect(self._do_popup_end_)
                # tag filter
                if self._popup_item_tag_filter_is_enable is True:
                    tags = list(set([i for k, v in tag_filter_dict.items() for i in v]))
                    tags = bsc_core.RawTextsMtd.sort_by_initial(tags)
                    if self.TAG_ALL in tags:
                        tags.remove(self.TAG_ALL)
                        tags.insert(0, self.TAG_ALL)
                    for i_tag in tags:
                        i_item_widget = gui_qt_wgt_utility._QtHItem()
                        i_item = gui_qt_wgt_utility.QtListWidgetItem()
                        i_item.setSizeHint(
                            QtCore.QSize(self._popup_tag_filter_item_width, self._popup_tag_filter_item_height)
                        )
                        #
                        self._popup_tag_filter_view.addItem(i_item)
                        self._popup_tag_filter_view.setItemWidget(i_item, i_item_widget)
                        i_item._connect_item_show_()
                        #
                        i_item_widget._set_name_text_(i_tag)
                        i_item_widget._set_icon_name_text_(i_tag)
                        i_item_widget._set_tool_tip_text_(i_tag)
                        #
                        i_item_widget._set_item_tag_filter_keys_src_add_(i_tag)

                press_pos = self._get_popup_pos_from_(self._get_entry_frame_widget_())
                width, height = self._get_popup_size_from_(self._get_entry_frame_widget_())
                item_count = int(self.HEIGHT_MAX/self._h_popup_item)
                height_max_0 = self._popup_view._compute_height_maximum_(item_count)
                height_max_1 = self._popup_tag_filter_view._compute_height_maximum_(item_count)
                height_max = max([height_max_0, height_max_1])
                height_max += self._h_popup_top_toolbar

                if self._popup_style == self.PopupStyle.FromFrame:
                    self._show_popup_(
                        press_pos,
                        (width, height_max)
                    )
                else:
                    desktop_rect = gui_qt_core.GuiQtUtil.get_qt_desktop_rect()
                    press_rect = self._get_popup_press_rect_()
                    press_point = self._compute_popup_press_point_(
                        self._get_entry_frame_widget_(), press_rect
                    )
                    height_max = self._popup_view._compute_height_maximum_(self._popup_item_row_maximum)
                    height_max += self._h_popup_top_toolbar
                    popup_width = self._get_popup_width_(values)
                    popup_width = max(self._popup_width_minimum, popup_width)
                    self._show_popup_as_style_0_(
                        press_point, press_rect,
                        desktop_rect,
                        popup_width,
                        height_max
                    )

                self._entry_widget._set_focused_(True)

                self._popup_is_activated = True
                # show
                self._popup_view._refresh_view_all_items_viewport_showable_()
                self._popup_tag_filter_view._refresh_view_all_items_viewport_showable_()

                if isinstance(self._entry_widget, QtWidgets.QLineEdit):
                    self._read_only_mark = self._entry_widget.isReadOnly()
                    self._entry_widget.setReadOnly(True)

    def _do_popup_end_(self):
        selected_item_widgets = self._popup_view._get_selected_item_widgets_()
        if selected_item_widgets:
            texts = [i._get_name_text_() for i in selected_item_widgets]
            self.user_popup_values_accepted.emit(texts)
            self.user_popup_value_accepted.emit(texts[0])
            #
            if self._get_popup_item_multiply_is_enable_() is True:
                checked_item_widgets = self._popup_view._get_checked_item_widgets_()
                if checked_item_widgets:
                    texts = [i._get_name_text_() for i in checked_item_widgets]
                    self.user_popup_values_accepted.emit(texts)
                    self.user_popup_value_accepted.emit(texts[0])
            #
            self.user_popup_finished.emit()
        #
        self._do_popup_close_()

    def _set_popup_item_size_(self, w, h):
        self._w_popup_item, self._h_popup_item = w, h
        self._popup_view.setGridSize(
            QtCore.QSize(self._w_popup_item, self._h_popup_item)
        )
        self._popup_view.verticalScrollBar().setSingleStep(h)

    def _set_popup_tag_filter_item_size_(self, w, h):
        self._popup_tag_filter_item_width, self._popup_tag_filter_item_height = w, h
        self._popup_tag_filter_view.setGridSize(
            QtCore.QSize(self._popup_tag_filter_item_width, self._popup_tag_filter_item_height)
        )

    def _do_popup_filter_(self):
        # tag filter
        selected_item_widgets = self._popup_tag_filter_view._get_selected_item_widgets_()
        if selected_item_widgets:
            item_src = selected_item_widgets[0]
            tags = [item_src._get_name_text_()]
            self._popup_view._set_view_tag_filter_data_src_(tags)
        # keyword filter
        self._popup_view._set_view_keyword_filter_data_src_([self._popup_keyword_filter_entry.text()])
        #
        self._popup_view._refresh_view_items_visible_by_any_filter_()
        self._popup_view._refresh_view_all_items_viewport_showable_()
        #
        if self._popup_auto_resize_is_enable is True:
            self._execute_auto_resize_()

    def _execute_popup_all_checked_(self):
        [i._set_checked_(True) for i in self._popup_view._get_all_item_widgets_() if i._get_is_visible_() is True]

    def _execute_popup_all_unchecked_(self):
        [i._set_checked_(False) for i in self._popup_view._get_all_item_widgets_() if i._get_is_visible_() is True]

    def _do_popup_close_(self):
        if isinstance(self._entry_widget, QtWidgets.QLineEdit):
            if self._read_only_mark is not None:
                self._entry_widget.setReadOnly(self._read_only_mark)
        #
        self._set_popup_activated_(False)

    def _execute_auto_resize_(self):
        visible_items = self._popup_view._get_all_visible_items_()
        press_pos = self._get_popup_pos_from_(self._entry_frame_widget)
        width, height = self._get_popup_size_from_(self._entry_frame_widget)
        height_max = self._popup_view._compute_height_maximum_(self._popup_item_row_maximum, includes=visible_items)
        height_max += self._h_popup_top_toolbar
        #
        self._show_popup_(
            press_pos,
            (width, height_max)
        )

    def _get_popup_values_(self):
        raise NotImplementedError()

    def _get_popup_values_current_(self):
        raise NotImplementedError()


class QtPopupAsChoose(_AbsQtPopupAsChoose):
    def __init__(self, *args, **kwargs):
        super(QtPopupAsChoose, self).__init__(*args, **kwargs)
        self._popup_quick_start_enable = True

    def _get_popup_values_(self):
        return self.parent()._bridge_choose_get_popup_texts_()

    def _get_popup_values_current_(self):
        return self.parent()._bridge_choose_get_popup_texts_current_()


class QtPopupAsHistory(_AbsQtPopupAsChoose):
    def __init__(self, *args, **kwargs):
        super(QtPopupAsHistory, self).__init__(*args, **kwargs)

    def _get_popup_values_(self):
        return self.parent()._bridge_history_get_popup_texts_()

    def _get_popup_values_current_(self):
        return self.parent()._bridge_history_get_popup_texts_current_()


# choose for icon
class QtPopupAsChooseForIcon(_AbsQtPopupAsChoose):
    QT_POPUP_VIEW_CLS = _QtViewAsIconForPopup

    def __init__(self, *args, **kwargs):
        super(QtPopupAsChooseForIcon, self).__init__(*args, **kwargs)
        self._popup_quick_start_enable = True

        self._set_popup_item_size_(40, 40)
        self._popup_item_row_maximum = 5

        self._popup_use_as_icon_choose = True

    def _get_popup_values_(self):
        return self.parent()._bridge_choose_get_popup_texts_()

    def _get_popup_values_current_(self):
        return self.parent()._bridge_choose_get_popup_texts_current_()


class QtPopupAsCompletion(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtFrameBaseDef,
    gui_qt_abstracts.AbsQtPopupBaseDef,
):
    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        c_x, c_y = x+1, y+1
        c_w, c_h = w-2, h-2
        h_top_tbr = self._h_popup_top_toolbar
        spacing = 2
        #
        self._rect_frame_draw.setRect(
            c_x, c_y, c_w, c_h
        )
        #
        self._rect_frame_draw.setRect(
            c_x, c_y, c_w, c_h
        )
        tbr_w = c_w
        #
        self._rect_popup_top_toolbar.setRect(
            c_x+2, c_y, c_w-4, h_top_tbr
        )
        self._rect_popup_top_toolbar_tool_tip.setRect(
            c_x, c_y, tbr_w-h_top_tbr, h_top_tbr
        )
        tbr_w = c_w
        # close button
        self.__popup_cancel_button.setGeometry(
            c_x+c_w-h_top_tbr*1, c_y, h_top_tbr, h_top_tbr
        )
        tbr_w -= (h_top_tbr+spacing)
        c_y += h_top_tbr
        c_h -= h_top_tbr

        self._popup_view.setGeometry(
            c_x+1, c_y+1, c_w-2, c_h-2
        )
        self._popup_view.updateGeometries()

    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtPopupAsCompletion, self).__init__(*args, **kwargs)
        # use tool tip
        self.setWindowFlags(QtCore.Qt.ToolTip | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        #
        self._init_frame_base_def_(self)
        self._init_popup_base_def_(self)
        #
        self.__popup_cancel_button = gui_qt_wgt_button.QtIconPressButton(self)
        self.__popup_cancel_button._set_name_text_('cancel popup')
        self.__popup_cancel_button._set_icon_file_path_(gui_core.GuiIcon.get('cancel'))
        self.__popup_cancel_button._set_icon_frame_draw_size_(18, 18)
        self.__popup_cancel_button.press_clicked.connect(self._do_popup_close_)
        self.__popup_cancel_button._set_tool_tip_text_(
            '"LMB-click" to cancel'
        )
        #
        self._popup_view = _QtViewForPopup(self)
        #
        self._popup_item_row_maximum = 10
        self._w_popup_item, self._h_popup_item = 20, 20
        self._popup_view.setGridSize(
            QtCore.QSize(self._w_popup_item, self._h_popup_item)
        )
        self._popup_view.setSpacing(2)
        self._popup_view.setUniformItemSizes(True)
        self._popup_view.itemClicked.connect(
            self._do_popup_end_
        )
        #
        self._choose_index = None
        #
        self._frame_border_color = gui_qt_core.QtBackgroundColors.Light
        self._hovered_frame_border_color = gui_qt_core.QtBackgroundColors.Hovered
        self._selected_frame_border_color = gui_qt_core.QtBackgroundColors.Hovered
        #
        self._frame_background_color = gui_qt_core.QtBackgroundColors.Dark

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)
        #
        painter._draw_frame_by_rect_(
            self._rect_frame_draw,
            border_color=gui_qt_core.QtColors.PopupBorder,
            background_color=self._frame_background_color,
            border_radius=1,
            border_width=2
        )
        painter._draw_line_by_points_(
            point_0=self._rect_popup_top_toolbar.bottomLeft(),
            point_1=self._rect_popup_top_toolbar.bottomRight(),
            border_color=self._frame_border_color,
        )

        c = self._popup_view._get_all_item_count_()
        if c:
            painter._draw_text_by_rect_(
                self._rect_popup_top_toolbar_tool_tip,
                (
                    'matching {}, press "Up" or "Down" to switch and press "Enter" to accept, '
                    'press "ESC" to cancel ...'
                ).format(c),
                font=gui_qt_core.QtFonts.NameNormal,
                font_color=gui_qt_core.QtColors.TextDisable,
                text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
            )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self._entry_widget:
            if event.type() == QtCore.QEvent.FocusOut:
                self._do_popup_close_()
            elif event.type() == QtCore.QEvent.KeyPress:
                if self._get_popup_is_activated_():
                    if event.key() == QtCore.Qt.Key_Up:
                        self._do_popup_view_scroll_to_pre_()
                        return True
                    elif event.key() == QtCore.Qt.Key_Down:
                        self._do_popup_view_scroll_to_next_()
                        return True
                    elif event.key() == QtCore.Qt.Key_Escape:
                        self._do_popup_close_()
                        return True
                    elif event.key() in {QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter}:
                        self._do_popup_end_()
                        return True
        return False

    def _set_entry_widget_(self, widget):
        self._entry_widget = widget
        self._entry_widget.installEventFilter(self._widget)
        self._widget.setFocusProxy(self._entry_widget)

        self._popup_view.setFocusProxy(self._entry_widget)

    def _do_popup_view_scroll_to_pre_(self):
        if self._popup_is_activated is True:
            self._popup_view._scroll_to_pre_item_()

    def _do_popup_view_scroll_to_next_(self):
        if self._popup_is_activated is True:
            self._popup_view._scroll_to_next_item_()

    def _do_popup_start_(self, *args, **kwargs):
        if self._entry_widget._get_choose_popup_is_activated_() is True:
            return
        input_widget = self.parent()
        self._popup_view._set_clear_()
        values = input_widget._generate_completion_texts_()
        if values:
            has_match = False
            text_current = self._entry_widget._get_value_()
            for index, i_text in enumerate(values):
                i_item_widget = gui_qt_wgt_utility._QtHItem()
                i_item = gui_qt_wgt_utility.QtListWidgetItem()
                i_item.setSizeHint(
                    QtCore.QSize(self._w_popup_item, self._h_popup_item)
                )
                #
                self._popup_view.addItem(i_item)
                self._popup_view.setItemWidget(i_item, i_item_widget)
                i_item._connect_item_show_()
                #
                i_item_widget._set_name_text_(i_text)
                i_item_widget._set_index_(index)
                if self._use_as_storage is True:
                    if os.path.isdir(i_text):
                        i_item_widget._set_icon_(
                            gui_qt_core.GuiQtDcc.get_qt_folder_icon(use_system=True)
                        )
                    elif os.path.isfile(i_text):
                        i_item_widget._set_icon_(
                            gui_qt_core.GuiQtDcc.get_qt_file_icon(i_text)
                        )
                    else:
                        i_item_widget._set_icon_name_text_(i_text)
                else:
                    i_item_widget._set_icon_name_text_(i_text)

                #
                if text_current == i_text:
                    has_match = True
                    i_item.setSelected(True)
            #
            if has_match is False:
                self._popup_view._get_all_items_()[0].setSelected(True)

            press_pos = self._get_popup_pos_0_(self._entry_frame_widget)
            width, height = self._get_popup_size_from_(self._entry_frame_widget)
            height_max = self._popup_view._compute_height_maximum_(self._popup_item_row_maximum)
            height_max += self._h_popup_top_toolbar

            self._show_popup_(
                press_pos,
                (width, height_max)
            )

            self._popup_view._set_scroll_to_selected_item_top_()

            self._entry_widget._set_focused_(True)

            self._popup_is_activated = True
        else:
            self._do_popup_close_()

    def _do_popup_end_(self, *args, **kwargs):
        selected_item_widget = self._popup_view._get_selected_item_widget_()
        if selected_item_widget:
            text = selected_item_widget._get_name_text_()
            #
            self.user_popup_value_accepted.emit(text)
        #
        self.user_popup_finished.emit()
        #
        self._do_popup_close_()

    def _do_popup_close_(self):
        self._set_popup_activated_(False)


class QtPopupAsChooseForGuide(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtFrameBaseDef,
    gui_qt_abstracts.AbsQtPopupBaseDef,
):
    def __init__(self, *args, **kwargs):
        super(QtPopupAsChooseForGuide, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.ToolTip | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #
        self.setPalette(gui_qt_core.GuiQtDcc.generate_qt_palette())
        #
        self._init_frame_base_def_(self)
        self._init_popup_base_def_(self)
        #
        self._popup_keyword_filter_entry = gui_qt_wgt_entry.QtEntryAsConstant(self)
        self._popup_keyword_filter_entry.hide()
        self._popup_keyword_filter_entry._set_entry_enable_(True)
        self._popup_keyword_filter_entry.setAlignment(
            QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter
        )
        self._popup_keyword_filter_entry.entry_value_changed.connect(
            self._do_popup_filter_
        )
        #
        self.__popup_cancel_button = gui_qt_wgt_button.QtIconPressButton(self)
        self.__popup_cancel_button._set_name_text_('close popup')
        self.__popup_cancel_button._set_icon_file_path_(gui_core.GuiIcon.get('close'))
        self.__popup_cancel_button._set_icon_hover_color_(gui_qt_core.QtBackgroundColors.DeleteHovered)
        self.__popup_cancel_button.press_clicked.connect(self._do_popup_close_)
        self.__popup_cancel_button._set_tool_tip_text_(
            '"LMB-click" to close'
        )
        #
        self._popup_view = _QtViewForPopup(self)
        #
        self._popup_item_row_maximum = 10
        self._w_popup_item, self._h_popup_item = 20, 20
        #
        self._popup_view.setGridSize(QtCore.QSize(self._w_popup_item, self._h_popup_item))
        self._popup_view.setSpacing(2)
        self._popup_view.setUniformItemSizes(True)
        self._popup_view.itemClicked.connect(
            self._do_popup_end_
        )
        #
        self._choose_index = None
        #
        self._frame_border_color = gui_qt_core.QtBackgroundColors.Light
        self._hovered_frame_border_color = gui_qt_core.QtBackgroundColors.Hovered
        self._selected_frame_border_color = gui_qt_core.QtBackgroundColors.Selected
        #
        self._frame_background_color = gui_qt_core.QtBackgroundColors.Dark

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        side = self._popup_side
        margin = self._popup_margin
        shadow_radius = self._popup_shadow_radius
        #
        x, y = 0, 0
        w, h = self.width(), self.height()

        h_top_tbr = self._h_popup_top_toolbar
        spacing = 2

        c_x, c_y = x+margin+side+1, y+margin+side+1
        c_w, c_h = w-margin*2-side*2-shadow_radius-2, h-margin*2-side*2-shadow_radius-2

        tbr_w = c_w

        self._rect_popup_top_toolbar.setRect(
            c_x+2, c_y, c_w-4, h_top_tbr
        )
        self._rect_popup_top_toolbar_tool_tip.setRect(
            c_x, c_y, tbr_w-h_top_tbr, h_top_tbr
        )
        self._popup_keyword_filter_entry.show()
        self._popup_keyword_filter_entry.setGeometry(
            c_x, c_y, tbr_w-h_top_tbr, h_top_tbr
        )
        # close button
        self.__popup_cancel_button.setGeometry(
            c_x+c_w-h_top_tbr*1, c_y, h_top_tbr, h_top_tbr
        )
        tbr_w -= (h_top_tbr+spacing)
        c_y += h_top_tbr
        c_h -= h_top_tbr
        #
        self._popup_view.setGeometry(
            c_x, c_y, c_w, c_h
        )
        self._popup_view.updateGeometries()

    def paintEvent(self, event):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        bck_rect = QtCore.QRect(
            x, y, w-1, h-1
        )
        painter = gui_qt_core.QtPainter(self)
        #
        painter._draw_popup_frame_(
            bck_rect,
            margin=self._popup_margin,
            side=self._popup_side,
            shadow_radius=self._popup_shadow_radius,
            region=self._popup_region,
            border_color=gui_qt_core.QtColors.PopupBorder,
            background_color=self._frame_background_color,
            border_width=2
        )
        painter._draw_line_by_points_(
            point_0=self._rect_popup_top_toolbar.bottomLeft(),
            point_1=self._rect_popup_top_toolbar.bottomRight(),
            border_color=self._frame_border_color,
        )
        #
        if not self._popup_keyword_filter_entry.text():
            painter._draw_text_by_rect_(
                self._rect_popup_top_toolbar_tool_tip,
                'entry to filter ...',
                font=gui_qt_core.QtFonts.NameNormal,
                font_color=gui_qt_core.QtColors.TextDisable,
                text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
            )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self._entry_widget:
            if event.type() == QtCore.QEvent.FocusOut:
                self._do_popup_close_()
            elif event.type() == QtCore.QEvent.WindowDeactivate:
                self._do_popup_close_()
            elif event.type() == QtCore.QEvent.Hide:
                self._do_popup_close_()
            elif event.type() == QtCore.QEvent.KeyPress:
                if self._get_popup_is_activated_():
                    if event.key() == QtCore.Qt.Key_Up:
                        self._do_popup_view_scroll_to_pre_()
                        return True
                    elif event.key() == QtCore.Qt.Key_Down:
                        self._do_popup_view_scroll_to_next_()
                        return True
                    elif event.key() == QtCore.Qt.Key_Escape:
                        self._do_popup_close_()
                        return True
                    else:
                        self._popup_keyword_filter_entry.keyPressEvent(event)
        return False

    def _do_popup_filter_(self):
        # keyword filter
        self._popup_view._set_view_keyword_filter_data_src_([self._popup_keyword_filter_entry.text()])
        #
        self._popup_view._refresh_view_items_visible_by_any_filter_()
        self._popup_view._refresh_view_all_items_viewport_showable_()

    def _set_entry_widget_(self, widget):
        self._entry_widget = widget
        self._entry_widget.installEventFilter(self._widget)
        self._widget.setFocusProxy(self._entry_widget)
        self._popup_keyword_filter_entry.setFocusProxy(self._entry_widget)

    def _do_popup_view_scroll_to_pre_(self):
        if self._popup_is_activated is True:
            self._popup_view._scroll_to_pre_item_()

    def _do_popup_view_scroll_to_next_(self):
        if self._popup_is_activated is True:
            self._popup_view._scroll_to_next_item_()

    def _do_popup_start_(self, index):
        input_widget = self.parent()
        values = input_widget._get_guide_child_name_texts_at_(index)
        if values:
            desktop_rect = gui_qt_core.GuiQtUtil.get_qt_desktop_rect()
            #
            press_pos = input_widget._get_guide_choose_point_at_(index)
            press_rect = input_widget._get_guide_choose_rect_at_(index)
            #
            text_current = input_widget._get_guide_name_text_at_(index)
            for seq, i_text in enumerate(values):
                i_item_widget = gui_qt_wgt_utility._QtHItem()
                i_item = gui_qt_wgt_utility.QtListWidgetItem()
                i_item.setSizeHint(QtCore.QSize(self._w_popup_item, self._h_popup_item))
                #
                self._popup_view.addItem(i_item)
                self._popup_view.setItemWidget(i_item, i_item_widget)
                i_item._connect_item_show_()
                i_item._update_item_keyword_filter_keys_tgt_([i_text])
                #
                if i_text:
                    i_item_widget._set_name_text_(i_text)
                    i_item_widget._set_icon_name_text_(i_text)
                #
                i_item_widget._set_index_(seq)
                if text_current == i_text:
                    i_item.setSelected(True)
            #
            self.setFocus(QtCore.Qt.PopupFocusReason)
            #
            height_max = self._popup_view._compute_height_maximum_(self._popup_item_row_maximum)
            height_max += self._h_popup_top_toolbar
            popup_width = self._get_popup_width_(values)
            popup_width = max(self._popup_width_minimum, popup_width)
            #
            self._show_popup_as_style_0_(
                press_pos, press_rect,
                desktop_rect,
                popup_width,
                height_max
            )
            self._choose_index = index
            input_widget._set_guide_choose_item_expand_at_(index)
            #
            self._popup_view._set_scroll_to_selected_item_top_()
            #
            self._entry_widget._set_focused_(True)
            #
            self._popup_is_activated = True
        else:
            self._do_popup_close_()

    def _do_popup_end_(self):
        if self._choose_index is not None:
            input_widget = self.parent()
            selected_item_widget = self._popup_view._get_selected_item_widget_()
            if selected_item_widget:
                name_text_cur = selected_item_widget._get_name_text_()
                #
                path_text_cur = input_widget._set_guide_name_text_at_(
                    name_text_cur,
                    self._choose_index
                )
                input_widget._refresh_guide_draw_geometry_()
                # choose
                input_widget.guide_text_choose_accepted.emit(path_text_cur)
            # clear latest
            input_widget._clear_guide_current_()
        #
        self._do_popup_close_()

    def _set_popup_activated_(self, boolean):
        super(QtPopupAsChooseForGuide, self)._set_popup_activated_(boolean)
        #
        if self._choose_index is not None:
            input_widget = self.parent()
            input_widget._set_guide_choose_item_collapse_at_(self._choose_index)

    def _get_popup_width_(self, texts):
        count = len(texts)
        _ = max([self.fontMetrics().width(i) for i in texts])+32
        _count_width = self.fontMetrics().width(str(count))
        if count > self._popup_item_row_maximum:
            return _+_count_width+24
        return _+_count_width

    def _do_popup_close_(self):
        self._set_popup_activated_(False)


# rgba choose
class QtPopupAsChooseForRgba(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtFrameBaseDef,
    gui_qt_abstracts.AbsQtPopupBaseDef,
):
    def _refresh_widget_draw_(self):
        self.update()
        self._popup_view.update()

    def _refresh_widget_draw_geometry_(self):
        side = self._popup_side
        margin = self._popup_margin
        shadow_radius = self._popup_shadow_radius
        #
        x, y = 0, 0
        w, h = self.width(), self.height()
        v_x, v_y = x+margin+side+1, y+margin+side+1
        v_w, v_h = w-margin*2-side*2-shadow_radius-2, h-margin*2-side*2-shadow_radius-2
        #
        self._popup_view.setGeometry(
            v_x, v_y, v_w, v_h
        )
        self._popup_view.update()

        self._save_chart_button.setGeometry(
            v_x, v_y+v_h-20, 20, 20
        )

    def __init__(self, *args, **kwargs):
        super(QtPopupAsChooseForRgba, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setFocusProxy(self.parent())
        self.setWindowFlags(QtCore.Qt.ToolTip | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowDoesNotAcceptFocus)
        #
        self._init_frame_base_def_(self)
        self._init_popup_base_def_(self)
        #
        self._frame_border_color = gui_qt_core.QtBackgroundColors.Light
        self._hovered_frame_border_color = gui_qt_core.QtBackgroundColors.Hovered
        self._selected_frame_border_color = gui_qt_core.QtBackgroundColors.Selected
        self._frame_background_color = gui_qt_core.QtBackgroundColors.Dark

        self._popup_view = gui_qt_wgt_chart.QtChartAsRgbaChoose(self)
        self._popup_view.setFocusPolicy(QtCore.Qt.ClickFocus)
        self._popup_view.installEventFilter(self)

        self._save_chart_button = gui_qt_wgt_button.QtIconPressButton(self)
        self._save_chart_button._set_icon_name_('tool/file-save')
        self._save_chart_button.press_clicked.connect(self._save_chart_)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self._entry_widget:
            if event.type() == QtCore.QEvent.FocusOut:
                self._do_popup_close_()
            elif event.type() == QtCore.QEvent.WindowDeactivate:
                self._do_popup_close_()
            elif event.type() == QtCore.QEvent.Hide:
                self._do_popup_close_()
        elif widget == self._popup_view:
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                self._do_popup_end_()
        return False

    def paintEvent(self, event):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        bck_rect = QtCore.QRect(
            x, y, w-1, h-1
        )
        painter = gui_qt_core.QtPainter(self)
        #
        painter._draw_popup_frame_(
            bck_rect,
            margin=self._popup_margin,
            side=self._popup_side,
            shadow_radius=self._popup_shadow_radius,
            region=self._popup_region,
            border_color=gui_qt_core.QtColors.PopupBorder,
            background_color=self._frame_background_color,
        )

    def _set_entry_widget_(self, widget):
        self._entry_widget = widget
        self._entry_widget.installEventFilter(self._widget)
        self._widget.setFocusProxy(self._entry_widget)
        self._popup_view.setFocusProxy(self._entry_widget)

    def _do_popup_start_(self):
        input_widget = self.parent()
        press_rect = input_widget._get_value_rect_()
        press_point = self._compute_popup_press_point_(input_widget, press_rect)
        desktop_rect = gui_qt_core.GuiQtUtil.get_qt_desktop_rect()
        self._show_popup_as_style_0_(
            press_point,
            press_rect,
            desktop_rect,
            320, 320
        )
        self._popup_view._set_color_rgba_255_(self._entry_widget._get_value_as_rgba_255_())
        self._entry_widget._set_focused_(True)

    def _do_popup_end_(self, *args, **kwargs):
        rgba = map(lambda x: int(x), self._popup_view._get_color_rgba_255_())
        self._entry_widget._set_value_as_rgba_255_(rgba)
        self.user_popup_values_accepted.emit(rgba)
        self.user_popup_finished.emit()
        self.parent()._refresh_widget_draw_()
        self._do_popup_close_()

    def _do_popup_close_(self, *args, **kwargs):
        self._set_popup_activated_(False)

    def _save_chart_(self):
        d = bsc_core.SysBaseMtd.get_home_directory()
        file_path = six.u('{}/screenshot/untitled-{}.jpg').format(d, bsc_core.TimeExtraMtd.generate_time_tag_36())

        w, h = self.width(), self.height()
        pixmap = QtGui.QPixmap(QtCore.QSize(w, h))
        self.render(pixmap)

        pixmap.save(file_path)
