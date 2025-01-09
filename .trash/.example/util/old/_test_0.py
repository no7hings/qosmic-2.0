# coding:utf-8
import re

# a = '/a/b/c/test<UDIM>.ext'
# b = '/a/b/c/test1001.ext'
#
# p = r'<udim>'
#
# r = re.finditer(p, a, re.IGNORECASE)
# start, end = list(r)[0].span()
#
# print b[:start]
#
# print b[start:start+4]

import string
a = 'abc12'
print str(a).rstrip(string.digits)
