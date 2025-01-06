# coding=utf-8
import enum
# gui
from .... import core as _gui_core
# qt
from ...core.wrap import *

from ... import core as _qt_core

from ... import abstracts as _qt_abstracts

from ..base import sbj as _bsc_sbj


class QtTrackTrim(
    QtWidgets.QWidget,

    _bsc_sbj.AbsQtSbjBaseDef
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

        bdr_w = 1
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
        super(QtTrackTrim, self).__init__(*args, **kwargs)
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

        painter._draw_alternating_colors_by_rect_(
            self._frame_rect,
            [_gui_core.GuiRgba.LightBlack, _gui_core.GuiRgba.Transparent],
            x_offset=-self.x(), y_offset=-self.y()
        )

        painter._set_text_color_(
            _gui_core.GuiRgba.DarkWhite
        )
        painter._set_font_(
            _qt_core.QtFont.generate(size=8)
        )
        if self._trim_flag == self.TrimFlag.Start:
            start_text = painter.fontMetrics().elidedText(
                str('{}'.format(self._node._track_model.start)),
                QtCore.Qt.ElideMiddle,
                self._text_rect.width(),
                QtCore.Qt.TextShowMnemonic
            )
            painter.drawText(
                self._text_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                start_text
            )
        elif self._trim_flag == self.TrimFlag.End:
            end_text = painter.fontMetrics().elidedText(
                str('{}'.format(self._node._track_model.basic_end)),
                QtCore.Qt.ElideMiddle,
                self._text_rect.width(),
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
        painter.drawRect(
            self._frame_rect
        )

    def _set_trim_flag_(self, flag):
        self._trim_flag = flag

    def _set_node_(self, widget):
        self._node = widget


class QtTrackNode(
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

    _bsc_sbj.AbsQtNodeDef,

    _bsc_sbj.AbsQtBypassDef,
):
    TRIM_FLAG = True
    SCALE_FLAG = True

    def _refresh_widget_all_(self):
        if self._track_model.is_trash > 0:
            self.hide()
        else:
            self.show()

        self._update_node_geometry_properties_()
        self._update_node_geometry_()

        self._update_node_draw_properties_()
        
        self._update_node_attachments_()

        flag = self._refresh_widget_draw_geometry_()

        if flag is True:
            self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()

        # fixme, condition is not very well
        # size = (w, h)
        # if size == self._size_tmp:
        #     return False
        #
        # self._size_tmp = size

        bdr_w = 1
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
            start_offset_x, bdy_frm_y, start_offset_x, frm_h
        )
        # time source
        scale_source_count = self._track_model.scale_source_count
        scale_source_w = self._track_model.compute_w_by_count(scale_source_count)
        self._time_source_rect.setRect(
            start_offset_x, bdy_frm_y, scale_source_w, frm_h
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
            self._track_model.basic_start_offset_to_start
        )
        basic_end_offset_x = self._track_model.compute_w_by_count(
            self._track_model.basic_end_offset_to_start
        )
        self._time_basic_frame_rect.setRect(
            basic_start_offset_x, hrd_frm_y,
            basic_end_offset_x-basic_start_offset_x, hrd_frm_h
        )
        if basic_start_offset_x > x:
            self._time_left_draw_flag = True
            self._time_left_frame_rect.setRect(
                x, hrd_frm_y, basic_start_offset_x-x, hrd_frm_h
            )
        else:
            self._time_left_draw_flag = False

        if basic_end_offset_x < x+w:
            self._time_right_draw_flag = True
            self._time_right_frame_rect.setRect(
                basic_end_offset_x, hrd_frm_y, x+w-basic_end_offset_x, hrd_frm_h
            )
        else:
            self._time_right_draw_flag = False
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
        self._trim_left_rect.setRect(
            bdy_frm_x, bdy_frm_y, ofs_w, bdy_frm_h
        )
        self._scale_left_rect.setRect(
            hrd_frm_x, hrd_frm_y, ofs_w, hrd_frm_h
        )
        #
        self._trim_right_rect.setRect(
            bdy_frm_x+frm_w-ofs_w, bdy_frm_y, ofs_w, bdy_frm_h
        )
        self._scale_right_rect.setRect(
            hrd_frm_x+frm_w-ofs_w, hrd_frm_y, ofs_w, hrd_frm_h
        )
        # input and output
        self._node_intput_rect.setRect(
            hrd_frm_x, hrd_frm_y, ofs_w, hrd_frm_h
        )
        self._node_output_rect.setRect(
            hrd_frm_x+frm_w-ofs_w, hrd_frm_y, ofs_w, hrd_frm_h
        )
        return True

    def _refresh_by_trash_(self):
        # is trash
        if self._track_model.is_trash > 0:
            self.hide()
        else:
            self.show()

        self._refresh_widget_draw_()

    def _refresh_by_bypass_(self):
        self._refresh_widget_draw_()

    def _update_basic_coord_as_move_(self, x, y):
        clip_start = self._track_model.compute_clip_start_loc(x)
        self._track_model.move_by_clip_start(clip_start)

        bsc_x = self._track_model.compute_basic_x_at(clip_start)

        layer_index = self._track_model.compute_layer_index_loc(y)
        self._track_model.layer_index = layer_index
        bsc_y = self._track_model.compute_basic_y_at(layer_index)
        # update coord
        self._node_basic_x, self._node_basic_y = bsc_x, bsc_y

    # resize
    def _update_basic_args_as_left_trim_(self, x, y, w, h):
        # position
        clip_start = self._track_model.trim_by_clip_start(
            self._track_model.compute_clip_start_loc(x), auto_cycle=_qt_core.QtUtil.is_ctrl_modifier()
        )
        # update geometry
        self._node_basic_x = self._track_model.compute_basic_x_at(clip_start)
        self._node_basic_w = self._track_model.compute_basic_w_by(self._track_model.clip_count)

    def _update_basic_args_as_right_trim_(self, w, h):
        clip_count = self._track_model.trim_by_clip_count(
            self._track_model.compute_clip_count_by(w), auto_cycle=_qt_core.QtUtil.is_ctrl_modifier()
        )
        # update size
        self._node_basic_w = self._track_model.compute_basic_w_by(clip_count)

    # scale
    def _update_basic_args_as_left_scale_(self, x, y, w, h):
        # position
        clip_start = self._track_model.scale_by_clip_start(
            self._track_model.compute_clip_start_loc(x)
        )
        # update geometry
        self._node_basic_x = self._track_model.compute_basic_x_at(clip_start)
        self._node_basic_w = self._track_model.compute_basic_w_by(self._track_model.clip_count)

    def _update_basic_args_as_right_scale_(self, w, h):
        # size
        clip_count = self._track_model.scale_by_clip_count(
            self._track_model.compute_clip_count_by(w)
        )
        # update size
        self._node_basic_w = self._track_model.compute_basic_w_by(clip_count)

    def _do_hover_move_(self, event):
        pos = event.pos()
        if self._node_selection_rect.contains(pos):
            self._graph._update_hover_node_(self)
            self._set_hovered_(True)
            # trim
            trim_flag = False
            if self.TRIM_FLAG is True:
                if self._trim_left_rect.contains(pos):
                    self._set_action_flag_(self.ActionFlag.NGSbjTrimLeft)
                    self._update_graph_action_flag_(self.ActionFlag.NGNodeAnyAction)
                    trim_flag = True
                elif self._trim_right_rect.contains(pos):
                    self._set_action_flag_(self.ActionFlag.NGSbjTrimRight)
                    self._update_graph_action_flag_(self.ActionFlag.NGNodeAnyAction)
                    trim_flag = True

            # scale
            scale_flag = False
            if self.SCALE_FLAG is True:
                if self._scale_left_rect.contains(pos):
                    self._set_action_flag_(self.ActionFlag.NGSbjScaleLeft)
                    self._update_graph_action_flag_(self.ActionFlag.NGNodeAnyAction)
                    scale_flag = True
                elif self._scale_right_rect.contains(pos):
                    self._set_action_flag_(self.ActionFlag.NGSbjScaleRight)
                    self._update_graph_action_flag_(self.ActionFlag.NGNodeAnyAction)
                    scale_flag = True

            if trim_flag is False and scale_flag is False:
                self._clear_all_action_flags_()
                self._graph._clear_all_action_flags_()
        else:
            self._graph._update_hover_node_(None)
            self._set_hovered_(False)
            self._clear_all_action_flags_()
            self._graph._clear_all_action_flags_()

    def _do_show_tool_tip_(self, event):
        self._tool_tip_css = self._track_model.to_string()
        # noinspection PyArgumentList
        QtWidgets.QToolTip.showText(
            QtGui.QCursor.pos(), self._tool_tip_css, self
        )

    def __init__(self, *args, **kwargs):
        super(QtTrackNode, self).__init__(*args, **kwargs)
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
        self._time_source_rect = QtCore.QRect()
        self._count_draw_rect = QtCore.QRect()
        self._trim_left_rect, self._trim_right_rect = QtCore.QRect(), QtCore.QRect()
        self._scale_left_rect, self._scale_right_rect = QtCore.QRect(), QtCore.QRect()

        self._pre_blend_rect = QtCore.QRect()
        self._post_blend_rect = QtCore.QRect()

        self._track_model = None
        self._track_last_model = None

        self._time_basic_frame_rect = QtCore.QRect()
        self._time_left_draw_flag = False
        self._time_left_frame_rect = QtCore.QRect()
        self._time_right_draw_flag = False
        self._time_right_frame_rect = QtCore.QRect()

        self._layer_index = 0

        self._start_trim = None
        self._end_trim = None

        self.installEventFilter(self)

    def __str__(self):
        return '{}(key={}, x={}, y={})'.format(
            self.__class__.__name__,
            self._track_model.key,
            self._node_global_selection_rect.x(),
            self._node_global_selection_rect.y()
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            if event.type() == QtCore.QEvent.Resize:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                self._clear_all_action_flags_()
                self._graph._clear_all_action_flags_()
                self._graph._update_hover_node_(None)
            elif event.type() == QtCore.QEvent.ToolTip:
                self._do_show_tool_tip_(event)
            # when pressing mark points
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._do_hover_move_(event)
                    if self._is_action_flag_match_(
                        self.ActionFlag.NGSbjTrimLeft, self.ActionFlag.NGSbjTrimRight
                    ):
                        self._do_press_start_for_any_action_(event)
                        return True
                    elif self._is_action_flag_match_(
                        self.ActionFlag.NGSbjScaleLeft, self.ActionFlag.NGSbjScaleRight
                    ):
                        self._do_press_start_for_any_action_(event)
                        return True
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
                        self.ActionFlag.NGSbjTrimLeft, self.ActionFlag.NGSbjTrimRight
                    ):
                        self._do_press_move_trim_(event)
                        return False
                    elif self._is_action_flag_match_(
                        self.ActionFlag.NGSbjScaleLeft, self.ActionFlag.NGSbjScaleRight
                    ):
                        self._do_press_scale_(event)
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
            # when releasing, execute action
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    # trim
                    if self._is_action_flag_match_(
                        self.ActionFlag.NGSbjTrimLeft, self.ActionFlag.NGSbjTrimRight
                    ):
                        self._do_press_trim_end_(event)
                        return False
                    # scale
                    elif self._is_action_flag_match_(
                        self.ActionFlag.NGSbjScaleLeft, self.ActionFlag.NGSbjScaleRight
                    ):
                        self._do_press_scale_end_(event)
                        return False
                    # move
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
            _qt_core.QtFont.generate(size=8)
        )

        start_text = painter.fontMetrics().elidedText(
            str(self._track_model.clip_start),
            QtCore.Qt.ElideMiddle,
            self._time_clip_start_rect.width(),
            QtCore.Qt.TextShowMnemonic
        )
        painter.drawText(
            self._time_clip_start_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
            start_text
        )
        end_text = painter.fontMetrics().elidedText(
            str(self._track_model.clip_end),
            QtCore.Qt.ElideMiddle,
            self._time_clip_end_rect.width(),
            QtCore.Qt.TextShowMnemonic
        )
        painter.drawText(
            self._time_clip_end_rect, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter,
            end_text
        )

        if self._track_model.speed == 1:
            count_text_0 = str(self._track_model.clip_count)
        else:
            count_text_0 = '{}x{}'.format(
                self._track_model.clip_count,
                round(self._track_model.speed, 2)
            )

        count_text = painter.fontMetrics().elidedText(
            count_text_0,
            QtCore.Qt.ElideMiddle,
            self._count_draw_rect.width(),
            QtCore.Qt.TextShowMnemonic
        )
        painter.drawText(
            self._count_draw_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            count_text
        )

        self._draw_frame_(painter)

    def _draw_frame_(self, painter):
        x, y, w, h = (
            self._frame_draw_rect.x(),
            self._frame_draw_rect.y(),
            self._frame_draw_rect.width(),
            self._frame_draw_rect.height()
        )
        if self._is_selected:
            border_rgba = _gui_core.GuiRgba.LightAzureBlue
            border_width = 2
            rect = QtCore.QRect(x+border_width/2, y+border_width/2, w-border_width/2, h-border_width/2)
        else:
            rect = self._frame_draw_rect
            border_rgba = _gui_core.GuiRgba.LightGray
            border_width = 1

        painter._set_border_color_(
            border_rgba
        )
        painter._set_background_color_(
            _gui_core.GuiRgba.Transparent
        )
        painter._set_border_width_(border_width)
        painter.drawRect(
            rect
        )

    def _draw_basic_(self, painter):
        if self._track_model.is_bypass > 0:
            rgb_0 = (127, 127, 127)
        else:
            rgb_0 = self._track_model.rgb

        # basic
        painter.setPen(QtGui.QColor(*rgb_0))
        painter.setBrush(QtGui.QColor(*rgb_0))
        painter.drawRect(self._time_basic_frame_rect)
        pre_cycle = self._track_model.pre_cycle
        post_cycle = self._track_model.post_cycle
        
        # cycle
        p_mid = self._time_source_rect.topLeft()
        x_mid, y_mid = p_mid.x(), p_mid.y()
        cycle_w, cycle_h = self._time_source_rect.width(), self._time_source_rect.height()

        for i in range(post_cycle):
            i_x, i_y = x_mid+i*cycle_w, y_mid
            if i % 2:
                i_rect = QtCore.QRect(
                    i_x+1, i_y+1, cycle_w, cycle_h
                )

                painter.setPen(QtGui.QColor(0, 0, 0, 0))
                i_brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 63))
                # i_brush.setStyle(QtCore.Qt.Dense4Pattern)
                painter.setBrush(i_brush)
                painter.drawRect(i_rect)

        for i in range(pre_cycle+1):
            i_x, i_y = x_mid-i*cycle_w, y_mid
            if i % 2:
                i_rect = QtCore.QRect(
                    i_x+1, i_y+1, cycle_w, cycle_h
                )
                painter.setPen(QtGui.QColor(0, 0, 0, 0))
                i_brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 63))
                # i_brush.setStyle(QtCore.Qt.Dense4Pattern)
                painter.setBrush(i_brush)
                painter.drawRect(i_rect)

        # no frames
        if self._time_left_draw_flag is True:
            painter._draw_alternating_colors_by_rect_(
                self._time_left_frame_rect,
                [_gui_core.GuiRgba.LightBlack, _gui_core.GuiRgba.Transparent],
                x_offset=-self.x(), y_offset=-self.y()
            )
        if self._time_right_draw_flag is True:
            painter._draw_alternating_colors_by_rect_(
                self._time_right_frame_rect,
                [_gui_core.GuiRgba.LightBlack, _gui_core.GuiRgba.Transparent],
                x_offset=-self._time_right_frame_rect.x()-self.x(), y_offset=-self.y()
            )

        # name
        painter._set_text_color_(_gui_core.GuiRgba.LightBlack)
        painter._set_font_(_qt_core.QtFont.generate(size=8))

        name_text_1 = painter.fontMetrics().elidedText(
            self._track_model.key,
            QtCore.Qt.ElideMiddle,
            self._name_draw_rect.width(),
            QtCore.Qt.TextShowMnemonic
        )
        painter.drawText(
            self._name_draw_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            name_text_1
        )

    def _setup_track_(self, **kwargs):
        self._track_model = self._graph._track_stage_model.create_one(self, **kwargs)

        if self._track_model.is_trash is True:
            self.hide()
        else:
            self.show()

        self._node_update_transformation_fnc_(self._track_model)

        self._build_timetrack_trim_()

    def _push_last_properties_(self):
        self._push_track_model_()

    def _push_track_model_(self):
        self._track_last_model = self._track_model.copy()

    def _node_update_transformation_fnc_(self, track_model):
        self._track_model = track_model

        x, y, w, h = self._track_model.compute_timetrack_args()
        self._node_basic_x, self._node_basic_y = x, y
        self._node_basic_w, self._node_basic_h = w, h
        self._refresh_widget_all_()

    def _build_timetrack_trim_(self):
        self._start_trim = QtTrackTrim(
            self._graph._timetrack_trim_sbj_layer
        )
        self._start_trim._set_trim_flag_(self._start_trim.TrimFlag.Start)
        self._start_trim.hide()
        self._start_trim._set_graph_(self._graph)
        self._start_trim._set_node_(self)

        self._end_trim = QtTrackTrim(
            self._graph._timetrack_trim_sbj_layer
        )
        self._end_trim._set_trim_flag_(self._end_trim.TrimFlag.End)
        self._end_trim.hide()
        self._end_trim._set_graph_(self._graph)
        self._end_trim._set_node_(self)

    def _update_node_attachments_(self):
        self._update_connections_()

        # time offset
        if self._start_trim is not None:
            start_trim = self._track_model.start_trim

            if start_trim == 0:
                self._start_trim.hide()
            elif start_trim > 0:
                trm_w = self._track_model.compute_w_by_count(start_trim)
                trm_x, trm_y = self.x()-trm_w, self.y()
                trm_h = self.height()
                self._start_trim.setGeometry(
                    trm_x, trm_y, trm_w, trm_h
                )
                self._start_trim.show()

        if self._end_trim is not None:
            end_trim = self._track_model.basic_end_trim
            if end_trim == 0:
                self._end_trim.hide()
            elif end_trim > 0:
                trm_w = self._track_model.compute_w_by_count(end_trim)
                trm_x, trm_y = self.x()+self.width(), self.y()
                trm_h = self.height()
                self._end_trim.setGeometry(
                    trm_x, trm_y, trm_w, trm_h
                )
                self._end_trim.show()
