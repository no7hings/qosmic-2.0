# coding=utf-8
import six

import collections

import lxbasic.core as bsc_core
# gui
from .... import core as _gui_core
# qt
from ....qt.core.wrap import *

from ....qt import core as _qt_core

from ....qt import abstracts as _qt_abstracts

from ...widgets import utility as _wgt_utility

from ...widgets import entry_frame as _wgt_entry_frame

from ...widgets import button as _wgt_button

from ...widgets import scroll as _wgt_scroll

from ...widgets import container as _wgt_container

from ...widgets import chart as _wgt_chart

from ...widgets.input import input_for_filter as _wgt_input_for_filter

from ...view_models import base as _vew_mod_base

from ...view_models.list import view as _vew_mod_list

from .. import base as _base

from . import item as _item


class _QtListItemDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, *args, **kwargs):
        QtWidgets.QStyledItemDelegate.__init__(self, *args, **kwargs)

    def paint(self, painter, option, index):
        self.parent()._view_model.draw_item(painter, option, index)

    def sizeHint(self, option, index):
        item = self.parent().itemFromIndex(index)
        return item.sizeHint()


class _QtListView(
    QtWidgets.QListWidget,
    _vew_mod_base.AbsView,
    _qt_abstracts.AbsQtThreadWorkerExtraDef,
):
    QT_MENU_CLS = _wgt_utility.QtMenu

    def __init__(self, *args, **kwargs):
        super(_QtListView, self).__init__(*args, **kwargs)

        self.setStyleSheet(_qt_core.QtStyle.get('QListView'))
        self.verticalScrollBar().setStyleSheet(_qt_core.QtStyle.get('QScrollBar'))
        self.horizontalScrollBar().setStyleSheet(_qt_core.QtStyle.get('QScrollBar'))

        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setMouseTracking(True)

        self.setResizeMode(self.Adjust)
        self.setViewMode(self.IconMode)

        self.setSelectionMode(self.ExtendedSelection)
        self.setVerticalScrollMode(self.ScrollPerItem)
        # disable for default
        self.setSortingEnabled(False)
        self.setDragEnabled(False)

        # noinspection PyUnresolvedReferences
        self.itemSelectionChanged.connect(self.item_select_changed.emit)

        self._view_model = _vew_mod_list.ListViewModel(self)
        self._view_model.data.item.cls = _item.QtListItem
        self._view_model.data.item.group_cls = _item.QtListGroupItem

        self.setItemDelegate(_QtListItemDelegate(self))

        self._item_dict = collections.OrderedDict()

        self._init_thread_worker_extra_def_(self)

        self.installEventFilter(self)
        self.viewport().installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.FocusIn:
                # self._is_focused = True
                parent = self.parent()
                if isinstance(parent, _wgt_entry_frame.QtEntryFrame):
                    parent._set_focused_(True)
            elif event.type() == QtCore.QEvent.FocusOut:
                # self._is_focused = False
                parent = self.parent()
                if isinstance(parent, _wgt_entry_frame.QtEntryFrame):
                    parent._set_focused_(False)
        # view port
        elif widget == self.viewport():
            if event.type() == QtCore.QEvent.ToolTip:
                self._view_model.do_item_popup_tool_tip(event)

            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.buttons() == QtCore.Qt.LeftButton:
                    self._view_model.do_item_press_click(event)
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.buttons() == QtCore.Qt.LeftButton:
                    self._view_model.do_item_press_dbl_click(event)
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.NoButton:
                    self._view_model.do_item_hover_move(event)

            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self.press_released.emit()
        return False

    def paintEvent(self, event):
        if not self.count():
            painter = _qt_core.QtPainter(self.viewport())
            painter._draw_empty_image_by_rect_(
                self.rect(),
                'placeholder/empty'
            )
        else:
            super(_QtListView, self).paintEvent(event)

    def contextMenuEvent(self, event):
        menu = None

        menu_data = self._view_model.get_menu_data()
        menu_content = self._view_model.get_menu_content()
        menu_data_generate_fnc = self._view_model.get_menu_data_generate_fnc()
        menu_name_dict = self._view_model.get_menu_name_dict()

        if menu_content:
            if menu is None:
                menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
            menu._set_menu_content_(menu_content, append=True)

        if menu_data:
            if menu is None:
                menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
            menu._set_menu_data_(menu_data)

        if menu_data_generate_fnc:
            if menu is None:
                menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
            menu._set_menu_data_(menu_data_generate_fnc())

        # data from item
        item = self.itemAt(event.pos())
        if item:
            item_menu_data = item._item_model.get_menu_data()
            item_menu_content = item._item_model.get_menu_content()
            item_menu_data_generate_fnc = item._item_model.get_menu_data_generate_fnc()
            item_menu_name_dict = item._item_model.get_menu_name_dict()
            menu_name_dict.update(item_menu_name_dict)

            if item_menu_content:
                if menu is None:
                    menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
                menu._set_menu_content_(item_menu_content, append=True)

            if item_menu_data:
                if menu is None:
                    menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
                menu._set_menu_data_(item_menu_data)

            if item_menu_data_generate_fnc:
                if menu is None:
                    menu = self.QT_MENU_CLS(self, name_dict=menu_name_dict)
                menu._set_menu_data_(item_menu_data_generate_fnc())

            if menu is not None:
                menu._update_menu_name_dict_(item_menu_name_dict)

        if menu is not None:
            menu._popup_start_()

    def wheelEvent(self, event):
        if _qt_core.QtUtil.is_ctrl_modifier():
            self._view_model.on_wheel(event)
            event.ignore()
        else:
            super(_QtListView, self).wheelEvent(event)

    def startDrag(self, actions):
        items = self.selectedItems()
        if items:
            current_item = self.currentItem()
            drag_data = self._view_model.generate_drag_data_for(items)
            if drag_data:
                mime_data = QtCore.QMimeData()

                c = len(drag_data)
                draw_c = min(c, 40)
                drag = QtGui.QDrag(self)
                x, y = 0, 0
                grd_w, grd_h = self.gridSize().width(), self.gridSize().height()
                spc = 4
                frm_w, frm_h = grd_w, 20
                pxm_w, pxm_h = grd_w, frm_h+spc*(draw_c-1)
                # fixme: painter error
                # pixmap = QtGui.QPixmap(pxm_w, pxm_h)
                # pixmap.fill(QtGui.QColor(63, 63, 63, 255))
                # painter = QtGui.QPainter(pixmap)
                #
                # if painter.isActive():
                #     for i_idx in range(draw_c):
                #         i_rect = QtCore.QRect(x+1, y+(i_idx*spc)+1, frm_w-2, frm_h-2)
                #         painter.setPen(QtGui.QColor(*_gui_core.GuiRgba.LightPinkPurple))
                #         painter.setBrush(QtGui.QColor(*_gui_core.GuiRgba.Dim))
                #         painter.drawRect(i_rect)
                #         # last item
                #         if i_idx == (draw_c-1):
                #             i_item_model = items[i_idx]._item_model
                #             painter.setPen(QtGui.QColor(*_gui_core.GuiRgba.DarkWhite))
                #             i_text_rect = QtCore.QRect(x+1+4, y+(i_idx*spc)+1, frm_w-2-4, frm_h-2)
                #             i_name = bsc_core.ensure_unicode(i_item_model.get_name())
                #             i_text = u'{} x {}'.format(i_name, c)
                #             i_text = i_item_model._font_metrics.elidedText(
                #                 i_text,
                #                 QtCore.Qt.ElideMiddle,
                #                 i_text_rect.width()-4,
                #                 QtCore.Qt.TextShowMnemonic
                #             )
                #             painter.drawText(
                #                 i_text_rect,
                #                 QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                #                 i_text
                #
                #             )
                #
                # painter.end()

                pixmap = current_item._item_model._pixmap_cache
                drag.setPixmap(pixmap)

                urls = []
                for i_data in drag_data:
                    for j_k, j_v in i_data.items():
                        if j_k == 'file':
                            # noinspection PyArgumentList
                            urls.append(QtCore.QUrl.fromLocalFile(j_v))
                        else:
                            mime_data.setData(
                                bsc_core.ensure_string(j_k),
                                QtCore.QByteArray(bsc_core.ensure_string(j_v).encode('utf-8'))
                            )
                if urls:
                    mime_data.setUrls(urls)
                drag.setMimeData(mime_data)
                drag.exec_(actions)


