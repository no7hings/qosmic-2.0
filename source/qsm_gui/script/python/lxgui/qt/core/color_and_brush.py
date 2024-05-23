# coding:utf-8
# gui
from ... import core as gui_core
# qt
from .wrap import *

from . import style as _style


class QtColors(object):
    Background = QtGui.QColor(63, 63, 63, 255)
    BackgroundHover = QtGui.QColor(*gui_core.GuiRgba.LightOrange)

    ToolTipText = QtGui.QColor(15, 15, 15, 255)
    ToolTipBorder = QtGui.QColor(15, 15, 15, 255)
    ToolTipBackground = QtGui.QColor(223, 223, 191, 255)

    BubbleBackground = QtGui.QColor(223, 223, 223, 255)
    BubbleBackgroundDisable = QtGui.QColor(127, 127, 127, 255)
    BubbleNextWaiting = QtGui.QColor(*gui_core.GuiRgba.LightYellow)
    BubbleNextFinished = QtGui.QColor(*gui_core.GuiRgba.LightGreen)
    BubbleBackgroundHover = QtGui.QColor(*gui_core.GuiRgba.LightOrange)
    BubbleBackgroundActioned = QtGui.QColor(*gui_core.GuiRgba.LightBlue)
    BubbleBorder = QtGui.QColor(127, 127, 127, 255)
    BubbleText = QtGui.QColor(31, 31, 31, 255)

    CapsuleBorderChecked = QtGui.QColor(127, 127, 127, 255)
    CapsuleBorderUnchecked = QtGui.QColor(55, 55, 55, 255)
    CapsuleBorderHover = QtGui.QColor(*gui_core.GuiRgba.LightOrange)
    CapsuleBorderActioned = QtGui.QColor(*gui_core.GuiRgba.LightBlue)
    CapsuleBackground = QtGui.QColor(47, 47, 47, 255)
    CapsuleBackgroundDisable = QtGui.QColor(55, 55, 55, 255)

    SubIconBorder = QtGui.QColor(207, 207, 207, 255)
    SubIconBackground = QtGui.QColor(127, 127, 127, 255)

    PopupBorder = QtGui.QColor(*gui_core.GuiRgba.LightBlue)

    TabBorder = QtGui.QColor(63, 63, 63, 255)
    TabBackground = QtGui.QColor(47, 47, 47, 255)
    TabBorderCurrent = QtGui.QColor(87, 87, 87, 255)
    TabBackgroundCurrent = QtGui.QColor(63, 63, 63, 255)

    TabGroupBorder = QtGui.QColor(87, 87, 87, 255)
    TabGroupBackground = QtGui.QColor(55, 55, 55, 255)
    TabGroupBackgroundCurrent = QtGui.QColor(63, 63, 63, 255)

    HeadBorder = QtGui.QColor(87, 87, 87, 255)
    HeadBackground = QtGui.QColor(83, 83, 83, 255)

    HeadText = QtGui.QColor(207, 207, 207, 255)
    HeadTextHover = QtGui.QColor(223, 223, 223, 255)

    ButtonBorder = QtGui.QColor(131, 131, 131, 255)
    ButtonBackground = QtGui.QColor(127, 127, 127, 255)

    Text = QtGui.QColor(223, 223, 223, 255)
    TextHover = QtGui.QColor(255, 255, 255, 255)
    TextEnable = QtGui.QColor(*gui_core.GuiRgba.Green)
    TextDisable = QtGui.QColor(*gui_core.GuiRgba.DarkGray)
    TextTemporary = QtGui.QColor(*gui_core.GuiRgba.Gray)
    TextWarning = QtGui.QColor(*gui_core.GuiRgba.Yellow)
    TextError = QtGui.QColor(*gui_core.GuiRgba.Red)
    TextLock = QtGui.QColor(*gui_core.GuiRgba.Purple)
    TextCorrect = QtGui.QColor(*gui_core.GuiRgba.Green)
    TextActive = QtGui.QColor(*gui_core.GuiRgba.Blue)

    TextKeywordFilter = QtGui.QColor(255, 127, 63, 255)
    TextKeywordFilterOccurrence = QtGui.QColor(255, 63, 63, 255)

    Progress = QtGui.QColor(63, 255, 127, 255)
    ProgressBackground = QtGui.QColor(47, 47, 47, 255)

    Red = QtGui.QColor(*gui_core.GuiRgba.Red)
    Yellow = QtGui.QColor(*gui_core.GuiRgba.Yellow)
    Transparent = QtGui.QColor(*gui_core.GuiRgba.Transparent)


