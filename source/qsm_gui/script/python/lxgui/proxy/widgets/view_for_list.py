# coding:utf-8
import six

import fnmatch

import collections

import functools

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# gui
from ... import core as gui_core
# qt widgets
from ...qt.widgets import base as gui_qt_wgt_base

from ...qt.widgets import button as gui_qt_wgt_button

from ...qt.widgets import entry as gui_qt_wgt_entry

from ...qt.widgets import chart as gui_qt_wgt_chart

from ...qt.widgets import view_for_list as gui_qt_wgt_view_for_list
# proxy abstracts
from .. import abstracts as gui_prx_abstracts
# proxy widgets
from . import utility as gui_prx_wdt_utility

from . import item as gui_prx_wgt_item

from . import container as gui_prx_wgt_container


class PrxListView(
    gui_prx_abstracts.AbsPrxWidget,
    gui_prx_abstracts.AbsPrxViewDef,
    #
    gui_prx_abstracts.AbsPrxViewFilterTagDef,
    #
    gui_prx_abstracts.AbsPrxViewVisibleConnectionDef,
):
    QT_WIDGET_CLS = gui_qt_wgt_entry.QtEntryFrame
    QT_VIEW_CLS = gui_qt_wgt_view_for_list.QtListWidget
    #
    FILTER_MAXIMUM = 50

    def __init__(self, *args, **kwargs):
        super(PrxListView, self).__init__(*args, **kwargs)
        self._qt_layout_0 = gui_qt_wgt_base.QtVBoxLayout(self._qt_widget)
        self._qt_layout_0.setContentsMargins(4, 4, 4, 4)
        self._qt_layout_0.setSpacing(2)
        #
        self._prx_top_tool_bar = gui_prx_wgt_container.PrxHToolBar()
        self._prx_top_tool_bar.set_name('top')
        self._prx_top_tool_bar.set_left_alignment()
        self._qt_layout_0.addWidget(self._prx_top_tool_bar.widget)
        self._prx_top_tool_bar.set_border_radius(1)
        # check
        self._prx_check_tool_box = self.create_top_tool_box('check', True, False, 0)
        #
        self._check_all_button = gui_qt_wgt_button.QtIconPressButton()
        self._check_all_button._set_name_text_('check all')
        self._check_all_button._set_icon_file_path_(gui_core.GuiIcon.get('all_checked'))
        self._prx_check_tool_box.add_widget(self._check_all_button)
        self._check_all_button.press_clicked.connect(self.__do_check_all_visible_items)
        self._check_all_button._set_tool_tip_text_(
            '"LMB-click" for checked all visible items'
        )
        #
        self._uncheck_all_button = gui_qt_wgt_button.QtIconPressButton()
        self._uncheck_all_button._set_icon_file_path_(gui_core.GuiIcon.get('all_unchecked'))
        self._uncheck_all_button._set_name_text_('uncheck all')
        self._prx_check_tool_box.add_widget(self._uncheck_all_button)
        self._uncheck_all_button.press_clicked.connect(self.__do_uncheck_all_visible_items)
        self._uncheck_all_button._set_tool_tip_text_(
            '"LMB-click" for unchecked all visible items'
        )
        # mode switch
        self._prx_mode_switch_tool_box = self.create_top_tool_box('mode', True, True, 0)
        #
        self._view_mode_swap_button = gui_qt_wgt_button.QtIconPressButton()
        self._prx_mode_switch_tool_box.add_widget(self._view_mode_swap_button)
        self._view_mode_swap_button._set_name_text_('icon mode')
        self._view_mode_swap_button._set_icon_file_path_(gui_core.GuiIcon.get('tool/icon-mode'))
        self._view_mode_swap_button.press_clicked.connect(self.__swap_view_mode)
        self._view_mode_swap_button._set_tool_tip_text_(
            '"LMB-click" for switch view mode to "icon" / "list"'
        )
        # scale switch

        self._prx_scale_switch_tool_box = self.create_top_tool_box('scale', True, False, 0)
        # sort
        self._prx_sort_switch_tool_box = self.create_top_tool_box('sort', True, False, 0)
        # filter
        self._prx_filter_tool_box = self.create_top_tool_box('filter', True, True, 1)
        #
        self._prx_filer_bar_0 = gui_prx_wdt_utility.PrxFilterBar()
        self._prx_filter_tool_box.add_widget(self._prx_filer_bar_0)
        # add custom menu
        self._qt_view = self.QT_VIEW_CLS()
        self._qt_layout_0.addWidget(self._qt_view)
        self._set_prx_view_def_init_(self._qt_view)
        self._qt_view._set_sort_enable_(True)
        #
        self._qt_info_chart = gui_qt_wgt_chart.QtChartAsInfo()
        self._qt_info_chart.hide()
        self._qt_layout_0.addWidget(self._qt_info_chart)
        self._qt_view.info_text_accepted.connect(
            self._qt_info_chart._set_info_text_
        )
        #
        self._prx_filter_bar = self._prx_filer_bar_0
        self._qt_view._set_view_keyword_filter_bar_(self._prx_filter_bar._qt_widget)

        self._item_dict = collections.OrderedDict()
        self._filter_completion_cache = None

        self.__add_scale_switch_tools()
        self.__add_sort_mode_switch_tools()

        self._prx_filter_bar._qt_widget.input_value_changed.connect(self.__keyword_filter_cbk)
        self._prx_filter_bar._qt_widget.input_value_change_accepted.connect(
            self._qt_view._do_keyword_filter_occurrence_
        )
        self._prx_filter_bar._qt_widget.occurrence_previous_press_clicked.connect(
            self._qt_view._do_keyword_filter_occurrence_to_previous_
        )
        self._prx_filter_bar._qt_widget.occurrence_next_press_clicked.connect(
            self._qt_view._do_keyword_filter_occurrence_to_next_
        )
        self._prx_filter_bar._qt_widget._set_input_completion_buffer_fnc_(self.__keyword_filter_completion_gain_fnc)

    @property
    def view(self):
        return self._qt_view

    @property
    def filter_bar(self):
        return self._prx_filter_bar

    def hide_top_tool_bar(self):
        self._prx_top_tool_bar.set_visible(False)

    def create_top_tool_box(self, name, expanded=True, visible=True, size_mode=0, insert_args=None):
        tool_box = gui_prx_wdt_utility.PrxHToolBox()
        if isinstance(insert_args, int):
            self._prx_top_tool_bar.insert_widget_at(insert_args, tool_box)
        else:
            self._prx_top_tool_bar.add_widget(tool_box)
        tool_box.set_name(name)
        tool_box.set_expanded(expanded)
        tool_box.set_visible(visible)
        tool_box.set_size_mode(size_mode)
        return tool_box

    # noinspection PyUnusedLocal
    def __keyword_filter_completion_gain_fnc(self, *args, **kwargs):
        keyword = args[0]
        if keyword:
            # cache fist
            if self._filter_completion_cache is None:
                self._filter_completion_cache = list(
                    set(
                        map(
                            lambda x: x.lower(),
                            [
                                j for i in self._qt_view._get_all_items_() for j in
                                i._generate_keyword_filter_keys_()
                            ]
                        )
                    )
                )
            #
            _ = fnmatch.filter(
                self._filter_completion_cache, six.u('*{}*').format(keyword)
            )
            return bsc_core.RawTextsMtd.sort_by_initial(_)[:self.FILTER_MAXIMUM]
        return []

    def __keyword_filter_cbk(self):
        self._qt_view._set_view_keyword_filter_data_src_(
            self._prx_filter_bar.get_keywords()
        )
        self._qt_view._refresh_view_items_visible_by_any_filter_()
        self._prx_filter_bar._qt_widget._set_occurrence_buttons_enable_(self._qt_view._has_keyword_filter_results_())
        self._qt_view._refresh_viewport_showable_auto_()

    def get_check_tool_box(self):
        return self._prx_check_tool_box

    def get_scale_switch_tool_box(self):
        return self._prx_scale_switch_tool_box

    def get_sort_switch_tool_box(self):
        return self._prx_sort_switch_tool_box

    def get_filter_tool_box(self):
        return self._prx_filter_tool_box

    def __add_scale_switch_tools(self):
        tools = []
        for i_key, i_enable, i_scale in [
            ('small', False, .75), ('medium', True, 1.0), ('large', False, 1.25), ('super', False, 1.5)
        ]:
            i_tool = gui_prx_wdt_utility.PrxEnableItem()
            self._prx_scale_switch_tool_box.add_widget(i_tool)
            # i_tool._qt_widget._set_size_(24, 24)
            # i_tool._qt_widget._set_icon_frame_draw_size_(24, 24)
            # i_tool._qt_widget._set_icon_file_draw_size_(20, 20)
            i_tool._qt_widget._set_exclusive_widgets_(tools)
            i_tool.set_name(i_key)
            i_tool.set_icon_name('tool/icon-{}'.format(i_key))
            i_tool.set_tool_tip('"LMB-click" for switch to scale to "{}"'.format(i_key))
            if i_enable is True:
                i_tool.set_checked(True)
            #
            tools.append(i_tool._qt_widget)
            i_tool.connect_check_changed_as_exclusive_to(
                functools.partial(self.__switch_view_scale, i_scale)
            )

    def __switch_view_scale(self, scale):
        self._qt_view._set_item_scale_percent_(scale)

    def __add_sort_mode_switch_tools(self):
        self._sort_mode_switch_tools = []
        for i_key, i_mode in [
            ('number', 0), ('name', 1)
        ]:
            i_tool = gui_prx_wdt_utility.PrxEnableItem()
            self._prx_sort_switch_tool_box.add_widget(i_tool)
            # i_tool._qt_widget._set_size_(24, 24)
            # i_tool._qt_widget._set_icon_frame_draw_size_(24, 24)
            # i_tool._qt_widget._set_icon_file_draw_size_(20, 20)
            i_tool._qt_widget._set_exclusive_widgets_(self._sort_mode_switch_tools)
            i_tool.set_name(i_key)
            i_tool.set_icon_name('tool/sort-by-{}-ascend'.format(i_key))
            i_tool.set_tool_tip('"LMB-click" for switch to sort mode to "{}"'.format(i_key))
            self._sort_mode_switch_tools.append(i_tool._qt_widget)
            #
            i_tool.connect_check_changed_as_exclusive_to(
                functools.partial(self.__switch_view_sort_mode, i_mode)
            )
            i_tool.connect_check_swapped_as_exclusive_to(
                self.__swap_view_sort_order
            )
        #
        self._sort_mode_switch_tools[0]._set_checked_(True)

    def __switch_view_sort_mode(self, mode):
        self._qt_view._set_item_sort_mode_(mode)

    def __swap_view_sort_order(self):
        self._qt_view._swap_item_sort_order_()
        order = ['ascend', 'descend'][self._qt_view._get_sort_order_()]
        for i in self._sort_mode_switch_tools:
            i_key = i._get_name_text_()
            i_icon_name = 'tool/sort-by-{}-{}'.format(i_key, order)
            i._set_icon_file_path_(
                gui_core.GuiIcon.get(i_icon_name),
            )

    def __swap_view_mode(self):
        self._qt_view._swap_view_mode_()
        self._view_mode_swap_button._set_name_text_(
            ['list mode', 'icon mode'][self.view._get_is_grid_mode_()]
        )
        self._view_mode_swap_button._set_icon_file_path_(
            gui_core.GuiIcon.get(['tool/list-mode', 'tool/icon-mode'][self.view._get_is_grid_mode_()])
        )

    def __do_check_all_visible_items(self):
        self._qt_view._set_all_visible_item_widgets_checked_(True)

    def __do_uncheck_all_visible_items(self):
        self._qt_view._set_all_visible_item_widgets_checked_(False)

    def set_view_list_mode(self):
        self._qt_view._set_list_mode_()

    def set_view_grid_mode(self):
        self._qt_view._set_grid_mode_()

    def set_item_frame_size(self, w, h):
        self._qt_view._set_item_frame_size_(w, h)

    def set_item_frame_size_basic(self, w, h):
        self._qt_view._set_item_size_basic_(w, h)

    def set_item_frame_draw_enable(self, boolean):
        self._qt_view._set_item_frame_draw_enable_(boolean)

    def set_item_icon_frame_size(self, w, h):
        self._qt_view._set_item_icon_frame_size_(w, h)
        self._qt_view._set_item_icon_size_(w-4, h-4)

    def set_item_icon_size(self, w, h):
        self._qt_view._set_item_icon_size_(w, h)

    def set_item_icon_frame_draw_enable(self, boolean):
        self._qt_view._set_item_icon_frame_draw_enable_(boolean)

    def set_item_name_frame_size(self, w, h):
        self._qt_view._set_item_name_frame_size_(w, h)
        self._qt_view._set_item_name_size_(w-4, h-4)

    def set_item_name_size(self, w, h):
        self._qt_view._set_item_name_size_(w, h)

    def set_item_name_frame_draw_enable(self, boolean):
        self._qt_view._set_item_name_frame_draw_enable_(boolean)

    def set_item_names_draw_range(self, range_):
        self._qt_view._set_item_names_draw_range_(range_)

    def set_item_image_frame_draw_enable(self, boolean):
        self.view._set_item_image_frame_draw_enable_(boolean)

    def create_item(self, *args, **kwargs):
        prx_item_widget = gui_prx_wgt_item.PrxListItemWidget()
        prx_item_widget.set_view(self)
        self.view._add_item_widget_(prx_item_widget.widget, **kwargs)
        return prx_item_widget

    # noinspection PyUnusedLocal
    def create_item_widget(self, *args, **kwargs):
        prx_item_widget = gui_prx_wgt_item.PrxListItemWidget()
        prx_item_widget.set_view(self)
        self.view._add_item_widget_(prx_item_widget.widget, **kwargs)
        return prx_item_widget

    def set_visible_tgt_raw_clear(self):
        self.set_visible_tgt_raw({})

    def set_visible_tgt_raw_update(self):
        dic = {}
        prx_items = self.get_all_items()
        for item_prx in prx_items:
            tgt_key = item_prx.get_visible_tgt_key()
            if tgt_key is not None:
                dic.setdefault(
                    tgt_key, []
                ).append(item_prx)
        #
        self.set_visible_tgt_raw(dic)

    def set_visible_tgt_raw(self, raw):
        self.set_gui_attribute(
            'visible_tgt_raw',
            raw
        )

    def get_visible_tgt_raw(self):
        return self.get_gui_attribute('visible_tgt_raw')

    def set_clear(self):
        self._item_dict.clear()
        self._filter_completion_cache = None
        self._qt_view._set_clear_()

    def _get_all_items_(self):
        return self.view._get_all_items_()

    def get_all_items(self):
        return [i._get_item_widget_().gui_proxy for i in self.view._get_all_items_()]

    def get_all_item_widgets(self):
        return [i._get_item_widget_().gui_proxy for i in self.view._get_all_items_()]

    def set_loading_update(self):
        self.view._set_loading_update_()

    def connect_refresh_action_for(self, fnc):
        self._qt_view.f5_key_pressed.connect(fnc)

    def get_checked_item_widgets(self):
        return [i.gui_proxy for i in self._qt_view._get_checked_item_widgets_()]

    def restore_all(self):
        self.set_clear()

    def set_drag_enable(self, boolean):
        self._qt_view._set_drag_enable_(boolean)

    def gui_bustling(self):
        return self._qt_view._gui_bustling_()

    def get_top_tool_bar(self):
        return self._prx_top_tool_bar

    def refresh_viewport_showable_auto(self):
        self._qt_view._refresh_viewport_showable_auto_()

    def set_completion_gain_fnc(self, fnc):
        self._prx_filter_bar.set_completion_gain_fnc(fnc)

    def set_filter_entry_tip(self, text):
        self._prx_filter_bar.set_tip(text)

    def set_menu_data(self, data):
        self._qt_view._set_menu_data_(data)

    def set_scroll_enable(self, boolean):
        self._qt_view._set_scroll_enable_(boolean)

    def get_current_item(self):
        _ = self._qt_view.currentItem()
        if _:
            return _.gui_proxy

    def set_selection_use_multiply(self):
        self._qt_view._set_selection_use_multiply_()

    def set_selection_use_single(self):
        self._qt_view._set_selection_use_single_()

    def get_selected_item_widgets(self):
        return [self._qt_view._get_item_widget_(i).gui_proxy for i in self.view.selectedItems()]

    def connect_press_released_to(self, fnc):
        self._qt_view.press_released.connect(fnc)