class QtListWidget(
    _base._BaseViewWidget
):
    FILTER_COMPLETION_MAXIMUM = 50

    def __init__(self, *args, **kwargs):
        super(QtListWidget, self).__init__(*args, **kwargs)
        # refresh
        self._refresh_button = _wgt_button.QtIconPressButton()
        self._grid_lot.addWidget(self._refresh_button, 0, 0, 1, 1)
        self._refresh_button.setFixedSize(self.TOOL_BAR_W, self.TOOL_BAR_W)
        self._refresh_button._set_icon_file_path_(
            _gui_core.GuiIcon.get('refresh')
        )
        self._refresh_button.press_clicked.connect(self.refresh.emit)
        # top
        self._top_scroll_box = _wgt_scroll.QtHScrollBox()
        self._grid_lot.addWidget(self._top_scroll_box, 0, 1, 1, 1)
        self._top_scroll_box._set_layout_align_left_or_top_()
        self._top_scroll_box.setFixedHeight(self.TOOL_BAR_W)
        # left
        self._left_scroll_box = _wgt_scroll.QtVScrollBox()
        self._grid_lot.addWidget(self._left_scroll_box, 1, 0, 1, 1)
        self._left_scroll_box._set_layout_align_left_or_top_()
        self._left_scroll_box.setFixedWidth(self.TOOL_BAR_W)

        self._check_tool_box = self._add_left_tool_box_('check')
        self._check_tool_box.hide()
        self._sort_and_group_tool_box = self._add_left_tool_box_('sort and group')
        self._keyword_filter_tool_box = self._add_top_tool_box_('keyword filter', size_mode=1)

        self._view = _QtListView()
        self._grid_lot.addWidget(self._view, 1, 1, 1, 1)
        self._view.setFocusProxy(self)
        self._view_model = self._view._view_model

        self._info_bar_chart = _wgt_chart.QtInfoChartBar()
        self._grid_lot.addWidget(self._info_bar_chart, 2, 1, 1, 1)
        self._info_bar_chart.hide()
        self._view.info_text_accepted.connect(
            self._info_bar_chart._set_text_
        )

        self._build_check_tool_box_()
        self._build_sort_and_group_tool_box_()
        self._build_keyword_filter_tool_box_()

        actions = [
            (self._view.selectAll, 'Ctrl+A'),
        ]
        for i_fnc, i_shortcut in actions:
            i_action = QtWidgets.QAction(self)
            # noinspection PyUnresolvedReferences
            i_action.triggered.connect(
                i_fnc
            )
            i_action.setShortcut(
                QtGui.QKeySequence(
                    i_shortcut
                )
            )
            i_action.setShortcutContext(
                QtCore.Qt.WidgetShortcut
            )
            self.addAction(i_action)

    def _set_item_check_enable_(self, boolean):
        self._check_tool_box.setVisible(boolean)
        self._view_model.set_item_check_enable(boolean)

    def _set_item_sort_enable_(self, boolean):
        self._item_sort_button.setVisible(boolean)
        self._view_model.set_item_sort_enable(boolean)

    def _set_item_group_enable_(self, boolean):
        self._item_group_button.setVisible(boolean)
        self._view_model.set_item_group_enable(boolean)

    def _add_top_tool_box_(self, name, size_mode=0):
        tool_box = _wgt_container.QtHToolBox()
        self._top_scroll_box.addWidget(tool_box)
        tool_box._set_expanded_(True)
        tool_box._set_name_text_(name)
        tool_box._set_size_mode_(size_mode)
        return tool_box

    def _add_left_tool_box_(self, name):
        tool_box = _wgt_container.QtVToolBox()
        self._left_scroll_box.addWidget(tool_box)
        tool_box._set_expanded_(True)
        tool_box._set_name_text_(name)
        return tool_box

    def _insert_left_tool_box_(self, index, name):
        tool_box = _wgt_container.QtVToolBox()
        self._left_scroll_box.insertWidget(index, tool_box)
        tool_box._set_expanded_(True)
        tool_box._set_name_text_(name)
        return tool_box

    def _build_check_tool_box_(self):
        self._check_all_button = _wgt_button.QtIconPressButton()
        self._check_all_button._set_name_text_('check all')
        self._check_all_button._set_icon_file_path_(_gui_core.GuiIcon.get('all_checked'))
        self._check_tool_box._add_widget_(self._check_all_button)
        self._check_all_button.press_clicked.connect(self._on_check_all_)
        self._check_all_button._set_tool_tip_text_(
            '"LMB-click" for checked all visible items'
        )
        self._check_all_button._set_menu_data_(
            [
                ('Check By',),
                ('visible', 'tool/show', self._on_check_visible_)
            ]
        )
        #
        self._uncheck_all_button = _wgt_button.QtIconPressButton()
        self._uncheck_all_button._set_icon_file_path_(_gui_core.GuiIcon.get('all_unchecked'))
        self._uncheck_all_button._set_name_text_('uncheck all')
        self._check_tool_box._add_widget_(self._uncheck_all_button)
        self._uncheck_all_button.press_clicked.connect(self._on_uncheck_all_)
        self._uncheck_all_button._set_tool_tip_text_(
            '"LMB-click" for unchecked all visible items'
        )
        self._uncheck_all_button._set_menu_data_(
            [
                ('Uncheck By',),
                ('visible', 'tool/show', self._on_uncheck_visible_)
            ]
        )

    def _build_sort_and_group_tool_box_(self):
        # sort
        self._item_sort_button = _wgt_button.QtIconPressButton()
        self._item_sort_button.hide()
        self._sort_and_group_tool_box._add_widget_(self._item_sort_button)
        self._item_sort_button._set_name_text_('sort')
        self._item_sort_button._set_icon_name_('tool/sort-by-name-ascend')
        self._item_sort_button._set_menu_data_generate_fnc_(
            self._view_model.generate_item_sort_menu_data
        )
        self._item_sort_button.press_clicked.connect(self._on_sort_order_swap_)
        # group
        self._item_group_button = _wgt_button.QtIconPressButton()
        self._item_group_button.hide()
        self._sort_and_group_tool_box._add_widget_(self._item_group_button)
        self._item_group_button._set_name_text_('group')
        self._item_group_button._set_icon_name_('tool/group-by')
        self._item_group_button._set_menu_data_generate_fnc_(
            self._view_model.generate_item_group_menu_data
        )
        # mode
        self._item_mode_button = _wgt_button.QtIconPressButton()
        self._sort_and_group_tool_box._add_widget_(self._item_mode_button)
        self._item_mode_button._set_name_text_('mode')
        self._item_mode_button._set_icon_name_('tool/icon-mode')
        self._item_mode_button.press_clicked.connect(self._on_item_mode_swap_)

    def _build_keyword_filter_tool_box_(self):
        self._keyword_filter_input = _wgt_input_for_filter.QtInputForFilter()
        self._keyword_filter_tool_box._add_widget_(self._keyword_filter_input)

        self._keyword_filter_input._set_input_completion_buffer_fnc_(self._keyword_filter_input_completion_buffer_fnc)
        self._keyword_filter_input.input_value_changed.connect(self._on_keyword_filer)
        self._keyword_filter_input.occurrence_previous_press_clicked.connect(
            self._view_model.occurrence_item_previous
        )
        self._keyword_filter_input.occurrence_next_press_clicked.connect(
            self._view_model.occurrence_item_next
        )
        self._keyword_filter_input._set_occurrence_buttons_enable_(True)

    def _on_check_all_(self):
        self._view_model.set_all_items_checked(True)

    def _on_check_visible_(self):
        self._view_model.set_visible_items_checked(True)

    def _on_uncheck_all_(self):
        self._view_model.set_all_items_checked(False)

    def _on_uncheck_visible_(self):
        self._view_model.set_visible_items_checked(False)

    def _on_sort_order_swap_(self):
        if self._view_model.is_item_sort_enable():
            self._view_model.swap_item_sort_order()
            order = ['ascend', 'descend'][self._view_model.get_item_sort_order()]
            self._item_sort_button._set_icon_name_('tool/sort-by-name-{}'.format(order))

    def _on_item_mode_swap_(self):
        self._view_model.swap_item_mode()
        mode = ['icon', 'list'][self._view_model.get_item_mode()]
        self._item_mode_button._set_icon_name_('tool/{}-mode'.format(mode))

    def _on_keyword_filer(self):
        self._view_model.set_keyword_filter_key_src(
            self._keyword_filter_input._get_all_keywords_()
        )
        self._view_model.refresh_items_visible_by_any_filter()

    def _keyword_filter_input_completion_buffer_fnc(self, *args, **kwargs):
        keyword = args[0]
        if keyword:
            _ = bsc_core.BscFnmatch.filter(
                self._view_model.generate_keyword_filter_completion_cache(), six.u('*{}*').format(keyword)
            )
            return bsc_core.BscTexts.sort_by_initial(_)[:self.FILTER_COMPLETION_MAXIMUM]
        return []
