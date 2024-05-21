# coding:utf-8
from lxgui.qt.core.wrap import *

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.abstracts as gui_qt_abstracts

import lxbasic.resource as bsc_resource

import lxbasic.storage as bsc_storage


class Keys(object):
    ankle_L = "ankle_L"
    ankle_R = "ankle_R"
    chest_M = "chest_M"
    elbow_L = "elbow_L"
    elbow_R = "elbow_R"
    finger_L = "finger_L"
    finger_R = "finger_R"
    head_M = "head_M"
    hip_L = "hip_L"
    hip_R = "hip_R"
    knee_L = "knee_L"
    knee_R = "knee_R"
    neck_M = "neck_M"
    pole_leg_L = "pole_leg_L"
    pole_leg_R = "pole_leg_R"
    root_M = "root_M"
    scapula_L = "scapula_L"
    scapula_R = "scapula_R"
    shoulder_L = "shoulder_L"
    shoulder_R = "shoulder_R"
    spine_M = "spine_M"
    thumb_L = "thumb_L"
    thumb_R = "thumb_R"
    toes_L = "toes_L"
    toes_R = "toes_R"
    wrist_L = "wrist_L"
    wrist_R = "wrist_R"

    All = [
        ankle_L,
        ankle_R,
        chest_M,
        elbow_L,
        elbow_R,
        finger_L,
        finger_R,
        head_M,
        hip_L,
        hip_R,
        knee_L,
        knee_R,
        neck_M,
        pole_leg_L,
        pole_leg_R,
        root_M,
        scapula_L,
        scapula_R,
        shoulder_L,
        shoulder_R,
        spine_M,
        thumb_L,
        thumb_R,
        toes_L,
        toes_R,
        wrist_L,
        wrist_R
    ]
    Main = [
        ankle_L,
        ankle_R,
        chest_M,
        elbow_L,
        elbow_R,
        finger_L,
        finger_R,
        head_M,
        hip_L,
        hip_R,
        knee_L,
        knee_R,
        neck_M,
        root_M,
        scapula_L,
        scapula_R,
        shoulder_L,
        shoulder_R,
        spine_M,
        thumb_L,
        thumb_R,
        toes_L,
        toes_R,
        wrist_L,
        wrist_R
    ]


