# coding:utf-8
import re

path = '/shl/chr/test_0'

pathsep = '/'

for i_path in [
    '/shl/chr/test_0/srf/surfacing',
    '/shl/chr/test_0/srf',
    '/shl/chr/test_1/srf',
    '/shl/chr/test_1/mod',
]:
    m = re.match(
        r'{0}{1}[^{1}]*'.format(path, pathsep), i_path
    )

    if m:
        print i_path, m.group()



print re.findall(
    re.compile('[<](.*?)[>]'), 'a/<bcd>'
)