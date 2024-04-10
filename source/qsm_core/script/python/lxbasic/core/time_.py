# coding:utf-8
import time

import datetime

from . import raw as bsc_cor_raw


class TimeExtraMtd(object):
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    TIME_TAG_FORMAT = '%Y_%m%d_%H%M_%S_%f'
    DATA_TAG_FORMAT = '%Y_%m%d'

    @classmethod
    def generate_time_tag_36(cls, multiply=1):
        return bsc_cor_raw.RawIntegerOpt(int(time.time()*multiply)).set_encode_to_36()

    @classmethod
    def generate_time_tag_36_(cls, multiply=1):
        s = time.time()
        y = time.localtime().tm_year
        m = time.localtime().tm_mon
        d = time.localtime().tm_mday
        c_s = time.mktime(time.strptime('{}-{}-{}'.format(y, m, d), '%Y-%m-%d'))
        return bsc_cor_raw.RawIntegerOpt(int((s-c_s)*multiply)).set_encode_to_36()


class TimePrettifyMtd(object):
    MONTH = [
        (u'01月', 'January'),
        (u'02月', 'February'),
        (u'03月', 'March'),
        (u'04月', 'April'),
        (u'05月', 'May'),
        (u'06月', 'June'),
        (u'07月', 'July'),
        (u'08月', 'August'),
        (u'09月', 'September'),
        (u'10月', 'October'),
        (u'11月', 'November'),
        (u'12月', 'December')
    ]
    WEEK = [
        (u'周一', 'Monday'),
        (u'周二', 'Tuesday'),
        (u'周三', 'Wednesday'),
        (u'周四', 'Thursday'),
        (u'周五', 'Friday'),
        (u'周六', 'Saturday'),
        (u'周天', 'Sunday'),
    ]

    @classmethod
    def to_prettify_by_timestamp(cls, timestamp, language=0):
        if isinstance(timestamp, float):
            return cls.to_prettify_by_timetuple(
                time.localtime(timestamp),
                language=language,
            )

    @classmethod
    def to_prettify_by_time_tag(cls, time_tag, language=0):
        year = int(time_tag[:4])
        month = int(time_tag[5:7])
        day = int(time_tag[7:9])
        hour = int(time_tag[10:12])
        minute = int(time_tag[12:14])
        second = int(time_tag[15:16])
        if year > 0:
            timetuple = datetime.datetime(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                second=second
            ).timetuple()
            return cls.to_prettify_by_timetuple(
                timetuple,
                language=language
            )

    @classmethod
    def to_prettify_by_timetuple(cls, timetuple, language=0):
        year, month, day, hour, minute, second, week, count_day, is_dst = timetuple
        cur_timetuple = time.localtime(time.time())
        year_, month_, day_, hour_, minute_, second_, week_, count_day_, is_dst_ = cur_timetuple
        #
        monday = day-week
        monday_ = day_-week_
        year_str = [u'{}年'.format(str(year).zfill(4)), str(year).zfill(4)][language]
        month_str = cls.MONTH[int(month)-1][language]
        day_str = [u'{}日'.format(str(day).zfill(2)), str(day).zfill(2)][language]
        if cur_timetuple[:1] == timetuple[:1]:
            if cur_timetuple[:2] == timetuple[:2]:
                if monday_ == monday:
                    week_str = u'{0}'.format(cls.WEEK[int(week)][language])
                    if day_ == day:
                        time_str = [
                            u'{}点{}分{}秒'.format(str(hour).zfill(2), str(minute).zfill(2), str(second).zfill(2)),
                            '{}:{}:{}'.format(str(hour).zfill(2), str(minute).zfill(2), str(second).zfill(2))
                        ][language]
                        return time_str
                    elif day_ == day+1:
                        sub_str = [u'昨天', 'Yesterday'][language]
                        return sub_str
                    return week_str
            #
            if language == 0:
                return u'{}{}'.format(month_str, day_str)
            return '{} {}'.format(day_str, month_str)
        #
        if language == 0:
            return u'{}{}'.format(year_str, month_str)
        return '{} {}'.format(month_str, year_str)

    def time_tag2timestamp(self, time_tag):
        pass

    @classmethod
    def to_timetuple(cls, any_time, time_format):
        import datetime

        return datetime.datetime.strptime(
            any_time, time_format
        ).timetuple()


class TimestampMtd(object):
    @classmethod
    def to_string(cls, pattern, timestamp):
        return time.strftime(
            pattern,
            time.localtime(timestamp)
        )


class TimestampOpt(object):
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    TIME_TAG_FORMAT = '%Y_%m%d_%H%M_%S'

    def __init__(self, timestamp):
        self._timestamp = timestamp

    @property
    def timestamp(self):
        return self._timestamp

    def get(self):
        return time.strftime(
            self.TIME_FORMAT,
            time.localtime(self._timestamp)
        )

    def get_as_tag(self):
        return time.strftime(
            self.TIME_TAG_FORMAT,
            time.localtime(self._timestamp)
        )

    def get_as_tag_36(self, multiply=1):
        return bsc_cor_raw.RawIntegerOpt(
            int(self._timestamp*multiply)
        ).set_encode_to_36()

    def get_as_tag_36_(self, multiply=1):
        s = self._timestamp
        y = time.localtime().tm_year
        m = time.localtime().tm_mon
        d = time.localtime().tm_mday
        c_s = time.mktime(time.strptime('{}-{}-{}'.format(y, m, d), '%Y-%m-%d'))
        return bsc_cor_raw.RawIntegerOpt(int((s-c_s)*multiply)).set_encode_to_36()

    def to_prettify(self, language):
        return TimePrettifyMtd.to_prettify_by_timestamp(self._timestamp, language)
