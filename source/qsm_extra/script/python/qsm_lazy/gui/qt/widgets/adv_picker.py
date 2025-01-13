# coding:utf-8
import copy

from lxgui.qt.core.wrap import *

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.abstracts as gui_qt_abstracts

import lxbasic.resource as bsc_resource

import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core


class _Keys(object):
    main = 'main'
    #
    root_fk_M = 'root_fk_M'
    root_x_M = 'root_x_M'
    hip_swinger_M = 'hip_swinger_M'
    #
    spine_fk_ik_swap_M = 'spine_fk_ik_swap_M'
    spine_fk_M = 'spine_fk_M'
    spine_ik_M = 'spine_ik_M'
    spine_ik_hybrid_M = 'spine_ik_hybrid_M'
    spine_ik_cv_M = 'spine_ik_cv_M'

    chest_fk_M = 'chest_fk_M'
    neck_fk_M = 'neck_fk_M'
    head_fk_M = 'head_fk_M'
    # arm left
    scapula_fk_L = 'scapula_fk_L'
    shoulder_fk_L = 'shoulder_fk_L'
    elbow_fk_L = 'elbow_fk_L'
    wrist_fk_L = 'wrist_fk_L'
    cup_fk_L = 'cup_fk_L'
    thumb_fk_L = 'thumb_fk_L'
    finger_fk_L = 'finger_fk_L'
    # arm right
    scapula_fk_R = 'scapula_fk_R'
    shoulder_fk_R = 'shoulder_fk_R'
    elbow_fk_R = 'elbow_fk_R'
    wrist_fk_R = 'wrist_fk_R'
    cup_fk_R = 'cup_fk_R'
    thumb_fk_R = 'thumb_fk_R'
    finger_fk_R = 'finger_fk_R'
    # leg left
    hip_fk_L = 'hip_fk_L'
    knee_fk_L = 'knee_fk_L'
    ankle_fk_L = 'ankle_fk_L'
    toes_fk_L = 'toes_fk_L'
    # leg right
    hip_fk_R = 'hip_fk_R'
    knee_fk_R = 'knee_fk_R'
    ankle_fk_R = 'ankle_fk_R'
    toes_fk_R = 'toes_fk_R'
    # arm extra
    arm_ik_pole_L = 'arm_ik_pole_L'
    arm_ik_pole_R = 'arm_ik_pole_R'

    arm_ik_L = 'arm_ik_L'
    finger_L = 'finger_L'
    arm_ik_R = 'arm_ik_R'
    finger_R = 'finger_R'

    arm_fk_ik_swap_L = 'arm_fk_ik_swap_L'
    arm_fk_ik_swap_R = 'arm_fk_ik_swap_R'
    # leg extra
    leg_fk_ik_swap_L = 'leg_fk_ik_swap_L'
    leg_fk_ik_swap_R = 'leg_fk_ik_swap_R'

    leg_ik_pole_L = 'leg_ik_pole_L'
    leg_ik_pole_R = 'leg_ik_pole_R'

    leg_ik_L = 'leg_ik_L'
    leg_ik_R = 'leg_ik_R'

    leg_ik_toe_L = 'leg_ik_toe_L'
    leg_ik_toe_R = 'leg_ik_toe_R'

    leg_ik_toe_roll_L = 'leg_ik_toe_roll_L'
    leg_ik_toe_roll_R = 'leg_ik_toe_roll_R'

    leg_ik_toe_roll_end_L = 'leg_ik_toe_roll_end_L'
    leg_ik_toe_roll_end_R = 'leg_ik_toe_roll_end_R'

    leg_ik_heel_L = 'leg_ik_heel_L'
    leg_ik_heel_R = 'leg_ik_heel_R'

    secondary_cloth = 'secondary_cloth'

    All = [
        main,

        root_fk_M,
        root_x_M,
        hip_swinger_M,

        spine_fk_ik_swap_M,
        spine_fk_M,
        spine_ik_M, spine_ik_hybrid_M, spine_ik_cv_M,
        chest_fk_M,
        neck_fk_M,
        head_fk_M,
        ankle_fk_L,
        ankle_fk_R,
        elbow_fk_L,
        elbow_fk_R,
        finger_fk_L,
        finger_fk_R,
        hip_fk_L,
        hip_fk_R,
        knee_fk_L,
        knee_fk_R,

        scapula_fk_L,
        scapula_fk_R,
        shoulder_fk_L,
        shoulder_fk_R,
        thumb_fk_L,
        thumb_fk_R,
        toes_fk_L,
        toes_fk_R,
        wrist_fk_L,
        wrist_fk_R,
        cup_fk_L,
        cup_fk_R,

        arm_ik_pole_L,
        arm_ik_pole_R,
        arm_ik_L,
        finger_L,
        arm_ik_R,
        finger_R,
        arm_fk_ik_swap_L,
        arm_fk_ik_swap_R,

        leg_fk_ik_swap_L, leg_fk_ik_swap_R,
        leg_ik_pole_L, leg_ik_pole_R,
        leg_ik_L, leg_ik_R,

        leg_ik_toe_L, leg_ik_toe_R,
        leg_ik_toe_roll_L, leg_ik_toe_roll_R,
        leg_ik_toe_roll_end_L, leg_ik_toe_roll_end_R,
        leg_ik_heel_L, leg_ik_heel_R,

        secondary_cloth,
    ]


