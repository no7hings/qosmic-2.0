# coding:utf-8
import hashlib

import six

import math

import copy

import re

import fnmatch

import random

import collections

import itertools


def auto_encode(text):
    if isinstance(text, six.text_type):
        return text.encode('utf-8')
    return text


class RawColorMtd(object):
    @classmethod
    def rgb2hex(cls, r, g, b):
        return hex(r)[2:].zfill(2)+hex(g)[2:].zfill(2)+hex(b)[2:].zfill(2)

    @classmethod
    def hex2rgb(cls, hex_color, maximum=255):
        hex_color = int(hex_color, base=16) if isinstance(hex_color, str) else hex_color
        r, g, b = ((hex_color >> 16)&0xff, (hex_color >> 8)&0xff, hex_color&0xff)
        if maximum == 255:
            return r, g, b
        elif maximum == 1.0:
            return round(float(r)/float(255), 4), round(float(g)/float(255), 4), round(float(b)/float(255), 4)

    @classmethod
    def hsv2rgb(cls, h, s, v, maximum=255):
        h = float(h%360.0)
        s = float(max(min(s, 1.0), 0.0))
        v = float(max(min(v, 1.0), 0.0))
        #
        c = v*s
        x = c*(1-abs((h/60.0)%2-1))
        m = v-c
        if 0 <= h < 60:
            r_, g_, b_ = c, x, 0
        elif 60 <= h < 120:
            r_, g_, b_ = x, c, 0
        elif 120 <= h < 180:
            r_, g_, b_ = 0, c, x
        elif 180 <= h < 240:
            r_, g_, b_ = 0, x, c
        elif 240 <= h < 300:
            r_, g_, b_ = x, 0, c
        else:
            r_, g_, b_ = c, 0, x
        #
        if maximum == 255:
            r, g, b = int(round((r_+m)*maximum)), int(round((g_+m)*maximum)), int(round((b_+m)*maximum))
        else:
            r, g, b = float((r_+m)), float((g_+m)), float((b_+m))
        return r, g, b

    # noinspection PyUnusedLocal
    @classmethod
    def rgb_to_hsv(cls, r, g, b, maximum=255):
        r, g, b = r/255.0, g/255.0, b/255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        m = mx-mn
        #
        h = 0.0
        if mx == mn:
            h = 0.0
        elif mx == r:
            if g >= b:
                h = ((g-b)/m)*60
            else:
                h = ((g-b)/m)*60+360
        elif mx == g:
            h = ((b-r)/m)*60+120
        elif mx == b:
            h = ((r-g)/m)*60+240
        #
        if mx == 0:
            s = 0.0
        else:
            s = m/mx
        v = mx
        h_ = h
        s_ = s
        v_ = v
        return h_, s_, v_

    # noinspection PyUnusedLocal
    @classmethod
    def get_complementary_rgb(cls, r, g, b, maximum=255):
        return abs(255-r), abs(255-g), abs(255-b)

    # noinspection PyUnusedLocal
    @classmethod
    def set_rgb_offset(cls, rgb, hsv_offset):
        r, g, b = rgb

    @classmethod
    def get_color_from_string(cls, string, count=1000, maximum=255, offset=0, seed=0):
        d = count
        a_0 = sum([ord(i)*(seq*10 if seq > 0 else 1) for seq, i in enumerate(string[::-1])])+offset
        a_1 = sum([ord(i)*(seq*10 if seq > 0 else 1) for seq, i in enumerate(string)])
        h = float(a_0%(360+seed)*d)/d
        s = float(45+a_1%55)/100.0
        v = float(45+a_1%55)/100.0
        return RawColorMtd.hsv2rgb(h, s, v, maximum)

    @classmethod
    def get_choice_colors(cls, count, maximum=255, offset=0, seed=0):
        list_ = []
        for i in range(count):
            list_.append(
                cls.get_rgb_from_index(i, count, maximum, offset, seed)
            )
        return list_

    @classmethod
    def get_rgb_from_index(cls, index, count, maximum=255, offset=0, seed=0):
        d = 1000.0
        p = float(index)/float(count)
        i_0 = 360.0*p
        i_1 = 360.0*(1.0-p)
        i_offset = 0
        a_0 = i_0+offset+seed+i_offset
        a_1 = i_1+offset+seed-i_offset
        h = float(a_0%360.0*d)/d
        s = float(0.125*d+(a_0%0.875*d))/d
        v = float(0.125*d+(a_1%0.875*d))/d
        return cls.hsv2rgb(h, s, v, maximum)

    @classmethod
    def rgb_to_aces(cls, r, g, b):
        in_rgb = [r, g, b]
        out_rgb = [0, 0, 0]
        matrix = [
            [0.9872240087030176, -0.007598371811662351, 0.0030725770585315355],
            [-0.006113228606856964, 1.0018614847396536, -0.00509596151113061],
            [0.015953288335912676, 0.005330035791388953, 1.0816806030657955]
        ]
        for i in range(3):
            for j in range(3):
                out_rgb[i] += matrix[i][j]*in_rgb[j]

        for i in range(3):
            out_rgb[i] = max(min(out_rgb[i], 1.0), 0.0)

        return out_rgb

    @classmethod
    def aces_to_rgb(cls, r, g, b):
        in_rgb = [r, g, b]
        out_rgb = [0, 0, 0]
        matrix = [
            [2.52194068, -1.13646443, -0.38523062],
            [-0.27597527, 1.44709525, -0.17125402],
            [-0.01505824, -0.06865287, 1.08271044]
        ]
        for i in range(3):
            for j in range(3):
                out_rgb[i] += matrix[i][j]*in_rgb[j]

        for i in range(3):
            out_rgb[i] = max(min(out_rgb[i], 1.0), 0.0)

        return out_rgb