class QtBorderColors(object):
    @staticmethod
    def get(key):
        return QtGui.QColor(
            *_style.GuiQtStyle.get_border(key)
        )

    Transparent = QtGui.QColor(
        *_style.GuiQtStyle.get_border('color-transparent')
    )

    Dim = QtGui.QColor(
        *_style.GuiQtStyle.get_border('color-dim')
    )
    Dark = QtGui.QColor(
        *_style.GuiQtStyle.get_border('color-dark')
    )
    Basic = QtGui.QColor(
        *_style.GuiQtStyle.get_border('color-basic')
    )
    Light = QtGui.QColor(
        *_style.GuiQtStyle.get_border('color-light')
    )
    HighLight = QtGui.QColor(
        *_style.GuiQtStyle.get_border('color-high-light')
    )
    Selected = QtGui.QColor(
        *_style.GuiQtStyle.get_border('color-selected')
    )
    Actioned = QtGui.QColor(
        *_style.GuiQtStyle.get_border('color-actioned')
    )
    Hovered = QtGui.QColor(
        *_style.GuiQtStyle.get_border('color-hovered')
    )

    Icon = QtGui.QColor(
        *_style.GuiQtStyle.get_border('color-icon')
    )

    Button = QtGui.QColor(
        *_style.GuiQtStyle.get_border('color-button')
    )
    ButtonDisable = QtGui.QColor(
        *_style.GuiQtStyle.get_border('color-button-disable')
    )

    Popup = QtGui.QColor(*gui_core.GuiRgba.LightOrange)
    SplitMoving = QtGui.QColor(127, 127, 127, 255)


class QtBackgroundColors(object):
    @staticmethod
    def get(key):
        return QtGui.QColor(
            *_style.GuiQtStyle.get_background(key)
        )

    Shadow = QtGui.QColor(0, 0, 0, 31)

    Transparent = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-transparent')
    )
    Black = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-black')
    )
    Dim = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-dim')
    )
    Dark = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-dark')
    )
    Basic = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-basic')
    )
    Light = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-light')
    )
    White = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-white')
    )

    Hovered = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-hovered')
    )
    Selected = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-selected')
    )
    #
    Checked = QtGui.QColor(127, 63, 127, 255)
    CheckHovered = QtGui.QColor(191, 127, 191, 255)
    #
    DeleteHovered = QtGui.QColor(255, 63, 127, 255)
    #
    Pressed = QtGui.QColor(95, 255, 159, 255)
    PressedHovered = QtGui.QColor(255, 179, 47, 255)
    #
    Actioned = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-actioned')
    )
    #
    Icon = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-icon')
    )
    #
    Button = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-button')
    )
    ButtonHovered = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-button-hovered')
    )
    ButtonDisable = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-button-disable')
    )
    ToolTip = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-tool-tip')
    )
    #
    ItemSelected = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-item-selected')
    )
    ItemSelectedIndirect = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-item-selected-indirect')
    )
    ItemHovered = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-item-hovered')
    )
    #
    ItemLoading = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-item-loading')
    )
    Error = QtGui.QColor(
        *_style.GuiQtStyle.get_background('color-error')
    )

    BDragChildPolish = QtGui.QColor(*gui_core.GuiRgba.LightYellow)
    BDragChildAdd = QtGui.QColor(*gui_core.GuiRgba.LightGreen)


class QtFontColors(object):
    @staticmethod
    def get(key):
        return QtGui.QColor(
            *_style.GuiQtStyle.get_font(key)
        )

    Black = QtGui.QColor(
        *_style.GuiQtStyle.get_font('color-black')
    )
    Dark = QtGui.QColor(
        *_style.GuiQtStyle.get_font('color-dark')
    )
    Basic = QtGui.QColor(
        *_style.GuiQtStyle.get_font('color-basic')
    )
    Light = QtGui.QColor(
        *_style.GuiQtStyle.get_font('color-light')
    )
    Hovered = QtGui.QColor(
        *_style.GuiQtStyle.get_font('color-hovered')
    )
    Selected = QtGui.QColor(
        *_style.GuiQtStyle.get_font('color-selected')
    )

    KeyBasic = QtGui.QColor(
        *_style.GuiQtStyle.get_font('color-key-basic')
    )
    KeyHovered = QtGui.QColor(
        *_style.GuiQtStyle.get_font('color-key-hovered')
    )
    ValueBasic = QtGui.QColor(
        *_style.GuiQtStyle.get_font('color-value-basic')
    )
    ValueHovered = QtGui.QColor(
        *_style.GuiQtStyle.get_font('color-value-hovered')
    )

    ToolTip = QtGui.QColor(
        *_style.GuiQtStyle.get_font('color-tool-tip')
    )
    #
    Normal = QtGui.QColor(
        *_style.GuiQtStyle.get_font('color-normal')
    )
    Correct = QtGui.QColor(
        *_style.GuiQtStyle.get_font('color-correct')
    )
    Warning = QtGui.QColor(
        *_style.GuiQtStyle.get_font('color-warning')
    )
    Error = QtGui.QColor(
        *_style.GuiQtStyle.get_font('color-error')
    )
    Active = QtGui.QColor(
        *_style.GuiQtStyle.get_font('color-active')
    )
    Disable = QtGui.QColor(
        *_style.GuiQtStyle.get_font('color-disable')
    )


class QtBrushes(object):
    Background = QtGui.QBrush(QtColors.Background)

    Text = QtGui.QBrush(QtColors.Text)
    TextDisable = QtGui.QBrush(QtColors.TextDisable)
    TextTemporary = QtGui.QBrush(QtColors.TextTemporary)
    TextWarning = QtGui.QBrush(QtColors.TextWarning)
    TextError = QtGui.QBrush(QtColors.TextError)
    TextCorrect = QtGui.QBrush(QtColors.TextCorrect)
    TextActive = QtGui.QBrush(QtColors.TextActive)
