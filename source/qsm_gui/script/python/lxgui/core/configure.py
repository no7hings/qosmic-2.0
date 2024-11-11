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


class GuiDirections(enum.IntEnum):
    LeftToRight = 0
    RightToLeft = 1
    TopToBottom = 2
    BottomToTop = 3


class GuiActionFlag(enum.IntEnum):
    AnyClick = 0x00
    #
    Press = 0x01
    PressClick = 0x02
    PressDblClick = 0x03
    PressMove = 0x04
    #
    HoverMove = 0x05
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
    TimeMove = 0x52
    NGTimeResizeLeft = 0x53
    NGTimeResizeRight = 0x54
    NGTimeScaleLeft = 0x55
    NGTimeScaleRight = 0x56
    #
    RectSelectClick = 0x61
    RectSelectMove = 0x62
    #
    NGGraphTrackClick = 0x71
    NGGraphTrackMove = 0x72
    NGNodePressClick = 0x73
    NGNodePressMove = 0x74
    NGNodeAnyAction = 0x75
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


class GuiItemMode(enum.IntEnum):
    Icon = 0
    List = 1
    Image = 2


class GuiSize:
    ItemHeightDefault = 20
    BubbleHeightDefault = 16
    EntryBaseHeightDefault = 20

    LayoutDefaultContentsMargins = 2, 2, 2, 2
    LayoutDefaultSpacing = 2

    FontSizeDefault = 8
    FontWeightDefault = 50

    InputHeight = 24
    InputHeightA = 82
    
    ItemNameHeight = 20
    ItemMtimeHeight = 20


class GuiSectorChartMode(enum.IntEnum):
    Completion = 0
    Error = 1