class RawColorChoiceOpt(object):
    def __init__(self, s_minimum=0.125, s_maximum=0.875, v_minimum=0.125, v_maximum=0.875, seed=0):
        random.seed(seed)

        self.__d = 100.0
        self.__s_minimum = s_minimum
        self.__s_maximum = s_maximum
        self.__v_minimum = v_minimum
        self.__v_maximum = v_maximum
        self.__hs = range(int(360*self.__d))
        self.__ss = range(int(self.__s_minimum*self.__d), int(self.__s_maximum*self.__d))
        self.__vs = range(int(self.__v_minimum*self.__d), int(self.__v_maximum*self.__d))

    def generate(self, maximum=255.0):
        h = random.choice(self.__hs)/self.__d
        s = random.choice(self.__ss)/self.__d
        v = random.choice(self.__vs)/self.__d
        return RawColorMtd.hsv2rgb(h, s, v, maximum)


class RawCoordMtd(object):
    @classmethod
    def get_region(cls, position, size):
        x, y = position
        width, height = size
        if 0 <= x < width/2 and 0 <= y < height/2:
            value = 0
        elif width/2 <= x < width and 0 <= y < height/2:
            value = 1
        elif 0 <= x < width/2 and height/2 <= y < height:
            value = 2
        else:
            value = 3
        return value

    @classmethod
    def set_region_to(cls, position, size, maximum_size, offset):
        x, y = position
        width, height = size
        maximum_w, maximum_h = maximum_size
        o_x, o_y = offset
        #
        region = cls.get_region(
            position=position,
            size=(maximum_w, maximum_h)
        )
        #
        if region == 0:
            x_ = x+o_x
            y_ = y+o_y
        elif region == 1:
            x_ = x-width-o_x
            y_ = y+o_y
        elif region == 2:
            x_ = x+o_x
            y_ = y-height-o_y
        else:
            x_ = x-width-o_x
            y_ = y-height-o_y
        #
        return x_, y_, region

    @classmethod
    def to_length(cls, position0, position1):
        x0, y0 = position0
        x1, y1 = position1
        return math.sqrt(((x0-x1)**2)+((y0-y1)**2))

    @classmethod
    def to_angle(cls, position0, position1):
        x0, y0 = position0
        x1, y1 = position1
        #
        radian = 0.0
        #
        r0 = 0.0
        r90 = math.pi/2.0
        r180 = math.pi
        r270 = 3.0*math.pi/2.0
        #
        if x0 == x1:
            if y0 < y1:
                radian = r0
            elif y0 > y1:
                radian = r180
        elif y0 == y1:
            if x0 < x1:
                radian = r90
            elif x0 > x1:
                radian = r270

        elif x0 < x1 and y0 < y1:
            radian = math.atan2((-x0+x1), (-y0+y1))
        elif x0 < x1 and y0 > y1:
            radian = r90+math.atan2((y0-y1), (-x0+x1))
        elif x0 > x1 and y0 > y1:
            radian = r180+math.atan2((x0-x1), (y0-y1))
        elif x0 > x1 and y0 < y1:
            radian = r270+math.atan2((-y0+y1), (x0-x1))
        return radian*180/math.pi


