# coding:utf-8
import cProfile

a = list(range(1000000))


def test():
    print a[100000]


cProfile.run('test()')