# coding:utf-8
import os

import enum


class GuiBase(object):
    ROOT = os.path.dirname(__file__.replace('\\', '/'))
    DATA_ROOT = '{}/.data'.format(ROOT)


class GuiOrientation(enum.IntEnum):
    Horizontal = 0
    Vertical = 1


class GuiAlignment(enum.IntEnum):
    Left = 0
    Right = 1


class GuiDirection(enum.IntEnum):
    LeftToRight = 0
    RightToLeft = 1
    TopToBottom = 2
    BottomToTop = 3


class GuiActionFlag(enum.IntEnum):
    AnyClick = 0x00
    #
    Press = 0x01
    PressDbClick = 0x02
    PressMove = 0x03
    HoverMove = 0x04
    #
    TrackPress = 0x11
    TrackMove = 0x12
    TrackCircle = 0x13
    #
    ZoomMove = 0x21
    #
    CheckPress = 0x31
    CheckDbClick = 0x32
    ExpandPress = 0x33
    OptionPress = 0x34
    ChoosePress = 0x35
    NextPress = 0x36
    ComponentPress = 0x37
    ComponentDbClick = 0x38
    #
    SplitHHover = 0x41
    SplitVHover = 0x42
    SplitHPress = 0x43
    SplitVPress = 0x44
    SplitHMove = 0x45
    SplitVMove = 0x46
    SwapH = 0x47
    SwapV = 0x48
    #
    ResizeLeft = 0x49
    ResizeRight = 0x4A
    ResizeUp = 0x4B
    ResizeDown = 0x4C
    Resize = 0x4D
    #
    ZoomWheel = 0x51
    #
    RectSelectClick = 0x61
    RectSelectMove = 0x62
    #
    NGGraphTrackClick = 0x71
    NGGraphTrackMove = 0x72
    NGNodePressClick = 0x73
    NGNodePressMove = 0x74
    #
    KeyAltPress = 0x81
    KeyControlPress = 0x82
    KeyShiftPress = 0x83
    KeyControlShiftPress = 0x84
    KeyPress = 0x85
    #
    DragPress = 0x91
    DragEnter = 0x92
    DragMove = 0x93
    DragLeave = 0x94
    DragRelease = 0x95
    DragChildPolish = 0x96
    DragChildRemove = 0x97
    DragChildAdd = 0x98
    DragChildAddCancel = 0x99


class GuiDragFlag(enum.IntEnum):
    Ignore = 0x00
    Copy = 0x01
    Move = 0x02


class GuiRectRegion(enum.IntEnum):
    Unknown = 0
    Top = 1
    Bottom = 2
    Left = 3
    Right = 4
    TopLeft = 5
    TopRight = 6
    BottomLeft = 7
    BottomRight = 8
    Inside = 9
    Outside = 10


class GuiAlignRegion(enum.IntEnum):
    Unknown = 0
    Top = 1
    Bottom = 2
    Left = 3
    Right = 4
    TopLeft = 5
    TopRight = 6
    BottomLeft = 7
    BottomRight = 8
    Center = 9


class GuiTagFilterMode(enum.IntEnum):
    MatchAll = 0
    MatchOne = 1


class GuiSortMode(enum.IntEnum):
    Number = 0
    Name = 1


class GuiSortOrder(enum.IntEnum):
    Ascend = 0
    Descend = 1


class GuiSize(object):
    ItemDefaultHeight = 20
    BubbleHeightDefault = 16
    EntryBaseHeightDefault = 20
    InputHeight = 24

    LayoutDefaultContentsMargins = 2, 2, 2, 2
    LayoutDefaultSpacing = 2

    FontSizeDefault = 8
    FontWeightDefault = 50


class GuiSectorChartMode(enum.IntEnum):
    Completion = 0
    Error = 1