class RawNestedArrayMtd(object):
    @classmethod
    def set_map_to(cls, array):
        """
        :param array: etc.[[1, 2], [1, 2]]
        :return: etc.[[1, 1], [1, 2], [2, 1], [2, 2]]
        """

        def rcs_fnc_(index_):
            if index_ < count:
                _array = array[index_]
                for _i in _array:
                    c[index_] = _i
                    rcs_fnc_(index_+1)
            else:
                list_.append(
                    copy.copy(c)
                )

        #
        list_ = []
        count = len(array)
        c = [None]*count
        rcs_fnc_(0)
        return list_


class RawIntArrayMtd(object):
    @staticmethod
    def merge_to(array):
        """
        :param array: etc.[1, 2, 3, 5, 6, 9]
        :return: etc.[(1, 3), (5, 6), 9]
        """
        list_ = []
        #
        if array:
            if len(array) == 1:
                return array
            else:
                minimum, maximum = min(array), max(array)
                #
                start, end = None, None
                count = len(array)
                cur_index = 0
                #
                array.sort()
                for i_index in array:
                    if cur_index > 0:
                        pre = array[cur_index-1]
                    else:
                        pre = None
                    #
                    if cur_index < (count-1):
                        nex = array[cur_index+1]
                    else:
                        nex = None
                    #
                    if pre is None and nex is not None:
                        start = minimum
                        if i_index-nex != -1:
                            list_.append(start)
                    elif pre is not None and nex is None:
                        end = maximum
                        if i_index-pre == 1:
                            list_.append((start, end))
                        else:
                            list_.append(end)
                    elif pre is not None and nex is not None:
                        if i_index-pre != 1 and i_index-nex != -1:
                            list_.append(i_index)
                        elif i_index-pre == 1 and i_index-nex != -1:
                            end = i_index
                            list_.append((start, end))
                        elif i_index-pre != 1 and i_index-nex == -1:
                            start = i_index
                    #
                    cur_index += 1
                #
        return list_


class RawValueMtd(object):
    @classmethod
    def step_to(cls, value, delta, step, value_range, direction):
        min0, max0 = value_range
        min1, max1 = min0+step, max0-step
        if value < min1:
            if 0 < delta:
                value += step
            else:
                value = min0
        elif min1 <= value <= max1:
            value += [-step, step][delta > 0]*direction
        elif max1 < value:
            if delta < 0:
                value -= step
            else:
                value = max0
        return value

    @classmethod
    def set_offset_range_to(cls, value, d_value, radix, value_range, direction):
        minimum, maximum = value_range
        value += d_value*direction
        value = int(value/radix)*radix
        value = max(min(value, maximum), minimum)
        return value

    @classmethod
    def map_to(cls, value, range_0, range_1):
        assert isinstance(range_0, (tuple, list)), 'Argument Error, "range_0" Must "tuple" or "list".'
        assert isinstance(range_1, (tuple, list)), 'Argument Error, "range_1" Must "tuple" or "list".'

        min0, max0 = range_0
        min1, max1 = range_1
        #
        if max0-min0 > 0:
            percent = float(value-min0)/float(max0-min0)
            #
            value_ = (max1-min1)*percent+min1
            return value_
        else:
            return min1

    @classmethod
    def get_percent_prettify(cls, value, maximum, round_count=3):
        round_range = 100
        if maximum > 0:
            percent = round(float(value)/float(maximum), round_count)*round_range
        else:
            if value > 0:
                percent = float(u'inf')
            elif value < 0:
                percent = float('-inf')
            else:
                percent = 0
        return percent