class PrxImageView(PrxListView):
    def __init__(self, *args, **kwargs):
        super(PrxImageView, self).__init__(*args, **kwargs)
        self.set_item_frame_size(128, 128+48)
        self.set_item_icon_frame_draw_enable(True)
        self.set_item_name_frame_draw_enable(True)
        self.set_item_image_frame_draw_enable(True)

    def set_textures(self, textures):
        for i_texture in textures:
            for j_texture_unit in i_texture.get_exists_units():
                self._add_texture(self.create_item(), j_texture_unit)

    def _add_texture(self, prx_item, texture_unit):
        def cache_fnc_():
            return [
                prx_item, texture_unit
            ]

        def build_fnc_(data):
            self._set_texture_show_deferred_(data)

        prx_item.set_show_fnc(
            cache_fnc_, build_fnc_
        )

    @staticmethod
    def _set_texture_show_deferred_(data):
        prx_item, texture_unit = data

        show_info_dict = collections.OrderedDict(
            [
                ('name', texture_unit.name),
            ]
        )
        if texture_unit.get_is_readable():
            info = texture_unit.get_info()
            show_info_dict['size'] = '{width} x {height}'.format(**info)
            image_file_path, image_sub_process_cmds = bsc_storage.ImgOiioOptForThumbnail(texture_unit.path).generate_thumbnail_create_args()
            prx_item.set_image(image_file_path)
            prx_item.set_image_show_args(image_file_path, image_sub_process_cmds)

        prx_item.set_name_dict(show_info_dict)
        prx_item.set_tool_tip(
            texture_unit.get_path()
        )
