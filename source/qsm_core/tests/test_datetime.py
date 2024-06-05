# coding:utf-8
from datetime import datetime, timedelta


def determine_time_period(input_time_str, language='en_US'):
    # 将输入的时间字符串转换为datetime对象
    input_time = datetime.strptime(input_time_str, '%Y-%m-%d %H:%M:%S')

    # 获取当前时间
    now = datetime.now()

    # 获取今天的日期（不包括时间）
    today = now.date()

    # 获取当前时间的周几，0代表星期一，6代表星期日
    now_weekday = now.weekday()

    # 获取本周开始的日期（星期一）
    start_of_week = today-timedelta(days=now_weekday)

    # 获取上周开始和结束的日期
    start_of_last_week = start_of_week-timedelta(days=7)
    end_of_last_week = start_of_week-timedelta(days=1)

    # 获取本月开始的日期
    start_of_month = today.replace(day=1)

    # 获取今年的开始日期
    start_of_year = today.replace(month=1, day=1)

    # 判断并返回对应的时间段描述
    if input_time.date() == today:
        return "今天" if language == 'chs' else "Today"
    elif input_time.date() >= start_of_week and input_time.date() < today:
        return "本周早些时候" if language == 'chs' else "Earlier this week"
    elif input_time.date() >= start_of_last_week and input_time.date() <= end_of_last_week:
        return "上周" if language == 'chs' else "Last week"
    elif input_time.date() >= start_of_month and input_time.date() < start_of_week:
        return "本月早些时候" if language == 'chs' else "Earlier this month"
    elif input_time.date() >= start_of_year and input_time.date() < start_of_month:
        month_str = input_time.strftime('%Y年%m月' if language == 'chs' else '%B %Y')
        return month_str
    else:
        year_str = "{}年".format(input_time.year) if language == 'chs' else str(input_time.year)
        return year_str


# 测试示例
print determine_time_period("2024-05-29 10:00:00", "chs")  # 如果今天是2024-05-29
print determine_time_period("2024-05-25 10:00:00", "chs")  # 本周早些时候
print determine_time_period("2024-05-21 10:00:00", "chs")  # 上周
print determine_time_period("2024-05-10 10:00:00", "chs")  # 本月早些时候
print determine_time_period("2024-03-30 10:00:00", "chs")  # 2024年03月
print determine_time_period("2023-12-30 10:00:00", "chs")  # 2023年

print determine_time_period("2024-05-29 10:00:00", "en_US")  # Today
print determine_time_period("2024-05-25 10:00:00", "en_US")  # Earlier this week
print determine_time_period("2024-05-21 10:00:00", "en_US")  # Last week
print determine_time_period("2024-05-10 10:00:00", "en_US")  # Earlier this month
print determine_time_period("2024-03-30 10:00:00", "en_US")  # March 2024
print determine_time_period("2023-12-30 10:00:00", "en_US")  # 2023