class RawListMtd(object):
    @classmethod
    def grid_to(cls, array, column_count):
        c = len(array)
        return [array[i:i+column_count] for i in range(0, c, column_count)]

    @classmethod
    def get_intersection(cls, a, b):
        _ = list(set(a) & set(b))
        _.sort(key=a.index)
        return _

    @classmethod
    def get_addition(cls, a, b):
        _ = list(set(a)-set(b))
        _.sort(key=a.index)
        return _

    @classmethod
    def get_deletion(cls, a, b):
        pass


class RawValueRangeMtd(object):
    @classmethod
    def set_map_to(cls, range_0, range_1, value_0):
        value_min_0, value_max_0 = range_0
        value_min_1, value_max_1 = range_1
        #
        percent = float(value_0-value_min_0)/(value_max_0-value_min_0)
        #
        value_1 = (value_max_1-value_min_1)*percent+value_min_1
        return value_1


class RawFrameRangeMtd(object):
    @classmethod
    def get(cls, frame_range, frame_step):
        start_frame, end_frame = map(int, frame_range)
        frame_step = int(frame_step)
        # (1001, 1001), 1
        if start_frame == end_frame:
            return [start_frame]
        # (1001, 1002), 1
        elif start_frame < end_frame:
            frames = range(start_frame, end_frame+1)
            count = len(frames)
            # (1001, 1002), 2
            if count == frame_step:
                return [start_frame, end_frame]
            # (1001, 1010), 4
            elif count > frame_step:
                # add frame offset
                frame_offset = 1-start_frame
                _ = [i for i in frames if not (i+frame_offset-1)%frame_step]
                if start_frame not in _:
                    _.insert(0, start_frame)
                if end_frame not in _:
                    _.append(end_frame)
                return _
            # (1001, 1002), 3
            else:
                return [start_frame]
        else:
            raise ValueError()


class RawFramesMtd(object):
    @classmethod
    def to_text(cls, frames):
        list_ = []
        _ = RawIntArrayMtd.merge_to(
            frames
        )
        for i in _:
            if isinstance(i, tuple):
                list_.append('{}-{}'.format(*i))
            else:
                list_.append(str(i))
        return ','.join(list_)


class RawIntegerMtd(object):
    @classmethod
    def get_file_size_prettify(cls, value):
        if value < 1.0:
            return str(round(float(value), 2))
        #
        dv = 1024
        if int(value) >= dv:
            list_ = [(dv**4, 'T'), (dv**3, 'G'), (dv**2, 'M'), (dv**1, 'K')]
            for i in list_:
                s = int(abs(value))/i[0]
                if s:
                    return str(round(float(value)/float(i[0]), 2))+i[1]
        #
        return str(round(float(value), 2))

    @classmethod
    def get_prettify(cls, value):
        if value < 1.0:
            return str(round(float(value), 2))
        #
        dv = 1000
        if int(value) >= dv:
            list_ = [(dv**4, 'T'), (dv**3, 'B'), (dv**2, 'M'), (dv**1, 'K')]
            for i in list_:
                s = int(abs(value))/i[0]
                if s:
                    return str(round(float(value)/float(i[0]), 2))+i[1]
        #
        return str(round(float(value), 2))

    @classmethod
    def get_prettify_(cls, value, mode):
        if mode == 0:
            return cls.get_prettify(value)
        else:
            return cls.get_file_size_prettify(value)

    @classmethod
    def byte_to_gb(cls, value):
        dv = 1024.0
        return float(value)/dv**3

    @classmethod
    def frame_to_time(cls, frame, fps=24):
        second = int(frame)/fps
        h = second/3600
        m = second/60-60*h
        s = second-3600*h-60*m
        return h, m, s

    @classmethod
    def frame_to_time_prettify(cls, frame, fps=24):
        h, m, s = cls.frame_to_time(frame, fps)
        return '%s:%s:%s'%(str(h).zfill(2), str(m).zfill(2), str(s).zfill(2))

    @classmethod
    def second_to_time(cls, second):
        h = int(int(second)/3600.0)
        m = int(int(second)/60.0-60.0*h)
        s = float(second-3600.0*h-60.0*m)
        return h, m, s

    @classmethod
    def second_to_time_prettify(cls, second, mode=0):
        h, m, s = cls.second_to_time(second)
        if mode == 0:
            return '%02d:%02d:%07.4f'%(h, m, s)
        return '%02d:%02d:%02d'%(h, m, s)

    @classmethod
    def second_to_minute(cls, second):
        dv = 60.0
        return float(second)/dv**1

    @classmethod
    def second_to_hours(cls, second):
        dv = 60.0
        return float(second)/dv**2

    @classmethod
    def microsecond_to_second(cls, microsecond):
        dv = 1000.0
        return float(microsecond)/dv**2

    @classmethod
    def microsecond_to_hours(cls, microsecond):
        return cls.second_to_hours(
            cls.microsecond_to_second(microsecond)
        )


