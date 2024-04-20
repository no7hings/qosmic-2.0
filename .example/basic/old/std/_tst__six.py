# coding:utf-8
from __future__ import print_function

import six

print(six.__file__)

if __name__ == '__main__':
    ss = [u'a', 'a']
    for i in ss:
        print(i, isinstance(i, str))

    print(six.string_types)
    for i in ss:
        print(i, isinstance(i, six.string_types))
