# coding=utf-8
import os

import lxbasic.core as bsc_core
# gui
from ... import core as _gui_core
# qt
from ..core.wrap import *


class AbsQtBuildBaseForItemDef(object):
    def _init_build_base_for_item_def_(self):
        pass

    def _get_view_(self):
        raise NotImplementedError()

    def _generate_item_show_runnable_(self, cache_fnc, build_fnc, post_fnc=None):
        return self._get_view_()._generate_thread_(cache_fnc, build_fnc, post_fnc=post_fnc)


# show base
# for item
class AbsQtShowBaseForVirtualItemDef(
    AbsQtBuildBaseForItemDef
):
    ShowStatus = _gui_core.GuiShowStatus

    def _refresh_widget_all_(self, *args, **kwargs):
        raise NotImplementedError()

    def _refresh_widget_draw_(self):
        raise NotImplementedError()

    def _get_view_(self):
        raise NotImplementedError()

    def _get_item_widget_(self):
        raise NotImplementedError()

    def _init_show_base_for_virtual_item_def_(self, widget):
        self._widget = widget
        #
        if bsc_core.BscApplication.get_is_maya():
            self._item_show_use_thread = False
        else:
            self._item_show_use_thread = True
        #
        self._item_show_runnable = None
        self._item_show_image_runnable = None
        #
        self._item_show_cache_fnc = None
        self._item_show_build_fnc = None
        #
        self._item_show_status = self.ShowStatus.Unknown
        # image
        self._item_show_image_cache_fnc = None
        self._item_show_image_build_fnc = None
        #
        self._item_show_image_status = self.ShowStatus.Unknown

        self._init_build_base_for_item_def_()

        self._item_show_flag = False
        self._item_show_image_flag = False

    def _set_item_show_flag_(self, boolean):
        self._item_show_flag = boolean

    def _get_item_show_flag_(self):
        return self._item_show_flag

    def _setup_item_show_(self, view):
        self._item_show_runnable = None
        self._item_show_image_runnable = None
        #
        self._item_show_timer = QtCore.QTimer(view)
        self._item_show_loading_index = 0
        self._item_show_loading_timer = QtCore.QTimer(view)
        self._item_show_loading_timer.timeout.connect(self._update_item_show_loading_)
        #
        self._item_show_image_timer = QtCore.QTimer(view)
        self._item_show_image_loading_index = 0
        self._item_show_image_loading_timer = QtCore.QTimer(view)
        self._item_show_image_loading_timer.timeout.connect(self._update_item_show_image_loading_)
        #
        self._item_show_image_sub_process = None
        self._item_show_image_cmd = None
        self._item_show_image_path = None

    def _set_item_show_build_fnc_(self, method):
        def cache_fnc_():
            return []

        # noinspection PyUnusedLocal
        def build_fnc_(data):
            method()

        if method is not None:
            self._set_item_show_fnc_(cache_fnc_, build_fnc_)

    # fnc
    def _set_item_show_fnc_(self, cache_fnc, build_fnc):
        if cache_fnc is not None and build_fnc is not None:
            if self._item_show_cache_fnc is None and self._item_show_build_fnc is None:
                self._item_show_cache_fnc = cache_fnc
                self._item_show_build_fnc = build_fnc
                self._item_show_status = self.ShowStatus.Waiting

                self._item_show_flag = True
                if self._get_item_is_viewport_showable_() is True:
                    self._checkout_item_show_()

    def _checkout_item_show_(self, delay_time=0):
        def run_fnc_():
            if self._item_show_cache_fnc is not None:
                self._start_item_show_()

        if self._item_show_flag is True:
            self._checkout_item_show_loading_()
            if delay_time > 0:
                self._item_show_timer.singleShot(delay_time, run_fnc_)
            else:
                run_fnc_()

    def _checkout_item_show_loading_(self):
        if self._item_show_status == self.ShowStatus.Waiting:
            self._item_show_loading_timer.start(100)

    def _start_item_show_(self):
        if self._item_show_flag is True:
            # update flag first
            self._item_show_flag = False
            self._item_show_status = self.ShowStatus.Loading
            if self._item_show_use_thread is True:
                self._item_show_runnable = self._generate_item_show_runnable_(
                    self._item_show_cache_fnc,
                    self._item_show_build_fnc,
                    self._finish_item_show_
                )
                self._item_show_runnable.do_start()
            else:
                self._item_show_build_fnc(
                    self._item_show_cache_fnc()
                )
                self._finish_item_show_()

    def _finish_item_show_(self):
        self._set_item_show_stop_(
            self.ShowStatus.Finished
        )

    def _set_item_show_stop_(self, status):
        self._item_show_status = status
        self._finish_item_show_loading_()

    def _get_item_show_is_finished_(self):
        return self._item_show_status in {
            self.ShowStatus.Completed, self.ShowStatus.Failed
        }

    # loading
    def _update_item_show_loading_(self):
        self._item_show_loading_index += 1
        # noinspection PyBroadException
        try:
            self._refresh_widget_draw_()
        except Exception:
            pass

    def _finish_item_show_loading_(self):
        # noinspection PyBroadException
        try:
            self._item_show_loading_timer.stop()
            self._refresh_widget_draw_()
        except Exception:
            pass

    # image fnc
    def _set_item_show_image_cmd_(self, image_file_path, cmd):
        def cache_fnc_():
            # noinspection PyBroadException
            try:
                bsc_core.BscProcess.execute_with_result(
                    cmd
                )
            except Exception:
                pass
            return []

        # noinspection PyUnusedLocal
        def build_fnc_(data):
            pass

        if cmd is not None:
            self._item_show_image_path = image_file_path
            self._set_item_show_image_fnc_(cache_fnc_, build_fnc_)

    def _set_item_show_image_fnc_(self, cache_fnc, build_fnc):
        if cache_fnc is not None and build_fnc is not None:
            if self._item_show_image_cache_fnc is None and self._item_show_image_build_fnc is None:
                self._item_show_image_cache_fnc = cache_fnc
                self._item_show_image_build_fnc = build_fnc

                self._item_show_image_flag = True

                self._item_show_image_status = self.ShowStatus.Waiting
                if self._get_item_is_viewport_showable_() is True:
                    self._checkout_item_show_image_()

    def _checkout_item_show_image_(self, delay_time=0):
        def run_fnc():
            if self._item_show_image_cache_fnc is not None:
                self._start_item_show_image_()

        if self._item_show_image_flag is True:
            self._checkout_item_show_image_loading_()
            if delay_time > 0:
                self._item_show_image_timer.singleShot(delay_time, run_fnc)
            else:
                run_fnc()

    def _checkout_item_show_image_loading_(self):
        if self._item_show_image_status == self.ShowStatus.Waiting:
            self._item_show_image_loading_timer.start(100)

    def _start_item_show_image_(self):
        if self._item_show_image_flag is True:
            self._item_show_image_status = self.ShowStatus.Loading
            self._item_show_image_flag = False
            if self._item_show_use_thread is True:
                self._item_show_image_runnable = self._generate_item_show_runnable_(
                    self._item_show_image_cache_fnc,
                    self._item_show_image_build_fnc,
                    self._finish_item_show_image_
                )
                self._item_show_image_runnable.do_start()
            else:
                self._item_show_image_build_fnc(
                    self._item_show_image_cache_fnc()
                )
                self._finish_item_show_image_()

    def _finish_item_show_image_(self):
        if self._item_show_image_path is not None:
            if os.path.isfile(self._item_show_image_path) is True:
                self._set_item_show_image_stop_(self.ShowStatus.Completed)
            else:
                self._set_item_show_image_stop_(self.ShowStatus.Failed)

    def _set_item_show_image_stop_(self, status):
        self._item_show_image_status = status
        if status == self.ShowStatus.Failed:
            item_widget = self._get_item_widget_()
            if item_widget is not None:
                item_widget._set_image_path_(
                    _gui_core.GuiIcon.get('image_loading_failed_error')
                )
        #
        self._finish_item_show_image_loading_()

    def _get_item_is_viewport_showable_(self, *args, **kwargs):
        raise NotImplementedError()

    def _update_item_show_image_loading_(self):
        self._item_show_image_loading_index += 1
        # noinspection PyBroadException
        try:
            self._refresh_widget_all_()
        except Exception:
            pass

    def _finish_item_show_image_loading_(self):
        # noinspection PyBroadException
        try:
            self._item_show_image_loading_timer.stop()
            self._refresh_widget_all_()
        except Exception:
            pass

    def _checkout_item_show_all_(self):
        self._checkout_item_show_()
        self._checkout_item_show_image_()

    def _stop_item_show_all_(self):
        self._set_item_show_stop_(self.ShowStatus.Stopped)
        self._set_item_show_image_stop_(self.ShowStatus.Stopped)

    def _kill_item_all_show_runnables_(self):
        if self._item_show_runnable is not None:
            self._item_show_runnable.do_kill()
        #
        if self._item_show_image_runnable is not None:
            self._item_show_image_runnable.do_kill()

    def _set_item_viewport_visible_(self, boolean):
        if boolean is True:
            self._checkout_item_show_all_()
        #
        self._set_item_widget_visible_(boolean)

    def _set_item_widget_visible_(self, boolean):
        raise NotImplementedError()

    def _set_viewport_show_enable_(self, boolean):
        self._is_viewport_show_enable = boolean

    def _set_item_show_start_auto_(self):
        if self._get_item_is_viewport_showable_() is True:
            self._checkout_item_show_all_()