class RawRgbRange(object):
    def __init__(self, count):
        self._p = 360.0/count

    def get_rgb(self, index, maximum=255, s_p=50, v_p=50):
        h = self._p*index
        return RawColorMtd.hsv2rgb(
            h, s_p/100.0, v_p/100.0, maximum
        )


class RawIntegerOpt(object):
    def __init__(self, raw):
        self._value = raw

    def set_encode_to_36(self):
        number = self._value
        num_str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if number == 0:
            return '0'

        base36 = []
        while number != 0:
            number, i = divmod(number, 36)
            base36.append(num_str[i])

        return ''.join(reversed(base36))


class RawTextMtd(object):
    @classmethod
    def to_number_embedded_args(cls, text):
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')
        #
        pieces = re.compile(r'(\d+)').split(text)
        pieces[1::2] = map(int, pieces[1::2])
        return pieces

    @classmethod
    def to_glob_pattern(cls, text):
        return re.sub(r'(\d)', '[0-9]', text)

    @classmethod
    def clear_up_to(cls, text):
        return re.sub(
            # keep chinese word and english word
            r'[^\u4e00-\u9fa5a-zA-Z0-9]', '_', text
        )

    @classmethod
    def to_integer(cls, text):
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')
        _ = re.sub(
            r'[^a-zA-Z0-9]', '0', text
        ).lower()
        return int(_, 36)

    @classmethod
    def get_first_word(cls, text):
        if text:
            if isinstance(text, six.text_type):
                text = text.encode('utf-8')
            _ = re.findall(
                r'[\u4e00-\u9fa5a-zA-Z0-9]', text
            )
            if _:
                return _[0]
            return text[0]
        return ''

    @classmethod
    def find_spans(cls, content_str, keyword_str, match_case_flag=False, match_word_flag=False):
        list_ = []
        if content_str and keyword_str:
            if match_word_flag is True:
                p = r'\b{}\b'.format(keyword_str)
            else:
                p = keyword_str

            if match_case_flag is True:
                r = re.finditer(p, content_str)
            else:
                r = re.finditer(p, content_str, re.I)
            for i in r:
                list_.append(i.span())
        return list_

    @staticmethod
    def to_prettify(text, capitalize=True):
        _ = re.sub(
            r'[^\u4e00-\u9fa5a-zA-Z0-9]', '_', text
        )
        if capitalize is True:
            return ' '.join([i if i.isupper() else i.capitalize() for i in _.split('_')])
        return ' '.join([i if i.isupper() else i.lower() for i in _.split('_')])

    @staticmethod
    def split_to(text):
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')
        return re.compile(r'[;,/\-\s]\s*').split(text)

    @staticmethod
    def split_any_to(text):
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')
        # noinspection RegExpUnnecessaryNonCapturingGroup
        return re.findall(r'[A-Z](?:[a-z]+)?|[A-Za-z]+|(?:[0-9]+)|[;,/\-\s]\s*', text)

    @staticmethod
    def find_words(text):
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')
        return re.findall(r'[A-Z](?:[a-z]+)?|[A-Za-z]+', text)


