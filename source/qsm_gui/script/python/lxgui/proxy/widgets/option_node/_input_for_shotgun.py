# coding:utf-8
# gui
from .... import core as _gui_core

from ....qt.widgets import utility as _qt_wgt_utility

from ....qt.widgets import input as _qt_wgt_input

import _base

import _input_base


#   entity
class PrxInputForShotgunEntityChoose(_input_base.AbsPrxInput):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = _qt_wgt_input.QtInputAsConstantWithChoose

    def __init__(self, *args, **kwargs):
        super(PrxInputForShotgunEntityChoose, self).__init__(*args, **kwargs)
        self._shotgun_entity_kwargs = {}
        # entry
        self._qt_input_widget._set_entry_enable_(True)
        # choose
        self._qt_input_widget._set_choose_popup_auto_resize_enable_(False)
        self._qt_input_widget._set_choose_index_show_enable_(True)
        self._qt_input_widget._set_choose_popup_tag_filter_enable_(True)
        self._qt_input_widget._set_choose_popup_keyword_filter_enable_(True)
        self._qt_input_widget._set_choose_popup_item_size_(40, 40)
        self._qt_input_widget._set_value_choose_button_icon_file_path_(
            _gui_core.GuiIcon.get('application/shotgrid')
        )
        self._qt_input_widget._set_choose_button_state_icon_file_path_(
            _gui_core.GuiIcon.get('state/popup')
        )

        self._data = []

        self._stg_entity_dict = {}

    def get(self):
        return self._qt_input_widget._get_value_()

    def set(self, *args, **kwargs):
        self._qt_input_widget._set_value_(args[0])

    def get_stg_entity(self):
        _ = self.get()
        if _ in self._stg_entity_dict:
            return self._stg_entity_dict[self.get()]

    def do_clear(self):
        self._stg_entity_dict = {}
        self._qt_input_widget._clear_input_()

    def set_shotgun_entity_kwargs(
        self,
        shotgun_entity_kwargs,
        name_field=None,
        image_field=None,
        keyword_filter_fields=None,
        tag_filter_fields=None
    ):
        def post_fnc_():
            pass

        def cache_fnc_():
            import lxbasic.shotgun as bsc_shotgun
            return [
                bsc_shotgun.StgConnector.generate_stg_gui_args(
                    shotgun_entity_kwargs, name_field, image_field, keyword_filter_fields, tag_filter_fields
                )
            ]

        def build_fnc_(data_):
            self._stg_entity_dict, names, image_url_dict, keyword_filter_dict, tag_filter_dict = data_[0]
            #
            self._qt_input_widget._set_choose_values_(names)
            # for popup
            #   image
            self._qt_input_widget._set_choose_popup_item_image_url_dict_(image_url_dict)
            #   filter
            self._qt_input_widget._set_choose_popup_item_keyword_filter_dict_(keyword_filter_dict)
            self._qt_input_widget._set_choose_popup_item_tag_filter_dict_(tag_filter_dict)

        self._qt_input_widget._run_build_extra_use_thread_(
            cache_fnc_, build_fnc_, post_fnc_
        )

    def connect_input_changed_to(self, fnc):
        # clear
        self._qt_input_widget.user_input_value_cleared.connect(
            fnc
        )
        # completion
        self._qt_input_widget.user_input_completion_finished.connect(
            fnc
        )
        # choose
        self._qt_input_widget.user_input_choose_changed.connect(
            fnc
        )

    def connect_tab_pressed_to(self, fnc):
        self._qt_input_widget.user_key_tab_pressed.connect(fnc)
        return True

    def set_focus_in(self):
        self._qt_input_widget._set_input_entry_focus_in_()

    def run_build_extra_use_thread(self, cache_fnc, build_fnc, post_fnc):
        self._qt_input_widget._run_build_extra_use_thread_(
            cache_fnc, build_fnc, post_fnc
        )


#   entities
class PrxInputForShotgunEntitiesChoose(_input_base.AbsPrxInput):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = _qt_wgt_input.QtInputAsList

    def __init__(self, *args, **kwargs):
        super(PrxInputForShotgunEntitiesChoose, self).__init__(*args, **kwargs)
        self._shotgun_entity_kwargs = {}
        # entry
        self._qt_input_widget._get_entry_widget_()._set_grid_size_(80, 20)
        self._qt_input_widget._get_entry_widget_()._view_as_grid_mode_()
        self._qt_input_widget._set_entry_enable_(True)
        # resize
        self._qt_input_widget._set_resize_enable_(True)
        self._qt_input_widget._get_resize_handle_()._set_resize_target_(self.widget)
        self._qt_input_widget._get_resize_handle_()._set_resize_minimum_(42)
        self._qt_input_widget._set_size_policy_height_fixed_mode_()
        #
        self._qt_input_widget._set_choose_popup_auto_resize_enable_(False)
        self._qt_input_widget._set_choose_popup_tag_filter_enable_(True)
        self._qt_input_widget._set_choose_popup_keyword_filter_enable_(True)
        self._qt_input_widget._set_choose_popup_item_size_(40, 40)
        self._qt_input_widget._set_value_choose_button_icon_file_path_(
            _gui_core.GuiIcon.get('application/shotgrid')
        )
        self._qt_input_widget._set_choose_button_state_icon_file_path_(
            _gui_core.GuiIcon.get('state/popup')
        )
        #
        self.widget.setFixedHeight(_base.OptionNodeBase.PortHeightA)
        #
        self._data = []

        self._stg_entity_dict = {}

    def get(self):
        return self._qt_input_widget._get_values_()

    def set(self, *args, **kwargs):
        self._qt_input_widget._set_values_(args[0])

    def append(self, value):
        self._qt_input_widget._append_value_(
            value
        )

    def do_clear(self):
        self._qt_input_widget._do_clear_()

    def set_shotgun_entity_kwargs(
        self,
        shotgun_entity_kwargs,
        name_field=None,
        image_field=None,
        keyword_filter_fields=None,
        tag_filter_fields=None
    ):
        def post_fnc_():
            pass

        def cache_fnc_():
            import lxbasic.shotgun as bsc_shotgun
            return [
                bsc_shotgun.StgConnector.generate_stg_gui_args(
                    shotgun_entity_kwargs, name_field, image_field, keyword_filter_fields, tag_filter_fields
                )
            ]

        def build_fnc_(data_):
            self._stg_entity_dict, names, image_url_dict, keyword_filter_dict, tag_filter_dict = data_[0]
            # for popup
            self._qt_input_widget._set_choose_values_(names)
            #   image
            self._qt_input_widget._set_choose_popup_item_image_url_dict_(image_url_dict)
            #   filter
            self._qt_input_widget._set_choose_popup_item_keyword_filter_dict_(keyword_filter_dict)
            self._qt_input_widget._set_choose_popup_item_tag_filter_dict_(tag_filter_dict)

        self._qt_input_widget._run_build_extra_use_thread_(
            cache_fnc_, build_fnc_, post_fnc_
        )

    def run_build_extra_use_thread(self, cache_fnc, build_fnc, post_fnc):
        self._qt_input_widget._run_build_extra_use_thread_(
            cache_fnc, build_fnc, post_fnc
        )
