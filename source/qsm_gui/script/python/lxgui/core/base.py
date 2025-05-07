# coding:utf-8
import os

import six

import math

import re

import copy

import platform

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.resource as bsc_resource

import lxbasic.content as bsc_content
# gui
from . import configure as gui_cor_configure


class GuiLanguage:
    CHS = 'chs'
    EN_US = 'en_us'


class GuiName:
    SortBy = 'Sort by'
    SortByChs = '排列方式'
    SortOrder = 'Sort Order'
    SortOrderChs = '排列顺序'

    GroupBy = 'Group by'
    GroupByChs = '分组依据'


class GuiState(object):
    NORMAL = 'normal'
    ENABLE = 'enable'
    DISABLE = 'disable'
    WARNING = 'warning'
    ERROR = 'error'
    LOCKED = 'locked'
    LOST = 'lost'


class GuiUtil(object):

    @staticmethod
    def get_is_linux():
        return platform.system() == 'Linux'

    @staticmethod
    def get_is_windows():
        return platform.system() == 'Windows'

    @classmethod
    def get_is_maya(cls):
        _ = os.environ.get('MAYA_APP_DIR')
        if _:
            return True
        return False

    @classmethod
    def get_is_houdini(cls):
        _ = os.environ.get('HIP')
        if _:
            return True
        return False

    @classmethod
    def get_is_katana(cls):
        _ = os.environ.get('KATANA_ROOT')
        if _:
            return True
        return False

    @classmethod
    def get_is_clarisse(cls):
        _ = os.environ.get('IX_PYTHON2HOME')
        if _:
            return True
        return False

    @classmethod
    def get_windows_user_directory(cls):
        return '{}{}/.qosmic'.format(
            os.environ.get('HOMEDRIVE', 'c:'),
            os.environ.get('HOMEPATH', '/temp')
        ).replace('\\', '/')

    @classmethod
    def get_linux_user_directory(cls):
        return '{}/.qosmic'.format(
            os.environ.get('HOME', '/home/{}'.format(bsc_core.BscSystem.get_user_name()))
        )

    @classmethod
    def get_user_directory(cls):
        if cls.get_is_windows():
            return cls.get_windows_user_directory()
        elif cls.get_is_linux():
            return cls.get_linux_user_directory()
        raise SystemError()

    @classmethod
    def get_user_history_cache_file(cls):
        return '{}/history.yml'.format(
            cls.get_user_directory()
        )

    @classmethod
    def get_user_history_file(cls, key):
        application = bsc_core.BscApplication.get_current()
        return '{}/history/{}/{}.yml'.format(
            cls.get_user_directory(), application, key
        )

    @classmethod
    def get_user_verify_file(cls, key):
        return '{}/verify/{}.json'.format(
            cls.get_user_directory(), key
        )

    @classmethod
    def get_user_thumbnail_cache_file(cls):
        return '{}/thumbnail.yml'.format(
            cls.get_user_directory()
        )

    @classmethod
    def get_language(cls):
        return bsc_core.BscEnviron.get_gui_language()

    @classmethod
    def language_is_chs(cls):
        return cls.get_language() == GuiLanguage.CHS

    @classmethod
    def choice_gui_name(cls, language, options):
        if options:
            if language == GuiLanguage.CHS:
                if 'name_chs' in options:
                    return options['name_chs']
            return options['name']
        return 'null'

    @classmethod
    def choice_gui_name_auto(cls, options):
        if options:
            if cls.get_language() == GuiLanguage.CHS:
                if 'name_chs' in options:
                    return options['name_chs']
            return options['name']
        return 'null'

    @classmethod
    def choice_gui_description(cls, language, options):
        if options:
            if language == GuiLanguage.CHS:
                if 'description_chs' in options:
                    return options['description_chs']
            return options['description']
        return 'null'

    @classmethod
    def choice_gui_tool_tip(cls, language, options):
        if options:
            if language == GuiLanguage.CHS:
                if 'tool_tip_chs' in options:
                    return options['tool_tip_chs']
            return options['tool_tip']
        return 'null'

    @classmethod
    def choice_gui_message(cls, language, options):
        if options:
            if language == GuiLanguage.CHS:
                if 'message_chs' in options:
                    return options['message_chs']
            return options['message']
        return 'null'