class RawTextOpt(object):
    def __init__(self, raw):
        if isinstance(raw, six.string_types):
            self.__raw = raw
        else:
            raise TypeError()

    def get_is_contain_chinese(self):
        check_str = self.__raw
        # to unicode
        if not isinstance(check_str, six.text_type):
            check_str = check_str.decode('utf-8')
        #
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def get_is_contain_space(self):
        return ' ' in self.__raw

    def to_rgb(self, maximum=255):
        string = self.__raw
        if string:
            _ = [str(ord(i)) for seq, i in enumerate(string)]
            _.reverse()
            a = int(''.join(_))
            h = float(a%25600)/100.0
            s = float(45+a%55)/100.0
            v = float(45+a%55)/100.0
            return RawColorMtd.hsv2rgb(h, s, v, maximum)
        return 0, 0, 0

    def to_rgb_(self, maximum=255, seed=0, s_p=45, v_p=45):
        string = self.__raw
        if string:
            d = 1000.0
            a = sum([ord(i)*(seq*10 if seq > 0 else 1) for seq, i in enumerate(string[::-1])])
            h = float(a%(360+seed)*d)/d
            s = float((s_p/2)+a%(s_p/2))/100.0
            v = float((v_p/2)+a%(v_p/2))/100.0
            # print h, s, v
            return RawColorMtd.hsv2rgb(h, s, v, maximum)
        return 0, 0, 0

    def to_rgb__(self, maximum=255, seed=0, s_p=45, v_p=45):
        """
        :param maximum:
        :param seed:
        :param s_p: minimum s
        :param v_p: minimum v
        :return:
        """
        string = self.__raw
        if string:
            d = 1000.0
            a = RawTextMtd.to_integer(string)
            h = float(a%(360+seed)*d)/d
            s = float((s_p/2)+a%(s_p/2))/100.0
            v = float((v_p/2)+a%(v_p/2))/100.0
            return RawColorMtd.hsv2rgb(h, s, v, maximum)
        return 0, 0, 0

    def to_rgb_0(self, maximum=255, seed=0, s_p=45, v_p=45):
        string = self.__raw
        if string:
            d = 1000.0
            hash_ = hashlib.md5(string.encode('utf-8')).hexdigest()
            h_a = int(hash_[0:8], 16)
            s_a = int(hash_[8:16], 16)
            v_a = int(hash_[16:24], 16)
            h = float(h_a%(360+seed)*d)/d
            s = float((s_p/2)+s_a%(s_p/2))/100.0
            v = float((v_p/2)+v_a%(v_p/2))/100.0
            return RawColorMtd.hsv2rgb(h, s, v, maximum)
        return 0, 0, 0

    def get_index(self):
        string = self.__raw
        return sum([ord(i)*(seq*10 if seq > 0 else 1) for seq, i in enumerate(string[::-1])])

    def set_clear_to(self):
        return re.sub(
            r'[^\u4e00-\u9fa5a-zA-Z0-9]', '_', self.__raw
        )

    def get_filter_by_pattern(self, pattern):
        return fnmatch.filter([self.__raw], pattern)

    def to_frames(self):
        list_ = []
        s = self.__raw
        texts = [i.strip() for i in s.split(',')]
        for i in texts:
            if '-' in i:
                i_start_frame, i_end_frame = [j.strip() for j in i.split('-')][:2]
                if ':' in i:
                    i_end_frame, i_frame_step = i_end_frame.split(':')
                else:
                    i_frame_step = 1
                list_.extend(
                    RawFrameRangeMtd.get(
                        (i_start_frame, i_end_frame), i_frame_step
                    )
                )
            else:
                list_.append(int(i))
        if list_:
            lis_ = list(set(list_))
            lis_.sort()
            return lis_
        return list_

    def to_frame_range(self):
        frames = self.to_frames()
        return min(frames), max(frames)

    def get_is_float(self):
        return sum([n.isdigit() for n in self.__raw.strip().split('.')]) == 2

    def get_is_matched(self, p):
        return fnmatch.filter([self.__raw], p)


