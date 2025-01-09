# coding:utf-8


class A(object):
    def __init__(self):
        pass

    def __test(self, *args, **kwargs):
        print args[0]


def test(*args, **kwargs):
    print 'B'

a = A()


A._A__test = test

a.__dict__['_A__test'] = test

a._A__test('AA')