class GuiXml(object):
    @classmethod
    def get_color(cls, *args):
        arg = args[0]
        if isinstance(arg, (float, int)):
            return gui_cor_configure.GuiXmlColor.All[int(arg)]
        elif isinstance(arg, six.string_types):
            return gui_cor_configure.GuiXmlColor.Dict.get(arg, '#dfdfdf')
        return '#dfdfdf'

    @classmethod
    def get_text(cls, text, text_color=gui_cor_configure.GuiXmlColor.White, font_family='Arial', font_size=8):
        html_color = cls.get_color(text_color)
        #
        text = text.replace(' ', '&nbsp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        _ = text.split('\n')
        if len(_) > 1:
            raw = u''.join([u'{}<br>'.format(i) for i in _])
        else:
            raw = text
        #
        return u'''
<html>
    <head>
        <style>
            p.s{{line-height: 100%; font-family: '{font_family}'; font-size: {font_size}pt; color: {text_color}; word-spacing: normal;}}
        </style>
    </head>
    <body>
        <p class="s">{raw}</p>
    </body>
</html>
        '''.format(
            **dict(
                font_family=font_family,
                font_size=font_size,
                text_color=html_color,
                raw=raw
            )
        )


class GuiChat(object):
    FNC_ANGLE = math.radians
    FNC_SIN = math.sin
    FNC_COS = math.cos
    FNC_TAN = math.tan
    FNC_FLOOR = math.floor

    @classmethod
    def get_regular_polygon_points(cls, pos_x, pos_y, side_count, radius, side):
        lis = []
        for seq in range(side_count):
            a = 360/side_count*seq
            x = math.sin(math.radians(a))*(radius-side)+pos_x
            y = math.cos(math.radians(a))*(radius-side)+pos_y
            lis.append((x, y))
        if lis:
            lis.append(lis[0])
        return lis

    @classmethod
    def get_angle_by_coord(cls, x1, y1, x2, y2):
        radian = 0.0
        #
        r0 = 0.0
        r90 = math.pi/2.0
        r180 = math.pi
        r270 = 3.0*math.pi/2.0
        #
        if x1 == x2:
            if y1 < y2:
                radian = r0
            elif y1 > y2:
                radian = r180
        elif y1 == y2:
            if x1 < x2:
                radian = r90
            elif x1 > x2:
                radian = r270
        elif x1 < x2 and y1 < y2:
            radian = math.atan2((-x1+x2), (-y1+y2))
        elif x1 < x2 and y1 > y2:
            radian = r90+math.atan2((y1-y2), (-x1+x2))
        elif x1 > x2 and y1 > y2:
            radian = r180+math.atan2((x1-x2), (y1-y2))
        elif x1 > x2 and y1 < y2:
            radian = r270+math.atan2((-y1+y2), (x1-x2))
        #
        return radian*180/math.pi

    @classmethod
    def get_length_by_coord(cls, x1, y1, x2, y2):
        return math.sqrt(((x1-x2)**2)+((y1-y2)**2))


class GuiEllipse2d(object):
    @classmethod
    def get_coord_at_angle(cls, start, radius, angle):
        x, y = start
        xp = math.sin(math.radians(angle))*radius/2+x+radius/2
        yp = math.cos(math.radians(angle))*radius/2+y+radius/2
        return xp, yp

    @classmethod
    def get_coord_at_angle_(cls, center, radius, angle):
        x, y = center
        xp = math.sin(math.radians(angle))*radius/2+x
        yp = math.cos(math.radians(angle))*radius/2+y
        return xp, yp


class GuiIcon(object):
    BRANCH = 'icons'
    ICON_KEY_PATTERN = r'[@](.*?)[@]'

    @classmethod
    def get(cls, key):
        return bsc_resource.BscResource.get(
            '{}/{}.*'.format(cls.BRANCH, key)
        )

    @classmethod
    def get_(cls, key):
        _ = re.findall(
            re.compile(cls.ICON_KEY_PATTERN, re.S), key
        )
        if _:
            cls.get(_)

    @classmethod
    def get_directory(cls):
        return cls.get('file/folder')

    @classmethod
    def get_by_file(cls, file_path):
        ext = os.path.splitext(file_path)[-1]
        if ext:
            _ = cls.get('file/{}'.format(ext[1:]))
            if _:
                return _
        return cls.get('file/file')

    @classmethod
    def find_all_keys_at(cls, group_branch):
        return bsc_resource.BscResource.find_all_file_keys_at(
            cls.BRANCH, group_branch, ext_includes={'.png', '.svg'}
        )


class GuiIconDirectory(object):
    BRANCH = 'icons'
    ICON_KEY_PATTERN = r'[@](.*?)[@]'

    @classmethod
    def get(cls, key):
        return bsc_resource.BscResource.get(
            '{}/{}'.format(cls.BRANCH, key)
        )


class GuiFont(object):
    BRANCH = 'fonts'

    @classmethod
    def get(cls, key):
        return bsc_resource.BscResource.get(
            '{}/{}.*'.format(cls.BRANCH, key)
        )

    @classmethod
    def get_all(cls, sub_key='*'):
        return bsc_resource.BscResource.get_all(
            '{}/{}.*'.format(cls.BRANCH, sub_key)
        )


class GuiDebug(object):
    @staticmethod
    def run(fnc):
        def fnc_(*args, **kwargs):
            # noinspection PyBroadException
            try:
                _fnc = fnc(*args, **kwargs)
                return _fnc
            except Exception:
                bsc_log.LogDebug.trace()
                raise
        return fnc_


class GuiDpiScale(object):
    @classmethod
    def get(cls, *args):
        return args[0]


class GuiThumbnailCache(object):
    LOG_KEY = 'gui history'
    MAXIMUM = 20

    FILE = GuiUtil.get_user_history_cache_file()
    CONTENT_CACHE = bsc_content.ContentCache(FILE)

    def __init__(self, file_path):
        self.__content_cache = bsc_content.ContentCache(file_path)

    def pull(self, key):
        c = self.__content_cache.generate()
        return c.get(key)

    def push(self, key, value):
        c = self.__content_cache.generate()
        c.set(key, value)
        c.save()


class GuiPlayModes(object):
    Video = 0x01
    ImageSequence = 0x02


class GuiApplication(object):
    @classmethod
    def show_tool_dialog(cls, *args, **kwargs):
        import lxgui.qt.core as gui_qt_core
        return gui_qt_core.QtApplication.show_tool_dialog(*args, **kwargs)

    @classmethod
    def exec_message_dialog(cls, *args, **kwargs):
        import lxgui.qt.core as gui_qt_core
        return gui_qt_core.QtApplication.exec_message_dialog(*args, **kwargs)

    @classmethod
    def exec_input_dialog(cls, *args, **kwargs):
        import lxgui.qt.core as gui_qt_core
        return gui_qt_core.QtApplication.exec_input_dialog(*args, **kwargs)