class GuiXmlColor(object):
    Red = 0x00
    Yellow = 0x01
    Orange = 0x02
    Green = 0x03
    Blue = 0x04
    White = 0x05
    Gray = 0x06
    Black = 0x07

    All = [
        '#ff003f',  # 0 (255, 0, 63)
        '#fffd3f',  # 1 (255, 255, 63)
        '#ff7f3f',  # 2 (255, 127, 63)
        '#3fff7f',  # 3 (64, 255, 127)
        '#3f7fff',  # 4 (63, 127, 255)

        '#dfdfdf',  # 5 (223, 223, 223)
        '#dfdfdf',  # 6 (191, 191, 191)
        '#7f7f7f',  # 7 (127, 127, 127)
        '#3f3f3f',  # 8 (63, 63, 63)
        '#1f1f1f'  # 9 (31, 31, 31)
    ]

    Dict = {
        Red: All[0],
        Yellow: All[1],
        Orange: All[2],
        Green: All[3],
        Blue: All[4],

        White: All[5],
        Gray: All[7],
        Black: All[9]
    }


class GuiRgba(object):
    # 63+48=111
    # 127+48=175
    Red = 255, 0, 63, 255
    DarkRed = 159, 0, 63, 255
    LightRed = 255, 47, 111, 255

    Brown = 255, 63, 63, 255

    Orange = 255, 127, 63, 255
    DarkOrange = 159, 95, 63, 255
    LightOrange = 255, 175, 111, 255

    Yellow = 255, 255, 63, 255
    DarkYellow = 159, 159, 63, 255
    LightYellow = 255, 255, 111, 255

    Green = 63, 255, 127, 255
    DarkGreen = 63, 159, 95, 255
    LightGreen = 111, 255, 175, 255

    Blue = 63, 127, 255, 255
    DarkBlue = 63, 95, 159, 255
    LightBlue = 111, 175, 255, 255

    BabyBlue = 63, 255, 255, 255
    DarkBabyBlue = 63, 159, 159, 255
    LightBabyBlue = 111, 255, 255, 255

    Purple = 127, 127, 255, 255
    DarkPurple = 95, 95, 159, 255
    LightPurple = 175, 175, 255, 255

    Pink = 255, 127, 127, 255
    DarkPink = 159, 95, 79, 255
    LightPink = 255, 175, 175, 255

    Violet = 127, 0, 255, 255

    White = 255, 255, 255, 255
    Black = 0, 0, 0, 255

    Gray = 127, 127, 127, 255
    DarkGray = 95, 95, 95, 255
    LightGray = 159, 159, 159, 255

    Light = 223, 223, 223, 255
    Dark = 55, 55, 55, 255
    Dim = 47, 47, 47, 255
    Transparent = 0, 0, 0, 0

    All = [
        Red, DarkRed, LightRed,
        LightOrange, Orange, DarkOrange,
        LightYellow, Yellow, DarkYellow,
        LightGreen, Green, DarkGreen,
        LightBlue, Blue, DarkBlue,
        LightPurple, Purple, DarkPurple,
        LightPink, Pink, DarkPink,
        White, Black, Gray, Light, Transparent
    ]


class GuiStatus(enum.IntEnum):
    Unknown = 0
    Started = 1
    Running = 2
    Waiting = 3
    Completed = 4
    Suspended = 5
    Failed = 6
    Stopped = 7
    Error = 8
    Killed = 9
    Finished = 10


class GuiShowStatus(enum.IntEnum):
    Unknown = -1
    Started = 0
    Loading = 1
    Waiting = 2
    Finished = 3
    Completed = 4
    Failed = 5
    Stopped = 6
    Killed = 7


class GuiValidationStatus(enum.IntEnum):
    Normal = 0x20
    Correct = 0x21
    Warning = 0x22
    Error = 0x23
    Ignore = 0x24
    Locked = 0x25
    Active = 0x26
    Disable = 0x27
    Unreadable = 0x28
    Unwritable = 0x29
    Lost = 0x2A
    New = 0x2B


class GuiActionState(enum.IntEnum):
    Normal = 0x30
    Enable = 0x31
    Disable = 0x32
    #
    PressEnable = 0x41
    PressDisable = 0x42
    #
    ChooseEnable = 0x51
    ChooseDisable = 0x52