class GuiXmlColor(object):
    TorchRed = 0x00
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
        TorchRed: All[0],
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
    # 175+48=223
    Red = 255, 0, 0, 255
    DarkRed = 159, 0, 0, 255
    LightRed = 255, 47, 47, 255

    TorchRed = 255, 0, 63, 255
    DarkTorchRed = 159, 0, 63, 255
    LightTorchRed = 255, 47, 111, 255

    Brown = 255, 63, 63, 255

    Orange = 255, 127, 63, 255
    DarkOrange = 159, 95, 63, 255
    LightOrange = 255, 175, 111, 255

    Yellow = 255, 255, 0, 255
    DarkYellow = 159, 159, 0, 255
    LightYellow = 255, 255, 63, 255

    LemonYellow = 255, 255, 63, 255
    DarkLemonYellow = 159, 159, 63, 255
    LightLemonYellow = 255, 255, 111, 255

    Green = 0, 255, 0, 255
    DarkGreen = 0, 159, 0, 255
    LightGreen = 47, 255, 47, 255

    BrightNeonGreen = 119, 255, 223, 255
    LightNeonGreen = 111, 255, 175, 255
    NeonGreen = 63, 255, 127, 255
    DarkNeonGreen = 63, 159, 95, 255

    LightBlue = 47, 47, 255, 255
    Blue = 0, 0, 255, 255
    DarkBlue = 0, 0, 159, 255

    LightAzureBlue = 111, 175, 255, 255
    AzureBlue = 63, 127, 255, 255
    DarkAzureBlue = 63, 95, 159, 255
    DimAzureBlue = 55, 87, 151, 255

    BabyBlue = 63, 255, 255, 255
    DarkBabyBlue = 63, 159, 159, 255
    LightBabyBlue = 111, 255, 255, 255

    Purple = 127, 127, 255, 255
    DarkPurple = 95, 95, 159, 255
    LightPurple = 175, 175, 255, 255

    Pink = 255, 127, 127, 255
    DarkPink = 159, 95, 95, 255
    LightPink = 255, 175, 175, 255

    PinkPurple = 255, 127, 255, 255
    DarkPinkPurple = 159, 95, 159, 255
    LightPinkPurple = 255, 175, 255, 255

    Violet = 127, 0, 255, 255

    White = 255, 255, 255, 255
    DarkWhite = 223, 223, 223, 255

    # +32
    LightGray = 159, 159, 159, 255
    # default
    Gray = 127, 127, 127, 255
    # -8
    GrayA = 119, 119, 119, 255
    # -16
    GrayB = 111, 111, 111, 255
    # -24
    GrayC = 103, 103, 103, 255
    # -32
    DarkGray = 95, 95, 95, 255
    # -56
    DimGray = 71, 71, 71, 255

    Black = 0, 0, 0, 255
    LightBlack = 31, 31, 31, 255

    Light = 223, 223, 223, 255
    # +16
    FadeBasicA = 79, 79, 79, 255
    # +8
    FadeBasic = 71, 71, 71, 255
    # default
    Basic = 63, 63, 63, 255
    # -8
    Dark = 55, 55, 55, 255
    # -16
    Dim = 47, 47, 47, 255
    #
    Transparent = 0, 0, 0, 0

    Shadow = 0, 0, 0, 31
    
    # button, 8x14
    BkgButton = 111, 111, 111, 255
    # hover + 32
    BkgButtonHover = 143, 143, 143, 255
    BkgButtonDisable = 79, 79, 79, 255
    # border +8
    BdrButton = 119, 119, 119, 255
    BdrButtonHover = 151, 151, 151, 255
    BdrButtonDisable = 87, 87, 87, 255

    # menu
    BkgMenu = 55, 55, 55, 255
    # border +32
    BdrMenu = 87, 87, 87, 255
    
    # scroll bar 8x10
    BkgScrollBar = 79, 79, 79, 255
    # hover +32
    BkgScrollBarHover = 111, 111, 111, 255
    # border +8
    BdrScrollBar = 87, 87, 87, 255
    BdrScrollBarHover = 119, 119, 119, 255

    # head 8x10
    BkgHead = 79, 79, 79, 255
    # hover +32
    BkgHeadHover = 111, 111, 111, 255
    # border +0
    BdrHead = 79, 79, 79, 255
    BdrHeadHover = 111, 111, 111, 255

    BkgToolTip = 223, 223, 191, 255
    BdrToolTip = LightBlack
    TxtToolTip = LightBlack
    
    Text = DarkWhite
    TextHoverA = LightBlack
    TextHover = White
    TextDark = 127, 127, 127, 255

    TxtMtime = 127, 127, 127, 255

    TxtEnable = NeonGreen
    TxtDisable = DarkGray
    TxtTemporary = Gray
    TxtWarning = LemonYellow
    TxtError = TorchRed
    TxtLock = Purple
    TxtCorrect = NeonGreen
    TxtActive = AzureBlue

    TxtKey = 191, 191, 191, 255
    TxtValue = 255, 255, 255, 255

    Border = 71, 71, 71, 255
    BorderHover = LightOrange
    BorderSelect = LightAzureBlue
    BorderAction = LightNeonGreen
    # +8
    BorderLight = 79, 79, 79, 255
    # +16
    BorderBright = 95, 95, 95, 255

    Background = Basic
    BackgroundHover = LightOrange
    BackgroundSelect = LightAzureBlue
    BackgroundAction = LightNeonGreen
    # +16
    BackgroundBright = 79, 79, 79, 255
    # +8
    BackgroundLight = 71, 71, 71, 255
    BackgroundDark = Dark
    BackgroundDim = Dim

    BkgCheck = Purple
    BkgCheckHover = LightPurple

    BkgPress = 95, 255, 159, 255
    BkgPressHover = 255, 179, 47, 255

    BkgDelete = 255, 0, 63, 255
    BkgDeleteHover = 255, 63, 127, 255

    BkgIcon = 127, 127, 127, 255
    BdrIcon = 159, 159, 159, 255
    
    BdrSubIcon = 207, 207, 207, 255
    BkgSubIcon = 127, 127, 127, 255

    # drag
    BkgDragChildPolish = LightLemonYellow
    BkgDragChildAdd = LightNeonGreen

    BdrPopup = LightAzureBlue
    BdrSplitMoving = 127, 127, 127, 255
    
    BdrCapsuleCheck = 127, 127, 127, 255
    BdrCapsuleUncheck = 55, 55, 55, 255
    BdrCapsuleHover = LightOrange
    BdrCapsuleAction = LightAzureBlue
    BkgCapsule = 47, 47, 47, 255
    BkgCapsuleDisable = 55, 55, 55, 255
    
    BdrTab = 63, 63, 63, 255
    BdrTabActive = 87, 87, 87, 255
    BkgTab = 47, 47, 47, 255
    BkgTabActive = 63, 63, 63, 255

    # tab
    BkgTabGroup = 55, 55, 55, 255
    BkgTabGroupActive = 63, 63, 63, 255
    # border +16
    BdrTabGroup = 71, 71, 71, 255
    BdrTabGroupActive = 79, 79, 79, 255
    
    BkgBubble = 223, 223, 223, 255
    BkgBubbleDisable = 127, 127, 127, 255
    BkgBubbleHover = LightOrange
    BkgBubbleAction = LightNeonGreen
    BkgBubbleNextWait = LightLemonYellow
    BkgBubbleNextFinish = LightNeonGreen
    BdrBubble = 127, 127, 127, 255
    TxtBubble = 31, 31, 31, 255
    TxtBubbleNext = 127, 127, 127, 255

    BkgProgress = 47, 47, 47, 255

    TxtHead = 207, 207, 207, 255
    TxtHeadHover = 223, 223, 223, 255
    
    TxtKeywordFilter = 255, 127, 63, 255
    TxtKeywordFilterOccurrence = 255, 63, 63, 255


