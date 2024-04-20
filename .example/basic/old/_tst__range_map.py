# coding:utf-8

def _set_value_map_(range1, range2, value1):
    min1, max1 = range1
    min2, max2 = range2
    #
    percent = float(value1 - min1) / (max1 - min1)
    #
    value2 = (max2 - min2) * percent + min2
    return value2


print _set_value_map_(
    (0, 1), (0, 5), .5
) / 10
