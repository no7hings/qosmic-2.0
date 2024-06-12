# coding:utf-8
import datetime

import time

today = datetime.datetime.today()
maximum = int(time.mktime(today.timetuple()))
print maximum
start_of_year = today.replace(month=1, day=1)
minimum = int(time.mktime(start_of_year.timetuple()))

print minimum

ctimes = range(minimum, maximum)

print ctimes