class GuiProcessStatus(enum.IntEnum):
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


class GuiProcessStatusMapper(object):
    MAPPER = {
        GuiProcessStatus.Unknown: 'Unknown',
        GuiProcessStatus.Started: 'Started',
        GuiProcessStatus.Running: 'Running',
        GuiProcessStatus.Waiting: 'Waiting',
        GuiProcessStatus.Completed: 'Completed',
        GuiProcessStatus.Suspended: 'Suspended',
        GuiProcessStatus.Failed: 'Failed',
        GuiProcessStatus.Stopped: 'Stopped',
        GuiProcessStatus.Error: 'Error',
        GuiProcessStatus.Killed: 'Killed',
        GuiProcessStatus.Finished: 'Finished',
    }
    MAPPER_CHS = {
    }


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
    Enable = Active
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


class GuiItemStatus(enum.IntEnum):
    Normal = 0

    Warning = 1
    Error = 2
    Correct = 3

    Enable = Normal
    Disable = 5


class GuiItemSortKey:
    Category = 'category'
    Type = 'type'
    Name = 'name'
    Mtime = 'mtime'
    Number = 'number'
    Default = 'default'

    ALL = [
        Category, Type, Name, Number, Default
    ]

    NAME_MAP = {
        Category: 'Category',
        Type: 'Type',
        Name: 'Name',
        Mtime: 'Modified',
        Number: 'Number',
        Default: 'Default'
    }
    NAME_MAP_CHS = {
        Category: '分类',
        Type: '类型',
        Name: '名字',
        Mtime: '修改时间',
        Number: '数量',
        Default: '默认',
    }


class GuiItemSortOrder:
    Ascending = 0
    Descending = 1

    ALL = [
        Ascending, Descending
    ]

    NAME_MAP = {
        Ascending: 'Ascending',
        Descending: 'Descending'
    }
    NAME_MAP_CHS = {
        Ascending: '递增',
        Descending: '递减'
    }


class GuiItemGroupKey:
    Category = 'category'
    Type = 'type'
    Name = 'name'
    Mtime = 'mtime'
    Null = 'null'

    ALL = [
        Category, Type, Name, Mtime, Null
    ]

    NAME_MAP = {
        Category: 'Category',
        Type: 'Type',
        Name: 'Name',
        Mtime: 'Modified',
        Null: 'None',
    }

    NAME_MAP_CHS = {
        Category: '分类',
        Type: '类型',
        Name: '名字',
        Mtime: '修改时间',
        Null: '无',
    }
