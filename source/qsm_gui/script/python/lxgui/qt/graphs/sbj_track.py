# coding=utf-8
import functools

import os.path

import enum

import collections

import lxbasic.core as bsc_core
# gui
from ... import core as _gui_core
# qt
from ..core.wrap import *

from .. import core as _qt_core

from .. import abstracts as _qt_abstracts

from . import graph_base as _graph_base

from . import sbj_base as _sbj_base

from . import model as _model


class QtTimetrackTrim(
    QtWidgets.QWidget,
    
    _sbj_base.AbsQtSbjBaseDef
):
    class TrimFlag(enum.IntEnum):
        Start = 0x00
        End = 0x01

    def _refresh_widget_all_(self):
        self._update_node_draw_properties_()

        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()

        bdr_w = self._ng_draw_border_w
        if self._trim_flag == self.TrimFlag.Start:
            frm_x, frm_y = x+bdr_w/2, y+bdr_w/2
            frm_w, frm_h = w, h-bdr_w
        elif self._trim_flag == self.TrimFlag.End:
            frm_x, frm_y = x, y+bdr_w/2
            frm_w, frm_h = w-bdr_w, h-bdr_w
        else:
            raise RuntimeError()

        self._frame_rect.setRect(
            frm_x, frm_y, frm_w, frm_h
        )

        hrd_frm_x, hrd_frm_y = frm_x, frm_y
        hrd_frm_w, hrd_frm_h = frm_w, frm_h/2
        # head
        self._head_frame_rect.setRect(
            hrd_frm_x, hrd_frm_y, hrd_frm_w, hrd_frm_h
        )

        mrg = self._ng_draw_icon_h/2
        
        bdy_frm_x, bdy_frm_y = frm_x, frm_y+frm_h/2
        bdy_frm_w, bdy_frm_h = frm_w, frm_h/2

        self._body_frame_rect.setRect(
            bdy_frm_x, bdy_frm_y, bdy_frm_w, bdy_frm_h
        )
        
        self._text_rect.setRect(
            bdy_frm_x+mrg, bdy_frm_y, bdy_frm_w-mrg*2, bdy_frm_h
        )

    def __init__(self, *args, **kwargs):
        super(QtTimetrackTrim, self).__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self._init_sbj_base_def_(self)

        self._frame_rect = QtCore.QRect()
        self._head_frame_rect = QtCore.QRect()
        self._body_frame_rect = QtCore.QRect()
        self._text_rect = QtCore.QRect()

        self._trim_flag = self.TrimFlag.Start

        self._node = None
        
        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtNGPainter(self)
        painter._set_antialiasing_(False)

        painter._set_text_color_(
            _gui_core.GuiRgba.DarkWhite
        )
        painter._set_font_(
            _qt_core.QtFont.generate(size=self._ng_draw_font_h, weight=50)
        )
        if self._trim_flag == self.TrimFlag.Start:
            start_text = self.fontMetrics().elidedText(
                str('{}'.format(self._node._track_model.start)),
                QtCore.Qt.ElideMiddle,
                self._text_rect.width()-4,
                QtCore.Qt.TextShowMnemonic
            )
            painter.drawText(
                self._text_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                start_text
            )
        elif self._trim_flag == self.TrimFlag.End:
            end_text = self.fontMetrics().elidedText(
                str('{}'.format(self._node._track_model.basic_end)),
                QtCore.Qt.ElideMiddle,
                self._text_rect.width()-4,
                QtCore.Qt.TextShowMnemonic
            )
            painter.drawText(
                self._text_rect, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter,
                end_text
            )

        self._draw_frame_(painter)

    def _draw_frame_(self, painter):

        painter._set_border_color_(
            _gui_core.GuiRgba.DarkGray
        )
        painter._set_background_color_(
            _gui_core.GuiRgba.Transparent
        )
        painter._set_border_width_(self._ng_draw_border_w)
        painter.drawRect(
            self._frame_rect
        )

    def _set_trim_flag_(self, flag):
        self._trim_flag = flag

    def _set_node_(self, widget):
        self._node = widget