class QtAdvCharacterPicker(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtActionBaseDef,
):
    user_select_control_key_accepted = qt_signal(list)
    user_select_control_key_changed = qt_signal()

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()

        nsp_h = self._main_h

        mrg = 2

        h_c = h-nsp_h-mrg*2

        w_0, h_0 = 54.0, 100.0

        w_min = abs(h_c*(w_0/h_0)+mrg*2)

        if self._namespace is not None:
            txt_w = QtGui.QFontMetrics(self._main_font).width(self._main_text)+8
            self._main_frame_rect.setRect(
                x+(w_min-txt_w)/2, h-nsp_h-mrg, txt_w, nsp_h
            )

        self._scale = h_c/h_0
        x_offset = w_min/2

        self._draw_path_dict = {}

        main_path = gui_qt_core.QtPainterPath()
        main_path._add_coords_(
            [
                (self._main_frame_rect.topLeft().x(), self._main_frame_rect.topLeft().y()),
                (self._main_frame_rect.topRight().x(), self._main_frame_rect.topRight().y()),
                (self._main_frame_rect.bottomRight().x(), self._main_frame_rect.bottomRight().y()),
                (self._main_frame_rect.bottomLeft().x(), self._main_frame_rect.bottomLeft().y()),
                (self._main_frame_rect.topLeft().x(), self._main_frame_rect.topLeft().y())
            ]
        )
        self._draw_path_dict['main'] = main_path

        for k, v in self._body_data.items():
            i_path = gui_qt_core.QtPainterPath()
            self._draw_path_dict[k] = i_path
            i_points = []
            for j in v:
                j_point = w_min-(j[0]*self._scale+x_offset), j[1]*self._scale
                i_points.append(j_point)

            i_points.append(i_points[0])
            i_path._add_coords_(i_points)

        self.setMinimumWidth(w_min)

    def _do_hover_move_(self, event):
        p = event.pos()

        self._sketch_key_hover = None
        for i_key, i_path in self._draw_path_dict.items():
            if i_path.contains(p):
                self._sketch_key_hover = i_key
                break

        self._refresh_widget_draw_()

    def _do_press_click_(self, event):
        if self._action_is_enable is False:
            return

        self._sketch_key_set_tmp = copy.copy(self._sketch_key_set_selected)
        # add
        if self._is_action_mdf_flags_include_(
            self.ActionFlag.KeyShiftPress
        ):
            if self._sketch_key_hover is not None:
                self._sketch_key_current = self._sketch_key_hover
                self._sketch_key_set_selected.add(self._sketch_key_hover)
        # sub
        elif self._is_action_mdf_flags_include_(
            self.ActionFlag.KeyControlPress
        ):
            if self._sketch_key_hover is not None:
                self._sketch_key_set_selected.discard(self._sketch_key_hover)
        # override
        else:
            if self._sketch_key_hover is not None:
                self._sketch_key_current = self._sketch_key_hover
                self._sketch_key_set_selected = {self._sketch_key_hover}
            else:
                self._sketch_key_current = None
                self._sketch_key_set_selected = set()

        self._refresh_widget_draw_()

    def _do_press_dbl_click_(self, event):
        if self._action_is_enable is False:
            return

        # add
        if self._is_action_mdf_flags_include_(
            self.ActionFlag.KeyShiftPress
        ):
            if self._sketch_key_hover is not None:

                keys = self._adv_control_cfg.find_next_keys_at(self._sketch_key_hover)
                self._sketch_key_set_selected.update(keys)
        # sub
        elif self._is_action_mdf_flags_include_(
            self.ActionFlag.KeyControlPress
        ):
            if self._sketch_key_hover is not None:
                keys = self._adv_control_cfg.find_next_keys_at(self._sketch_key_hover)
                [self._sketch_key_set_selected.discard(x) for x in keys]
        # override
        else:
            if self._sketch_key_hover is not None:
                keys = self._adv_control_cfg.find_next_keys_at(self._sketch_key_hover)
                self._sketch_key_set_selected.update(keys)

        self._refresh_widget_draw_()

    def _do_press_release_(self, event):
        if self._action_is_enable is False:
            return

        if self._sketch_key_set_tmp != self._sketch_key_set_selected:
            self.user_select_control_key_changed.emit()

        control_keys = []
        for i_key in self._sketch_key_set_selected:
            if i_key == _Keys.secondary_cloth:
                control_keys.append('secondary_cloth')

            i_control_keys = self._get_control_keys_(i_key, self._control_includes)
            if i_control_keys:
                control_keys.extend(i_control_keys)

        self.user_select_control_key_accepted.emit(control_keys)

    def _do_show_tool_tip_(self, event):
        if self._sketch_key_hover is not None:
            css = gui_qt_core.QtUtil.generate_tool_tip_css(
                self._sketch_key_hover,
                action_tip=[
                    '"鼠标左键点击" 选择当前',
                    '"鼠标左键双击" 选择所有的子集',
                    '按“SHIFT”加选，按“CTRL”减选',
                ] if gui_core.GuiUtil.get_language() == 'chs'
                else [
                    '"LMB-click" to select current',
                    '"LMB-dbl-click" to select all below',
                    'Press "SHIFT" add, press "CTRL" sub'
                ]
            )

            # noinspection PyArgumentList
            QtWidgets.QToolTip.showText(
                QtGui.QCursor.pos(), css, self
            )

    def _get_control_keys_(self, key, control_includes):
        list_ = []
        for i in control_includes:
            i_keys = self._adv_control_cfg.get_control_keys_at(key, i)
            if i_keys:
                list_.extend(i_keys)
        return list_

    def _get_extra_control_keys_(self, key):
        return self._adv_control_cfg.get_control_keys_at(key, 'extra')

    def __init__(self, *args, **kwargs):
        super(QtAdvCharacterPicker, self).__init__(*args, **kwargs)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.setMinimumSize(48, 48)

        self._init_action_base_def_(self)

        self._adv_control_cfg = qsm_gnl_core.AdvCharacterControlConfigure()

        self._body_json_file = bsc_resource.ExtendResource.get('gui/adv-picker/v1.json')
        if self._body_json_file is None:
            raise RuntimeError()

        self._margin = 2

        self._scale = 1.0

        self._namespace = None
        self._main_text = None
        self._main_frame_rect = QtCore.QRect()
        self._main_h = 20
        self._main_font = gui_qt_core.QtFont.generate(size=10)
        self._main_text_color = gui_core.GuiRgba.LightBlack
        self._main_frame_border_color = gui_core.GuiRgba.LightBlack
        self._main_frame_background_color = gui_core.GuiRgba.DarkWhite
        self.setFont(self._main_font)

        self._sketch_key_hover = None

        self._sketch_key_current = None
        self._sketch_key_set_tmp = set()
        self._sketch_key_set_selected = set()

        self._left_frame_rect = QtCore.QRect()
        self._right_frame_rect = QtCore.QRect()

        self._select_mode = 0

        self._selection_flag = None

        self._body_data = bsc_storage.StgFileOpt(self._body_json_file).set_read()

        self._draw_path_dict = {}

        self._control_includes = ['default']

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                self._sketch_key_hover = None
            elif event.type() == QtCore.QEvent.ToolTip:
                self._do_show_tool_tip_(event)

            elif event.type() == QtCore.QEvent.KeyPress:
                if event.modifiers() == QtCore.Qt.ControlModifier:
                    self._add_action_modifier_flag_(
                        self.ActionFlag.KeyControlPress
                    )
                elif event.modifiers() == QtCore.Qt.ShiftModifier:
                    self._add_action_modifier_flag_(
                        self.ActionFlag.KeyShiftPress
                    )
            elif event.type() == QtCore.QEvent.KeyRelease:
                self._clear_action_modifier_flags_()

            elif event.type() == QtCore.QEvent.MouseButtonPress:

                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.PressClick)
                    self._do_press_click_(event)
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.PressDblClick)
                    self._do_press_dbl_click_(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self._do_press_release_(event)

                self._clear_all_action_flags_()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    pass
                else:
                    self._do_hover_move_(event)

        return False

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)
        painter.setRenderHint(painter.Antialiasing)

        if self.hasFocus():
            alpha = 159
        else:
            alpha = 127

        # painter.fillRect(rect, QtGui.QColor(255, 0, 0, 255))

        for i_key, i_path in self._draw_path_dict.items():
            if i_key in _Keys.All:
                # select
                # hover
                if i_key == self._sketch_key_hover:
                    i_r, i_g, i_b, _ = gui_core.GuiRgba.LightOrange
                    painter._set_border_color_(i_r, i_g, i_b, 255)
                    painter._set_background_color_(i_r, i_g, i_b, alpha)
                    # painter._set_background_style_(QtCore.Qt.FDiagPattern)
                    if i_key in self._sketch_key_set_selected:
                        if i_key == self._sketch_key_current:
                            painter._set_border_width_(4)
                        else:
                            painter._set_border_width_(2)
                    else:
                        painter._set_border_width_(1)
                elif i_key in self._sketch_key_set_selected:
                    if i_key == self._sketch_key_current:
                        i_r, i_g, i_b, _ = gui_core.GuiRgba.LightAzureBlue
                        painter._set_border_color_(i_r, i_g, i_b, 255)
                        painter._set_background_color_(i_r, i_g, i_b, alpha)
                        # painter._set_background_style_(QtCore.Qt.FDiagPattern)
                        painter._set_border_width_(4)
                    else:
                        i_r, i_g, i_b, _ = gui_core.GuiRgba.AzureBlue
                        painter._set_border_color_(i_r, i_g, i_b, 255)
                        painter._set_background_color_(i_r, i_g, i_b, alpha)
                        # painter._set_background_style_(QtCore.Qt.BDiagPattern)
                        painter._set_border_width_(2)
                # default
                else:
                    if '_fk_ik_swap_' in i_key:
                        i_r, i_g, i_b, _ = gui_core.GuiRgba.Pink
                    elif '_ik_' in i_key:
                        i_r, i_g, i_b, _ = gui_core.GuiRgba.LemonYellow
                    elif i_key.startswith('secondary_'):
                        i_r, i_g, i_b, _ = gui_core.GuiRgba.NeonGreen
                    else:
                        i_r, i_g, i_b, _ = gui_core.GuiRgba.Purple

                    painter._set_border_color_(i_r, i_g, i_b, 255)
                    painter._set_background_color_(i_r, i_g, i_b, alpha)
                    painter._set_border_width_(1)

                painter.drawPath(i_path)

        if self._namespace is not None:
            painter._set_text_color_(
                self._main_text_color
            )
            painter.drawText(
                self._main_frame_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                self._main_text
            )

    def _clear_all_selection_(self):
        self._sketch_key_current = None
        self._sketch_key_set_tmp = set()
        self._sketch_key_set_selected = set()

        self._refresh_widget_draw_()

    def _has_focus_(self):
        return self.hasFocus()

    def _set_namespace_(self, text):
        if text != self._namespace:
            self._namespace = text
            self._main_text = '{}:Main'.format(self._namespace)

            self._clear_all_selection_()

            self._refresh_widget_all_()

    def _get_namespace_(self):
        return self._namespace

    def _set_control_includes_(self, keys):
        self._control_includes = keys