class QtChartForBodyPicker(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtActionBaseDef,
):

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()

        w_0, h_0 = 48.0, 100.0

        p = h / h_0
        x_offset = w/2

        self._draw_path_dict = {}
        for k, v in self._body_data.items():
            i_path = gui_qt_core.QtPainterPath()
            self._draw_path_dict[k] = i_path
            i_points = []
            for j in v:
                j_point = j[0]*p+x_offset, j[1]*p
                i_points.append(j_point)

            i_points.append(i_points[0])
            i_path._add_points_(i_points)

    def _do_hover_move_(self, event):
        p = event.pos()

        self._key_hover = None
        for i_key, i_path in self._draw_path_dict.items():
            if i_path.contains(p):
                self._key_hover = i_key
                break

        self._refresh_widget_draw_()

    def _do_press_click_(self, event):
        # add
        if self._is_action_mdf_flags_include_(
            self.ActionFlag.KeyShiftPress
        ):
            if self._key_hover is not None:
                self._key_current = self._key_hover
                self._keys_selected.add(self._key_hover)
        elif self._is_action_mdf_flags_include_(
            self.ActionFlag.KeyControlPress
        ):
            if self._key_hover is not None:
                self._keys_selected.discard(self._key_hover)
        else:
            if self._key_hover is not None:
                self._key_current = self._key_hover
                self._keys_selected = {self._key_hover}
            else:
                self._key_current = None
                self._keys_selected = set()

        self._refresh_widget_draw_()

    def _do_press_dbl_click_(self, event):
        # add
        if self._is_action_mdf_flags_include_(
            self.ActionFlag.KeyShiftPress
        ):
            if self._key_hover is not None:
                keys = self._get_extend_keys_(self._key_hover)
                self._keys_selected.update(keys)
        # sub
        elif self._is_action_mdf_flags_include_(
            self.ActionFlag.KeyControlPress
        ):
            if self._key_hover is not None:
                keys = self._get_extend_keys_(self._key_hover)
                [self._keys_selected.discard(x) for x in keys]
        else:
            if self._key_hover is not None:
                keys = self._get_extend_keys_(self._key_hover)
                self._keys_selected.update(keys)

        self._refresh_widget_draw_()

    def _do_show_tool_tip_(self, event):
        if self._key_hover is not None:
            css = gui_qt_core.GuiQtUtil.generate_tool_tip_css(
                self._key_hover,
                action_tip=[
                    '"LMB-click" to select current',
                    '"LMB-dbl-click" to select all below',
                ]
            )

            # noinspection PyArgumentList
            QtWidgets.QToolTip.showText(
                QtGui.QCursor.pos(), css, self
            )

    def _get_extend_keys_(self, key):
        key_paths = self._selection_cfg.get_keys('*.{}.*'.format(key))
        return set([x.split('.')[-1] for x in key_paths])

    def __init__(self, *args, **kwargs):
        super(QtChartForBodyPicker, self).__init__(*args, **kwargs)
        
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        self._init_action_base_def_(self)

        self._configure = bsc_resource.RscExtendConfigure.get_as_content('gui/body-picker')
        self._selection_cfg = self._configure.get_as_content('selection_tree')

        self._body_json_file = bsc_resource.ExtendResource.get('gui/body.json')
        if self._body_json_file is None:
            raise RuntimeError()

        self._key_hover = None

        self._key_current = None
        self._keys_selected = set()

        self._keys_selected_extend = set()

        self._select_mode = 0

        self._selection_flag = None

        self._body_data = bsc_storage.StgFileOpt(self._body_json_file).set_read()

        self._draw_path_dict = {}

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                self._key_hover = None
            elif event.type() == QtCore.QEvent.ToolTip:
                self._do_show_tool_tip_(event)

            elif event.type() == QtCore.QEvent.KeyPress:
                if event.modifiers() == QtCore.Qt.ControlModifier:
                    self._set_action_mdf_flag_add_(
                        self.ActionFlag.KeyControlPress
                    )
                elif event.modifiers() == QtCore.Qt.ShiftModifier:
                    self._set_action_mdf_flag_add_(
                        self.ActionFlag.KeyShiftPress
                    )
            elif event.type() == QtCore.QEvent.KeyRelease:
                self._clear_action_modifier_flags_()

            elif event.type() == QtCore.QEvent.MouseButtonPress:

                if event.button() == QtCore.Qt.LeftButton:
                    self._do_press_click_(event)
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    self._do_press_dbl_click_(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                pass
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    pass
                else:
                    self._do_hover_move_(event)

        return False

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)

        painter.setRenderHint(painter.Antialiasing)

        # painter.fillRect(rect, QtGui.QColor(255, 0, 0, 255))

        for i_key, i_path in self._draw_path_dict.items():
            if i_key in Keys.Main:

                if i_key in self._keys_selected:
                    if i_key == self._key_current:
                        i_r, i_g, i_b, _ = gui_core.GuiRgba.LightBlue
                        painter._set_border_color_(i_r, i_g, i_b, 255)
                        painter._set_background_color_(i_r, i_g, i_b, 255)
                        painter._set_background_style_(QtCore.Qt.FDiagPattern)
                        painter._set_border_width_(4)
                    else:
                        i_r, i_g, i_b, _ = gui_core.GuiRgba.LightBlue
                        painter._set_border_color_(i_r, i_g, i_b, 159)
                        painter._set_background_color_(i_r, i_g, i_b, 127)
                        painter._set_background_style_(QtCore.Qt.BDiagPattern)
                        painter._set_border_width_(2)
                elif i_key == self._key_hover:
                    i_r, i_g, i_b, _ = gui_core.GuiRgba.LightOrange
                    painter._set_border_color_(i_r, i_g, i_b, 159)
                    painter._set_background_color_(i_r, i_g, i_b, 127)
                    # painter._set_background_style_(QtCore.Qt.FDiagPattern)
                    painter._set_border_width_(1)
                else:
                    i_r, i_g, i_b, _ = gui_core.GuiRgba.BabyBlue
                    painter._set_border_color_(i_r, i_g, i_b, 127)
                    painter._set_background_color_(i_r, i_g, i_b, 95)
                    painter._set_border_width_(1)

                painter.drawPath(i_path)