class QtTimeTrack(
    QtWidgets.QWidget,

    _qt_abstracts.AbsQtFrameBaseDef,
    _qt_abstracts.AbsQtTypeDef,
    _qt_abstracts.AbsQtNameBaseDef,
    _qt_abstracts.AbsQtIconBaseDef,
    _qt_abstracts.AbsQtImageBaseDef,

    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForHoverDef,
    _qt_abstracts.AbsQtActionForPressDef,
    _qt_abstracts.AbsQtActionForSelectDef,

    _sbj_base.AbsQtNodeDef,

    _sbj_base.AbsQtBypassDef,
):
    def _refresh_widget_all_(self):
        self._update_node_rect_properties_()
        self._update_node_geometry_()

        self._update_node_draw_properties_()
        self._refresh_widget_draw_geometry_()

        self._update_attachments_()

        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()

        bdr_w = self._ng_draw_border_w
        x_0, y_0 = x+bdr_w/2, y+bdr_w/2
        w_0, h_0 = w-bdr_w, h-bdr_w

        self._frame_draw_rect.setRect(x_0, y_0, w_0, h_0)
        # for selection
        self._node_selection_rect.setRect(
            x, y, w, h
        )
        # frame
        frm_x, frm_y = x_0, y_0
        frm_w, frm_h = w_0, h_0
        self._node_rect_frame.setRect(
            frm_x, frm_y, frm_w, frm_h
        )
        hrd_frm_x, hrd_frm_y = frm_x, frm_y
        hrd_frm_w, hrd_frm_h = frm_w, frm_h/2

        mrg = self._ng_draw_icon_h/2
        # time offset
        start_offset = self._track_model.start_offset
        start_offset_x = self._track_model.compute_w_by_count(start_offset)
        # head
        self._head_frame_rect.setRect(
            hrd_frm_x, hrd_frm_y, hrd_frm_w, hrd_frm_h
        )
        # body
        bdy_frm_x, bdy_frm_y = frm_x, frm_y+frm_h/2
        bdy_frm_w, bdy_frm_h = frm_w, frm_h/2

        self._body_frame_rect.setRect(
            bdy_frm_x, bdy_frm_y, bdy_frm_w, bdy_frm_h
        )
        # time offset line
        self._time_start_draw_line.setLine(
            start_offset_x, frm_y, start_offset_x, frm_h
        )
        # time
        self._time_start_rect.setRect(
            start_offset_x+mrg, bdy_frm_y, 64, bdy_frm_h
        )
        self._time_clip_start_rect.setRect(
            bdy_frm_x+mrg, bdy_frm_y, bdy_frm_w*(1.0/3.0)-mrg, bdy_frm_h
        )
        self._time_clip_end_rect.setRect(
            bdy_frm_x+bdy_frm_w*(2.0/3.0), bdy_frm_y, bdy_frm_w*(1.0/3.0)-mrg, bdy_frm_h
        )
        # time basic
        basic_start_offset_x = self._track_model.compute_w_by_count(
            self._track_model.basic_start_offset
        )
        basic_end_offset_x = self._track_model.compute_w_by_count(
            self._track_model.basic_end_offset
        )
        self._time_basic_frame_draw_rect.setRect(
            basic_start_offset_x, hrd_frm_y,
            basic_end_offset_x-basic_start_offset_x, hrd_frm_h
        )
        # count
        tme_c_x = max(bdy_frm_x, start_offset_x)
        tme_c_w = min(bdy_frm_w-tme_c_x, basic_end_offset_x-start_offset_x)
        self._count_draw_rect.setRect(
            tme_c_x, bdy_frm_y, tme_c_w, bdy_frm_h
        )

        self._name_draw_rect.setRect(
            tme_c_x, hrd_frm_y, tme_c_w, hrd_frm_h
        )
        # resize
        ofs_w = self._ng_draw_icon_h
        ofs_w = min(ofs_w, frm_w/2)
        self._time_resize_left_rect.setRect(
            bdy_frm_x, bdy_frm_y, ofs_w, bdy_frm_h
        )
        self._time_scale_left_rect.setRect(
            hrd_frm_x, hrd_frm_y, ofs_w, hrd_frm_h
        )
        #
        self._time_resize_right_rect.setRect(
            bdy_frm_x+frm_w-ofs_w, bdy_frm_y, ofs_w, bdy_frm_h
        )
        self._time_scale_right_rect.setRect(
            hrd_frm_x+frm_w-ofs_w, hrd_frm_y, ofs_w, hrd_frm_h
        )

        pre_blend_w = self._track_model.compute_w_by_count(
            self._track_model.pre_blend
        )
        self._pre_blend_rect.setRect(
            frm_x, frm_y, pre_blend_w, hrd_frm_h
        )
        # input and output
        self._node_intput_rect.setRect(
            hrd_frm_x, hrd_frm_y, ofs_w, hrd_frm_h
        )
        self._node_output_rect.setRect(
            hrd_frm_x+frm_w-ofs_w, hrd_frm_y, ofs_w, hrd_frm_h
        )

    def _update_basic_coord_(self, x, y):
        clip_start = self._track_model.compute_clip_start_loc(x)
        bsc_x = self._track_model.compute_basic_x_at(clip_start)
        self._track_model.offset_by_clip_start(clip_start)

        layer_index = self._track_model.compute_layer_index_loc(y)
        self._track_model.layer_index = layer_index
        bsc_y = self._track_model.compute_basic_y_at(layer_index)
        # print bsc_y
        # update coord
        self._node_basic_x, self._node_basic_y = bsc_x, bsc_y

    def _update_basic_args_as_left_(self, x, y, w, h):
        clip_start = self._track_model.compute_clip_start_loc(x)
        clip_end = self._track_model.clip_end
        clip_start = min(clip_start, clip_end-1)
        bsc_x = self._track_model.compute_basic_x_at(clip_start)
        self._track_model.clip_start = clip_start
        clip_count = self._track_model.clip_count
        bsc_w = self._track_model.compute_basic_w_by(clip_count)
        # update geometry
        self._node_basic_x, self._node_basic_y = bsc_x, self._node_basic_y
        self._node_basic_w, self._node_basic_h = bsc_w, self._node_basic_h

    def _update_basic_args_as_right_(self, w, h):
        clip_count = self._track_model.compute_clip_count_by(w)
        clip_count = max(clip_count, 1)
        bsc_w = self._track_model.compute_basic_w_by(clip_count)
        self._track_model.clip_count = clip_count
        # update size
        self._node_basic_w, self._node_basic_h = bsc_w, self._node_basic_h

    def _do_hover_move_(self, event):
        pos = event.pos()
        if self._node_selection_rect.contains(pos):
            self._set_hovered_(True)
            if self._time_resize_left_rect.contains(pos):
                self._set_action_flag_(self.ActionFlag.NGTimeResizeLeft)
                self._update_graph_action_flag_(self.ActionFlag.NGNodeAnyAction)
            elif self._time_resize_right_rect.contains(pos):
                self._set_action_flag_(self.ActionFlag.NGTimeResizeRight)
                self._update_graph_action_flag_(self.ActionFlag.NGNodeAnyAction)
            #
            elif self._time_scale_left_rect.contains(pos):
                self._set_action_flag_(self.ActionFlag.NGTimeScaleLeft)
                self._update_graph_action_flag_(self.ActionFlag.NGNodeAnyAction)
            elif self._time_scale_right_rect.contains(pos):
                self._set_action_flag_(self.ActionFlag.NGTimeScaleRight)
                self._update_graph_action_flag_(self.ActionFlag.NGNodeAnyAction)
            else:
                self._clear_all_action_flags_()
                self._graph._clear_all_action_flags_()
        else:
            self._set_hovered_(False)
            self._clear_all_action_flags_()

    def __init__(self, *args, **kwargs):
        super(QtTimeTrack, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        
        self._init_type_base_def_(self)
        self._init_name_base_def_(self)
        self._init_icon_base_def_(self)
        self._init_image_base_def_(self)

        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)
        self._init_action_for_select_def_(self)
        
        self._init_frame_base_def_(self)

        self._init_node_def_(self)
        self._init_bypass_def_(self)

        self._time_start_rect = QtCore.QRect()
        self._time_clip_start_rect, self._time_clip_end_rect = QtCore.QRect(), QtCore.QRect()
        self._time_start_draw_line = QtCore.QLine()
        self._count_draw_rect = QtCore.QRect()
        self._time_resize_left_rect, self._time_resize_right_rect = QtCore.QRect(), QtCore.QRect()
        self._time_scale_left_rect, self._time_scale_right_rect = QtCore.QRect(), QtCore.QRect()

        self._track_model = None
        self._track_last_model = None

        self._time_basic_frame_draw_rect = QtCore.QRect()
        
        self._layer_index = 0

        self._start_timetrack_trim = None
        self._end_timetrack_trim = None

        self._pre_blend_rect = QtCore.QRect()
        self._post_blend_rect = QtCore.QRect()

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            #
            if event.type() == QtCore.QEvent.Resize:
                pass
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._do_hover_move_(event)
                    if self._is_action_flag_match_(
                        self.ActionFlag.NGTimeResizeLeft, self.ActionFlag.NGTimeResizeRight
                    ):
                        self._do_press_resize_start_(event)
                        return False
                    elif self._is_action_flag_match_(
                        self.ActionFlag.NGTimeScaleLeft, self.ActionFlag.NGTimeScaleRight
                    ):
                        return False
                    else:
                        self._update_press_click_flag_(event)
                        if self._is_action_flag_match_(
                            self.ActionFlag.NGNodePressClick,
                        ):
                            self._do_press_click_start_(event)
                            self._do_press_move_start_(event)
                #
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    if self._is_action_flag_match_(
                        self.ActionFlag.NGTimeResizeLeft, self.ActionFlag.NGTimeResizeRight
                    ):
                        self._do_press_resize_(event)
                        return False
                    elif self._is_action_flag_match_(
                        self.ActionFlag.NGTimeScaleLeft, self.ActionFlag.NGTimeScaleRight
                    ):
                        return False
                    else:
                        if not self._graph._is_action_mdf_flags_include_(
                            self.ActionFlag.RectSelectMove
                        ):
                            self._update_press_move_flag_(event)
                            if self._is_action_flag_match_(
                                self.ActionFlag.NGNodePressMove
                            ):
                                self._do_press_click_(event)
                                self._do_press_move_(event)
                elif event.buttons() == QtCore.Qt.RightButton:
                    pass
                elif event.buttons() == QtCore.Qt.MidButton:
                    pass
                elif event.button() == QtCore.Qt.NoButton:
                    self._do_hover_move_(event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._is_action_flag_match_(
                        self.ActionFlag.NGTimeResizeLeft, self.ActionFlag.NGTimeResizeRight
                    ):
                        self._do_press_resize_end_(event)
                        return False
                    elif self._is_action_flag_match_(
                        self.ActionFlag.NGTimeScaleLeft, self.ActionFlag.NGTimeScaleRight
                    ):
                        return False
                    else:
                        if self._is_action_flag_match_(
                            self.ActionFlag.NGNodePressClick,
                            self.ActionFlag.NGNodePressMove
                        ):
                            self._do_press_click_end_(event)
                            self._do_press_move_end_(event)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
                #
                self._clear_all_action_flags_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtNGPainter(self)

        painter._set_antialiasing_(False)
        # basic
        self._draw_basic_(painter)
        # time offset
        if self._track_model.start_offset > 0:
            painter._set_border_color_(
                _gui_core.GuiRgba.Red
            )
            painter.drawLine(
                self._time_start_draw_line
            )
            start_text_ = str(self._track_model.start)
            painter.drawText(
                self._time_start_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                start_text_
            )
        # time
        painter._set_text_color_(
            _gui_core.GuiRgba.DarkWhite
        )
        painter._set_font_(
            _qt_core.QtFont.generate(size=self._ng_draw_font_h, weight=50)
        )

        start_text = self.fontMetrics().elidedText(
            str(self._track_model.clip_start),
            QtCore.Qt.ElideMiddle,
            self._time_clip_start_rect.width()-4,
            QtCore.Qt.TextShowMnemonic
        )
        painter.drawText(
            self._time_clip_start_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
            start_text
        )
        end_text = self.fontMetrics().elidedText(
            str(self._track_model.clip_end),
            QtCore.Qt.ElideMiddle,
            self._time_clip_end_rect.width()-4,
            QtCore.Qt.TextShowMnemonic
        )
        painter.drawText(
            self._time_clip_end_rect, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter,
            end_text
        )
        
        count_text = self.fontMetrics().elidedText(
            str('{}({})'.format(self._track_model.clip_count, self._track_model.speed)),
            QtCore.Qt.ElideMiddle,
            self._count_draw_rect.width()-4,
            QtCore.Qt.TextShowMnemonic
        )
        painter.drawText(
            self._count_draw_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            count_text
        )

        self._draw_frame_(painter)

    def _draw_frame_(self, painter):
        if self._is_selected:
            border_rgba = _gui_core.GuiRgba.LightAzureBlue
        elif self._is_hovered:
            border_rgba = _gui_core.GuiRgba.LightOrange
        else:
            border_rgba = _gui_core.GuiRgba.LightGray

        painter._set_border_color_(
            border_rgba
        )
        painter._set_background_color_(
            _gui_core.GuiRgba.Transparent
        )
        painter._set_border_width_(2)
        painter.drawRect(
            self._frame_draw_rect
        )

    def _draw_basic_(self, painter):
        head_rgb_0 = self._track_model.rgb
        head_rgb_1 = list(head_rgb_0)+[31]

        painter._set_border_color_(
            head_rgb_0
        )
        painter._set_background_color_(
            head_rgb_1
        )
        painter.drawRect(
            self._frame_draw_rect
        )

        painter._set_border_color_(
            head_rgb_0
        )
        painter._set_background_color_(
            head_rgb_0
        )
        painter.drawRect(
            self._time_basic_frame_draw_rect
        )

        painter._set_text_color_(
            _gui_core.GuiRgba.LightBlack
        )
        painter._set_font_(
            _qt_core.QtFont.generate(size=self._ng_draw_font_h, weight=75)
        )

        text = self.fontMetrics().elidedText(
            self._track_model.key,
            QtCore.Qt.ElideMiddle,
            self._name_draw_rect.width()-4,
            QtCore.Qt.TextShowMnemonic
        )
        painter.drawText(
            self._name_draw_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            text
        )

    def _setup_track_(self, key, start, source_start, source_end, pre_cycle, post_cycle, layer_index):
        self._track_model = self._graph._track_stage_model.create_one(
            self, key, start, source_start, source_end, pre_cycle, post_cycle, layer_index
        )
        self._pull_track_model_(self._track_model)

        self._build_timetrack_trim_()

    def _push_last_properties_(self):
        self._push_track_model_()
    
    def _push_track_model_(self):
        self._track_last_model = self._track_model.copy()
    
    def _pull_track_model_(self, time_model):
        self._track_model = time_model
        x, y, w, h = self._track_model.compute_timetrack_args()
        self._node_basic_x, self._node_basic_y = x, y
        self._node_basic_w, self._node_basic_h = w, h
        self._refresh_widget_all_()

    def _build_timetrack_trim_(self):
        self._start_timetrack_trim = QtTimetrackTrim(
            self._graph._timetrack_trim_sbj_layer
        )
        self._start_timetrack_trim._set_trim_flag_(self._start_timetrack_trim.TrimFlag.Start)
        self._start_timetrack_trim.hide()
        self._start_timetrack_trim._set_graph_(self._graph)
        self._start_timetrack_trim._set_node_(self)

        self._end_timetrack_trim = QtTimetrackTrim(
            self._graph._timetrack_trim_sbj_layer
        )
        self._end_timetrack_trim._set_trim_flag_(self._end_timetrack_trim.TrimFlag.End)
        self._end_timetrack_trim.hide()
        self._end_timetrack_trim._set_graph_(self._graph)
        self._end_timetrack_trim._set_node_(self)

    def _update_attachments_(self):
        self._update_connections_()

        # time offset
        if self._start_timetrack_trim is not None:
            start_trim = self._track_model.start_trim

            if start_trim == 0:
                self._start_timetrack_trim.hide()
            elif start_trim > 0:
                trm_w = self._track_model.compute_w_by_count(start_trim)
                trm_x, trm_y = self.x()-trm_w, self.y()
                trm_h = self.height()
                self._start_timetrack_trim.setGeometry(
                    trm_x, trm_y, trm_w, trm_h
                )
                self._start_timetrack_trim.show()

        if self._end_timetrack_trim is not None:
            end_trim = self._track_model.basic_end_trim
            if end_trim == 0:
                self._end_timetrack_trim.hide()
            elif end_trim > 0:
                trm_w = self._track_model.compute_w_by_count(end_trim)
                trm_x, trm_y = self.x()+self.width(), self.y()
                trm_h = self.height()
                self._end_timetrack_trim.setGeometry(
                    trm_x, trm_y, trm_w, trm_h
                )
                self._end_timetrack_trim.show()