class RawStrCamelcaseMtd(object):
    def __init__(self, string):
        self.__raw = string

    @classmethod
    def to_prettify(cls, string):
        return ' '.join([i.capitalize() for i in re.findall(r'[a-zA-Z][a-z]*[0-9]*', string)])

    @classmethod
    def to_underline(cls, string):
        return re.sub(re.compile(r'([a-z]|\d)([A-Z])'), r'\1_\2', string).lower()


class RawStrUnderlineMtd(object):
    @classmethod
    def find_words(cls, string):
        if isinstance(string, six.text_type):
            string = auto_encode(string)
        return re.findall(r'([A-Za-z]+)', string)


class RawTextsMtd(object):
    @classmethod
    def sort_by_number(cls, texts):
        texts.sort(key=lambda x: RawTextMtd.to_number_embedded_args(x))
        return texts

    @classmethod
    def sort_by_initial(cls, texts):
        texts.sort(key=lambda x: x[0].lower())
        return texts


class RawTextsOpt(object):
    def __init__(self, raw):
        self._raw = raw

    def sort_by_number(self):
        return RawTextsMtd.sort_by_number(self._raw)


class RawStrUnderlineOpt(object):
    def __init__(self, string):
        self.__raw = string

    def to_prettify(self, capitalize=True, word_count_limit=None):
        if capitalize is True:
            _ = ' '.join([i if i.isupper() else i.capitalize() for i in self.__raw.split('_')])
            if isinstance(word_count_limit, int):
                c = len(_)
                if c >= word_count_limit+3:
                    return '{}...'.format(_[:word_count_limit])
            return _
        _ = ' '.join([i if i.isupper() else i.lower() for i in self.__raw.split('_')])
        if isinstance(word_count_limit, int):
            c = len(_)
            if c >= word_count_limit+3:
                return '{}...'.format(_[:word_count_limit])
        return _

    def to_camelcase(self):
        return re.sub(r'_(\w)', lambda x: x.group(1).upper(), self.__raw)


class RawBBoxMtd(object):
    @classmethod
    def compute_geometry_args(cls, p_0, p_1, use_int_size=False):
        x, y, z = p_0
        x_1, y_1, z_1 = p_1
        c_x, c_y, c_z = x+(x_1-x)/2, y+(y_1-y)/2, z+(z_1-z)/2
        w, h, d = x_1-x, y_1-y, z_1-z
        if use_int_size is True:
            w, h, d = int(math.ceil(w)), int(math.ceil(h)), int(math.ceil(d))
        return (x, y, z), (c_x, c_y, c_z), (w, h, d)

    @classmethod
    def get_radius(cls, p_0, p_1, pivot):
        o_x, o_y, o_z = pivot
        x_0, y_0, z_0 = p_0
        x_1, y_1, z_1 = p_1
        r_0 = abs(math.sqrt((x_0+o_x)**2+(z_0+o_z)**2))
        r_1 = abs(math.sqrt((x_1+o_x)**2+(z_1+o_z)**2))
        return max(r_0, r_1)


class RawSizeMtd(object):
    @classmethod
    def set_clamp_to(cls, width, height, maximum, minimum):
        if width > height:
            p = float(height)/float(width)
            if width > maximum:
                w = maximum
                return w, w*p
            else:
                w = minimum
                return w, w*p
        elif width < height:
            p = float(width)/float(height)
            if height > maximum:
                h = maximum
                return h*p, h
            else:
                h = minimum
                return h*p, h
        else:
            w = max(min(width, maximum), minimum)
            return w, w

    @classmethod
    def fit_to(cls, size_0, size_1):
        """
        :param size_0: tuple(w, h), etc. image size
        :param size_1: tuple(w, h), etc. window size
        :return:
        """
        w_0, h_0 = size_0
        w_1, h_1 = size_1
        p_0 = float(w_0)/float(h_0)
        p_1 = float(w_1)/float(h_1)
        m_1 = min(w_1, h_1)
        if p_0 > 1:
            if p_0 > p_1:
                w, h = w_1, w_1/p_0
            elif p_0 < p_1:
                w, h = h_1*p_0, h_1
            else:
                w, h = w_1, h_1
        elif p_0 < 1:
            if p_0 > p_1:
                w, h = w_1, w_1/p_0
            elif p_0 < p_1:
                w, h = h_1*p_0, h_1
            else:
                w, h = w_1, h_1
        else:
            w, h = m_1, m_1
        x, y = int((w_1-w)/2), int((h_1-h)/2)
        return x, y, w, h


