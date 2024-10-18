# coding:utf-8
import time

import datetime
# process
from . import raw as _raw


class TimeExtraMtd(object):
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    TIME_TAG_FORMAT = '%Y_%m%d_%H%M_%S_%f'
    DATE_TAG_FORMAT = '%Y_%m%d'

    @classmethod
    def generate_time_tag_36(cls, multiply=1.0):
        return _raw.BscIntegerOpt(int(time.time()*multiply)).encode_to_36()

    @classmethod
    def generate_time_tag_36_(cls, multiply=1.0):
        s = time.time()
        y = time.localtime().tm_year
        m = time.localtime().tm_mon
        d = time.localtime().tm_mday
        c_s = time.mktime(time.strptime('{}-{}-{}'.format(y, m, d), '%Y-%m-%d'))
        return _raw.BscIntegerOpt(int((s-c_s)*multiply)).encode_to_36()


class BscTimePrettify(object):
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
    def to_prettify_by_timestamp(cls, timestamp, language=1):
        """
        0 is chinese
        """
        if isinstance(timestamp, float):
            return cls.to_prettify_by_timetuple(
                time.localtime(timestamp),
                language=language,
            )

    @classmethod
    def to_prettify_by_timestamp_(cls, timestamp, language='en_us'):
        """
        0 is chinese
        """
        return cls.to_prettify_by_timestamp(timestamp, 0 if language=='chs' else 1)

    @classmethod
    def to_prettify_by_time_tag(cls, time_tag, language=1):
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
    def to_prettify_by_timetuple(cls, timetuple, language=1):
        year, month, day, hour, minute, second, week, count_day, is_dst = timetuple
        timetuple_cur = time.localtime(time.time())
        year_cur, month_cur, day_cur, hour_cur, minute_cur, second_cur, week_cur, count_day_cur, is_dst_cur = timetuple_cur
        #
        monday = day-week
        monday_cur = day_cur-week_cur
        # same year, return year
        if timetuple_cur[:1] == timetuple[:1]:
            # same month, return month day
            if timetuple_cur[:2] == timetuple[:2]:
                # same week, return week
                if monday_cur == monday:
                    week_str = u'{0}'.format(cls.WEEK[int(week)][language])
                    # same day, return time
                    if day_cur == day:
                        time_str = [
                            u'今天{}点{}分{}秒'.format(str(hour).zfill(2), str(minute).zfill(2), str(second).zfill(2)),
                            'Today {}:{}:{}'.format(str(hour).zfill(2), str(minute).zfill(2), str(second).zfill(2))
                        ][language]
                        return time_str
                    return week_str
            #
            month_str = cls.to_month(month, language)
            day_str = cls.to_day(day, language)
            if language == 0:
                return u'{}{}'.format(month_str, day_str)
            return '{} {}'.format(day_str, month_str)
        #
        year_str = cls.get_year(year, language)
        return year_str

    @classmethod
    def to_prettify_by_timetuple_(cls, timetuple, language='en_us'):
        return cls.to_prettify_by_timetuple(timetuple, 0 if language=='chs' else 1)

    @classmethod
    def get_year(cls, year, language):
        return [u'{}年'.format(str(year).zfill(4)), str(year).zfill(4)][language]

    @classmethod
    def to_month(cls, month, language):
        return cls.MONTH[int(month)-1][language]

    @classmethod
    def to_day(cls, day, language):
        return [u'{}日'.format(str(day).zfill(2)), str(day).zfill(2)][language]

    def time_tag2timestamp(self, time_tag):
        pass

    @classmethod
    def to_timetuple(cls, any_time, time_format):
        import datetime

        return datetime.datetime.strptime(
            any_time, time_format
        ).timetuple()


class BscTimestamp(object):
    @classmethod
    def to_string(cls, pattern, timestamp):
        return time.strftime(
            pattern,
            time.localtime(timestamp)
        )

    @classmethod
    def to_time_tuple(cls, timestamp):
        return time.localtime(timestamp)

    @classmethod
    def get_current_time_tuple(cls):
        return time.localtime(time.time())


class BscTimestampOpt(object):
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
        return _raw.BscIntegerOpt(
            int(self._timestamp*multiply)
        ).encode_to_36()

    def get_as_tag_36_(self, multiply=1):
        s = self._timestamp
        y = time.localtime().tm_year
        m = time.localtime().tm_mon
        d = time.localtime().tm_mday
        c_s = time.mktime(time.strptime('{}-{}-{}'.format(y, m, d), '%Y-%m-%d'))
        return _raw.BscIntegerOpt(int((s-c_s)*multiply)).encode_to_36()

    def to_prettify(self, language):
        return BscTimePrettify.to_prettify_by_timestamp(self._timestamp, language)


class DateTime(object):
    @classmethod
    def to_period(cls, input_time_str, language='en_US'):
        input_time = datetime.datetime.strptime(input_time_str, '%Y-%m-%d %H:%M:%S')

        now = datetime.datetime.now()

        today = now.date()

        yesterday = today-datetime.timedelta(days=1)

        now_weekday = now.weekday()

        start_of_week = today-datetime.timedelta(days=now_weekday)

        start_of_last_week = start_of_week-datetime.timedelta(days=7)
        end_of_last_week = start_of_week-datetime.timedelta(days=1)

        start_of_month = today.replace(day=1)

        start_of_year = today.replace(month=1, day=1)

        weekdays_chs = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        weekdays_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        if input_time.date() == today:
            return "今天" if language == 'chs' else "Today"
        elif input_time.date() == yesterday:
            return "昨天" if language == 'chs' else "Yesterday"
        elif start_of_week <= input_time.date() < today:
            weekday_str = weekdays_chs[input_time.weekday()] if language == 'chs' else weekdays_en[input_time.weekday()]
            return weekday_str
        elif start_of_last_week <= input_time.date() <= end_of_last_week:
            return "上周" if language == 'chs' else "Last week"
        elif start_of_month <= input_time.date() < start_of_week:
            return "本月早些时候" if language == 'chs' else "Earlier this month"
        elif start_of_year <= input_time.date() < start_of_month:
            month_str = input_time.strftime('%Y年%m月' if language == 'chs' else '%B %Y')
            return month_str
        else:
            year_str = "{}年".format(input_time.year) if language == 'chs' else str(input_time.year)
            return year_str

    @classmethod
    def to_tag(cls):
        pass