# for view
class AbsQtShowBaseForViewDef(object):
    def _get_all_items_(self):
        raise NotImplementedError()

    def _init_show_base_for_view_def_(self, widget):
        self._widget = widget

    def _get_view_item_viewport_showable_(self, item):
        i_rect = self._widget.visualItemRect(item)
        i_w, i_h = i_rect.width(), i_rect.height()
        # check is visible
        if i_w != 0 and i_h != 0:
            viewport_rect = self._widget.rect()
            v_t, v_b = viewport_rect.top(), viewport_rect.bottom()
            i_t, i_b = i_rect.top(), i_rect.bottom()
            if v_b >= i_t and i_b >= v_t:
                return True
        return False

    def _refresh_all_items_viewport_showable_(self, includes=None):
        if isinstance(includes, (tuple, list)):
            items_ = includes
        else:
            items_ = self._widget._get_all_items_()
        #
        for i_item in items_:
            if i_item.isHidden() is False:
                if self._get_view_item_viewport_showable_(i_item) is True:
                    i_item._set_item_viewport_visible_(True)
        # todo: use update() error in maya 2017?
        # noinspection PyBroadException
        try:
            self._widget.update()
        except Exception:
            pass

    def _refresh_viewport_showable_auto_(self):
        self._refresh_all_items_viewport_showable_(
            self._get_all_show_items_()
        )

    @qt_slot()
    def _refresh_viewport_showable_by_scroll_(self):
        self._refresh_viewport_showable_auto_()

    def _get_all_show_items_(self):
        return [i for i in self._get_all_items_() if i._get_item_show_flag_() is True]