class RawRectMtd(object):
    @classmethod
    def fit_to(cls, pos, size_0, size_1):
        x_0, y_0 = pos
        w_0, h_0 = size_0
        w_1, h_1 = size_1
        p_0 = float(w_0)/float(h_0)
        p_1 = float(w_1)/float(h_1)
        m_1 = min(w_1, h_1)
        if p_0 > 1:
            if p_0 > p_1:
                w, h = w_1, w_1/p_0
            elif p_0 < p_1:
                w, h = h_1*p_0, h_1
            else:
                w, h = w_1, h_1
        elif p_0 < 1:
            if p_0 > p_1:
                w, h = w_1, w_1/p_0
            elif p_0 < p_1:
                w, h = h_1*p_0, h_1
            else:
                w, h = w_1, h_1
        else:
            w, h = m_1, m_1
        x, y = int((w_1-w)/2), int((h_1-h)/2)
        return x_0+x, y_0+y, w, h


class RawVariablesMtd(object):
    @classmethod
    def get_all_combinations(cls, variables):
        list_ = []
        for i in itertools.product(*[[{k: i} for i in v] for k, v in variables.items()]):
            i_dic = collections.OrderedDict()
            for j_dic in i:
                i_dic.update(j_dic)
            list_.append(i_dic)
        return list_


class RawPointArrayOpt(object):
    def __init__(self, point_array):
        self.__raw = point_array

    def round_to(self, round_count=8):
        list_ = []
        for i in self.__raw:
            x, y, z = i
            x_, y_, z_ = round(x, round_count), round(y, round_count), round(z, round_count)
            list_.append((x_, y_, z_))
        return list_


class RawMatrix33Opt(object):
    def __init__(self, matrix=None):
        if matrix is None:
            self.__raw = self.get_default()
        else:
            self.__raw = matrix

    @classmethod
    def get_default(cls):
        return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    @classmethod
    def identity_to(cls, matrix):
        for row in range(3):
            for col in range(0, 3):
                matrix[row][col] = int(row == col)
        return matrix

    @classmethod
    def get_identity(cls):
        return cls.identity_to(cls.get_default())

    # noinspection PyUnusedLocal
    def add_to(self, matrix):
        m1 = self.__raw
        m2 = matrix
        m = self.get_default()
        for row in range(0, 3):
            for col in range(0, 3):
                m[row][col] = self.__raw[row][col]+m2[row][col]
        return m

    def multiply_to(self, matrix):
        m1 = self.__raw
        m2 = matrix
        m = self.get_default()
        for row in range(0, 3):
            for col in range(0, 3):
                m[row][col] = m1[row][0]*m2[0][col]+m1[row][1]*m2[1][col]+m1[row][2]*m2[2][col]
        return m


class RawIndexMtd(object):
    @classmethod
    def to_next(cls, maximum, minimum, value):
        idx = max(min(value, maximum), minimum)
        if idx == maximum:
            idx = minimum
        else:
            idx += 1
        return idx

    @classmethod
    def to_previous(cls, maximum, minimum, value):
        idx = max(min(value, maximum), minimum)
        if idx == minimum:
            idx = maximum
        else:
            idx -= 1
        return idx


class RawElementArrayOpt(object):
    def __init__(self, elements):
        self.__set = set()
        self.__index_dict = {}
        self.__raw = elements

    def append(self, element):
        if element not in self.__set:
            self.__set.add(element)
            self.__raw.append(element)
            index = len(self.__set)-1
            self.__index_dict[element] = index
            return index
        return self.__index_dict[element]

    def extend(self, elements):
        indices = []
        for i in elements:
            indices.append(self.append(i))
        return indices


class RawStackOpt(object):
    def __init__(self, elements):
        self.__raw = elements
        self.__index_dict = {}
        for seq, i in enumerate(self.__raw):
            self.__index_dict[i] = seq

    def index(self, element):
        return self.__index_dict[element]
